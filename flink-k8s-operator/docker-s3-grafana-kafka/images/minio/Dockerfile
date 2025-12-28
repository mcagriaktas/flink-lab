FROM minio/minio:RELEASE.2023-08-23T10-07-06Z

ENV MINIO_ROOT_USER_FILE=
ENV MINIO_ROOT_PASSWORD_FILE=
ENV BUCKET_NAME=
ENV MINIO_DOMAIN=minio 

RUN microdnf install curl -y && microdnf clean all

COPY ./init-sh/minio-starter.sh /usr/bin/
RUN chmod +x /usr/bin/minio-starter.sh

COPY ./init-sh/minio-installer.sh /usr/bin/
RUN chmod +x /usr/bin/minio-installer.sh

ENTRYPOINT ["minio-starter.sh"]