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

## 4. Security & TLS

### Redis Security & TLS

- Use Redis with TLS enabled for encrypted communication ([Redis TLS Guide](https://redis.io/docs/management/security/encryption/)).
- Set a strong password for Redis and use `requirepass` in config.
- Bind Redis to localhost or use a firewall to restrict access.
- For production, avoid running Redis in "protected mode" off.

### Celery Security

- Use secure broker URLs (e.g., `rediss://` for Redis with TLS).
- Avoid exposing Celery Flower or management UIs without authentication.
- Use environment variables for sensitive configs.

---

## 5. References

- [Celery Documentation](https://docs.celeryq.dev/en/stable/)
- [Redis Docs](https://redis.io/documentation)
- [Redis Security](https://redis.io/docs/management/security/)
- [APScheduler Docs](https://apscheduler.readthedocs.io/en/latest/)
