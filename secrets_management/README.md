# Secrets Management

This folder contains best practices and tools for managing secrets (API keys, credentials) securely in your MLOps workflows.

---

## Why Secrets Management?
Storing secrets in code or config files is insecure. Use secret managers to store and access secrets securely.

---

## Example Tools
- [HashiCorp Vault](https://www.vaultproject.io/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault/)

---

## Best Practices
- Never commit secrets to version control
- Use environment variables or secret managers
- Rotate secrets regularly

---

## References
- [12 Factor App: Config](https://12factor.net/config)
