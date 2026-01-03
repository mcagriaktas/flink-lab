# producer.py
from confluent_kafka import Producer
import json
from time import sleep

producer_conf = {
   # Essential Configs
    'bootstrap.servers': 'localhost:19092,localhost:29092,localhost:39092',     # Kafka broker address
    'client.id': 'python-producer',             # Client ID for the producer

    # Message Delivery
    'acks': 'all',                              # Ensure all replicas acknowledge
    'message.timeout.ms': 120000,               # Timeout for message delivery
    'request.timeout.ms': 30000,                # Timeout for requests to the broker
    'max.in.flight.requests.per.connection': 5, # Maximum in-flight requests
    'enable.idempotence': True,                 # Ensure exactly-once delivery
    'retries': 2147483647,                      # Number of retries on failure
    'retry.backoff.ms': 100,                    # Delay between retries

    # Batching & Compression
    'compression.type': 'none',                 # Compression type (none, gzip, snappy, lz4, zstd)
    'linger.ms': 0,                             # Delay in milliseconds to wait for batching
    'batch.num.messages': 10000,                # Maximum number of messages per batch
    'batch.size': 16384,                        # Maximum batch size in bytes

    # Memory & Buffers
    'message.max.bytes': 1000000000,               # Maximum message size
    'queue.buffering.max.messages': 100000,     # Maximum number of messages in the queue
    'queue.buffering.max.kbytes': 1048576,      # Maximum size of the queue in KB
    'queue.buffering.max.ms': 0,                # Maximum time to buffer messages

    # Network & Timeouts
    'socket.timeout.ms': 60000,                 # Socket timeout
    'socket.keepalive.enable': True,            # Enable TCP keep-alive
    'socket.send.buffer.bytes': 0,              # Socket send buffer size (0 = OS default)
    'socket.receive.buffer.bytes': 0,           # Socket receive buffer size (0 = OS default)
    'socket.max.fails': 3,                      # Maximum socket connection failures

    # Security - Basic
    # 'security.protocol': 'PLAINTEXT',           # Security protocol (PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL)
    # 'ssl.ca.location': None,                    # Path to CA certificate
    # 'ssl.certificate.location': None,           # Path to client certificate
    # 'ssl.key.location': None,                   # Path to client private key
    # 'ssl.key.password': None,                   # Password for the private key

    # SASL Authentication
    # 'sasl.mechanism': 'PLAIN',                  # SASL mechanism (PLAIN, GSSAPI, SCRAM-SHA-256, SCRAM-SHA-512)
    # 'sasl.username': None,                      # SASL username
    # 'sasl.password': None,                      # SASL password
}

producer = Producer(producer_conf)
topic = "cagri-source"

import sys

# Define 1 MB in bytes
TARGET_SIZE = 1024 * 1024  # 1,048,576 bytes

def delivery_report(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        # Avoid printing the full 'msg' object here because it is 1MB large!
        print(f'Message delivered to topic:{msg.topic()}, partition:[{msg.partition()}] at offset {msg.offset()}')

for i in range(10000000):
    # 1. Create your prefix
    prefix = f'cagri-{i}'

    # 2. Calculate how much padding is needed
    # We use len(prefix) assuming standard ASCII characters (1 char = 1 byte)
    padding_needed = TARGET_SIZE - len(prefix)

    # 3. Create the full 1 MB string
    # We add the prefix + a repeated character (like 'x') to fill the rest
    value_str = prefix + ('x' * padding_needed)

    try:
        producer.produce(topic, key=None, value=value_str, callback=delivery_report)

        # Trigger the callback to clear the internal buffer
        producer.poll(0)

    except BufferError:
        # If the local buffer is full, wait a bit
        print(f"Local buffer full, waiting...")
        producer.poll(1)

    sleep(0.01) # Optional: comment this out if you want to test maximum throughput

producer.flush()
print("Done!")
