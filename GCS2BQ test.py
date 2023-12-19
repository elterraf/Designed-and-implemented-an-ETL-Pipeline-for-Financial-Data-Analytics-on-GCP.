from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import *
import sys

# creating spark session
spark = SparkSession.builder \
.appName("gcs-to-bq") \
.config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar") \
.getOrCreate()

# Reading the commnad line arguments
data_uri = sys.argv[1]
file_format = sys.argv[2]
partition_field = sys.argv[3]
project_id = sys.argv[4]
dataset_name = sys.argv[5]
table_name = sys.argv[6]
gcs_temp_bucket = sys.argv[7]

# creating bigquery table by concatinating the project_id and dataset_name and table_name
bigquery_table = f"{project_id}.{dataset_name}.{table_name}"


today = datetime.now().strftime("%Y-%m-%d")
print(today)
path = f"{data_uri}/{partition_field}={today}"
print(path)

# Reading the parquet files from GCS bucket, assigning the schema manually and converting the date to proper format

input_df = spark \
.read \
.option("recursiveFilelookup","True") \
.format(file_format) \
.option("header","True") \
.load(path) \
.withColumn("id", col('id').cast('int')) \
.withColumn("Symbol", col('Symbol').cast('string')) \
.withColumn("Date",to_date("Date", 'dd-MMM-yy')) \
.withColumn("Open_Price", col('Open_Price').cast('float')) \
.withColumn("High_Price", col('High_Price').cast('float')) \
.withColumn('Low_Price',col('Low_Price').cast('float')) \
.withColumn("Close_Price", col('Close_Price').cast('float')) \
.withColumn("WAP", col('WAP').cast('float')) \
.withColumn("No_of_Shares", col('No_of_Shares').cast('int')) \
.withColumn("No_of_Trades", col('No_of_Trades').cast('int')) \
.withColumn("Total_Turnover", col('Total_Turnover').cast('float')) \
.withColumn("Deliverable_Quantity", col('Deliverable_Quantity').cast('int')) \
.withColumn("Percentage_Deli_Qty_to_Traded_Qty", col('Percentage_Deli_Qty_to_Traded_Qty').cast('float')) \
.withColumn("Spread_High_Low", col('Spread_High_Low').cast('float')) \
.withColumn("Spread_Close_Open", col('Spread_Close_Open').cast('float'))


# Load the processed data from GCS location into a BigQuery table
input_df.write \
    .mode("append") \
    .format("com.google.cloud.spark.bigquery") \
    .option("temporaryGcsBucket", gcs_temp_bucket) \
    .option("table", bigquery_table) \
    .option("createDisposition", "CREATE_IF_NEEDED") \
    .option("writeDisposition", "WRITE_TRUNCATE") \
    .save()