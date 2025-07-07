🛠️ Infrastructure Interview Preparation Guide
Target Role: Infrastructure Engineer (Linux, Red Hat OpenShift, Windows Server, Automation, Networking, Security)

📌 Purpose
Prepare for infrastructure interviews focusing on Linux (RHEL), Windows Server, Red Hat OpenShift, automation (Ansible, Python, Bash, PowerShell), virtualization (VMware ESXi), endpoint management (SCCM/Intune), log analysis (Splunk/ELK), networking (Cisco), CCTV/VMS, ITIL/Agile, and decision-making skills. Emphasize practical, hands-on implementation and operational readiness over innovation, ensuring robust infrastructure foundations before advancing to cutting-edge solutions.

✅ Chapter 1: Linux Fundamentals & System Administration
Goal: Master Linux server management (RHEL focus).
What to Know:

File system: ls, cd, find, du, df
Users/Groups: adduser, usermod, passwd, groups
Permissions: chmod, chown, umask
Processes: ps, top, kill, nice
systemd: systemctl, journalctl
Disk/Memory: df, free, iotop
Network: ping, ip, ss, netstat
Logs: /var/log/, journalctl
RHEL-specific: yum, dnf, subscription-manager

Practice:

Create user, restrict shell:

Why: Prevents login for security; useful for service accounts.
How: sudo adduser --shell /sbin/nologin restricted_user
Explanation: Creates restricted_user with no shell access, verified via /etc/passwd.


Debug systemd service:

Why: Identifies service failures (e.g., misconfigured ExecStart).
How: systemctl status myservice, journalctl -u myservice, edit /etc/systemd/system/myservice.service, reload with systemctl daemon-reload.
Explanation: Checks logs, corrects config, reloads systemd.


Monitor/clean disk space:

Why: Prevents outages due to full disks.
How: df -h, du -sh *, find / -size +100M, remove files with rm.
Explanation: Identifies and deletes large, unnecessary files.


Configure RHEL subscription:

Why: Ensures access to updates/packages.
How: subscription-manager register, subscription-manager attach, verify with yum repolist.
Explanation: Registers system for RHEL repository access.


Set up SSH key-based authentication:

Why: Enhances security over passwords.
How: ssh-keygen, ssh-copy-id user@host.
Explanation: Generates key pair, copies public key to remote server.



Sample Questions:

Q: How do you secure a Linux user account?

A: Set strong passwords, restrict shell (/sbin/nologin), use sudo for privileges, and enable SSH key auth.
Why: Minimizes unauthorized access risks.


Q: How do you handle a full disk issue?

A: Use df -h to check usage, du -sh to find large files, delete or archive unneeded data.
Why: Restores system functionality quickly.




✅ Chapter 2: Shell Scripting & Automation
Goal: Automate infrastructure tasks with Bash and Python.
What to Know:

Bash: if, for, while, functions
Parsing: awk, sed, cut, grep
Scheduling: cron
JSON: jq
Python: subprocess, paramiko

Practice:

Script service uptime monitoring:

Why: Ensures critical services are running.
How:

#!/bin/bash
SERVICE="myservice"
if ! systemctl is-active --quiet $SERVICE; then
    echo "$(date): $SERVICE down" >> /var/log/service_monitor.log
    # Send alert (e.g., email or webhook)
fi


Explanation: Checks service status, logs failures, triggers alerts.


Cron for MariaDB backup:

Why: Prevents data loss.
How: Add to crontab -e:

0 2 * * * /usr/bin/mysqldump -u root -p'password' mydb > /backup/mydb_$(date +\%F).sql


Explanation: Schedules daily backup at 2 AM.


Python script for SSH automation:

Why: Automates remote tasks.
How:

import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('hostname', username='user', key_filename='~/.ssh/id_rsa')
stdin, stdout, stderr = client.exec_command('uptime')
print(stdout.read().decode())
client.close()


Explanation: Executes remote command securely via SSH.


Parse logs with awk:

Why: Identifies issues in logs.
How: awk '/ERROR/ {print $0}' /var/log/app.log
Explanation: Filters ERROR lines for analysis.



Sample Questions:

Q: How do you automate repetitive server tasks?

A: Use Bash for simple tasks (e.g., log parsing), Python for complex automation (e.g., SSH tasks), and cron for scheduling.
Why: Reduces manual effort, ensures consistency.


Q: How do you debug a failing Bash script?

A: Add set -x for tracing, check exit codes ($?), and log output.
Why: Pinpoints script errors effectively.




✅ Chapter 3: systemd & Service Management
Goal: Master systemd for service deployment and management, emphasizing Red Hat environments.
What to Know:

.service files: Structure, directives (ExecStart, Restart, EnvironmentFile).
Timers: Scheduling tasks.
Targets: Grouping services for boot dependencies.
Debugging: systemctl, journalctl.
Advanced: Socket activation, transient units, drop-in configs.

Why:

systemd is the standard init system in RHEL, critical for service reliability.
Advanced features like timers and sockets enable sophisticated automation.

Practice:

Deploy FastAPI with systemd:

Why: Ensures reliable app uptime.
How: Create /etc/systemd/system/fastapi.service:

[Unit]
Description=FastAPI Service
After=network.target

[Service]
ExecStart=/usr/bin/uvicorn main:app --host 0.0.0.0 --port 8000
WorkingDirectory=/app
Restart=always
EnvironmentFile=/etc/fastapi/env

[Install]
WantedBy=multi-user.target


