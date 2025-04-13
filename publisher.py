# publisher.py
import os
import re
import requests
import asyncio
from nats.aio.client import Client as NATS

def push_file_to_git(local_repo_path, filename, commit_msg):
    """
    Change directory into the repo, add the file, commit, and push.
    Assumes git is installed and configured on the runner.
    """
    os.chdir(local_repo_path)
    os.system(f"git add {filename}")
    os.system(f"git commit -m \"{commit_msg}\"")
    os.system("git push origin main")

def fetch_file_from_github(raw_url):
    """
    Downloads the full file from the given GitHub raw URL.
    """
    response = requests.get(raw_url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch the file from GitHub. Status code:", response.status_code)

def extract_anchored_section(file_content, anchor_name):
    """
    Extracts content between the markers:
       # [START <anchor_name>]
          ... code ...
       # [END <anchor_name>]
    """
    pattern = rf"# \[START {anchor_name}\](.*?)# \[END {anchor_name}\]"
    match = re.search(pattern, file_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return f"Anchor '{anchor_name}' not found."

async def run_publisher(nats_server):
    nc = NATS()
    print(f"Connecting to NATS server at {nats_server}...")
    await nc.connect(servers=[nats_server])
    
    # Update the URL with your GitHub username, repository, and branch as necessary.
    raw_url = "https://raw.githubusercontent.com/<your-username>/<your-repo>/main/user_file.py"
    anchor = "pubsub_code"
    
    print("Fetching file from GitHub...")
    file_content = fetch_file_from_github(raw_url)
    
    print(f"Extracting content for anchor '{anchor}'...")
    extracted_code = extract_anchored_section(file_content, anchor)
    
    subject = "code.update"
    print(f"Publishing extracted code to subject '{subject}' on NATS server {nats_server}...")
    await nc.publish(subject, extracted_code.encode())
    await nc.flush()
    await nc.close()
    print("Publishing completed.")

if __name__ == '__main__':
    import sys
    # The nats_server should be provided via the CI/CD pipeline; otherwise, use a default.
    nats_server = sys.argv[1] if len(sys.argv) > 1 else "nats://127.0.0.1:4222"
    asyncio.run(run_publisher(nats_server))
