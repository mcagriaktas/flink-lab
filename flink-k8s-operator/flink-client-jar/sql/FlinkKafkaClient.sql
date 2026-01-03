SET 'execution.checkpointing.interval' = '10s';
SET 'execution.checkpointing.timeout' = '10min';
SET 'execution.checkpointing.max-concurrent-checkpoints' = '1';
SET 'execution.checkpointing.tolerable-failure-number' = '3';
SET 'pipeline.name' = 'flink-cagri-production-pipeline-java';

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
    'properties.max.partition.fetch.bytes' = '1572864'
);

CREATE TABLE cagri_sink (
    value_string STRING
    ) WITH (
    'connector' = 'kafka',
    'topic' = 'cagri-sink',
    'properties.bootstrap.servers' = 'host.docker.internal:19093,host.docker.internal:29093,host.docker.internal:39093',
    'format' = 'json',
    'properties.acks' = 'all',
    'properties.enable.idempotence' = 'true',
    'properties.max.request.size' = '1572864'
);

INSERT INTO cagri_sink
    SELECT SUBSTRING(value_string, 7) AS value_string
FROM cagri_source;