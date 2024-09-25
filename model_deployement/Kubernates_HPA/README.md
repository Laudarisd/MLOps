## Kubernetes

## Horizontal Pod Autoscaling

Kubernetes (K8s) is a powerful, open-source platform used to automate the deployment, scaling, and management of containerized applications. It's especially useful for managing large-scale applications with many moving parts, enabling automatic scaling, load balancing, and more. In Kubernetes, applications are run inside containers (typically Docker containers) and these containers are managed by pods, which are the smallest deployable units in Kubernetes. 

Pods are groups of one or more containers that share storage, network, and other resources.



In  Kubernates, a horizontalPodAutoscaler automatically scales the number of pods in a replication controller, deployment, replica set or stateful set based on observed CPU utilization (or, with custom metrics support, on some other application-provided metrics). Horizontal Pod Autoscaling (HPA) in Kubernetes automatically adjusts the number of pods in a deployment or replica set based on observed CPU, memory, or custom metrics. It scales the application horizontally by increasing or decreasing the number of pods to meet the traffic or resource demands, ensuring that your application is resilient, scalable, and cost-efficient.


### Key Concepts:
- **Pods** : A pod is the smallest unit of deployment in Kubernetes, which encapsulates one or more containers (typically Docker containers). Each pod runs on a node in the 
    Kubernetes cluster and shares the same network namespace, storage, and other resources. Pods are managed by controllers like Deployments, ReplicaSets, and StatefulSets.
- **ReplicaSets** : A ReplicaSet is a controller that ensures a specified number of pod replicas are running at any given time. It is used to maintain the desired number of pods for a deployment or replica set, and can automatically scale the number of replicas based on the desired state.
- **Deployments** : A Deployment is a higher-level controller that manages ReplicaSets and enables features like rolling updates, rollbacks, and scaling. It provides declarative updates to pods and ReplicaSets, ensuring that the desired state is maintained.
- **Horizontal Pod Autoscaler (HPA)** : A Horizontal Pod Autoscaler automatically scales the number of pods in a deployment or replica set based on CPU usage, memory usage, or custom
 
 
### How HPA Works:
- Kubernetes continuously monitors the resource consumption of each pod (e.g., CPU usage, memory).
- The HPA controller periodically checks the metrics and adjusts the number of pods if necessary.
- For example, if traffic increases and the CPU usage exceeds a specified threshold, the HPA will create new pods to handle the increased load.
- Similarly, if the traffic decreases, it will scale down the number of pods to save resources.

---

## High-Level Steps to Implement Kubernetes with Horizontal Pod Autoscaling (HPA)

1. **Set Up Kubernetes Cluster**:

- First, you need a running Kubernetes cluster. This can be done locally using tools like Minikube or in the cloud using platforms like Google Kubernetes Engine (GKE), Amazon EKS, or Azure AKS. For this example, we will use Minikube to set up a local Kubernetes cluster.

- Install Minikube by following the instructions in the [Minikube documentation](https://minikube.sigs.k8s.io/docs/start/).


Minikubes helps to create a multi-node cluster with the following command:
    
    ```bash
    minikube start --nodes 3
    ```


2. **Containerize Your Application**:

- Your application needs to be packaged into a Docker container.

- This means you’ll write a Dockerfile that defines the environment in which your application will run and how it will be executed.

3. **Deploy Your Application on Kubernetes**:

 - After your application is containerized, you will deploy it to the Kubernetes cluster using a Deployment configuration. This deployment will specify how many replicas of the pod should be running.

4. **Set Up Horizontal Pod Autoscaling (HPA)**:

- Once the application is deployed, you will configure the HPA. This configuration will define the CPU or memory threshold that triggers Kubernetes to scale the number of pods.

5. **Monitor and Manage Scaling**:

- The HPA will automatically scale the number of pods based on the load. You can monitor the number of pods and the resource usage using Kubernetes dashboards or command-line tools like kubectl.



---



## References:

- [minikube](https://minikube.sigs.k8s.io/docs/tutorials/multi_node/)
- [Kubernates(Horizontal Pod Autoscaling)](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
