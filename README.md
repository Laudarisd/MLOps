# MLops
MLOps, short for Machine Learning Operations, is a key aspect of Machine Learning engineering that focuses on efficiently deploying machine learning models into production and ensuring their ongoing maintenance and monitoring. It is a collaborative effort that typically involves data scientists, DevOps engineers, and IT professionals working together.

<div align="center">
  <img src="./img/6.png" alt="Sample Image" width="500">
  <p><em>This paper shows the Hidden Technical Debt in Machine Learning Systems. The paper discusses the challenges of deploying machine learning systems in production and the hidden technical debt that can accumulate over time. MLOps aims to address these challenges by providing best practices and tools for managing machine learning models in production.</em></p>
</div>

[reference](https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf)


According to SIG MLOps(Special Interest Group for Machine Learning Operations), the best MLOps setup is one where machine learning models are handled just like any other software in a CI/CD(continous Integration/Continous Development) system. These models are deployed alongside the services that use them, as part of a smooth release process. By following these practices, we aim to speed up the use of AI in software and deliver smarter software faster. Below, we explain key ideas in MLOps, such as step-by-step development, automation, continous development, version control, testing, reproducibility, and monitoring. 


In this repository, we will cover various aspects of MLOps, including best practices, tools, and techniques for deploying, monitoring, and managing machine learning models in production. We will explore topics from backeend development to front-end development, and from data management to model training and validation. Moreover, we will also explore continuous integration and continuous deployment (CI/CD), model versioning, containerization, orchestration, and monitoring.


---