Steps: Write service file, run systemctl daemon-reload, systemctl enable fastapi, systemctl start fastapi.
Explanation: Configures service with environment variables and auto-restart.


Auto-restart on failure:

Why: Minimizes downtime.
How: Set Restart=always, test by killing process (kill <pid>).
Explanation: Ensures service restarts on crashes.


View service logs:

Why: Diagnoses issues.
How: journalctl -u fastapi -n 50
Explanation: Shows recent logs for debugging.


EnvironmentFile usage:

Why: Secures sensitive configs.
How: Create /etc/fastapi/env with API_KEY=secret, reference in .service.
Explanation: Separates configs from service definition.


Create systemd timer for backup:

Why: Automates scheduled tasks.
How: Create /etc/systemd/system/backup.timer and backup.service:

[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target

[Unit]
Description=Backup Service

[Service]
ExecStart=/usr/bin/mysqldump -u root -p'password' mydb > /backup/mydb_$(date +\%F).sql


Steps: Enable timer with systemctl enable backup.timer, start with systemctl start backup.timer.
Explanation: Schedules daily backups.


Socket activation for service:

Why: Reduces resource usage for on-demand services.
How: Create /etc/systemd/system/fastapi.socket:

[Unit]
Description=FastAPI Socket

[Socket]
ListenStream=8000
Accept=yes

[Install]
WantedBy=sockets.target


Steps: Link to fastapi.service, enable socket with systemctl enable fastapi.socket.
Explanation: Starts service only on incoming connections.


Drop-in config for customization:

Why: Modifies service without altering original file.
How: Create /etc/systemd/system/fastapi.service.d/override.conf:

[Service]
MemoryMax=512M


Steps: Run systemctl daemon-reload, restart service.
Explanation: Limits service memory usage.



Sample Questions:

Q: How do you handle a systemd service that fails to start?

A: Check systemctl status, review journalctl -u service, verify ExecStart path and permissions, reload with systemctl daemon-reload.
Why: Identifies misconfigurations or dependency issues.


Q: Why use timers over cron?

A: Timers integrate with systemd, provide better logging (journalctl), and support dependencies.
Why: Enhances reliability and visibility.


Q: How do you optimize a systemd service for high availability?

A: Use Restart=always, set StartLimitInterval, and configure socket activation for on-demand scaling.
Why: Ensures uptime and efficient resource use.


Q: How do you troubleshoot a hung systemd service?

A: Use systemctl status, check journalctl -u service -b, verify resource limits, and strace process if needed.
Why: Pinpoints resource or config issues.




✅ Chapter 4: Git, GitLab CI/CD & Automation Pipelines
Goal: Build CI/CD pipelines for infrastructure automation.
What to Know:

Git: Branches, tags, commits, rebasing, cherry-picking.
GitLab CI/CD: .gitlab-ci.yml, runners, variables.
Stages: Build, test, deploy, rollback.
Artifacts: Storing build outputs.
Pipeline triggers: Manual, scheduled, webhooks.

Practice:

Deploy FastAPI with GitLab CI/CD:

Why: Automates deployment.
How: Create .gitlab-ci.yml:

stages:
  - build
  - deploy

build:
  stage: build
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
  artifacts:
    paths:
      - myapp

deploy:
  stage: deploy
  script:
    - ssh user@server "docker pull myapp:$CI_COMMIT_SHA && docker run -d -p 8000:8000 myapp:$CI_COMMIT_SHA"


Steps: Push to GitLab, monitor pipeline, verify deployment.
Explanation: Builds Docker image, deploys to server.


Auto-restart with systemd:

Why: Ensures app restarts.
How: Update .service file, trigger restart via CI.
Explanation: Maintains service continuity.


Branch-based workflow:

Why: Supports parallel development.
How: git branch feature-x, push, create merge request.
Explanation: Isolates changes, enables review.


Tag releases:

Why: Marks stable releases.
How: git tag v1.0, git push origin v1.0.
Explanation: Triggers release pipeline.


Scheduled pipeline for backups:

Why: Automates recurring tasks.
How: Add to .gitlab-ci.yml:

backup:
  stage: deploy
  script:
    - ssh user@server "mysqldump -u root -p'password' mydb > /backup/mydb_$(date +\%F).sql"
  only:
    - schedules


Steps: Configure schedule in GitLab UI.
Explanation: Runs backup nightly.


Rollback with GitLab:

Why: Reverts failed deployments.
How: Store previous image tag in artifacts, redeploy via docker run.
Explanation: Ensures quick recovery.



Sample Questions:

Q: How do you secure GitLab CI/CD secrets?

A: Use GitLab variables or HashiCorp Vault, mask sensitive data in logs.
Why: Prevents credential leaks.


Q: How do you optimize CI/CD pipelines?

A: Cache dependencies, parallelize jobs, use lightweight runners.
**Why



**: Improves pipeline speed and efficiency.

Q: How do you handle a failed pipeline?
A: Check pipeline logs, verify scripts, rerun failed jobs, or rollback.
Why: Ensures rapid issue resolution.




✅ Chapter 5: Docker & Containerization
Goal: Package and deploy applications in containers with advanced configurations.
What to Know:

Dockerfiles: Multi-stage builds, best practices.
Volumes: Persistent storage, bind mounts.
Networking: Bridge, host, overlay networks.
Docker Compose: Multi-container orchestration.
Security: Non-root users, image scanning.
Optimization: Layer caching, minimal images.
Registries: Docker Hub, private registries (e.g., Red Hat Quay).
Docker Swarm: Basic clustering.

Why:

Containers ensure consistency across environments.
Advanced configurations improve security, scalability, and performance.

Practice:

Dockerize FastAPI:

Why: Simplifies deployment.
How: Create Dockerfile:

FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
USER nobody
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


Steps: Build (docker build -t myapp .), run (docker run -d -p 8000:8000 myapp).
Explanation: Uses multi-stage build, runs as non-root for security.


Use docker-compose with app + DB:

Why: Manages multi-container apps.
How: Create docker-compose.yml:

version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - app-data:/app/data
  db:
    image: mariadb:latest
    environment:
      MYSQL_ROOT_PASSWORD: example
    volumes:
      - db-data:/var/lib/mysql
volumes:
  app-data:
  db-data:


Steps: Run docker-compose up -d.
Explanation: Defines app and DB services with persistent volumes.


Debug container logs:

Why: Identifies runtime issues.
How: docker logs <container_id>
Explanation: Displays container output for troubleshooting.


Optimize Docker image:

Why: Reduces size, improves performance.
How: Use python:3.9-slim, minimize layers, clean up in RUN.
Explanation: Shrinks image footprint.


Scan image for vulnerabilities:

Why: Ensures secure images.
How: Use docker scan myapp or Red Hat Quay security scanning.
Explanation: Identifies and mitigates CVEs.


Set up private registry:

Why: Secures internal images.
How: Deploy Red Hat Quay, push image: docker push quay.example.com/myapp.
Explanation: Centralizes image storage.


Configure Docker network:

Why: Isolates container traffic.
How: docker network create mynet, run container with --network mynet.
Explanation: Enhances security and performance.


Use Docker Swarm for clustering:

Why: Enables basic orchestration.
How: Initialize swarm (docker swarm init), deploy service (docker service create).
Explanation: Scales containers across nodes.



Sample Questions:

Q: How do you secure a Docker container?

A: Run as non-root, scan images, limit capabilities, use minimal base images.
Why: Reduces attack surface.


Q: How do you troubleshoot a container crash?

A: Check docker logs, inspect docker inspect, verify resource limits.
Why: Identifies crash causes (e.g., OOM, misconfiguration).


Q: Why use Docker Compose over single containers?

A: Simplifies multi-container management, defines dependencies, and ensures consistency.
Why: Streamlines complex app deployments.


Q: How do you optimize Docker image builds?

A: Use multi-stage builds, cache layers, remove unnecessary files.
Why: Speeds up builds, reduces image size.




✅ Chapter 6: Kubernetes & OpenShift Basics
Goal: Orchestrate containers with Kubernetes and Red Hat OpenShift, including advanced scaling and ingress.
What to Know:

Core Components: Pods, Deployments, Services, ReplicaSets.
ConfigMaps/Secrets: Configuration and sensitive data management.
Helm Charts: Templated deployments.
kubectl vs oc: Kubernetes vs OpenShift CLI differences.
Horizontal Pod Autoscaling (HPA): Dynamic scaling based on metrics.
Ingress/Nginx: Traffic routing, load balancing.
Minikube: Local Kubernetes testing.
OpenShift: Routes, Builds, ImageStreams.
Monitoring: Prometheus, Grafana integration.
Storage: Persistent Volumes (PV), Persistent Volume Claims (PVC).

Why:

Kubernetes/OpenShift provide robust container orchestration.
HPA and Nginx ensure scalability and efficient traffic management.
Minikube enables local testing for rapid development.

Practice:

Deploy app with ConfigMap:

Why: Manages app configurations.
How: Create configmap.yaml:

apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  APP_ENV: production
  DB_HOST: mysql-service


Steps: Apply (oc apply -f configmap.yaml), reference in Deployment.
Explanation: Provides environment variables to app.


Monitor pod status/logs:

Why: Ensures app health.
How: oc get pods, oc logs <pod_name>.
Explanation: Verifies pod state, checks for errors.


Deploy with Helm:

Why: Simplifies complex deployments.
How: Create chart (helm create myapp), install (helm install myapp ./myapp).
Explanation: Packages app with reusable templates.


Scale deployment with HPA:

Why: Dynamically adjusts to load.
How: Create hpa.yaml:

apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70


Steps: Apply (oc apply -f hpa.yaml), monitor (oc get hpa).
Explanation: Scales pods based on CPU usage.


Configure Nginx Ingress:

Why: Routes external traffic efficiently.
How: Create ingress.yaml:

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-service
                port:
                  number: 8000


Steps: Deploy Nginx Ingress Controller, apply (oc apply -f ingress.yaml).
Explanation: Routes traffic to app service.


Test with Minikube:

Why: Validates configs locally.
How: Start Minikube (minikube start), deploy app (kubectl apply -f deployment.yaml).
Explanation: Simulates Kubernetes environment.


Set up OpenShift Route:

Why: Exposes app externally.
How: oc expose svc/myapp --hostname=myapp.example.com.
Explanation: Creates route for external access.


Configure Persistent Volume:

Why: Ensures data persistence.
How: Create pvc.yaml:

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myapp-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi


Steps: Apply (oc apply -f pvc.yaml), mount in Deployment.
Explanation: Provides persistent storage for app data.



Sample Questions:

Q: How does HPA decide when to scale pods?

A: Uses metrics (e.g., CPU/memory) from Metrics Server, scales based on thresholds (e.g., 70% CPU).
Why: Ensures resource efficiency and performance.


Q: Why use Nginx Ingress over OpenShift Route?

A: Nginx offers advanced routing (e.g., path rewriting); Routes are simpler for OpenShift-specific use.
Why: Matches tool to use case.


Q: How do you debug a failing pod in Kubernetes?

A: Check kubectl describe pod, view logs (kubectl logs), verify events and resource limits.
Why: Identifies misconfigurations or resource issues.


Q: How do you secure an OpenShift deployment?

A: Use Secrets for credentials, enforce RBAC, scan images with Quay, and restrict network policies.
Why: Reduces security risks.


Q: How do you test Kubernetes locally?

A: Use Minikube to simulate cluster, deploy and test manifests.
Why: Enables rapid iteration without production impact.




✅ Chapter 7: FastAPI & REST API Deployment
Goal: Deploy robust backend services with advanced configurations.
What to Know:

FastAPI: Routing, models, middleware, async.
Deployment: uvicorn, Gunicorn, Nginx, systemd.
Security: JWT, OAuth2.
Load Balancing: Nginx, Kubernetes Ingress.
Monitoring: Prometheus endpoints, logging.

Practice:

Deploy API with Nginx + HTTPS:

Why: Secures API traffic.
How: Configure Nginx:

server {
    listen 443 ssl;
    server_name api.example.com;
    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}


Steps: Install certs (e.g., Let’s Encrypt), restart Nginx.
Explanation: Proxies traffic to FastAPI, ensures HTTPS.


Build /predict endpoint:

Why: Demonstrates ML integration.
How:

from fastapi import FastAPI
app = FastAPI()

@app.post("/predict")
async def predict(data: dict):
    return {"prediction": "example"}


Steps: Test with curl -X POST http://localhost:8000/predict -d '{"data": "test"}'.
Explanation: Handles ML model inference requests.


Rate limiting with middleware:

Why: Protects from abuse.
How: Use slowapi:

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.get("/limited")
@limiter.limit("5/minute")
async def limited_endpoint(request: Request):
    return {"message": "OK"}


Explanation: Limits requests to prevent overload.


Secure API with JWT:

Why: Ensures authorized access.
How: Use python-jose:

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def verify_token(token: str = Depends(oauth2_scheme)):
    # Verify JWT
    return {"user": "authenticated"}


Explanation: Validates tokens for secure access.



Sample Questions:

Q: How do you scale a FastAPI app?

A: Use Gunicorn for multiple workers, deploy in Kubernetes with HPA, and load balance with Nginx.
Why: Handles high traffic efficiently.


Q: How do you monitor a FastAPI app?

A: Expose /metrics endpoint, integrate with Prometheus, and log requests.
Why: Tracks performance and issues.




✅ Chapter 8: MariaDB, SQL & NoSQL
Goal: Manage data storage for applications.
What to Know:

SQL: Queries, joins, indexes.
Backups: mysqldump, incremental backups.
API Integration: SQLAlchemy, PyMongo.
NoSQL: MongoDB (documents), Redis (caching).

Practice:

Cron MariaDB backup:

Why: Prevents data loss.
How: See Chapter 2.
Explanation: Automates daily backups.


Connect FastAPI to MariaDB:

Why: Enables data-driven APIs.
How:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine("mysql+pymysql://user:pass@localhost/db")
Session = sessionmaker(bind=engine)


Steps: Install pymysql, query DB in FastAPI.
Explanation: Provides ORM for database access.


MongoDB query:

Why: Handles unstructured data.
How:

from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["mydb"]
collection = db["mycollection"]
result = collection.find_one({"key": "value"})


Explanation: Queries MongoDB collection.


Redis caching:

Why: Improves API performance.
How:

import redis
r = redis.Redis(host="localhost", port=6379)
r.setex("key", 3600, "value")


Explanation: Caches data with TTL.



Sample Questions:

Q: How do you optimize MariaDB performance?

A: Add indexes, optimize queries, tune my.cnf (e.g., innodb_buffer_pool_size).
Why: Improves query speed and resource use.


Q: When to use NoSQL over SQL?

A: Use NoSQL (e.g., MongoDB) for unstructured data or high scalability; SQL for structured, relational data.
Why: Matches database to workload.




✅ Chapter 9: Apache Airflow & MLflow
Goal: Automate ML pipelines with Airflow and MLflow.
What to Know:

Airflow: DAGs, operators, sensors, XCom.
MLflow: Tracking, projects, models, registry.
Scheduling: Cron expressions, retries.
Deployment: Airflow on Kubernetes, MLflow server.

Practice:

Register/deploy model with MLflow:

Why: Tracks ML experiments.
How:

import mlflow
mlflow.log_param("param", value)
mlflow.log_model(model, "model")


Steps: Run in MLflow project, register model.
Explanation: Logs parameters and model for versioning.


Airflow DAG: ETL → train → deploy:

Why: Automates ML pipeline.
How:

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
dag = DAG("ml_pipeline", start_date=datetime(2025, 1, 1), schedule_interval="@daily")
def etl(): pass
def train(): pass
def deploy(): pass
PythonOperator(dag=dag, task_id="etl", python_callable=etl)


Explanation: Defines pipeline stages.


Airflow sensor:

Why: Waits for external events.
How: Use FileSensor to wait for data file.
Explanation: Pauses DAG until condition met.


Deploy MLflow server:

Why: Centralizes model tracking.
How: mlflow server --host 0.0.0.0.
Explanation: Runs tracking server.



Sample Questions:

Q: How do you debug a failing Airflow DAG?

A: Check Airflow logs (airflow logs), verify task dependencies, test operators individually.
Why: Isolates task failures.


Q: Why use MLflow for model management?

A: Tracks experiments, versions models, and supports deployment.
Why: Simplifies ML lifecycle.




✅ Chapter 10: AWS & GPU Server Management
Goal: Manage cloud and GPU-based servers.
What to Know:

AWS: EC2, S3, IAM, VPC, CloudWatch.
GPU: nvidia-smi, CUDA, cuDNN.
SSH/SCP: Secure access, file transfer.
Firewalls: Security groups, NACLs.

Practice:

Deploy FastAPI on EC2:

Why: Scales API in cloud.
How: Launch EC2, install FastAPI, configure systemd.
Explanation: Runs app in AWS environment.


Script GPU usage logging:

Why: Monitors GPU health.
How:

nvidia-smi --query-gpu=utilization.gpu --format=csv >> /var/log/gpu.log


Explanation: Logs GPU metrics.


Configure IAM role:

Why: Secures resource access.
How: Attach S3 access role to EC2.
Explanation: Grants least privilege access.


Set up VPC firewall:

Why: Restricts unauthorized access.
How: Configure security group for port 8000.
Explanation: Limits traffic to app port.



Sample Questions:

Q: How do you optimize GPU usage on EC2?

A: Use nvidia-smi to monitor, adjust workload distribution, select appropriate instance type.
Why: Maximizes compute efficiency.


Q: How do you secure an EC2 instance?

A: Use IAM roles, security groups, disable password SSH, and patch regularly.
Why: Reduces attack surface.




✅ Chapter 11: Windows Server 2022 Administration
Goal: Manage Windows Server environments.
What to Know:

Active Directory: Users, groups, GPOs.
PowerShell: Scripting, automation.
Services: Dependencies, recovery.
Event Viewer: Log analysis.
File Sharing: SMB, NTFS, DFS.

Practice:

Create AD user:

Why: Manages access.
How: New-ADUser -Name "User" -Path "OU=Users,DC=example,DC=com".
Explanation: Creates user in specified OU.


PowerShell script for disk usage:

Why: Monitors server health.
How:

Get-Disk | Select-Object Number, @{Name="FreeSpaceGB";Expression={[math]::Round($_.FreeSpace/1GB,2)}}


Explanation: Reports disk usage.


Configure file share:

Why: Enables resource sharing.
How: New-SmbShare -Name "DataShare" -Path "C:\Data".
Explanation: Creates share for domain users.


Backup AD:

Why: Ensures domain recovery.
How: ntdsutil snapshot "create" quit quit.
Explanation: Creates AD snapshot.



Sample Questions:

Q: How do you troubleshoot a Windows service?

A: Check Event Viewer, verify dependencies, test recovery options.
Why: Identifies and resolves service issues.


Q: How do you secure AD?

A: Use strong GPOs, enable auditing, restrict admin accounts.
Why: Prevents unauthorized access.




✅ Chapter 12: Microsoft SCCM/Intune
Goal: Manage endpoints with SCCM and Intune.
What to Know:

SCCM: Software deployment, OS imaging, patches.
Intune: MDM, compliance, app protection.
Packaging: MSI, App-V.
Reporting: Client health, deployment status.

Practice:

Deploy app via SCCM:

Why: Automates software distribution.
How: Create application in SCCM console, deploy to collection.
Explanation: Ensures consistent delivery.


Set Intune compliance policy:

Why: Enforces device security.
How: Configure encryption policy in Intune portal.
Explanation: Restricts non-compliant devices.


Patch management with SCCM:

Why: Keeps systems secure.
How: Deploy update group with maintenance window.
Explanation: Minimizes disruption.


Monitor client health:

Why: Ensures endpoint compliance.
How: Use SCCM Client Status report.
Explanation: Identifies unhealthy clients.



Sample Questions:

Q: How do you troubleshoot SCCM deployment failures?

A: Check logs (C:\Windows\CCM\Logs), verify network, and review deployment status.
Why: Pinpoints failure causes.


Q: How does Intune enhance endpoint management?

A: Provides cloud-based MDM, supports mobile devices, and integrates with Azure AD.
Why: Enables modern management.




✅ Chapter 13: VMware ESXi Virtualization
Goal: Manage virtualized environments with ESXi/vSphere.
What to Know:

ESXi: VM creation, snapshots.
vSphere: Cluster management, DRS, HA.
PowerCLI: Automation.
Networking: vSwitches, port groups.
Storage: Datastores, VMFS, NFS.

Practice:

Create VM with PowerCLI:

Why: Automates provisioning.
How:

Connect-VIServer -Server "vcenter.example.com" -User "admin" -Password "pass"
New-VM -Name "MyVM" -Template "RHEL-Template" -VMHost "esxi-host" -Datastore "datastore1"


Explanation: Deploys VM from template.


Take VM snapshot:

Why: Enables rollback.
How: New-Snapshot -VM "MyVM" -Name "Pre-Update".
Explanation: Captures VM state.


Configure vSwitch:

Why: Enables VM networking.
How: New-VirtualSwitch -VMHost "esxi-host" -Name "vSwitch1".
Explanation: Sets up virtual switch.


Monitor ESXi host:

Why: Ensures resource availability.
How: Get-VMHost -Name "esxi-host" | Select-Object Name, CpuUsageMhz.
Explanation: Displays host metrics.



Sample Questions:

Q: How do you optimize ESXi performance?

A: Use DRS, set resource limits, monitor with PowerCLI.
Why: Prevents contention, improves efficiency.


Q: How do you handle VM migration?

A: Use vMotion (Move-VM), verify resource availability.
Why: Ensures zero-downtime migration.




✅ Chapter 14: Splunk/ELK for Log Management
Goal: Analyze logs for monitoring and troubleshooting.
What to Know:

Splunk: SPL, dashboards, alerts.
ELK: Logstash, Elasticsearch, Kibana.
Log Parsing: Regex, field extraction.
Alerting: Real-time notifications.

Practice:

Create Splunk dashboard:

Why: Visualizes metrics.
How: Write SPL (index=main ERROR | timechart count), save as dashboard.
Explanation: Shows error trends.


ELK log ingestion:

Why: Centralizes logs.
How:

input { file { path => "/var/log/app.log" } }
output { elasticsearch { hosts => ["localhost:9200"] } }


Explanation: Forwards logs to Elasticsearch.


Set up Splunk alert:

Why: Notifies on issues.
How: Create alert for index=main ERROR | stats count > 10.
Explanation: Triggers on high error counts.


Query error logs:

Why: Identifies issues.
How: index=main sourcetype=app ERROR | table _time, host, message.
Explanation: Lists errors with details.



Sample Questions:

Q: How do you scale Splunk?

A: Use distributed deployment with indexers, search heads, forwarders.
Why: Handles large log volumes.


Q: How do you troubleshoot ELK log loss?

A: Check Logstash pipeline, verify Elasticsearch, ensure filebeat runs.
Why: Identifies pipeline issues.




✅ Chapter 15: Cisco Networking Technologies
Goal: Manage Cisco-based network infrastructure.
What to Know:

VLANs: Segmentation, tagging.
Routing: OSPF, BGP, static routes.
Firewalls/ACLs: Access control.
Monitoring: SNMP, NetFlow.
Cisco IOS: CLI, configuration.

Practice:

Configure VLAN:

Why: Segments traffic.
How:

vlan 10
 name MY_VLAN
interface g0/1
 switchport mode access
 switchport access vlan 10


Explanation: Assigns port to VLAN.


Set up ACL:

Why: Restricts access.
How:

access-list 101 permit tcp any host 192.168.1.1 eq 80
interface g0/1
 ip access-group 101 in


Explanation: Allows HTTP traffic.


Configure OSPF:

Why: Enables dynamic routing.
How:

router ospf 1
 network 192.168.1.0 0.0.0.255 area 0


Explanation: Advertises network.


Monitor with SNMP:

Why: Tracks performance.
How:

snmp-server community public RO
snmp-server host 192.168.1.100 public


Explanation: Enables SNMP monitoring.



Sample Questions:

Q: How do you troubleshoot VLAN issues?

A: Check show vlan brief, verify trunking, test with ping.
Why: Isolates misconfigurations.


Q: Why use BGP over OSPF?

A: BGP for inter-domain; OSPF for intra-domain, faster convergence.
Why: Matches protocol to scale.




✅ Chapter 16: CCTV Cameras & Video Management Systems
Goal: Manage surveillance systems.
What to Know:

IP Cameras: Configuration, RTSP.
VMS: Milestone, Genetec, storage policies.
Networking: Bandwidth, QoS.
Security: Access control, encryption.

Practice:

Configure IP camera:

Why: Enables video feed.
How: Set static IP via web interface.
Explanation: Ensures stable access.


Set up VMS retention:

Why: Manages storage.
How: Configure 30-day retention in Milestone.
Explanation: Balances storage and compliance.


Monitor bandwidth with QoS:

Why: Prevents congestion.
How:

class-map match-all VIDEO
 match protocol rtsp
policy-map VIDEO_QOS
 class VIDEO
  bandwidth percent 50


Explanation: Prioritizes video traffic.


Backup video feed:

Why: Ensures data availability.
How: Schedule export in VMS.
Explanation: Protects against loss.



Sample Questions:

Q: How do you optimize CCTV bandwidth?

A: Use QoS, H.265 compression, limit frame rate.
Why: Ensures smooth delivery.


Q: How do you secure VMS?

A: Use HTTPS, VLANs, role-based access.
Why: Protects sensitive video data.




✅ Chapter 17: ITIL & Agile Methodologies
Goal: Apply ITIL and Agile for service and project management.
What to Know:

ITIL: Incident, Problem, Change Management.
Agile: Scrum, Kanban.
Service Desk: Ticketing, SLAs.
DevOps: CI/CD with Agile.

Practice:

Handle ITIL incident:

Why: Restores service quickly.
How: Log in ServiceNow, prioritize, resolve, document RCA.
Explanation: Follows ITIL process.


Plan Agile sprint:

Why: Organizes tasks.
How: Define stories in Jira, assign points, schedule sprint.
Explanation: Aligns team on deliverables.


Change management:

Why: Minimizes risks.
How: Submit RFC, assess impact, implement.
Explanation: Ensures controlled changes.


Set up Kanban:

Why: Tracks progress.
How: Create Trello board with To-Do, In-Progress, Done.
Explanation: Visualizes workflow.



Sample Questions:

Q: How do you prioritize ITIL incidents?

A: Based on impact and urgency.
Why: Restores critical services first.


Q: How does Agile benefit infrastructure?

A: Iterative sprints enable rapid feedback.
Why: Enhances adaptability.




✅ Chapter 18: Ansible for Configuration Management
Goal: Automate infrastructure with Ansible.
What to Know:

Playbooks: YAML tasks.
Roles: Reusable configurations.
Inventory: Host groups, variables.
Modules: yum, service, file.
Ansible Galaxy: Community roles.

Practice:

Deploy FastAPI with Ansible:

Why: Automates deployment.
How:

- hosts: webservers
  tasks:
    - name: Install Python
      yum: name=python3-pip state=present
    - name: Install FastAPI
      pip: name=fastapi uvicorn
    - name: Start FastAPI
      service: name=fastapi state=started enabled=yes


Explanation: Installs and starts app.


Manage users:

Why: Automates provisioning.
How:

- hosts: all
  tasks:
    - name: Create user
      user: name=jdoe shell=/sbin/nologin state=present


Explanation: Creates restricted user.


Configure Nginx:

Why: Standardizes web server.
How:

- hosts: webservers
  tasks:
    - name: Deploy Nginx config
      template: src=nginx.conf.j2 dest=/etc/nginx/nginx.conf
    - name: Restart Nginx
      service: name=nginx state=restarted


Explanation: Deploys config, restarts service.


Use Ansible role:

Why: Reuses configurations.
How: ansible-galaxy init myrole, apply with playbook.
Explanation: Structures automation.



Sample Questions:

Q: How do you debug Ansible?

A: Use --check, -vvv, check logs.
Why: Identifies errors.


Q: Why use roles?

A: Modularizes tasks, improves reusability.
Why: Simplifies complex setups.




✅ Chapter 19: Product Deployment Lifecycle
Goal: Deploy infrastructure products end-to-end using Red Hat Enterprise technologies (Docker, OpenShift, Kubeflow, MLflow, Jenkins).
What to Know:

Planning: Requirements, architecture, vendor collaboration.
Build: App development, containerization (Docker).
Test: Unit, integration, load testing (pytest, Locust).
Deploy: Jenkins CI/CD, OpenShift, Kubeflow for ML.
Monitor: Prometheus, Grafana, MLflow tracking.
Rollback: OpenShift rollbacks, Jenkins pipeline retries.

Why:

A structured lifecycle ensures reliable, scalable deployments.
Red Hat technologies (OpenShift, Quay) provide enterprise-grade orchestration.
Kubeflow and MLflow support ML workloads, critical for data-driven apps.

Step-by-Step Deployment of ML Pipeline:

Plan Architecture:

Why: Ensures scalability, HA, and compliance.
How: Design with OpenShift cluster, Nginx Ingress, MariaDB, and Kubeflow for ML.
Components:
OpenShift: Orchestrates containers, manages routes.
Docker/Quay: Builds and stores images.
Jenkins: Automates CI/CD pipeline.
Kubeflow: Manages ML workflows (training, serving).
MLflow: Tracks experiments, models.
Prometheus/Grafana: Monitors metrics.


Explanation: Defines a robust, scalable stack.


Build and Containerize App:

Why: Ensures consistency across environments.
How: Create FastAPI app with /predict endpoint, Dockerize:

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]


