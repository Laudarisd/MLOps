# Docker in MLOps Infrastructure

This folder contains Dockerfiles and guides for containerizing services in your MLOps stack.

---

## 1. What is Docker?
Docker is a platform for packaging applications and their dependencies into portable containers. Containers ensure consistency across development, testing, and production.

---

## 2. Sample Dockerfile
- See `Dockerfile` for a Python ML service example.
- Build the image:
	```sh
	docker build -t my-ml-service .
	```
- Run the container:
	```sh
	docker run -p 8000:8000 my-ml-service
	```

---

## 3. Best Practices
- Use minimal base images (e.g., python:3.10-slim)
- Pin dependency versions in `requirements.txt`
- Use `.dockerignore` to exclude unnecessary files

---

## 4. Security
- Regularly update images
- Scan images for vulnerabilities (e.g., Trivy)

---

## 5. References
- [Docker Documentation](https://docs.docker.com/)
- [Best Practices for Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
