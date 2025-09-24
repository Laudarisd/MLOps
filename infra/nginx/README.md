# NGINX for MLOps Infrastructure

This folder contains configuration and setup instructions for using NGINX as a reverse proxy, load balancer, or static file server in your MLOps stack.

---

## 1. What is NGINX?

NGINX is a high-performance web server and reverse proxy. In MLOps, it is commonly used to:

- Route traffic to APIs (e.g., FastAPI, Flask, model servers)
- Load balance requests across multiple backend services
- Serve static files (dashboards, documentation, etc.)
- Add SSL/TLS (HTTPS) to your endpoints

---

## 2. Basic Reverse Proxy Example

Create a file `default.conf`:

```nginx
server {
    listen 80;
    server_name _;

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 3. Running NGINX with Docker

```sh
docker run -d -p 80:80 -v $(pwd)/default.conf:/etc/nginx/conf.d/default.conf:ro nginx:alpine
```

---


## 4. Security & TLS/SSL

### Enabling HTTPS (TLS/SSL)
- Obtain a certificate (e.g., with [Let's Encrypt](https://letsencrypt.org/))
- Update your NGINX config:
    ```nginx
    server {
            listen 443 ssl;
            server_name your.domain.com;
            ssl_certificate /etc/nginx/certs/fullchain.pem;
            ssl_certificate_key /etc/nginx/certs/privkey.pem;
            ... # other config
    }
    ```
- Redirect HTTP to HTTPS for all traffic
- Use strong TLS ciphers and disable old protocols

### Other Security Best Practices
- Restrict allowed IPs or use authentication for admin endpoints
- Regularly update your NGINX image or package
- Use security headers (Content-Security-Policy, X-Frame-Options, etc.)

---

---

## 5. References

- [NGINX Documentation](https://nginx.org/en/docs/)
- [NGINX Reverse Proxy Guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Docker Hub: nginx](https://hub.docker.com/_/nginx)
