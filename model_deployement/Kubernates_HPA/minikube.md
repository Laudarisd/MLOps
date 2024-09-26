Kubernets is an open-source patform designed to automate the deployment, scaling, and operation of containerised applications. It helps developers to manage clusrters of containers(such as Docker containers) efficiently, provising scalability, resilience, and fault tolerance.

When gettig started with Kubernetes, one of the simplest ways to set up a local cluster for testing and development is by using `Minikube`. Minikube allows you to run a kubernetes cluster locally on our computer.

## Why Do We Need  a Kubernetes Cluster?

A Kubernetes cluster is a set of nodes (machines) that run containerized applications. The cluster consists of at least one master node (which manages the cluster) and multiple worker nodes (which run the actual applications).


Some benefits of using Kubernetes clusters include:

- **Scalability**: Easily scale up or down by adding/removing nodes or containers (pods).
- **High Availability**: The cluster ensures that applications are always running and distributed across nodes, reducing downtime.
- **Resource Efficiency**: Kubernetes optimizes the use of resources (CPU, memory) across nodes and can autoscale applications based on demand.
- **Self-Healing**: If an application crashes or a node goes down, Kubernetes automatically restarts or replaces the application to ensure minimal downtime.


---

# What is Minikube?
Minikube is a lightweight Kubernetes implementation that allows us to run a single-node Kubernetes cluster locally. It’s designed for testing and development purposes and is perfect for learning Kubernetes without the complexity of a full-fledged cloud setup.

### Use cases of Minikunbe:
 - Running a local Kubernetes cluster for development.
 - Testing Kubernetes applications in a lightweight environment.
 - Experimenting with Kubernetes features without the need for cloud services.

 --- 

 ## Setting Up Minikube

 ### Prerequisites:
 - Virtualization software (e.g., VirtualBox, KVM, HyperKit): Minikube runs a virtual machine (VM) to host the Kubernetes cluster, so you need a hypervisor installed on our machine. This helps to create a VM to run the Kubernetes cluster.
    - Windows: Hyper-V or VirtualBox
    - macOS: HyperKit or VirtualBox
    - Linux: KVM or VirtualBox

- kubectl: The Kubernetes command-line tool (kubectl) is used to interact with the Kubernetes cluster. You can install kubectl using the package manager for our operating system. The kubectl tool allows us to run commands against Kubernetes clusters.

---

## Step-by-Step Guide to Set Up Minikube:

### Step 1: Install a Hypervisor

Depending on our operating system, we need to install a hypervisor to run the Minikube VM. Here are some common options:

