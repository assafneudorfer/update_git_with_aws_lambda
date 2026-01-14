import os
import json
import subprocess
import shutil
from datetime import datetime

def lambda_handler(event, context):
    """
    Lambda function that updates date.txt in a GitHub repository.
    """
    # Configuration from environment variables
    github_token = os.environ.get('GITHUB_TOKEN')
    repo_url = os.environ.get('REPO_URL')  # e.g., github.com/username/repo
    branch = os.environ.get('BRANCH', 'main')

    if not github_token or not repo_url:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing GITHUB_TOKEN or REPO_URL environment variables')
        }

    # Working directory in Lambda's /tmp
    work_dir = '/tmp/repo'

    # Clean up any existing directory
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)

    try:
        # Clone the repository
        clone_url = f'https://x-access-token:{github_token}@{repo_url}'
        subprocess.run(
            ['git', 'clone', '--depth', '1', '-b', branch, clone_url, work_dir],
            check=True,
            capture_output=True
        )

        # Update date.txt with current timestamp
        date_file = os.path.join(work_dir, 'date.txt')
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        with open(date_file, 'w') as f:
            f.write(f'Last updated: {current_time}\n')

        # Configure git
        subprocess.run(['git', 'config', 'user.email', 'lambda@automated.bot'], cwd=work_dir, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Lambda Bot'], cwd=work_dir, check=True)

        # Stage, commit, and push
        subprocess.run(['git', 'add', 'date.txt'], cwd=work_dir, check=True)

        # Check if there are changes to commit
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=work_dir)
        if result.returncode != 0:
            subprocess.run(
                ['git', 'commit', '-m', f'Update date.txt: {current_time}'],
                cwd=work_dir,
                check=True
            )
            subprocess.run(['git', 'push'], cwd=work_dir, check=True)
            message = f'Successfully updated date.txt at {current_time}'
        else:
            message = 'No changes to commit'

        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }

    except subprocess.CalledProcessError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Git operation failed: {e.stderr.decode() if e.stderr else str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
