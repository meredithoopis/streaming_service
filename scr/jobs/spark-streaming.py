from time import sleep 
import pyspark 
from transformers import pipeline 
import json 
from pyspark.sql import SparkSession 
from pyspark.sql.functions import from_json, col, when, udf 
from pyspark.sql.types import StructType, StructField, StringType, FloatType

#with open('../config/config.py', 'r') as f: 
 #   config = f.read()
    #print(config)
config = {
    "kafka": {
        "sasl.username": "WI6XZHQSU32ARU4D", 
        "sasl.password": "AacadYeHho/VrEGCllTCj93f9RVyK+UZpBC00mYYK+bfcROM1SeAm/8aGAFHazAA", 
        "bootstrap.servers": "pkc-ldvj1.ap-southeast-2.aws.confluent.cloud:9092", 
        'security.protocol': 'SASL_SSL', 
        'sasl.mechanisms': 'PLAIN', 
        'session.timeout.ms': 50000
    }, 
    "schema_registry": {
        "url": "https://psrc-7q7vj.ap-southeast-2.aws.confluent.cloud", 
        "basic.auth.user.info": "PDG5HG43YEQT5WVN:BJgGZFTa8urycqJnmsfPUoiG/tE5rgjh7ZE3QhnJMgif+KXijXbP1E/HxMfL1TlQ"
    }
}


#Load pipeline 
classifier = pipeline(model = "SamLowe/roberta-base-go_emotions")
def sentiment_analysis(comment) -> str: 
    if comment: 
        return (classifier(comment))[0]['label']
    return "Empty"

#print(sentiment_analysis(hello[1]['title']))

def start_streaming(spark):
    topic = 'news'
    while True: 
        try: 
            stream_df = (spark.readStream.format("socket")
                        .option("host", "0.0.0.0")
                        .option("port", 9999)
                        .load())
            schema = StructType(
                [
                    StructField("url", StringType()), 
                    StructField("title", StringType()),
                    StructField("content", StringType()),
                    StructField("date", StringType()),

                ]
            ) 
            stream_df = stream_df.select(from_json(col('value'), schema).alias('data')).select(("data.*"))
            sentiment_analysis_udf = udf(sentiment_analysis, StringType())
            stream_df = stream_df.withColumn('sentiment', when(col('title').isNotNull(), sentiment_analysis_udf(col('title'))).otherwise(None))
            kafka_df = stream_df.selectExpr("CAST(url AS STRING) AS KEY", "to_json(struct(*)) AS value")
            query = (kafka_df.writeStream
                    .format("kafka")
                    .option("kafka.bootstrap.servers", config['kafka']['bootstrap.servers'])
                    .option("kafka.security.protocol", config['kafka']['security.protocol'])
                    .option("kafka.sasl.mechanism", config['kafka']['sasl.mechanisms'])
                    .option('kafka.sasl.jaas.config',
                           'org.apache.kafka.common.security.plain.PlainLoginModule required username="{username}" '
                           'password="{password}";'.format(
                               username=config['kafka']['sasl.username'],
                               password=config['kafka']['sasl.password']
                           ))
                    .option('checkpointLocation', '/checkpoint')
                    .option('topic', topic)
                    .start()
                    .awaitTermination()
                    )
        except Exception as e: 
            print(f"Exception encountered: {e}. Retrying in 10 seconds...")
            sleep(10)
        
if __name__ == "__main__": 
    spark_conn = SparkSession.builder.appName("Socket_Stream_Consumer").getOrCreate()
    start_streaming(spark_conn)