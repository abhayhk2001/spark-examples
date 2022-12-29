Create Docker Image and Push

```
sudo su
docker build -t py_minio:1.0
docker tag py_minio:1.0 abhayhk1/py_minio:1.0 
docker login
docker image push abhayhk1/py_minio:1.0 
``` 

In kubernetes environment
```

```