Steps: Build (docker build -t quay.example.com/myapp:latest), push to Quay.
Explanation: Uses Gunicorn for production-grade serving.


Test with Jenkins:

Why: Validates functionality and performance.
How: Configure Jenkins pipeline (Jenkinsfile):

pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pytest tests/'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t quay.example.com/myapp:$BUILD_NUMBER .'
                sh 'docker push quay.example.com/myapp:$BUILD_NUMBER'
            }
        }
    }
}


Steps: Run tests, build and push image.
Explanation: Ensures app quality before deployment.


Deploy with OpenShift:

Why: Orchestrates containers at scale.
How: Create Deployment, Service, Route:

apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: quay.example.com/myapp:latest
          ports:
            - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - port: 8000
      targetPort: 8000
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: myapp-route
spec:
  host: myapp.example.com
  to:
    kind: Service
    name: myapp-service


Steps: Apply (oc apply -f deploy.yaml), expose route.
Explanation: Deploys app, exposes via OpenShift Route.


Set up Kubeflow for ML:

Why: Manages ML training and serving.
How: Deploy Kubeflow on OpenShift, create pipeline:

from kfp import dsl
@dsl.pipeline(name="ML Pipeline")
def ml_pipeline():
    train = dsl.ContainerOp(
        name="train",
        image="quay.example.com/ml-model:latest",
        command=["python", "train.py"]
    )


