# Security in MLOps Infrastructure

This folder contains best practices, scripts, and configuration examples for securing your MLOps infrastructure.

---

## 1. IAM & Access Control

- Use least privilege for all users and services
- Rotate credentials regularly
- Use environment variables or secret managers for sensitive data

---

## 2. Network Security

- Restrict inbound/outbound traffic with firewalls or security groups
- Use VPN or private networking for sensitive services
- Enable HTTPS for all web endpoints

---

## 3. Container Security

- Use official, minimal base images (e.g., python:3.10-slim, nginx:alpine)
- Regularly update images and dependencies
- Scan images for vulnerabilities (e.g., Trivy, Clair)

---

## 4. Kubernetes Security (if using k8s)

- Use RBAC for access control
- Enable PodSecurityPolicies or Pod Security Standards
- Use network policies to restrict pod communication

---

## 5. Monitoring & Auditing

- Enable logging for all services
- Monitor for suspicious activity (e.g., failed logins, privilege escalation)
- Regularly review audit logs

---

## 6. References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CNCF Cloud Native Security Whitepaper](https://github.com/cncf/tag-security/blob/main/security-whitepaper/CNCF_cloud-native-security-whitepaper-Nov2020.pdf)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/overview/)
