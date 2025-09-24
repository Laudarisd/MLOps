# Autoscaling in MLOps Infrastructure

This folder contains guides and configuration examples for enabling autoscaling in your MLOps stack (Docker, Kubernetes, or cloud-native).

---

## 1. What is Autoscaling?

Autoscaling automatically adjusts the number of running instances (containers, pods, VMs) based on demand, optimizing cost and performance.

---

## 2. Kubernetes Horizontal Pod Autoscaler (HPA)

- See `../k8s/hpa.yaml` for a sample HPA manifest
- To enable HPA:
  1. Deploy your app and metrics server
  2. Apply the HPA manifest:
     ```sh
     kubectl apply -f ../k8s/hpa.yaml
     ```
  3. Monitor scaling with:
     ```sh
     kubectl get hpa
     ```

---

## 3. Docker Swarm Autoscaling

- Use external tools (e.g., Docker Compose + Watchtower, custom scripts)
- No built-in autoscaler in Docker Swarm

---

## 4. Cloud Autoscaling (AWS, Azure, GCP)

- Use managed services (e.g., AWS EC2 Auto Scaling Groups, Azure VMSS, GCP Instance Groups)
- Configure scaling policies in the respective cloud console

---

## 5. References

- [Kubernetes HPA Docs](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [AWS Auto Scaling](https://docs.aws.amazon.com/autoscaling/)
- [Azure VMSS](https://learn.microsoft.com/azure/virtual-machine-scale-sets/)
- [GCP Instance Groups](https://cloud.google.com/compute/docs/instance-groups/)
