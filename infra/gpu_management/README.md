# GPU Management

This folder contains scripts for GPU-aware job scheduling and management.

- `gpu_scheduler.py`: Example script for scheduling jobs on GPUs.








Got it 👍 — here’s a **full README.md** dedicated to your GPU Prometheus Exporter setup.

I’ve made it **step-by-step**, included all errors you encountered, and documented the fixes.

This way you (or future team members) can follow it without confusion.

---

# GPU Exporter Setup for Prometheus

This README documents how to set up the **NVIDIA DCGM Exporter** to expose GPU metrics on port **9400** for Prometheus scraping. It covers installation, configuration, common errors, and fixes.

---

## 📌 Overview

***Exporter Used:** NVIDIA DCGM Exporter (`nvcr.io/nvidia/k8s/dcgm-exporter`)

***Purpose:** Collect GPU utilization, memory, temperature, and other metrics

***Port:**`9400` (exposed as `/metrics`)

***Integration:** Scraped by Prometheus (`job_name: "gpu"`)

---

## ⚙️ Requirements

1.**NVIDIA Driver Installed**

   Confirm driver + CUDA are working:

```bash

   nvidia-smi

```

   Expected: Table showing GPUs, utilization, and processes.

2.**Docker Installed**

```bash

   docker --version

```

3.**NVIDIA Container Toolkit Installed** (to enable GPU access inside Docker containers).

---

## 🚀 Installation Steps

### 1. Install NVIDIA Container Toolkit

```bash

# Add NVIDIA repo

distribution=$(./etc/os-release;echo $ID$VERSION_ID)\

  && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \

     sudogpg--dearmor-o/usr/share/keyrings/nvidia-container-toolkit.gpg\

  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/$distribution/libnvidia-container.list | \

     sed's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit.gpg] https://#g'|\

     sudotee/etc/apt/sources.list.d/nvidia-container-toolkit.list


# Install toolkit

sudoapt-getupdate

sudoapt-getinstall-ynvidia-container-toolkit


# Configure Docker runtime for NVIDIA

sudonvidia-ctkruntimeconfigure--runtime=docker


# Restart Docker

sudosystemctlrestartdocker

```

---

### 2. Test GPU Access in Docker

⚠️ Common mistake: Using invalid CUDA image tags.

The correct format is:

```

nvidia/cuda:<version>-<flavor>-ubuntu<distro>

```

✅ Example test (works on Ubuntu 20.04):

```bash

dockerrun--rm--gpusallnvidia/cuda:12.2.0-base-ubuntu20.04nvidia-smi

```

Expected: Same `nvidia-smi` output as the host system.

---

### 3. Run GPU Exporter

Create a script `gpu_exporter_run.sh`:

```bash

#!/usr/bin/env bash

# GPU Exporter (NVIDIA DCGM Exporter)

# Exposes GPU metrics for Prometheus on port 9400


set-euopipefail


CONTAINER_NAME="gpu-exporter"

EXPORTER_PORT=9400

IMAGE="nvcr.io/nvidia/k8s/dcgm-exporter:latest"


echo"[INFO] Starting NVIDIA DCGM Exporter on port ${EXPORTER_PORT}..."


# Remove old container if exists

ifdockerps-a--format'{{.Names}}'|grep-Eq"^${CONTAINER_NAME}\$";then

    echo"[INFO] Removing old container: ${CONTAINER_NAME}"

    dockerrm-f"${CONTAINER_NAME}">/dev/null2>&1||true

fi


# Run DCGM Exporter

dockerrun-d--rm--gpusall\

  --name "${CONTAINER_NAME}" \

  -p${EXPORTER_PORT}:9400\

  ${IMAGE}


echo"[INFO] GPU Exporter is running."

echo"      Metrics available at: http://localhost:${EXPORTER_PORT}/metrics"

```

Make it executable:

```bash

chmod+xgpu_exporter_run.sh

./gpu_exporter_run.sh

```

---

## 🔍 Verifying Metrics

Check exporter output:

```bash

curlhttp://localhost:9400/metrics|grepDCGM_FI_DEV_GPU_UTIL

```

Expected:

```

DCGM_FI_DEV_GPU_UTIL{gpu="0"} 12

DCGM_FI_DEV_GPU_UTIL{gpu="1"} 45

```

Prometheus → **Targets** page will show:

```

gpu (1/1 up)

Endpoint: http://localhost:9400/metrics

```

---

## 🛑 Common Errors & Fixes

### ❌ `docker: could not select device driver "" with capabilities: [[gpu]].`

***Cause:** NVIDIA Container Toolkit not installed or not configured.

***Fix:**

```bash

  sudo apt-get install -y nvidia-container-toolkit

  sudo nvidia-ctk runtime configure --runtime=docker

  sudo systemctl restart docker

```

---

### ❌ `manifest for nvidia/cuda:11.8.0-base not found`

***Cause:** Wrong CUDA image tag.

***Fix:** Use a valid image:

```bash

  docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu20.04 nvidia-smi

```

---

### ❌ Prometheus shows `gpu (0/1 up) connect: connection refused`

***Cause:** GPU exporter not running, or wrong port.

***Fix:** Ensure exporter container is running:

```bash

  docker ps |grepgpu-exporter

```

  and Prometheus scrape config has:

```yaml

  - job_name: "gpu"

    static_configs:

      - targets: ["localhost:9400"]

```

---

## 📊 Prometheus Integration

Add this job in `prometheus.yml`:

```yaml

- job_name: "gpu"

  static_configs:

    - targets: ["localhost:9400"]

      labels:

        service: "GPU Exporter"

        description: "GPU utilization, memory usage, temperature"

```

---

## ✅ Next Steps

* Add **Grafana dashboards** for GPU monitoring
* Add **alerts** in `celery_rules.yml`, e.g.:

```yaml

- alert: HighGPUUsage

  expr: DCGM_FI_DEV_GPU_UTIL > 90

  for: 5m

  labels:

    severity: warning

  annotations:

    summary: "High GPU Utilization"

    description: "GPU {{ $labels.gpu }} is over 90% utilization for 5 minutes"

```

---

## 📌 TL;DR

* Install NVIDIA Container Toolkit ✅
* Test with CUDA container ✅
* Run DCGM Exporter ✅
* Scrape in Prometheus ✅
* Visualize in Grafana 🚀

---

👉 Do you want me to also prepare a **Grafana dashboard JSON** (with GPU utilization, memory, temperature panels) so when you’re ready, you can just import it and monitor GPUs immediately?