Steps: Install Kubeflow, run pipeline.
Explanation: Automates ML workflow.


Track with MLflow:

Why: Manages ML experiments.
How: Deploy MLflow server, log model:

import mlflow
mlflow.set_tracking_uri("http://mlflow.example.com")
mlflow.log_param("epoch", 10)
mlflow.log_model(model, "model")


Steps: Run MLflow server in OpenShift, log experiments.
Explanation: Tracks model versions and metrics.


Monitor with Prometheus/Grafana:

Why: Tracks performance and issues.
How: Deploy Prometheus in OpenShift, scrape /metrics endpoint.
Steps: Configure Prometheus, create Grafana dashboards.
Explanation: Visualizes app and ML pipeline metrics.


Rollback with Jenkins/OpenShift:

Why: Mitigates deployment failures.
How: Use oc rollback or Jenkins pipeline to redeploy previous image.
Explanation: Restores stable state.



Sample Questions:

Q: How do you deploy an ML model in OpenShift?

A: Containerize model, deploy with Kubeflow, expose via Route, monitor with Prometheus.
Why: Ensures scalable ML serving.


Q: How does Jenkins integrate with OpenShift?

A: Use Jenkins OpenShift plugin to trigger builds, push to Quay, and deploy via oc apply.
Why: Automates end-to-end pipeline.


