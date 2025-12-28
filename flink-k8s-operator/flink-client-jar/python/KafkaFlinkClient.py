#!/usr/bin/env python3

from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col

def get_table_env():
    # --------------------------------------------
    # Defination PyFlink Configratuin for Scripts
    # --------------------------------------------
    env_settings = EnvironmentSettings.in_streaming_mode()
    table_env = TableEnvironment.create(env_settings)

    table_env.get_config().set("pipeline.name", "cagri-flink-sql-job")

    return table_env

def kafka_source(table_env):
    # --------------------------------------------
    # Defination Kafka Topic's Connection and Consumer Configurations
    # --------------------------------------------
    return table_env.execute_sql("""
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

def kafka_sink(table_env):
    # --------------------------------------------
    # Defination Kafka Topic's Connection and Producer Configurations
    # --------------------------------------------
    return table_env.execute_sql("""
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

def kafka_transform_table_api(src_df):
    # --------------------------------------------
    # Transfrom the value_string column to cagri-xyz -> xyz
    # --------------------------------------------
    transformed_df = src_df.select(col('value_string').substring(7, 100).alias('value_string'))
    return transformed_df

def kafka_transfrom_sql_api(table_env):
    # --------------------------------------------
    # Transfrom the value_string column to cagri-xyz -> xyz
    # --------------------------------------------
    return table_env.execute_sql("""
    INSERT INTO cagri_sink
      SELECT SUBSTRING(value_string, 7) AS value_string
    FROM cagri_source
  """)

def main():
    # --------------------------------------------
    # Defination Kafka Topic's Table for Flink
    # --------------------------------------------
    table_env = get_table_env()
    kafka_source(table_env)
    kafka_sink(table_env)

    # --------------------------------------------
    # Read Source Kafka Topic then Use Data and Load the Target Source with Table API
    # --------------------------------------------
    # src_df = table_env.from_path("cagri_source")
    # table_api_transformed_df = kafka_transform_table_api(src_df)
    # table_api_transformed_df.execute_insert("cagri_sink").wait()

    # --------------------------------------------
    # Use Data and Load the Target Source with SQL API
    # --------------------------------------------
    kafka_transfrom_sql_api(table_env)


if __name__ == "__main__":
    main()