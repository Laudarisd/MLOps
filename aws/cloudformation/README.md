# CloudFormation

This folder contains AWS CloudFormation templates for infrastructure as code (IaC).

---

## What is CloudFormation?

AWS CloudFormation is a service that helps you model and set up your AWS resources using templates written in YAML or JSON. It automates the provisioning and updating of your infrastructure in a safe and repeatable way.

---

## Step-by-Step: How to Use CloudFormation

### 1. Author a Template

- Write your infrastructure as code in YAML or JSON (see `template.yaml` for an S3 bucket example).

### 2. Deploy Using AWS Console

1. Go to AWS Console > CloudFormation
2. Click "Create stack" > "With new resources (standard)"
3. Upload `template.yaml` or paste its contents
4. Click Next, set stack name, and follow the prompts
5. Review and create the stack

### 3. Deploy Using AWS CLI

```sh
aws cloudformation create-stack --stack-name my-stack --template-body file://template.yaml
```

To update an existing stack:

```sh
aws cloudformation update-stack --stack-name my-stack --template-body file://template.yaml
```

### 4. Check Stack Status

```sh
aws cloudformation describe-stacks --stack-name my-stack
```

### 5. Delete a Stack

```sh
aws cloudformation delete-stack --stack-name my-stack
```

---

## Example: S3 Bucket Template

See `template.yaml` for a minimal S3 bucket CloudFormation template.

---

## Tips

- Use parameters and outputs in your templates for flexibility and reusability.
- Use the AWS CloudFormation Designer (in the Console) for visual editing.
- Stack events and logs help debug deployment issues.

---

## References

- [AWS CloudFormation Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [Template Anatomy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html)
- [AWS CLI CloudFormation Commands](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/index.html)
