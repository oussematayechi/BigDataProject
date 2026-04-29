from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when, lit, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType
import json

# ─── Spark Session ────────────────────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("IoTPatientMonitoring") \
    .config("spark.mongodb.write.connection.uri", "mongodb://admin:admin123@mongodb:27017/patient_monitoring?authSource=admin") \
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
            "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# ─── Schema ───────────────────────────────────────────────────────────────────
schema = StructType([
    StructField("timestamp",   StringType(), True),
    StructField("patientId",   StringType(), True),
    StructField("deviceId",    StringType(), True),
    StructField("metric",      StringType(), True),
    StructField("value",       FloatType(),  True),
    StructField("unit",        StringType(), True),
    StructField("alertLevel",  StringType(), True),
])

# ─── Read from ALL metric topics ──────────────────────────────────────────────
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe",
            "patient.heartrate,patient.temperature,"
            "patient.oxygen,patient.bloodpressure,patient.respiratoryrate") \
    .option("startingOffsets", "latest") \
    .load()

df = df_raw.selectExpr("CAST(value AS STRING) as json_str", "topic") \
           .select(from_json(col("json_str"), schema).alias("data"), col("topic")) \
           .select("data.*", "topic")

# ─── Threshold Classification ─────────────────────────────────────────────────
df_classified = df.withColumn(
    "alertLevel",
    when(col("metric") == "HeartRate",
         when((col("value") < 40) | (col("value") > 150), lit("critical"))
        .when((col("value") < 50) | (col("value") > 120), lit("warning"))
        .otherwise(lit("normal"))
    ).when(col("metric") == "Temperature",
         when((col("value") > 39.5) | (col("value") < 35), lit("critical"))
        .when(col("value") > 38.0, lit("warning"))
        .otherwise(lit("normal"))
    ).when(col("metric") == "OxygenLevel",
         when(col("value") < 90, lit("critical"))
        .when(col("value") < 93, lit("warning"))
        .otherwise(lit("normal"))
    ).when(col("metric") == "BloodPressure",
         when((col("value") > 180) | (col("value") < 70), lit("critical"))
        .when(col("value") > 130, lit("warning"))
        .otherwise(lit("normal"))
    ).when(col("metric") == "RespiratoryRate",
         when((col("value") < 8) | (col("value") > 30), lit("critical"))
        .when((col("value") < 10) | (col("value") > 24), lit("warning"))
        .otherwise(lit("normal"))
    ).otherwise(lit("normal"))
).withColumn("processed_at", current_timestamp())

# ─── Write ALL readings to MongoDB ────────────────────────────────────────────
def write_to_mongo(batch_df, batch_id):
    if batch_df.count() == 0:
        return

    # Write every reading to sensor_readings collection
    batch_df.write \
        .format("mongodb") \
        .mode("append") \
        .option("database", "patient_monitoring") \
        .option("collection", "sensor_readings") \
        .save()

    # Write only alerts (warning/critical) to alerts collection + print to console
    alerts_df = batch_df.filter(col("alertLevel").isin("warning", "critical"))
    alert_count = alerts_df.count()

    if alert_count > 0:
        alerts_df.write \
            .format("mongodb") \
            .mode("append") \
            .option("database", "patient_monitoring") \
            .option("collection", "alerts") \
            .save()

        # Print alerts to console for demo visibility
        print(f"\n🚨 Batch {batch_id} — {alert_count} ALERT(s) detected:")
        alerts_df.select("patientId", "metric", "value", "unit", "alertLevel") \
                 .show(truncate=False)

    print(f"✅ Batch {batch_id}: {batch_df.count()} readings processed, {alert_count} alerts.")

# ─── Write Alerts back to Kafka alert topics ──────────────────────────────────
def write_alerts_to_kafka(batch_df, batch_id):
    alerts_df = batch_df.filter(col("alertLevel").isin("warning", "critical"))
    if alerts_df.count() == 0:
        return

    from pyspark.sql.functions import to_json, struct, udf
    from pyspark.sql.types import StringType

    # Determine target Kafka topic based on alertLevel
    alerts_with_topic = alerts_df.withColumn(
        "kafka_topic",
        when(col("alertLevel") == "critical", lit("patient.alerts.critical"))
        .otherwise(lit("patient.alerts.warning"))
    )

    alerts_with_topic \
        .select(
            col("kafka_topic").alias("topic"),
            to_json(struct(
                col("patientId"), col("deviceId"), col("metric"),
                col("value"), col("unit"), col("alertLevel"), col("timestamp")
            )).alias("value")
        ) \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .save()

# ─── Start Streaming Queries ──────────────────────────────────────────────────
query_mongo = df_classified.writeStream \
    .foreachBatch(write_to_mongo) \
    .option("checkpointLocation", "/tmp/checkpoint_mongo") \
    .trigger(processingTime="10 seconds") \
    .start()

query_kafka_alerts = df_classified.writeStream \
    .foreachBatch(write_alerts_to_kafka) \
    .option("checkpointLocation", "/tmp/checkpoint_kafka_alerts") \
    .trigger(processingTime="10 seconds") \
    .start()

print("🚀 Spark Streaming started. Waiting for data from Kafka...")
spark.streams.awaitAnyTermination()