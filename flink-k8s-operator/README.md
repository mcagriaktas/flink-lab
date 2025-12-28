# Flink-K8S-Operator (Application Mode)

Flink Kubernetes Operator with Flink 2.0.0 and S3 High Availability (HA) mode.

Application Mode: Application Mode runs one job on the cluster. The cluster is only for this single job. In production, this makes things easier. When you open the Flink UI, you will see that you cannot cancel the job. This is because the Flink Kubernetes Operator will restart the pod automatically if there is any problem. For this reason, Application Mode is simple to use and easy to manage.

<p align="center">
  <img width="407" height="394" alt="Untitled" src="https://github.com/user-attachments/assets/10050a45-8ae8-49ea-8835-3e5def85c4d6" />
</p>

Medium Article: https://medium.com/@mucagriaktas/high-availability-flink-on-kubernetes-with-s3-and-kafka-4-0-0-application-mode-99634399fdb1?postPublishedType=initial

## Requirements:
1. Docker-Desktop
2. Linux

### Pre-Request for Env.
In this deployment we need to use S3 for our Flink HA, for this reaons we need to build a S3 Minio container, also there're alot of panel for Flink monitoring, for this reaons I added: 
1. Kafka Cluster : `host.docker.internal:19093,host.docker.internal:29093,host.docker.internal:39093`
2. S3-Minio      : `http://localhost:9001/`
3. Pushgateway   : `http://localhost:9091/`
4. Promethues    : `http://localhost:9090/`
5. Grafana       : `http://localhost:3000/`
6. Kafka-UI      : `http://localhost:8080/`

Start the demo: There're some enviorement in the docker-compose.yml, for this reason update `.env` file or use default values, if you update the `.evn` file `bucket_name` ensure to the change `flink-k8s-deployment/flink-cluster-deployment.yaml` HA kubernetes configuration too.
```bash
cd docker-s3-grafana-kafka
docker compose up -d --build
```

---

### Artitecture:
```bash
--> docker-s3-grafana-kafka : S3 (Minio), Grafana, Prometheus, Pushgateway
--> flink-client-jar        : Flink ETL Code (JAVA-SCALA3-PYTHON)
--> flink-container-image   : Flink Image Builder
--> flink-k8s-deployment    : Flink K8S Operator yml
```

### Some Detail Explanation (Medium Article)
Firstly you can read the article firstly or follow build setup and explore!
LINKKKKKK

### How to Start

1. Install Cert-Manager:
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.1/cert-manager.yaml

# Wait for cert-manager to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=cert-manager -n cert-manager --timeout=300s
```

2. Install Flink K8S Operator:
```bash
helm repo add flink-operator-repo https://downloads.apache.org/flink/flink-kubernetes-operator-1.13.0/

# Install the Flink operator
helm install flink-kubernetes-operator \
  flink-operator-repo/flink-kubernetes-operator \
  --namespace flink \
  --create-namespace
```

3. Build the Image:
```bash
# Scala Jar
cd flink-client-jar/scala
scala-cli package FlinkKafkaClient.scala -f --assembly -o flink-client.jar
cd ../..

# Java Jar
cd flink-client-jar/java
mvn clean package
cd ../..

cp flink-client-jar/java/target/flink-k8s-client-1.0.jar flink-container-image/.

cd flink-container-image && \
imagename=v1 && \
dockerhub_username=mucagriaktas && \
docker build -t flink-cagri:$imagename . && \
docker tag flink-cagri:$imagename $dockerhub_username/flink-client:$imagename && \
docker push $dockerhub_username/flink-client:$imagename && \
cd ..
```

4. Install Flink Cluster (with your configs):
```bash
kubectl apply -f flink-k8s-deployment/flink-cluster-deploy.yaml

kubectl wait --for=condition=ready pod -l app=flink-cagri -n flink --timeout=300s
```

5. Start the data-get for testing:
DO NOT FORGET, the data-get is creating every msg 1mb, it's might be overhelm your pc!
```bash
python3 docker-s3-grafana-kafka/data-generator/data-gen.py
```

6. Check Kafka-UI and Grafana dashboard:
```bash
http://localhost:8080 # Kafka UI
http://localhost:3000 # Grafana Dashboard
http://localhost:8081 # flink UI
```

---

NOT: If your kubernetes cluster is not allow autoscale, give the Flink service account resource:

1. kubectl delete configmap autoscaler-flink-cagri -n flink
2. kubectl edit clusterrole flink-operator
```bash
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - get
  - list
  - watch
```
