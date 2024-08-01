# MLops Pipeline Workflow

## Overview
This document outlines the workflows for running AI model inference in parallel using both a Linux remote server and a cloud system. Each pipeline includes steps for handling data reception, inference processing, result posting, and CI/CD integration with Jenkins.

## Pipeline for Linux Remote Server

1. **User Interaction**:
   - Multiple users crop images using CAD software.
   - Cropped images are saved to the Linux remote server.

2. **Image Saved to Linux Remote Server**:
   - Cropped images are saved to the Linux server.

3. **FastAPI Endpoint (Trigger Data Receive)**:
   - A FastAPI endpoint on the Linux server detects new images.

4. **Monitoring Service**:
   - The FastAPI endpoint triggers the MLops pipeline by sending a notification to the message queue.

5. **Message Queue**:
   - Manages and distributes tasks for parallel processing.

6. **MLops Pipeline on Linux**:
   - Parallel Inference with Kubernetes on the Linux server.
   - Auto-Scaling based on workload.

7. **Save Results**:
   - Save results to the Linux server.
   - Save results to local PCs.

8. **FastAPI Endpoint (Result Post)**:
   - Another FastAPI endpoint posts the inference results back to the CAD UI.

9. **Send Results to CAD UI**:
   - Results are sent back to the CAD UI for display.

10. **Save Results to Database**:
    - Results are stored for further analysis and retrieval.

11. **CI/CD Pipeline**:
    - Jenkins is used for automating the deployment and updates of the MLops pipeline.

## Pipeline for Cloud System

1. **User Interaction**:
   - Multiple users crop images using CAD software.
   - Cropped images are saved to cloud storage.

2. **Image Saved to Cloud Storage**:
   - Cropped images are saved to the cloud storage.

3. **Cloud Function (Trigger Data Receive)**:
   - Cloud function detects new images.

4. **Cloud MLops Services**:
   - Managed by cloud services, typically auto-scaling and running inferences.

5. **Save Results**:
   - Save results to cloud storage.
   - Save results to local PCs.

6. **Cloud Function (Result Post)**:
   - Posts the inference results back to the CAD UI.

7. **Send Results to CAD UI**:
   - Results are sent back to the CAD UI for display.

8. **Save Results to Database**:
   - Results are stored for further analysis and retrieval.

9. **CI/CD Pipeline**:
   - Jenkins is used for automating the deployment and updates of the MLops pipeline.

## Combined Workflow Diagram

### Pipeline for Linux Remote Server:

```mermaid
graph TD
    A[User Interaction (Cropping Images)] --> B[Image Saved to Linux Remote Server]
    B --> C[FastAPI Endpoint (Trigger Data Receive)]
    C --> D[Monitoring Service]
    D --> E[Message Queue]
    E --> F[Parallel Inference with Kubernetes on Linux]
    F --> G[Auto-Scaling based on workload]
    G --> H[Save Results to Linux Server]
    G --> I[Save Results to Local PCs]
    H --> J[FastAPI Endpoint (Result Post)]
    I --> J
    J --> K[Send Results to CAD UI]
    K --> L[Save Results to Database]
    L --> M[CI/CD Pipeline (Jenkins)]





```mermaid
graph TD
    A[User Interaction (Cropping Images)] --> B[Image Saved to Cloud Storage]
    B --> C[Cloud Function (Trigger Data Receive)]
    C --> D[Cloud MLops Services (Auto-Scaling, Inference)]
    D --> E[Save Results to Cloud Storage]
    D --> F[Save Results to Local PCs]
    E --> G[Cloud Function (Result Post)]
    F --> G
    G --> H[Send Results to CAD UI]
    H --> I[Save Results to Database]
    I --> J[CI/CD Pipeline (Jenkins)]
