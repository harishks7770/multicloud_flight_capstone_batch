from pyspark.sql import functions as F

# 1. CONFIGURE STORAGE VARIABLES
AWS_ACCESS_KEY = "<your_access_key>"
AWS_SECRET_KEY = "<your_secret_key>"
BUCKET_NAME = "<your_bucket_name>"

# Path using the modern s3a protocol for cluster storage 
s3_raw_path = f"<your_s3_raw_file_path>"

# --------------------------------------------------------------------------------

# 2. READ MULTILINE JSON RAW PAYLOADS FROM S3
df_raw = (spark.read
          .option("multiline", "true")
          .option("fs.s3a.access.key", AWS_ACCESS_KEY)
          .option("fs.s3a.secret.key", AWS_SECRET_KEY)
          .json(s3_raw_path))

print("Raw data read successfully. Data structure lookahead:")
df_raw.printSchema()

# ----------------------------------------------------------------------------------

# 3. UNPACK THE NESTED ARRAY
df_exploded = df_raw.select(
    F.col("time").alias("api_fetch_timestamp"), 
    F.explode("states").alias("flight")
)

# OpenSky maps arrays by index values: 
# 0=icao24, 1=callsign, 2=country, 5=longitude, 6=latitude, 7=altitude, 9=velocity
df_transformed = df_exploded.select(
    F.from_unixtime("api_fetch_timestamp").cast("timestamp").alias("ingested_at"),
    F.col("flight").getItem(0).cast("string").alias("icao24"),
    F.trim(F.col("flight").getItem(1)).cast("string").alias("callsign"),
    F.col("flight").getItem(2).cast("string").alias("origin_country"),
    F.col("flight").getItem(5).cast("double").alias("longitude"),
    F.col("flight").getItem(6).cast("double").alias("latitude"),
    F.col("flight").getItem(7).cast("double").alias("altitude_meters"),
    F.col("flight").getItem(9).cast("double").alias("velocity_ms")
).filter(F.col("icao24").isNotNull())

# Render a live scannable table view directly in the notebook 
display(df_transformed.limit(10))

# ---------------------------------------------------------------------------------------

# 4. WRITE TO DELTA TABLE WITH SCHEMA EVOLUTION
s3_output_path = f"s3a://capstone1010/processed/flight_delta_table"

(df_transformed.write
 .format("delta")
 .mode("append")
 .option("mergeSchema", "true")  # Enables Delta schema evolution
 .option("fs.s3a.access.key", AWS_ACCESS_KEY)
 .option("fs.s3a.secret.key", AWS_SECRET_KEY)
 .save(s3_output_path))

print("🎉 Transformation Complete! Structured Delta table saved with Schema Evolution enabled.")
