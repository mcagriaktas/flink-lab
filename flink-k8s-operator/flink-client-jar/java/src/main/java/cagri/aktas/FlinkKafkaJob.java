package cagri.aktas;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class FlinkKafkaJob {

    public static StreamTableEnvironment createStreamingEnv() {
        var env = StreamExecutionEnvironment.getExecutionEnvironment();

        env.setParallelism(4);
        
        // Checkpointing Config
        env.enableCheckpointing(10000); 
        
        var checkpointConfig = env.getCheckpointConfig();
        checkpointConfig.setCheckpointTimeout(600000);
        checkpointConfig.setMaxConcurrentCheckpoints(1);
        checkpointConfig.setTolerableCheckpointFailureNumber(3);

        var tableEnv = StreamTableEnvironment.create(env);
        
        // Set Pipeline Name
        tableEnv.getConfig().getConfiguration().setString("pipeline.name", "flink-cagri-production-pipeline-java");

        return tableEnv;
    }

    public static void createKafkaSource(StreamTableEnvironment tableEnv) {
        tableEnv.executeSql("""
            CREATE TABLE cagri_source (
                value_string STRING
            ) WITH (
                'connector' = 'kafka',
                'topic' = 'cagri-source',
                'properties.bootstrap.servers' = 'host.docker.internal:19093,host.docker.internal:29093,host.docker.internal:39093',
                'properties.group.id' = 'flink-cagri-job-java',
                'scan.startup.mode' = 'group-offsets', 
                'properties.auto.offset.reset' = 'earliest',
                'properties.enable.auto.commit' = 'true',
                'format' = 'raw',
                'properties.commit.offsets.on.checkpoint' = 'true',

                -- FOR CONSUMER (READING):
                'properties.max.partition.fetch.bytes' = '1572864'
            )
        """);
        }

    public static void createKafkaSink(StreamTableEnvironment tableEnv) {
        tableEnv.executeSql("""
            CREATE TABLE cagri_sink (
                value_string STRING
            ) WITH (
                'connector' = 'kafka',
                'topic' = 'cagri-sink',
                'properties.bootstrap.servers' = 'host.docker.internal:19093,host.docker.internal:29093,host.docker.internal:39093',
                'format' = 'json',
                'properties.acks' = 'all',
                'properties.enable.idempotence' = 'true',

                -- FOR PRODUCER (WRITING):
                'properties.max.request.size' = '1572864' 
            )
        """);
        }

    public static void transformData(StreamTableEnvironment tableEnv) {
        tableEnv.executeSql("""
            INSERT INTO cagri_sink
            SELECT SUBSTRING(value_string, 7) AS value_string
            FROM cagri_source
        """);
    }

    public static void main(String[] args) {
        // 1. Setup Environment
        var tableEnv = createStreamingEnv();

        // 2. Define Source and Sink
        createKafkaSource(tableEnv);
        createKafkaSink(tableEnv);

        // 3. Transform and Execute
        transformData(tableEnv);

        System.out.println("✅ Flink job submitted. cagri-source ➡️ cagri-sink" );
    }
}