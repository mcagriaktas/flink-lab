//> using scala "3.7.2"
//> using dep "org.apache.flink:flink-table-api-java-bridge:2.0.1"
//> using dep "org.apache.flink:flink-streaming-java:2.0.1"
//> using dep "org.apache.flink:flink-clients:2.0.1"
//> using dep "org.apache.flink:flink-connector-kafka:4.0.0-2.0"
//> using dep "org.apache.flink:flink-table-runtime:2.0.1"

import org.apache.flink.table.api._
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment
import org.apache.flink.configuration.Configuration

def streamingEnv(): StreamTableEnvironment = {
  val env = StreamExecutionEnvironment.getExecutionEnvironment

  env.setParallelism(4)
  env.enableCheckpointing(env.getCheckpointConfig.getCheckpointInterval)
  env.getCheckpointConfig.setCheckpointTimeout(600000)
  env.getCheckpointConfig.setMaxConcurrentCheckpoints(1)
  env.getCheckpointConfig.setTolerableCheckpointFailureNumber(3)

  val tableEnv = StreamTableEnvironment.create(env)
  val conf = tableEnv.getConfig.getConfiguration

  conf.setString("pipeline.name", "flink-cagri-production-pipeline")

  return tableEnv
}

def kafkaSource(tableEnv: StreamTableEnvironment): Unit = {
  tableEnv.executeSql("""
    CREATE TABLE cagri_source (
        value_string STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'cagri-source',
        'properties.bootstrap.servers' = 'host.docker.internal:19093,host.docker.internal:29093,host.docker.internal:39093',
        'properties.group.id' = 'flink-cagri-job',
        'scan.startup.mode' = 'group-offsets', 
        'properties.auto.offset.reset' = 'earliest',
        'properties.enable.auto.commit' = 'true',
        'format' = 'raw',
        'properties.commit.offsets.on.checkpoint' = 'true'
    )
  """)
}

def kafkaSink(tableEnv: StreamTableEnvironment): Unit = {
  tableEnv.executeSql("""
    CREATE TABLE cagri_sink (
        value_string STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'cagri-sink',
        'properties.bootstrap.servers' = 'host.docker.internal:19093,host.docker.internal:29093,host.docker.internal:39093',
        'format' = 'json',
        'properties.acks' = 'all',
        'properties.enable.idempotence' = 'true'
    )
  """)
}

def transfromData(tableEnv: StreamTableEnvironment): Unit = {
  tableEnv.executeSql("""
    INSERT INTO cagri_sink
      SELECT SUBSTRING(value_string, 7) AS value_string
    FROM cagri_source
  """)
}

@main
def flinkKafkaJob(args: String*): Unit = {
  val tableEnv = streamingEnv()

  // Source and Sink Table
  kafkaSource(tableEnv)
  kafkaSink(tableEnv)

  // Transfrom Data
  transfromData(tableEnv)

  println("✅ Flink job submitted. cagri-source ➡️ cagri-sink")
}