# vault_config.hcl
# Sample Vault server configuration
storage "file" {
  path = "./vault-data"
}
listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = 1
}
