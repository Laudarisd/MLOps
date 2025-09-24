# Lambda

This folder contains AWS Lambda functions and deployment scripts.

---

## What is AWS Lambda?

AWS Lambda is a serverless compute service that lets you run code without provisioning or managing servers. You pay only for the compute time you use.

---

## Step-by-Step: Deploying and Using Lambda (Beginner Guide)

### 1. Prerequisites

- AWS account ([Sign up](https://aws.amazon.com/))
- AWS Console access
- (Optional) AWS CLI installed and configured

### 2. Author a Lambda Function

- Write your function in Python (see `lambda_function.py` for an example)
- The handler function should be named `handler(event, context)`

### 3. Deploy Using AWS Console

1. Go to AWS Console > Lambda > Create function
2. Choose "Author from scratch"
3. Set function name, runtime (e.g., Python 3.10)
4. Upload your code (zip file or inline editor)
5. Set handler to `lambda_function.handler`
6. Create or select an IAM role for permissions
7. Click Create function

### 4. Deploy Using AWS CLI

1. Zip your function code:
   ```sh
   zip function.zip lambda_function.py
   ```
2. Create the Lambda function:
   ```sh
   aws lambda create-function --function-name my-function \
     --runtime python3.10 --role arn:aws:iam::123456789012:role/lambda-role \
     --handler lambda_function.handler --zip-file fileb://function.zip
   ```

### 5. Invoke the Lambda Function

- Using AWS Console: Click "Test" and provide a sample event
- Using AWS CLI:
  ```sh
  aws lambda invoke --function-name my-function output.json
  ```

### 6. Update the Lambda Function

```sh
zip function.zip lambda_function.py
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip
```

### 7. Delete the Lambda Function

```sh
aws lambda delete-function --function-name my-function
```

---

## Tips

- Use IAM roles to grant your function access to other AWS services
- Set environment variables for configuration
- Monitor logs in AWS CloudWatch

---

## References

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [AWS CLI Lambda Commands](https://docs.aws.amazon.com/cli/latest/reference/lambda/index.html)
