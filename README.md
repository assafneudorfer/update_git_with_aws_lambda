# AWS Lambda Git Date Updater

A simple AWS Lambda function that runs daily and updates `date.txt` in this repository.

## Prerequisites

- AWS CLI configured with credentials
- Terraform >= 1.0
- GitHub Personal Access Token with `repo` scope

## Setup

1. **Create GitHub Token**
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate a new token with `repo` scope
   - Copy the token

2. **Configure Terraform**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
   Edit `terraform.tfvars` with your values:
   ```hcl
   aws_region   = "us-east-1"
   github_token = "ghp_your_token"
   repo_url     = "github.com/your-username/your-repo"
   branch       = "main"
   ```

3. **Deploy**
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

## Test Manually

Invoke the Lambda manually to test:
```bash
aws lambda invoke --function-name git-date-updater output.json
cat output.json
```

## Cleanup

Remove all resources:
```bash
terraform destroy
```

## How It Works

- CloudWatch Events triggers the Lambda daily at midnight UTC
- Lambda clones the repo, updates `date.txt` with current timestamp
- Changes are committed and pushed back to the repository