Q: Why use Kubeflow for ML?

A: Automates training, serving, and hyperparameter tuning.
Why: Simplifies ML operations.




✅ Chapter 20: System Security
Goal: Secure infrastructure against threats.
What to Know:

Firewalls: firewalld, iptables, Windows Firewall.
SELinux: Enforcing, policies, contexts.
SSH Hardening: Key-based auth, disable root.
Vulnerability Scanning: OpenVAS, Nessus.
Encryption: TLS, BitLocker, Ansible Vault.
RBAC: Role-based access control in OpenShift.

Practice:

Configure firewalld:

Why: Restricts access.
How: firewall-cmd --add-port=8000/tcp --permanent; firewall-cmd --reload.
Explanation: Opens app port.


Enable SELinux:

Why: Enhances access control.
How: Set SELINUX=enforcing in /etc/selinux/config.
Explanation: Enforces mandatory controls.


Harden SSH:

Why: Prevents brute-force attacks.
How:

PermitRootLogin no
PasswordAuthentication no


Explanation: Enforces key-based auth.


Run vulnerability scan:

Why: Identifies weaknesses.
How: Use OpenVAS, review report.
Explanation: Prioritizes remediation.



Sample Questions:

Q: How do you secure an OpenShift cluster?

A: Use RBAC, network policies, scan images, and enable SELinux.
Why: Reduces attack vectors.


