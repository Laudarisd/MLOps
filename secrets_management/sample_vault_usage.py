# sample_vault_usage.py
"""
Sample code for reading a secret from HashiCorp Vault.
"""
import hvac

client = hvac.Client(url='http://localhost:8200', token='myroot')
secret = client.secrets.kv.v2.read_secret_version(path='mlops/secret')
print(secret['data']['data'])
