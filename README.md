# SF Crime Statistics with Spark Streaming

Project 2 of the [Data Streaming](https://www.udacity.com/course/data-streaming-nanodegree--nd029) Nanodegree Program.

## Getting started

1. Install requirements using `./start.sh` if you use conda for Python. If you use pip rather than conda, then use `pip install -r requirements.txt`.

2. Navigate to the folder where you unzipped your Kafka download:
    * Begin with starting Zookeeper `bin/zookeeper-server-start.sh config/zookeeper.properties`
    * Then start Kafka server `bin/kafka-server-start.sh config/server.properties`

3. Start the bootstrap Kafka producer b `python kafka_server.py`

You can test the Kafka producer with the Kafka Console Reader

```cli
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic mh.crime.report --from-beginning
```

### Udacity Data Streaming provided workspace instructions

The path to Zookeeper and Kafka is /usr/bin:
* `/usr/bin/zookeeper-server-start config/zookeeper.properties`
* `/usr/bin/kafka-server-start config/server.properties`

Running the Kafka Console Consumer in the Data Streaming provided workspace 
```cli
/usr/bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic mh.crime.report --from-beginning
```
## Screenshots from step 2
_not done_

## Answers to step 3 questions

Write the answers to these questions in the README.md doc of your GitHub repo:

### 1. How did changing values on the SparkSession property parameters affect the throughput and latency of the data?
_not done_

### 1. What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?
_not done_


## Dependencies

[kafka-python](https://kafka-python.readthedocs.io)