Q: How do you handle a detected vulnerability?

A: Patch system, update images, re-scan to verify.
Why: Mitigates risks.




✅ Chapter 21: Troubleshooting Infrastructure
Goal: Diagnose and resolve infrastructure issues.
What to Know:

Logs: journalctl, Event Viewer, Splunk.
Network: tcpdump, wireshark, ping.
Performance: top, vmstat, Get-Counter.
RCA: 5 Whys, fishbone diagram.

Practice:

Resolve service failure:

Why: Restores services.
How: journalctl -u service, fix config, restart.
Explanation: Corrects misconfigurations.


Debug network issue:

Why: Ensures connectivity.
How: tcpdump -i eth0 host 192.168.1.1.
Explanation: Captures packets.


Fix high CPU usage:

Why: Prevents degradation.
How: Use top, adjust nice or terminate process.
Explanation: Restores performance.


Simulate outage:

Why: Tests recovery.
How: Stop service, restore from backup.
Explanation: Validates DR plan.



Sample Questions:

Q: How do you troubleshoot a slow Kubernetes pod?

A: Check kubectl describe, logs, resource limits, and network latency.
Why: Identifies bottlenecks.


Q: How do you perform RCA?

A: Use 5 Whys, analyze logs, validate fixes.
Why: Prevents recurrence.




