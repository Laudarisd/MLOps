# NVIDIA Triton Inference Server Setup Guide

This folder contains instructions and sample configs for running NVIDIA Triton Inference Server to serve AI/ML models in your MLOps stack.

---

## 1. What is Triton Server?
NVIDIA Triton Inference Server is an open-source server for serving deep learning models from frameworks like TensorFlow, PyTorch, ONNX, and more. It supports GPU and CPU inference, model versioning, and high-performance batching.

---

## 2. Prerequisites
- Docker installed (recommended)
- NVIDIA GPU and drivers (for GPU inference)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) (for GPU support)
- Your trained model(s) exported in a supported format (e.g., ONNX, TensorFlow SavedModel, TorchScript)

---

## 3. Prepare Model Repository
- Create a directory structure like:
  ```
  model_repository/
    my_model/
      1/
        model.onnx
      config.pbtxt
  ```
- See [Triton Model Repository docs](https://github.com/triton-inference-server/server/blob/main/docs/model_repository.md) for details.

---

## 4. Run Triton Server with Docker
```sh
docker run --gpus=all --rm -p8000:8000 -p8001:8001 -p8002:8002 \
  -v $(pwd)/model_repository:/models \
  nvcr.io/nvidia/tritonserver:23.09-py3 \
  tritonserver --model-repository=/models
```
- Ports:
  - 8000: HTTP/gRPC
  - 8001: gRPC
  - 8002: Metrics (Prometheus)

---

## 5. Test Inference
- Use [tritonclient](https://github.com/triton-inference-server/client) Python SDK:
  ```python
  import tritonclient.http as httpclient
  client = httpclient.InferenceServerClient(url="localhost:8000")
  # Prepare input/output and call client.infer(...)
  ```
- Or use curl for HTTP requests.

---

## 6. Security & Best Practices
- Run behind NGINX or a load balancer for TLS/SSL and authentication
- Restrict access to inference endpoints
- Monitor with Prometheus (metrics on port 8002)

---

## 7. References
- [Triton Inference Server Docs](https://github.com/triton-inference-server/server)
- [Model Repository Format](https://github.com/triton-inference-server/server/blob/main/docs/model_repository.md)
- [Triton Client Examples](https://github.com/triton-inference-server/client)
