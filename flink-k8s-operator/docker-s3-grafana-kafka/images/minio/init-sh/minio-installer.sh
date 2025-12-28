#!/bin/bash

echo "Starting MinIO configuration..."

echo "MINIO_ROOT_USER length: ${#MINIO_ROOT_USER}"
echo "MINIO_ROOT_PASSWORD length: ${#MINIO_ROOT_PASSWORD}"
echo "AWS_ACCESS_KEY_ID length: ${#AWS_ACCESS_KEY_ID}"
echo "AWS_SECRET_ACCESS_KEY length: ${#AWS_SECRET_ACCESS_KEY}"

# Configure MinIO
echo "Configuring MinIO..."
mc config host add minio http://localhost:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"

if [ $? -ne 0 ]; then
    echo "Failed to configure MinIO host. Error code: $?"
    mc config host add minio http://localhost:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"
    # exit 1
fi

Creating key pair
echo "Creating service account..."
mc admin user svcacct add minio "${MINIO_ROOT_USER}" --access-key "${AWS_ACCESS_KEY_ID}" --secret-key "${AWS_SECRET_ACCESS_KEY}"

if [ $? -ne 0 ]; then
   echo "Failed to create service account. Error code: $?"
   mc admin user svcacct add minio "${MINIO_ROOT_USER}" --access-key "${AWS_ACCESS_KEY_ID}" --secret-key "${AWS_SECRET_ACCESS_KEY}"
   exit 1
fi

# Creating bucket for the bucket name
echo "Creating $BUCKET_NAME bucket..."
mc mb minio/$BUCKET_NAME

if [ $? -ne 0 ]; then
    echo "Failed to create $BUCKET_NAME bucket. Error code: $?"
    mc mb minio/$BUCKET_NAME
    exit 1
fi

echo "MinIO initialization completed successfully."