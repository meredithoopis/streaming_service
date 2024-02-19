Streaming service: Using news data and sentiment analysis model 
===============================

This is a streaming service as a way to learn about streaming data. In the pipeline, the data will be crawled then streamed through Socket. After that, the streamed data will be received by Spark to perform aggregation as well as predicting the suitable sentiment for the title of the article using a Hugging Face model. Finally, metadata about articles and corresponding sentiments will be streamed to Kafka. 

## About 
- **crawl.py**: Crawl the data from VnExpress using Selenium:[VnExpress](https://e.vnexpress.net/)
- **streaming-socket.py**: Streaming data through Socket 
- **spark-streaming.py**: Reading streams from socket, perform aggregations using Spark then streamed to Kafka


### Requirements
- Python >= 3.9(Using a virtual environment)
- Docker + Docker Compose 
- An Elasticsearch cloud account: Create an account, then a deployment and link the deployment to the Confluent cluster. 
- A Confluent account: Create an account, then a cluster, then an environment and a topic, and connect to the Schema Registry. 
- Connecting to Elasticsearch sink through Confluent ([Reference](https://docs.confluent.io/cloud/current/connectors/cc-elasticsearch-service-sink.html) amd complete credentials in the config.py file) 

### How-to
Clone this repository and run: 
```bash 
cd scr
```
Install required packages: 
```bash 
pip install -r requirements.txt
```
Running Docker to start all services, go to the corresponding port to check Spark master: 
```bash
docker-compose up -d
```

1. You can use the already crawled data or run the following command to crawl new data: 

```bash
python crawl.py
```

2. Go to the spark-master terminal to stream data through Socket: 

```bash
docker exec -it spark-master /bin/bash
```
After that, run the following: 
```bash 
cd jobs 
```
and 
```
python streaming-socket.py 
```

4. Aggregating data using Spark and streamed to Kafa: Open another terminal and run:

```bash
docker exec -it spark-master spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 jobs/spark-streaming.py
```


## Illustrations
### Checking the topic in Kafka 
![confluent.png](imgs%2Fconfluent.png)

### Checking the indice in Elasticsearch cloud
![elastic.png](imgs%2Felastic.png)