## Contents
1. [Introduction](#introduction)
2. [Process and TOOLs for MLOps](#Process-and-TOOLs-for-MLOps)
3. [MLOps Architecture](#MLOps-Architecture)
4. [Cloud Based MLOps](#Cloud-Based-MLOps)


---

## Introduction
As machine learning and AI become more common in software, we need to create good practices and tools to help test, deploy, manage, and monitor these models in real-life situations. This is where MLOps comes in, helping to prevent pproblems in machine elarning applications.

<div align="center">
  <img src="./img/1.png" alt="Sample Image" width="500">
  <p><em>A common life cycle of MLOps engineering.</em></p>
</div>

[reference](https://www.databricks.com/glossary/mlops)



***What is the purpose of MLOps?***
MLOps is an effective method for building and improving machine learning and AI solutions. By using MLOps, data scientists and machine learning engineers can work together more efficiently, speeding up the development and deployment of models. It also incorporates continuous integration and deployment (CI/CD) practices, along with proper monitoring, validation, and management of ML models.

***Why do we need MLOps?***
Deploying machine learning models is challenging due to the complexity of the machine learning lifecycle, which includes tasks like data collection, preparation, model training, tuning, deployment, and monitoring. It also involves collaboration between teams such as Data Engineering, Data Science, and ML Engineering. MLOps helps streamline these processes, ensuring they work smoothly together through experimentation, iteration, and continuous improvement.

***What are the benefits of MLOps?***
MLOps offers key benefits like efficiency, scalability, and risk reduction. It makes model development faster, improves model quality, and speeds up deployment. MLOps supports scaling by allowing thousands of models to be managed and monitored through CI/CD pipelines. It also improves collaboration between teams and helps with the reproducibility of ML pipelines. In terms of risk reduction, MLOps ensures models comply with regulations, enhances transparency, and provides quicker responses to policy and regulatory needs.

***What are the key components of MLOps?***
The components of MLOps can be visualize and described as follows:

- Exploratory data analysis (EDA)
- Data Prep and Feature Engineering
- Model training and tuning
- Model review and governance
- Model inference and serving
- Model monitoring
- Automated model retraining


<div align="center">
  <img src="./img/2.png" alt="Sample Image" width="500">
  <p><em>Key components of MLOps.</em></p>
</div>

[reference](https://www.databricks.com/glossary/mlops)


---

## Process and TOOLs for MLOps

```table
🚀 **MLOps Workflow** 🚀

        ⬇️                        ⬇️                             ⬇️
+---------------+        +-------------------+        +-----------------------+
|  Programming  |  ----> | Model Development |  ----> |    Model Training &   |
| (Python, ML   |        |  - Fasetapi       |        |    Validation         |
| Libraries)    |        |  - Sheldon Core   |        |                       |
+---------------+        +-------------------+        +-----------------------+
         ⬇️                       ⬇️                             ⬇️
+------------------+     +-------------------+        +-----------------------+
| Containerization | --->| Deployment (CI/CD)|  ----> |  Monitoring & Logging |
|   (Docker)       |     |  (Jenkins, etc.)  |        |  (Prometheus, Grafana)|
+------------------+     +-------------------+        +-----------------------+
        ⬇️                        ⬇️                             ⬇️
+------------------+     +-------------------+        +-----------------------+
| Version Control  | --->|  Orchestration    |  ----> | Scaling & Management  |
|    (Git)         |     |  (Kubernetes)     |        |  (Kubeflow, Seldon)   |
+------------------+     +-------------------+        +-----------------------+
```

*Programming Languagse*:
- **Python**

*ML Libraries*:
- **Scikit-learn**
- **TensorFlow or PyTorch**

*ML Model Deployment*
- **REST API Frameworks**: 
  - **FastAPI**, **Flask**, **Django**
- **Advanced Platforms**: 
  - **Seldon Core**: Kubernetes-native platform for deploying, scaling, and managing thousands of models.
  - **Kubeflow**: End-to-end orchestration for machine learning workflows on Kubernetes.
  - **TensorFlow Serving**: A flexible, high-performance serving system for machine learning models in production.
  - **TorchServe**: PyTorch-native model serving platform for large-scale deployment.

*Cloud Platforms & Deployment*
- **AWS**
- **Azure**
- **Google Cloud Platform**

*Deployment(CI/CD)*:
- **Jenkins**

*Container & Orchestration*:
- **Docker**
- **Kubernetes**

*Monitoring & Logging*:
- **Prometheus**
- **Grafana**

*Version Control*:
- **Git**

*Scaling & Management*:
- **Kubeflow**
- **Seldon**

*Data Management*:
- **Databricks**
- **Snowflake**



<div align="center">
  <img src="./img/1.webp" alt="Sample Image" width="500">
  <p><em>Comparison of deployment platforms for machine learning models, highlighting the trade-offs between customization and out-of-the-box capabilities.</em></p>
</div>

[Reference](https://superwise.ai/blog/kserve-vs-seldon-core/)


---

## MLOps Architecture
In the following section we will focus on main components of MLOps architecture. The main components of MLOps architecture are as follows:

1. **Data Management**: This component is responsible for managing the data used in the machine learning pipeline. It includes data collection, storage, and preprocessing.[click here](./data_management/README.md)
2. **Model Development**: This component is responsible for developing machine learning models. It includes data preparation, feature engineering, model training, and model validation.[click here](./model_development/README.md)
3. **Model Deployment**: This component is responsible for deploying machine learning models into production. It includes model serving, model inference, and model monitoring.[click here](./model_deployement/README.md)
4. **Monitoring & Logging**: This component is responsible for monitoring and logging machine learning models in production. It includes tracking model performance, detecting model drift, and logging model predictions.[click here](./monitoring_and_logging/README.md)
5. **Model Governance & Compliance**: This component is responsible for ensuring that machine learning models comply with regulations and best practices. It includes model review, model governance, and model compliance.[click here](./model_governance_and_compliance/README.md)

<div align="center">
  <img src="./img/7.png" alt="Sample Image" width="500">
  <p><em>MLOps Architectures.</em></p>
</div>

[Reference](https://www.igmguru.com/blog/machine-learning-operations-mlops-overview-definition-and-architecture)

---

# Cloud-Based MLOps

Cloud-based MLOps platforms provide comprehensive solutions for deploying, managing, and monitoring machine learning models in the cloud. They offer scalability, flexibility, and cost-effectiveness, making it easier to manage machine learning workflows. These platforms typically provide features like auto-scaling, CI/CD pipelines, model versioning, model monitoring, and integration with various cloud services.

### Popular Cloud-Based MLOps Platforms

1. **Amazon SageMaker (AWS)**:
   - **Overview**: A fully managed service that enables data scientists and developers to build, train, and deploy machine learning models quickly.
   - **Features**: 
     - Model building and training with built-in algorithms.
     - Support for training on GPUs and deploying models in production.
     - Integration with AWS services like S3 for data storage, Lambda for serverless computing, and CloudWatch for monitoring.
     - Automated model tuning, deployment scaling, and built-in monitoring.
   - **Example**: Deploying an image classification model using SageMaker.
     ```bash
     from sagemaker import Session
     from sagemaker.tensorflow import TensorFlowModel
     
     model = TensorFlowModel(model_data='s3://your-model-path/model.tar.gz',
                             role='your-sagemaker-role',
                             framework_version='2.4.1')
     
     predictor = model.deploy(initial_instance_count=1, instance_type='ml.m5.large')
     ```
   - **Use Case**: Large-scale machine learning applications where integration with other AWS services is essential.

2. **Google AI Platform (Google Cloud)**:
   - **Overview**: A unified platform that lets you build, deploy, and manage machine learning models with scalable infrastructure.
   - **Features**:
     - Managed Jupyter Notebooks for model development.
     - Training models with GPUs/TPUs.
     - Automatic hyperparameter tuning, model versioning, and serving.
     - Integration with BigQuery for large-scale data analytics and Vertex AI for MLOps orchestration.
   - **Example**: Training and deploying a custom TensorFlow model using Google AI Platform.
     ```bash
     gcloud ai-platform jobs submit training your_job_name \
     --module-name trainer.task \
     --package-path ./trainer \
     --region us-central1 \
     --python-version 3.7 \
     --runtime-version 2.3
     ```
   - **Use Case**: Organizations looking to integrate machine learning models with GCP’s powerful data analytics tools like BigQuery.

3. **Azure Machine Learning (Microsoft Azure)**:
   - **Overview**: A cloud-based platform to accelerate the machine learning lifecycle with automated machine learning (AutoML), deployment, and monitoring.
   - **Features**:
     - Drag-and-drop interface for creating machine learning workflows.
     - Model training with deep learning and AutoML.
     - Model deployment and monitoring on cloud or edge devices.
     - Integration with Azure DevOps for CI/CD and GitHub for version control.
   - **Example**: Training and deploying a model on Azure ML.
     ```python
     from azureml.core import Workspace, Experiment
     
     ws = Workspace.from_config()
     experiment = Experiment(workspace=ws, name='my_experiment')
     
     run = experiment.submit(config=your_config)
     run.wait_for_completion(show_output=True)
     ```
   - **Use Case**: Businesses that rely on Microsoft Azure for their cloud infrastructure and need seamless integration with their Azure environment.

4. **Databricks (on AWS/Azure)**:
   - **Overview**: A unified data analytics platform that allows teams to collaborate on machine learning models, integrating with major cloud providers.
   - **Features**:
     - Managed Apache Spark for scalable data processing.
     - MLflow for experiment tracking, model registry, and deployment.
     - AutoML for rapid model development.
     - Collaboration features like shared notebooks for data science teams.
   - **Example**: Using Databricks and MLflow for model tracking.
     ```python
     import mlflow
     mlflow.set_experiment('my_experiment')
     
     with mlflow.start_run():
         mlflow.log_param('param1', value)
         mlflow.log_metric('accuracy', accuracy_score)
         mlflow.sklearn.log_model(model, 'model')
     ```
   - **Use Case**: Companies that need scalable data processing and machine learning with collaboration capabilities.

### Example of Cloud-Based MLOps Practice

In a typical **cloud-based MLOps** workflow, the process involves:

1. **Data Preparation**: 
   - Using services like AWS S3, GCP Cloud Storage, or Azure Blob Storage to store and retrieve datasets.
   - Preprocessing data using managed Jupyter Notebooks or Apache Spark (via Databricks).
   
2. **Model Training and Tuning**: 
   - Using Amazon SageMaker, Google AI Platform, or Azure ML for training models on cloud infrastructure (GPUs/TPUs).
   - Automatic hyperparameter tuning using tools like SageMaker Automatic Model Tuning or Google AI HyperTune.

3. **Model Deployment**: 
   - Deploying the trained model as a REST API using cloud platforms’ serving capabilities (e.g., SageMaker Endpoint, GCP AI Platform, or Azure Kubernetes Service for serving models at scale).

4. **Model Monitoring**:
   - Setting up monitoring for model performance using Prometheus/Grafana on Kubernetes or using cloud-native monitoring tools like AWS CloudWatch, Azure Monitor, or Google Stackdriver.

### Benefits of Cloud-Based MLOps

- **Scalability**: Easily scale up resources (CPUs, GPUs, TPUs) for training and serving large models.
- **Cost-Effectiveness**: Pay for the resources you use, with the ability to auto-scale up and down.
- **Flexibility**: Choose from various tools and services, enabling hybrid architectures across cloud platforms.
- **Seamless Integration**: Integrate with other cloud-native services like storage, databases, and CI/CD pipelines.


---


References:

- https://www.databricks.com/glossary/mlops
- https://medium.com/israeli-tech-radar/machine-learning-model-serving-overview-c01a6aa3e823