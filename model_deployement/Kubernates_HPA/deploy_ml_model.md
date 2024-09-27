Well, we are finally here...


Let's deploy our ML model using Kubernetes HPA including Docker, fast api and kubernetes.



## Step 1: Create a Dockerfile

Well, we must know Docker and how it works before deploying anything....

So I will try to explain each steps while deploying our ML model using Kubernetes HPA.

---
- **Step 1:** Create a Dockerfile

Docker file is a file that contains all the instructions to build a docker image.
Important thing is that, this file must be named as `Dockerfile` and must be in the root directory of the project. Similarly, it must include application information and dependencies.

In conclusion, we need to build docker image for our app. Docker image is a file that contains all the dependencies and configurations required to run the app. For this process, we docker file and requirements.txt file.

Le's create Docker file:

```bash
touch Dockerfile
```

For instance, my Dockerfile looks like this:

```Dockerfile
# Use a lightweight Python image
FROM python:3.8-slim

# Install necessary system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy all the local files to the working directory
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI server when the container starts
CMD ["uvicorn", "server_run:app", "--host", "0.0.0.0", "--port", "8000"]

```

- **Step 2:** Create a requirements.txt file

Before making a Docker image, we need to create a requirements.txt file that contains all the dependencies of our project.

```bash
touch requirements.txt
```

For instance, my requirements.txt file looks like this:

```txt
    fastapi
    uvicorn
    opencv-python-headless  # For OpenCV without GUI dependencies
    numpy
    concurrent-log-handler
    ultralytics  
```

### Possible Errors

remote permission denied error and to get rid of sudo :

```bash
sudo usermod -aG docker $USER
```

if this doesn't work, try this
```bash
sudo username -aG docker <username>
```



## Step 2: Build Docker Image

Now it's time to create a docker image for our app. We can do this by running the following command:

```bash
docker build -t <image_name> .
```
For instance, my image name is `aice' and I will run the following command:

```bash
docker build -t aice .
```

It might take few minutes to build the image and it can be heavy depending on the project.


## Step 3: Run Docker Image

After building the image, we can run the image using the following command:

```bash
docker run -d --name <container_name> -p 8000:8000 <image_name>
```

For instance, my container name is `aice_container` and I will run the following command:

```bash
docker run -d --name aice_container -p 8000:8000 aice
```


---
After successfully making docker image, we need to push it to our docker hub account. For this, we need to login to our docker account using the following command:

```bash
docker login
```
login with your docker id and passwrod.

Thne tag the image using the following command:

```bash
docker tag <image_id> <docker_id>/<image_name>
```

For instance, if our image id is `aice` and docker id is `laudar`, then we will run the following command:

```bash
docker tag aice laudar/aice
```



## Step 4: Push Docker Image to Docker Hub

Push the docker image to your docker hub account using the following command:

```bash
docker push <docker_id>/<image_name>
```

Forinstance, if our github username is `laudar` and image name is `aice`, then we will run the following command:

```bash
docker push laudar/aice
```

If we pushed the image successfully, we can see the image in our docker hub account.


## Step 5: Deploy ML Model using Kubernetes HPA

- First step is to make `deployment.yaml`. For instance we will use `aice-deployment.yaml` file.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aice-deployment
spec:
  replicas: 2  # Number of pods
  selector:
    matchLabels:
      app: aice
  template:
    metadata:
      labels:
        app: aice
    spec:
      containers:
      - name: aice-container
        image: laudari/aice:latest  # Docker Hub image
        ports:
        - containerPort: 8000
```
This file defines a Deployment with two replicas of your application using the Docker image you pushed to Docker Hub.



- Second step is to make `service.yaml`. For instance we will use `aice-service.yaml` file.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: aice-service
spec:
  type: NodePort  # Expose service to external traffic
  selector:
    app: aice
  ports:
  - protocol: TCP
    port: 8000  # Service port
    targetPort: 8000  # Container port
    nodePort: 30007  # Port on the node (between 30000-32767)

```
This file defines a Service that exposes your application to external traffic on port 30007.


- Third step is to make `hpa.yaml`. For instance we will use `aice-hpa.yaml` file.

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: aice-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: aice-deployment
  minReplicas: 2  # Minimum number of replicas
  maxReplicas: 10  # Maximum number of replicas
  targetCPUUtilizationPercentage: 50  # Target CPU utilization

```
This file defines a Horizontal Pod Autoscaler that scales your application based on CPU utilization. The number of replicas will be between 2 and 10, and the target CPU utilization is 50%.


## Step 6: Deploy ML Model using Kubernetes HPA

- Apply Deployment

```bash
kubectl apply -f aice-deployment.yaml
```

- Apply Service

```bash
kubectl apply -f aice-service.yaml
```
- verigy the deployment and service

```bash
kubectl get pods
```

output will be like this:

```bash
NAME                               READY   STATUS    RESTARTS   AGE
aice-deployment-7d6d7b7ddf-abcde   1/1     Running   0          1m
aice-deployment-7d6d7b7ddf-fghij   1/1     Running   0          1m

```

Make sure that we pull image in docker hub and its running.


- Apply HPA

```bash
kubectl apply -f aice-hpa.yaml
```


