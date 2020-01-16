import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as psf

# TODO Create a schema for incoming resources
schema = StructType([
    StructField('crime_id', dataType=StringType(), nullable=False),
    StructField('original_crime_type_name', dataType=StringType(), nullable=False),
    StructField('report_date', dataType=StringType(), nullable=False),
    StructField('call_date', dataType=StringType(), nullable=False),
    StructField('offense_date', dataType=StringType(), nullable=False),
    StructField('call_time', dataType=StringType(), nullable=False),
    StructField('call_date_time', dataType=StringType(), nullable=False),
    StructField('disposition', dataType=StringType(), nullable=False),
    StructField('address', dataType=StringType(), nullable=False),
    StructField('city', dataType=StringType(), nullable=False),
    StructField('state', dataType=StringType(), nullable=False),
    StructField('state', dataType=StringType(), nullable=False),
    StructField('agency_id', dataType=StringType(), nullable=False),
    StructField('address_type', dataType=StringType(), nullable=False),
    StructField('common_location', dataType=StringType(), nullable=True)
])


def run_spark_job(spark: SparkSession):
    # TODO Create Spark Configuration
    # Create Spark configurations with max offset of 200 per trigger
    # set up correct bootstrap server and port
    df = spark \
        .readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers', 'localhost:9092') \
        .option('subscribe', 'marcus.kafka.producer') \
        .option('startingOffsets', 'earliest') \
        .option('maxOffsetPerTrigger', 200) \
        .option('stopGracefullyOnShutdown', 'true') \
        .load()

    # Show schema for the incoming resources for checks
    df.printSchema()

    # TODO extract the correct column from the kafka input resources
    # Take only value and convert it to String
    kafka_df = df.selectExpr("CAST(value AS STRING)")

    service_table = kafka_df \
        .select(psf.from_json(psf.col('value'), schema).alias("DF")) \
        .select("DF.*")

    # TODO select original_crime_type_name and disposition
    distinct_table = service_table \
        .select('original_crime_type_name', 'disposition', 'call_date_time') \
        .withColumn('watermark_time', psf.to_timestamp(col='call_date_time', format="yyyy-MM-dd'T'HH:mm:ss.SSS")) \
        .distinct() \
        .withWatermark(eventTime='watermark_time', delayThreshold='1 minute')

    # count the number of original crime type
    agg_df = distinct_table.dropna() \
        .select('original_crime_type_name') \
        .agg({'original_crime_type_name': 'count'}) \
        .orderBy('count(original_crime_type_name)', ascending=False)

    # TODO Q1. Submit a screen shot of a batch ingestion of the aggregation
    # TODO write output stream
    query = agg_df \
        .writeStream \
        .format("console") \
        .outputMode("complete") \
        .start()

    # TODO attach a ProgressReporter
    query.awaitTermination()

    # TODO get the right radio code json path
    radio_code_json_filepath = 'radio_code.json'
    radio_code_df = spark.read.json(radio_code_json_filepath)

    # clean up your data so that the column names match on radio_code_df and agg_df
    # we will want to join on the disposition code

    # TODO rename disposition_code column to disposition
    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition")

    # TODO join on disposition column
    join_query = agg_df.join(radio_code_df, on='disposition', how='inner')

    join_query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # TODO Create Spark in Standalone mode
    spark_session = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("KafkaSparkStructuredStreaming") \
        .getOrCreate()

    logger.info("Spark started")

    run_spark_job(spark_session)

    spark_session.stop()
