

# S3

This folder contains scripts and configs for managing AWS S3 buckets and objects.

---

## What is S3?
Amazon S3 (Simple Storage Service) is AWS's object storage service for storing and retrieving any amount of data.

---

## Step-by-Step: How to Use S3

### 0. Install and Configure AWS CLI
- **Install AWS CLI:**
  - [Download & Install Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
  - On Windows: Download the MSI installer and follow the prompts.
  - On Mac/Linux: Use `pip install awscli` or package manager.
- **Configure AWS CLI:**
  - Run in terminal:
	```sh
	aws configure
	```
  - Enter your AWS Access Key, Secret Key, region, and output format.

### 1. Create an S3 Bucket
- Using AWS Console: Go to S3 > Create bucket > Set name and region > Create
- Using AWS CLI:
	```sh
	aws s3 mb s3://my-mlops-bucket
	```

### 2. Upload Data to S3
- Using AWS Console: Open your bucket > Upload > Add files > Upload
- Using AWS CLI:
	```sh
	aws s3 cp myfile.txt s3://my-mlops-bucket/
	aws s3 sync ./data/ s3://my-mlops-bucket/data/
	```

### 3. Download Data from S3
- Using AWS CLI:
	```sh
	aws s3 cp s3://my-mlops-bucket/myfile.txt ./
	aws s3 sync s3://my-mlops-bucket/data/ ./data/
	```

### 4. List Bucket Contents
- Using AWS CLI:
	```sh
	aws s3 ls s3://my-mlops-bucket/
	```

### 5. Delete Objects or Buckets
- Using AWS CLI:
	```sh
	aws s3 rm s3://my-mlops-bucket/myfile.txt
	aws s3 rb s3://my-mlops-bucket --force
	```

---

## Using the Terminal
- Open your terminal (Command Prompt, PowerShell, or Terminal on Mac/Linux).
- Run AWS CLI commands as shown above.
- Use `aws help` for more options.

---

## Local S3 Emulation (Optional)
You can use [LocalStack](https://github.com/localstack/localstack) to emulate S3 locally for testing:
1. Install Docker and run:
	```sh
	docker run -d -p 4566:4566 localstack/localstack
	```
2. Set AWS CLI endpoint:
	```sh
	aws --endpoint-url=http://localhost:4566 s3 mb s3://local-bucket
	```
3. Use the same AWS CLI commands with `--endpoint-url` for local testing.

---

## Example: Python Script to Upload to S3
```python
import boto3
s3 = boto3.client('s3')
s3.upload_file('localfile.txt', 'my-mlops-bucket', 'uploadedfile.txt')
```

---

## References
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/index.html)
- [Boto3 S3 Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
- [LocalStack S3](https://docs.localstack.cloud/user-guide/aws/s3/)

## References
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/index.html)
- [Boto3 S3 Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