✅ Chapter 22: Operational Readiness & Behavioral Questions
Goal: Demonstrate operational readiness, leadership, and problem-solving, focusing on practical infrastructure management over innovation.
What to Know:

STAR Method: Situation, Task, Action, Result.
Operational Readiness: Ensure systems are stable, documented, and maintainable before innovating.
Leadership: Collaboration, conflict resolution.
Weaknesses: Actionable improvement plans.
Problem-Solving: Structured, data-driven.
Documentation: Runbooks, diagrams, Confluence.

Why:

Infrastructure roles prioritize stability and reliability over innovation.
Behavioral skills show ability to manage operations and teams effectively.

Practice:

Strengths:

Q: What are your strongest technical skills?
A: Expert RHEL administration, Ansible automation, OpenShift deployments. Automated 50+ servers, reducing setup time by 70% (STAR: Situation: manual setup; Task: automate; Action: wrote playbooks; Result: faster deployment).
Why: Highlights practical expertise.


Weakness:

Q: What’s a weakness you’re improving?
A: Initially struggled with delegation, now use Jira for task tracking and train team, improving efficiency.
Why: Shows growth and teamwork.


Leadership:

Q: Describe a time you led a project.
A: Led OpenShift migration for 20 servers. Coordinated vendors, set milestones, completed 2 weeks early (STAR).
Why: Demonstrates project leadership.


