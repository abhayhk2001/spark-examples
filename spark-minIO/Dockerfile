FROM abhayhk1/spark-py:3.1.3
USER root
WORKDIR /app
COPY requirements.txt .
COPY spark-minIO.py .
RUN pip install -r requirements.txt

# bin/docker-image-tool.sh -r docker.io/abhayhk1 -t 3.1.3 -u 1000 -b java_image_tag=11-jre-slim -p ./kubernetes/dockerfiles/spark/bindings/python/Dockerfile build

