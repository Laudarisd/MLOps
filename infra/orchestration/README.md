# Orchestration in MLOps

This folder contains scripts and configs for orchestrating distributed tasks and workflows (e.g., Celery, Redis, schedulers).

---

## 1. What is Orchestration?
Orchestration coordinates multiple tasks, jobs, or services, ensuring they run in the correct order and handle dependencies, retries, and failures.

---

## 2. Celery Example
- See `celery_worker.py` for a sample Celery worker.
- Use Redis as a message broker (see `redis_config.py`).
- Start a worker:
  ```sh
  celery -A celery_worker worker --loglevel=info
  ```

---

## 3. Scheduling Jobs
- Use `scheduler.py` for scheduled jobs (e.g., with APScheduler).
- Example:
  ```sh
  python scheduler.py
  ```

---

## 4. References
- [Celery Documentation](https://docs.celeryq.dev/en/stable/)
- [Redis Docs](https://redis.io/documentation)
- [APScheduler Docs](https://apscheduler.readthedocs.io/en/latest/)
