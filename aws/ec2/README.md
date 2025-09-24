# EC2

This folder contains scripts and configs for managing AWS EC2 instances.

---

## What is EC2?

Amazon EC2 (Elastic Compute Cloud) provides scalable virtual servers (instances) in the AWS cloud. You can use EC2 for running applications, training ML models, hosting APIs, and more.

---

## Step-by-Step: Launching and Using EC2 (Beginner Guide)

### 1. Prerequisites

- AWS account ([Sign up](https://aws.amazon.com/))
- AWS Console access
- (Optional) AWS CLI installed and configured

### 2. Launch an EC2 Instance (AWS Console)

1. Go to [AWS Console](https://console.aws.amazon.com/)
2. Navigate to EC2 > Instances > Launch Instance
3. Choose an Amazon Machine Image (AMI), e.g., Ubuntu, Amazon Linux
4. Choose an instance type (e.g., t2.micro for free tier)
5. Configure instance details (default is fine for beginners)
6. Add storage (default is fine)
7. Add tags (optional)
8. Configure security group (allow SSH: port 22, and other ports as needed)
9. Review and launch
10. Create/download a key pair (for SSH access)
11. Click Launch

### 3. Connect to Your EC2 Instance

- On the Instances page, select your instance and click "Connect"
- For SSH (Linux/Mac/WSL):
  ```sh
  ssh -i /path/to/your-key.pem ec2-user@<public-ip>
  # or for Ubuntu AMI:
  ssh -i /path/to/your-key.pem ubuntu@<public-ip>
  ```
- For Windows: Use [PuTTY](https://www.putty.org/) and convert `.pem` to `.ppk` with PuTTYgen

### 4. (Optional) Launch EC2 Using AWS CLI

```sh
aws ec2 run-instances --image-id ami-xxxxxx --count 1 --instance-type t2.micro --key-name my-key --security-group-ids sg-xxxxxx --subnet-id subnet-xxxxxx
```

Find AMI IDs in the AWS Console or with:

```sh
aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm*"
```

### 5. Stop, Start, or Terminate an Instance

```sh
# Stop
aws ec2 stop-instances --instance-ids i-xxxxxx
# Start
aws ec2 start-instances --instance-ids i-xxxxxx
# Terminate
aws ec2 terminate-instances --instance-ids i-xxxxxx
```

---

## Tips

- Always stop or terminate instances when not in use to avoid charges
- Use security groups to control access
- Use IAM roles for secure access to AWS services

---

## References

- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/index.html)
- [EC2 Getting Started Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
