# Model Deployment
There are several ways to deploy a model. Some of the popular ways are as follows:

1. **REST API Frameworks**: 
   - **FastAPI**, **Flask**, **Django**
2. **Advanced Platforms**:
    - **Seldon Core**: Kubernetes-native platform for deploying, scaling, and managing thousands of models.
    - **Kubeflow**: End-to-end orchestration for machine learning workflows on Kubernetes.
    - **TensorFlow Serving**: A flexible, high-performance serving system for machine learning models in production.
    - **TorchServe**: PyTorch-native model serving platform for large-scale deployment.


# Choice of Framework

### 1. **REST API Frameworks**:
   - **FastAPI**, **Flask**, **Django**

**When to Use**:
- **Small to Medium Applications**: When deploying a few machine learning models or building a prototype.
- **Lightweight Applications**: When you need to expose your ML model as an API quickly with minimal infrastructure.
- **Quick Development**: Ideal when the focus is on developing and testing APIs without needing advanced scalability features.

**Pros**:
- **Simple Setup**: Easy to develop and deploy small-scale applications.
- **Flexible**: Can easily integrate with other services (databases, frontends, etc.).
- **Great for Prototyping**: Quickly deploy models for testing or demonstration.
- **Community Support**: Popular frameworks with a large ecosystem of libraries and support.

**Cons**:
- **Limited Scalability**: Not ideal for large-scale or high-traffic applications.
- **Manual Scaling**: Requires manual intervention for scaling, orchestration, and monitoring.
- **Lacks Advanced Features**: No built-in model versioning, A/B testing, or advanced deployment strategies.

### 2. **Advanced Platforms**:
   - **Seldon Core**: Kubernetes-native platform for deploying, scaling, and managing thousands of models.
   - **Kubeflow**: End-to-end orchestration for machine learning workflows on Kubernetes.
   - **TensorFlow Serving**: A flexible, high-performance serving system for machine learning models in production.
   - **TorchServe**: PyTorch-native model serving platform for large-scale deployment.

**When to Use**:
- **Large-Scale Applications**: Ideal when deploying, scaling, and managing many models in production.
- **Model Lifecycle Management**: When you need features like model versioning, monitoring, and A/B testing.
- **Kubernetes Environments**: When using Kubernetes for orchestration and require a Kubernetes-native platform for scaling.
- **CI/CD Pipelines**: When automating the continuous integration and deployment of ML models with multiple pipelines.

**Pros**:
- **Scalability**: Can handle thousands of models, ensuring automated scaling, versioning, and management.
- **Model Management**: Built-in features for model lifecycle management (versioning, rolling updates, A/B testing).
- **Automation**: Integrates with CI/CD pipelines, automating deployment and monitoring processes.
- **High Performance**: Optimized for production environments with high availability and low-latency inference.

**Cons**:
- **Complex Setup**: Requires significant knowledge of Kubernetes and can be challenging to set up.
- **Overkill for Small Projects**: These platforms may add unnecessary complexity and overhead for small-scale deployments.
- **Resource-Intensive**: Requires more infrastructure and resources, especially for larger clusters.

---

## Summary

- **Use REST API Frameworks** (FastAPI, Flask, Django):
   - Ideal for quick deployment of a few models, prototyping, or building small to medium-scale applications.
   - Best for cases where you don't need to manage hundreds of models or require advanced scalability.

- **Use Advanced Platforms** (Seldon Core, Kubeflow, TensorFlow Serving, TorchServe):
   - Suitable for large-scale applications with multiple models requiring full automation, scaling, and management.
   - Best when using Kubernetes and need advanced model management features like versioning, A/B testing, and monitoring.










**Server Handler - get request from client and send response to client**




**Server Engine - handle the request and process required tasks in server side**


**Server Handler- send response to client server**

 In this project we are implementing FASTAPI as server handler and server engine. So there are several methods to handle server post request.

 One important point is that FASTAPI direclt doesn't allow us to send multiple response to client. So we have to use some other methods to send multiple response to client such as `Zip and send`, `Streeaming response`, or `multiple file upload endpoint`.

For example:

```pyhton
from fastapi import FastAPI
from fastapi.responses import FileResponse
import zipfile
import os
from tempfile import NamedTemporaryFile

app = FastAPI()

@app.get("/download-files")
async def download_files():
    # List of files to be zipped and sent
    files_to_send = ["/path/to/file1.txt", "/path/to/file2.pdf", "/path/to/file3.jpg"]
    
    # Create a temporary zip file
    with NamedTemporaryFile(delete=False) as tmp_zip:
        with zipfile.ZipFile(tmp_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
            for file_path in files_to_send:
                archive.write(file_path, os.path.basename(file_path))
        
        # Return the zip file as a response
        return FileResponse(
            tmp_zip.name,
            media_type="application/zip",
            filename="files.zip"
        )
```


Another method for streaming response is as follows:

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io
import zipfile

app = FastAPI()

@app.get("/stream-files")
async def stream_files():
    files_to_send = ["/path/to/file1.txt", "/path/to/file2.pdf", "/path/to/file3.jpg"]
    
    def iter_files():
        with io.BytesIO() as zip_buffer:
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_path in files_to_send:
                    zip_file.write(file_path)
            yield zip_buffer.getvalue()
    
    return StreamingResponse(
        iter_files(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=files.zip"}
    )
```

And multiple file upload endpoint is as follows:

```python

from fastapi import FastAPI, File, UploadFile
from typing import List

app = FastAPI()

@app.post("/upload-files/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

```





**Receive data in client side**