- **Windows**: Install VirtualBox or Hyper-V.
    - Open a PowerShell window as an administrator and run the following command to enable Hyper-V:
        ```bash
            dism.exe /Online /Enable-Feature:Microsoft-Hyper-V /All
        ```
    - Alternatively, you can install VirtualBox by downloading the installer from the [VirtualBox website](https://www.virtualbox.org/).

- **macOS**: Install HyperKit or VirtualBox.
    - HyperKit is the default hypervisor for Minikube on macOS. You can install it using Homebrew:
        ```bash
            brew install hyperkit
        ```
    - If you prefer to use VirtualBox, you can download the installer from the [VirtualBox website](https://www.virtualbox.org/).

- **Linux**: Install KVM or VirtualBox.
    - For KVM, we can install it using the package manager for your Linux distribution (e.g., apt, yum, dnf).
    ```bash
        sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
        sudo apt-get install virt-manager
    ```

    - For VirtualBox, you can download the installer from the [VirtualBox website](https://www.virtualbox.org/).


### Step 2: Install Minikube

- **Windows**:
    - Download the Minikube installer from the [Minikube releases page](https://github.com/kubernetes/minikube/releases/tag/v1.34.0)
    - Run the installer and follow the on-screen instructions.

- **macOS**:
    - Install Minikube using Homebrew:
        ```bash
            brew install minikube
        ```

- **Linux**: 
    - Downlload and install Minikube using the following commnads:
        ```bash
            curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
            sudo install minikube-linux-amd64 /usr/local/bin/minikube
        ```

### Step 3: Install kubectl

`kubectl` is the command-line tool that allows you to interact with your Kubernetes cluster. Install it by following the instructions below:

- **Windows**:
    - Download the kubectl binary from the [Kubernetes release page](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/).
    - Add the kubectl binary to your PATH environment variable.

- **macOS**:
    - Install kubectl using Homebrew:
        ```bash
            brew install kubectl
        ```

- **Linux**:
    - Download the kubectl binary using the following command:
        ```bash
            curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
            sudo install kubectl /usr/local/bin/kubectl
        ```


### Step 4: Start Minikube

Once you have installed Minikube and kubectl, you can start a local Kubernetes cluster using Minikube. Run the following command:

```bash
minikube start
```
Minikube will automatically download the necessary Kubernetes components and create a local cluster.

### Step 5: Verify the Cluster and installation

Once the cluster is up and running, verify the installation using the kubectl command:

```bash
kubectl get nodes
```

This command should display the nodes in your Kubernetes cluster, which should show a single node (the Minikube VM).
 
 ```bash
 NAME       STATUS   ROLES    AGE   VERSION
minikube   Ready    master   10m   v1.21.0
```


### Step 6: Step 6: Deploy an Application to Minikube
To test that Minikube is working correctly, deploy a simple Kubernetes application. For example, deploy a Nginx web server:
    
    ```bash
    kubectl create deployment nginx --image=nginx
    ```

This command creates a deployment named `nginx` using the official Nginx Docker image. You can expose the deployment as a service to access it from outside the cluster:

```bash
kubectl expose deployment nginx --port=80 --type=NodePort
```

This command creates a service of type `NodePort` that exposes the Nginx deployment on a port accessible from outside the cluster. You can access the Nginx service using the Minikube IP address and the NodePort:

This command will open a browser window with the Nginx welcome page.

Finally, use Minikube to get the URL of the Nginx service:

```bash
minikube service nginx
```
```bash
minikube service nginx --url
```



---

### Installation and Activation of Minikube in Linux server

1. **INstall Virtualization**:
    - VirtualBox installation:
        ```bash
        sudo apt-get update
        sudo apt-get install virtualbox
        ```

2. **Install kubectl**:
    - Download the latest release with the command:
        ```bash
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        ```
    - Make it executable:
        ```bash
        chmod +x kubectl
        ```
    - Move the binary in to your PATH:
        ```bash
        sudo mv kubectl /usr/local/bin/
        ```
    - Test to ensure the version you installed is up-to-date:
        ```bash
        kubectl version --client
        # Output
        Client Version: v1.31.1
        Kustomize Version: v5.4.2
        ```

3. **Install Minikube**:

- Download the latest release with the command:
    ```bash
        curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    ```
- Make the binary executable:
    ```bash
        chmod +x minikube-linux-amd64
    ```
- Add the Minikube executable to your path:
    ```bash
        sudo mv minikube-linux-amd64 /usr/local/bin/minikube
    ```

- Verify the installation:
    ```bash
        minikube version
    
    # Output
    minikube version: v1.34.0
    commit: 210b148df93a80eb872ecbeb7e35281b3c582c61
    ```

4. **Start Minikube**:
Once Minikube is installed, you can start your Kubernetes cluster. You can specify the driver (VirtualBox, KVM, etc.) based on your installed hypervisor.

- Start Minikube with the VirtualBox driver:
    ```bash
    minikube start --driver=virtualbox
    ```
If you have another hypervisor installed, you can specify it as the driver. For example, to start Minikube with the KVM driver, you can use the following command:

```bash
minikube start --driver=kvm2
```

- Verify that Minikube is running:
    ```bash
    minikube status
    ```
    ```bash
    kubectl get nodes
    ```
    - output should be like:
        ```bash
        NAME       STATUS   ROLES           AGE    VERSION
        minikube   Ready    control-plane   102m   v1.31.0
        ```

---

To start a cluster with 2 nodes in the driver of your choice

```bash
minikube start --nodes 2 -p <profile-name>
```
This command will start a multi-node cluster with 2 nodes using the specified driver. The `-p` flag allows you to specify a profile name for the cluster.

- Get the list of nodes in the cluster:

```bash
kubectl get nodes

or 

kubectl get nodes -o wide
```

For instance, if I start with `minikube start --nodes 2 -p aice` then the oput[ut will be like:

```bash
NAME       STATUS   ROLES           AGE     VERSION
aice       Ready    control-plane   7m34s   v1.31.0
aice-m02   Ready    <none>          6m9s    v1.31.0
```

Where, 

- `aice` is the master node
- `aice-m02` is the worker node

We will use 

- Check the status of the cluster:

```bash
minikube status -p <profile-name>
```




**Understanding --nodes and Node Count in Kubernetes**

When you specify --nodes in Minikube or any other Kubernetes setup (such as a cloud provider), you are defining the number of nodes in the Kubernetes cluster.

    - Nodes in Kubernetes are individual machines (either physical or virtual) that make up the cluster.
        
    - Each node provides CPU, memory, and storage resources, but it is not directly tied to the number of processors (CPU cores) in that node.

**What Happens with --nodes 5?**

If you create a Kubernetes cluster with --nodes=5, it means you are creating a cluster with 5 separate machines (nodes), not necessarily 5 processors. Each node could have 1 or more CPUs depending on how the node is configured.

for example:

- If you run

```bash
nimikube start --nides=5
```

This command will create a Kubernetes cluster with 5 nodes. Each node will have its own resources (CPU, memory, storage) and will be managed by the Kubernetes control plane.

### Stopping and Deleting a Minikube Cluster

To stop a Minikube cluster, you can use the following command:



**Higher Nodes in a Cluster: Is it Good?**

Yes, having more nodes in a Kubernetes cluster can be beneficial, depending on your use case. Here's why:

    - Increased Resource Capacity: Each node in a Kubernetes cluster typically represents a separate machine (either physical or virtual) that contributes CPU, memory, and storage to the overall cluster. More nodes mean more overall resources for running applications.

    - Improved Availability: If you have more nodes, your cluster is less likely to experience downtime. Kubernetes can spread pods across different nodes, so if one node fails, the pods can still run on other nodes.

    - Load Distribution: More nodes allow Kubernetes to spread workloads across the cluster, reducing the likelihood that any single node will become a bottleneck.

    - Fault Tolerance: In a multi-node cluster, Kubernetes can handle node failures. If a node goes down, Kubernetes can automatically reschedule the pods on other nodes, providing redundancy.

**When is a Higher Number of Nodes Beneficial?**

    - Production Workloads: In production environments where you need high availability, scalability, and fault tolerance, more nodes help you scale up resources while ensuring uptime.
    - Distributed Applications: For applications with significant CPU, memory, and disk requirements,   adding more nodes helps balance the load.
    - Large Deployments: More nodes are essential when you have a large number of deployments or workloads that need to run concurrently.
    - Note: While more nodes provide greater capacity and availability, they also come with increased management complexity and resource costs (especially if you’re using cloud resources).


**Does --nodes=5 Mean I Have 5 Processors?**

No, --nodes=5 does not mean you have 5 processors. Instead, it means you have 5 separate nodes (machines) in your Kubernetes cluster. Each node can have 1 or more CPUs (processors), depending on how you configure the node.

### Number of Nodes vs. Number of Processors (CPUs)
    - Node: A machine in the Kubernetes cluster that runs applications. It can be virtual or physical and can have multiple CPUs (or processors) and memory.

    - CPU (Processor): Each node has a certain number of CPUs (or cores) available for running containers. You can control how many CPUs are allocated to each node (machine), but the number of nodes does not directly correlate to the number of CPUs.


Example:

1. Cluster with 5 nodes:

- 5 separate virtual/physical machines running Kubernetes.
- Each node could have different configurations, like 2 CPUs and 4GB RAM, depending on how the node is set up.

2. Single node with 5 CPUs:

- A single machine with 5 CPU cores allocated for running workloads.
3. 5 Nodes with 4 CPUs each:

- In this case, you have 5 separate nodes, each with 4 CPUs (totaling 20 CPUs across the entire cluster).


### How to Control Node CPU Allocation?
In Kubernetes (especially in cloud or local virtual environments), you can control how many CPUs are assigned to each node.

For example, with Minikube, you can specify the number of CPUs when starting a cluster:

```bash
minikube start --nodes=5 --cpus=2
```

This command starts a Minikube cluster with 5 nodes, each with 2 CPUs. The --cpus flag allows you to specify the number of CPUs for each node.


```bash
minikube stop
```

This command will stop the running Minikube cluster. To delete the Minikube cluster and free up resources, you can use the following command:

```bash
minikube delete
```

This command will delete the Minikube cluster and remove all associated resources. Be careful when using this command, as it will delete all data associated with the cluster.

---

##3 Can We Generate Multiple Clusters on the Same Machine?






## Let's practice with an application
















