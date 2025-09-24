# TWArch AI Server: Production-Ready FastAPI + Celery + GPU Inference

```

# TWArch AI Server: Production-Ready FastAPI + Celery + GPU Inference


<p align="center">

<pre>

┌─────────────────────────────────────────────────────────────────────────────────┐

│                              TASKS (Broker)                                    │

│                   Celery publishes tasks to Redis                              │

└─────────────────────────────────────────────────────────────────────────────────┘


┌─────────────┐    HTTP POST     ┌─────────────┐     Celery client     ┌─────────────────────┐

│   Client    │ ───────────────▶ │   FastAPI   │ ────────────────────▶ │   Redis (Broker)    │

│ (upload)    │  /receive_data   │   (router)  │   send_task("gpuX")   │  queues gpu0/gpu1    │

└─────────────┘                  └─────────────┘                      └─────────────────────┘

                                                                                  │  (pull)

                                                                                  ▼

┌─────────────────────────────────────────────────────────────────────────────────┐

│                           Celery Worker (gpuX)                                 │

│  - run_batch_detection                                                         │

│  - Load YOLO model from model_weights/                                         │

│  - Process images from received_data/                                          │

│  - Save detections to results/<request>/                                       │

│  - Return result metadata to Redis                                             │

└─────────────────────────────────────────────────────────────────────────────────┘

                                                                                  │

                                                                                  │ writes .txt

                                                                                  ▼

┌─────────────────────────────────────────────────────────────────────────────────┐

│                              Filesystem                                        │

│  - received_data/: Uploaded images                                             │

│  - results/<request>/: Detection .txt files                                    │

│  - logs/: Worker logs                                                          │

└─────────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────┐

│                            RESULTS (Backend)                                   │

│                 Worker stores return dict in Redis                             │

└─────────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────┐                                      ┌─────────────────────┐

│  Celery Worker      │ ── store {"result_txt_abspath", ...} ▶ │   Redis (Backend)  │

│  (task return value)│                                      │  task:<task_id>     │

└─────────────────────┘                                      └─────────────────────┘

                                                                                  ▲

                                                                                  │  AsyncResult(task_id).get()

┌─────────────────────────────────────────────────────────────────────────────────┐

│                              FastAPI (Response)                                │

│  - Fetch result from Redis                                                     │

│  - Check if .txt file exists                                                   │

│  - Return FileResponse(.txt) or error                                          │

└─────────────────────────────────────────────────────────────────────────────────┘

                                                                                  │

                                                                                  │ FileResponse(result_txt_abspath)

                                                                                  ▼

┌─────────────────────────────────────────────────────────────────────────────────┐

│                               Client                                           │

│  - Receives YOLO .txt file with detections                                     │

│  - Parses bbox, class, confidence                                              │

└─────────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────┐

│                            MONITORING & SCALING                                │

│  - Prometheus: Scrapes metrics from FastAPI, Celery, GPU, Node                │

│  - Grafana: Dashboards for visualization                                       │

│  - Flower: Celery task monitoring                                              │

│  - Round-robin GPU assignment for load balancing                               │

└─────────────────────────────────────────────────────────────────────────────────┘

</pre>

</p>

```

---

## 📁 Project Structure

| Folder/File                | Description & Links                                                                 |

|----------------------------|------------------------------------------------------------------------------------|

|[`app/`](app/)             | Main application code ([api/](app/api/), [db/](app/db/), [utils/](app/utils/), [yolo_backbone/](app/yolo_backbone/)) |

|[`app/api/`](app/api/)     | FastAPI router, Celery app, tasks ([router.py](app/api/router.py), [celery_app.py](app/api/celery_app.py), [tasks.py](app/api/tasks.py)) |

|[`app/db/`](app/db/)       | DB utilities ([db_utils.py](app/db/db_utils.py))                                   |

|[`app/utils/`](app/utils/)| Logging and shared utilities ([logging.py](app/utils/logging.py))                  |

|[`app/yolo_backbone/`](app/yolo_backbone/)| YOLO model code ([models/](app/yolo_backbone/models/), [utils/](app/yolo_backbone/utils/)) |

|[`model_weights/`](model_weights/)| YOLO model weights (.pt files)                                              |

|[`results/`](results/)     | Detection results (.txt files)                                                     |

|[`logs/`](logs/)           | Log files                                                                          |

|[`samples/`](samples/)     | Sample images for testing                                                          |

|[`test_images/`](test_images/)| Test images                                                                      |

