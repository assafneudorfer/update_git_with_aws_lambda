variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "github_token" {
  description = "GitHub Personal Access Token with repo permissions"
  type        = string
  sensitive   = true
}

variable "repo_url" {
  description = "GitHub repository URL (without https://) e.g., github.com/username/repo"
  type        = string
}

variable "branch" {
  description = "Git branch to update"
  type        = string
  default     = "main"
}
