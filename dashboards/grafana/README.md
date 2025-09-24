---
## 8. Troubleshooting

- **Grafana not starting:**
  - Check service status: `sudo systemctl status grafana-server`
  - Check logs: `sudo journalctl -u grafana-server`
- **Prometheus not connecting:**
  - Verify Prometheus is running and accessible at the configured URL.
  - Check firewall rules and network connectivity.
- **No data in dashboards:**
  - Ensure exporters (Node, GPU, Celery, FastAPI) are running and targets are up in Prometheus.
- **Permission errors:**
  - Run commands with `sudo` if needed.
  - Ensure correct file permissions for provisioning files.
---
## 9. Security Tips

- Change the default Grafana admin password after first login.
- Restrict access to Grafana and Prometheus ports (use firewalls or security groups).
- Use HTTPS for Grafana in production.
- Limit user permissions in Grafana for team members.

---

## 10. Backup & Restore

- **Export dashboards:** In Grafana UI, go to Dashboard → Settings → JSON Model → Export.
- **Import dashboards:** Dashboard → Import → Upload JSON or use ID.
- **Backup provisioning files:** Save `/etc/grafana/provisioning/` and custom config files.

---

## 11. Upgrade & Maintenance

- To upgrade Grafana:
  ```sh
  sudo apt-get update
  sudo apt-get install --only-upgrade grafana
  ```
- Restart after upgrade: `sudo systemctl restart grafana-server`
- Regularly update exporters and Prometheus for new features and security patches.

---

## 12. More Information

- See the [Main Project README](../../README.md) for a full project overview and context.
  Got it 👍

I’ll prepare a **professional Grafana setup guide + provisioning files** so you (or your team) can always redeploy the monitoring stack without missing steps.

Here’s a consolidated **README + config** that covers everything we did until now:

---

# 📊 Grafana Setup for TWArch AI Server Monitoring

This document describes how to set up **Grafana** to visualize metrics from **Prometheus**, including:

***Celery** task monitoring (success, failure, pending, runtime rules)

***FastAPI** metrics (request counts, latencies)

***Node Exporter** (CPU, memory, disk, network)

***NVIDIA GPU Exporter (DCGM)** (GPU utilization, memory, temperature)

---

## 1. Install Grafana

```bash

# Add Grafana repository

sudoapt-getinstall-ysoftware-properties-common

sudoadd-apt-repository"deb https://packages.grafana.com/oss/deb stable main"


# Add GPG key

wget-q-O-https://packages.grafana.com/gpg.key|sudoapt-keyadd-


# Install Grafana

sudoapt-getupdate

sudoapt-getinstallgrafana-y


# Enable and start Grafana

sudosystemctlenablegrafana-server

sudosystemctlstartgrafana-server


# Check status

sudosystemctlstatusgrafana-server

```

Default UI → [http://localhost:3000](http://localhost:3000)

Default login: **admin / admin**

---

## 2. Provision Prometheus Datasource

Create a file:

📂 `/etc/grafana/provisioning/datasources/prometheus.yaml`

```yaml

apiVersion: 1

deleteDatasources:

  - name: Prometheus

    orgId: 1


datasources:

  - name: Prometheus

    type: prometheus

    access: proxy

    orgId: 1

    url: http://61.97.120.204:9090   # Your Prometheus server

    isDefault: true

    editable: false

```

Restart Grafana:

```bash

sudosystemctlrestartgrafana-server

```

✅ Now Grafana auto-loads Prometheus without manual UI setup.

---

## 3. Validate Prometheus Targets

In Prometheus UI (`http://61.97.120.204:9090/targets`) you should see:

*`node` → `61.97.120.204:9100`

*`gpu` → `61.97.120.204:9400`

*`celery` → `61.97.120.204:8888`

*`fastapi` → `61.97.120.204:8000`

*`prometheus` → `61.97.120.204:9090`

---

## 4. Recording Rules (Celery)

📂 `/mnt/sdb/sudip/TWArch_Production/prometheus_config/celery_rules.yml`

```yaml

groups:

  - name: celery.rules

    interval: 15s

    rules:

      - record: job:celery_tasks_total

        expr: sum(celery_tasks)

      - record: job:celery_tasks_success_total

        expr: sum(celery_tasks{state="SUCCESS"})

      - record: job:celery_tasks_failed_total

        expr: sum(celery_tasks{state="FAILURE"})

      - record: job:celery_tasks_pending_total

        expr: sum(celery_tasks{state="PENDING"})

      - record: job:celery_tasks_received_total

        expr: sum(celery_tasks{state="RECEIVED"})

      - record: job:celery_tasks_success_by_name

        expr: sum by (name) (celery_tasks_by_name{state="SUCCESS"})

      - record: job:celery_tasks_runtime_avg

        expr: avg(rate(celery_tasks_runtime_seconds_sum[5m]) / rate(celery_tasks_runtime_seconds_count[5m]))

```

✅ These give **ready-to-use metrics** for Grafana dashboards.

---

## 5. Dashboards to Import (Recommended)

***Node Exporter Full** → `1860` (Grafana.com dashboard ID)

***NVIDIA DCGM GPU Dashboard** → `12239`

***Celery / RabbitMQ / Redis Monitoring** → custom (we can export your Celery rules dashboard)

***FastAPI / Starlette Prometheus** → custom or community dashboards

Import dashboards:

Grafana → **Dashboards → Import → Use ID or JSON file**

---

## 6. Ports Summary

* Grafana UI: `:3000`
* Prometheus: `:9090`
* Node Exporter: `:9100`
* GPU Exporter: `:9400`
* Celery Exporter: `:8888`
* FastAPI: `:8000`

---

## 7. Final Verification

* Open Grafana → **Explore → Prometheus**
* Test queries:

  *`DCGM_FI_DEV_GPU_UTIL` → GPU utilization

  *`node_cpu_seconds_total` → CPU usage

  *`job:celery_tasks_success_total` → Celery tasks

  *`http_requests_total` (or similar) → FastAPI requests

---

✅ With this setup:

* Grafana auto-connects to Prometheus at startup.
* All exporters are already scraped by Prometheus.
* Recording rules (Celery) make metrics easy to visualize in Grafana dashboards.

---

Do you want me to now **generate a ready-to-import Grafana dashboard JSON** that already includes **CPU, GPU, Celery, and FastAPI panels** so you don’t need to build it from scratch?