|[`readme_collection/`](readme_collection/)| Additional guides: [Grafana](readme_collection/grafana_setup.md), [Prometheus](readme_collection/README.md#prometheus), [GPU Docker](readme_collection/gpu_docker_container.md)|

|[`requirements.txt`](requirements.txt)| Python dependencies                                                          |

|[`docker-compose.yml`](docker-compose.yml)| (If present) Docker orchestration                                            |

---

## 📚 Extended Documentation

-[Grafana Setup &amp; Monitoring](readme_collection/grafana_setup.md)

-[Prometheus &amp; Exporter Setup](readme_collection/README.md#prometheus)

-[GPU Docker Container &amp; Exporter](readme_collection/gpu_docker_container.md)

---

## � Dependencies

### System Requirements

-**Python 3.8+**

-**Redis Server** (for broker/backend)

-**NVIDIA GPU** (optional, for GPU inference)

-**Docker** (optional, for containerized deployment)

### Python Packages (from `requirements.txt`)

-`fastapi` - Web framework

-`uvicorn` - ASGI server

-`celery` - Distributed task queue

-`redis` - Redis client

-`torch` - PyTorch for ML

-`ultralytics` - YOLO models

-`prometheus-client` - Metrics

-`flower` - Celery monitoring

---

## �🚀 Quick Start

### 1. Clone and Setup

```bash

gitclone<your-repo-url>

cdTWArch_Production

```

### 2. Install System Dependencies

```bash

sudoaptupdate&&sudoaptinstall-yredis-serverpython3-venvpython3-devbuild-essential

```

### 3. Create Virtual Environment

```bash

python3-mvenvvenv

sourcevenv/bin/activate

pipinstall-rrequirements.txt

```

### 4. Configure Environment

- Edit `config.yml` for model paths, GPU settings, etc.
- Ensure model weights are in `model_weights/`
- Set up Redis (default: localhost:6379)

### 5. Start Services

```bash

# Start Redis

sudosystemctlstartredis-server


# Start Celery workers (one per GPU)

./celery_gpu0.sh&

./celery_gpu1.sh&


# Start FastAPI server

uvicornserver_run:app--host0.0.0.0--port8000--reload

```

### 6. Test the API

```bash

curl-XPOST"http://localhost:8000/receive_data"\

  -F "ImageClass=0" \

  -F"ImageFileName=@samples/floor/sample.jpg"\

  -F "if_db=false" \

  -F"wait=true"

```

### 7. (Optional) Monitoring

```bash

# Flower dashboard

celery-Aapp.api.celery_app.celery_appflower--port=5555


# Prometheus (if set up)

./prometheus_run.sh


# Grafana (if set up)

sudosystemctlstartgrafana-server

```

---

## 🔧 Troubleshooting

### Common Issues

-**Celery worker not starting**: Check Redis is running (`redis-cli ping`). Ensure virtualenv is activated.

-**GPU not detected**: Run `nvidia-smi`. Check `CUDA_VISIBLE_DEVICES` in scripts.

-**File not found errors**: Verify paths in `config.yml` and ensure directories exist.

-**API returns 500**: Check logs in `logs/` folder. Ensure model weights are present.

### Logs

- FastAPI logs: Console or `logs/main.log`
- Celery logs: `logs/celery_gpu0.log`, etc.
- Redis logs: `journalctl -u redis-server`

### Reset Everything

```bash

# Kill processes

pkill-f"uvicorn"

pkill-f"celery worker"

pkill-f"python3"


# Clear Redis

redis-cliFLUSHALL


# Restart services

sudosystemctlrestartredis-server

```

---

## 🔌 API Usage

### POST `/receive_data`

Upload an image for detection.

**Parameters (Form Data):**

-`ImageClass` (int): Image class ID (e.g., 0 for floor)

-`ImageFileName` (file): Image file

-`if_db` (bool): Save to database (default: false)

-`wait` (bool): Wait for result (default: true)

**Response:**

- If `wait=true`: YOLO `.txt` file with detections
- If `wait=false`: JSON with task status

**Example:**

```bash

curl-XPOST"http://localhost:8000/receive_data"\

  -F "ImageClass=0" \

  -F"ImageFileName=@samples/floor/sample.jpg"\

  -F "if_db=false" \

  -F"wait=true"\

  -o result.txt

```

### GET `/debug_counters`

Get internal counters.

**Response:**

```json

{

  "received":10,

  "enqueued":10,

  "completed":9,

  "responded":9,

  "pending_requests":1

}

```

See [API details and more examples](readme_collection/README.md#6-api-endpoints).

---

## 🛠️ Monitoring & Scaling

-[Grafana Setup](readme_collection/grafana_setup.md)

-[Prometheus Setup](readme_collection/README.md#prometheus)

-[Celery Exporter &amp; Flower](readme_collection/README.md#monitoring--scaling)

---

## Run Project in order

**While running bash files**

1) Start Redis server

```bash

sudosystemctlstartredis-server

```

2) Start Celery workers (one per GPU)

```bash

./celery_gpu0.sh&

./celery_gpu1.sh&

```

3) Start FastAPI server

```bash

uvicornserver_run:app--host0.0.0.0--port8000--reload

```

If using docer compose file

```bash

docker-composeup--build

```

---

## 📝 About

This project demonstrates a **production-level AI inference server** with:

- FastAPI for HTTP API
- Celery for distributed GPU task queue
- Redis as broker/backend
- YOLOv5/YOLOv8 for detection
- Prometheus & Grafana for monitoring

For detailed guides, troubleshooting, and advanced setup, see [`readme_collection/`](readme_collection/).

---

probably missing (quick checklist)

 TLS everywhere (edge, Redis TLS, S3 TLS).

 AuthN/Z for API & Flower; disable Grafana anonymous.

 Object storage for uploads/results (MinIO/S3) + presigned URLs.

 Airflow trigger path (webhook from MinIO/S3 events) + model registry (MLflow).

 Central logs via Loki/Promtail; trace via OpenTelemetry later.

 Backups & retention (S3 bucket lifecycle rules; DB snapshots; log retention).

 Resource limits on containers; GPU persistence mode; worker autoscaling.

 CI/CD (build → test → scan → deploy); pinned versions; SBOM; image signing.

 Data governance: PII policy, delete/retention windows, audit logs.

 Disaster recovery: restore runbooks; test restores quarterly.

 Client

  |

  v

Reverse Proxy (Nginx/Traefik) --injects--> X-Internal-Api-Key

  |

  v

FastAPI (/jobs)  <-- checks X-Internal-Api-Key

  | \

  |  \__ (async) push JSON → Redis list twarch:pending

  |                 ^

  |                 |  job status in twarch:jobs:{id}

  |                 |

  |            Redis (broker+backend+app keys)

  |

  v

Batcher ---- Celery send_task(queue=gpuN) ---> Workers (gpu0,gpu1,…) -> YOLO

    |

    +--> write result .txt

    +--> update job status in Redis