New Problem-Solving:

Q: How do you approach new problems?
A: Identify symptoms, check logs, test hypotheses, implement fixes. Resolved network outage via tcpdump, fixing VLAN (STAR).
Why: Shows structured approach.


Critical System Failure:

Q: Describe a critical failure you resolved.
A: DB crashed due to disk failure. Restored backup, applied failover, updated RAID, minimizing downtime to 2 hours (STAR).
Why: Proves crisis management.


Production Pressure:

Q: How do you handle production pressure?
A: Stay calm, prioritize tasks, communicate. Mitigated DDoS with firewall rules, restored service in 1 hour (STAR).
Why: Shows composure.


Reverse-Engineering:

Q: How do you understand complex systems?
A: Review docs, analyze configs/logs, test components. Mapped legacy app dependencies for migration (STAR).
Why: Demonstrates analytical skills.


Operational Readiness:

Q: How do you ensure systems are ready before innovating?
A: Stabilize infrastructure with automation (Ansible), monitoring (Prometheus), and documentation (Confluence). Ensured 99.9% uptime before implementing ML pipeline (STAR).
Why: Prioritizes reliability over premature innovation.



Sample Questions:

Q: How do you prioritize stability over innovation?

A: Ensure robust monitoring, automation, and documentation before experimenting with new tools.
Why: Maintains reliable operations.


Q: How do you handle team conflicts during operations?

A: Facilitate open discussion, align on goals, escalate if needed.
Why: Ensures team cohesion.


Q: How do you document infrastructure changes?

A: Write detailed runbooks in Confluence, include diagrams, and review regularly.
Why: Ensures maintainability and knowledge transfer.


