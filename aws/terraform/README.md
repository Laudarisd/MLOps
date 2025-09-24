# Terraform

This folder contains Terraform scripts for provisioning AWS infrastructure (e.g., S3, EC2, IAM).

---

## What is Terraform?

Terraform is an open-source Infrastructure as Code (IaC) tool by HashiCorp. It allows you to define, provision, and manage cloud resources (like AWS, Azure, GCP) using simple configuration files.

---

## Step-by-Step: Using Terraform for AWS (Beginner Guide)

### 1. Prerequisites

- AWS account ([Sign up](https://aws.amazon.com/))
- AWS CLI installed and configured (`aws configure`)
- [Terraform installed](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

### 2. Write Your Terraform Configuration

- See `main.tf` for an example that provisions an S3 bucket.

### 3. Initialize Terraform

Open a terminal and run:

```sh
cd aws/terraform
terraform init
```

This downloads the AWS provider and sets up your working directory.

### 4. Preview the Changes

```sh
terraform plan
```

This shows what Terraform will do without making changes.

### 5. Apply the Configuration

```sh
terraform apply
```

Type `yes` when prompted. Terraform will create the resources in your AWS account.

### 6. Inspect the State

Terraform keeps track of resources in a `terraform.tfstate` file. You can inspect it or use:

```sh
terraform show
```

### 7. Destroy the Resources

To clean up and avoid charges:

```sh
terraform destroy
```

---

## Tips

- Use variables and outputs for flexible, reusable configs
- Store state files securely (consider remote backends for teams)
- Use `terraform fmt` to auto-format your configs

---

## References

- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Getting Started Guide](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-build)
