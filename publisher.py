import re
import requests
import asyncio
import sys
from nats.aio.client import Client as NATS

def fetch_file_from_github(raw_url):
    response = requests.get(raw_url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch file from GitHub")

def extract_anchored_section(file_content):
    pattern = r"# \[START pubsub_code\](.*?)# \[END pubsub_code\]"
    match = re.search(pattern, file_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        raise Exception("Anchors not found!")

async def run_publisher(nats_server, raw_url):
    print(f"Connecting to NATS server at {nats_server}...")
    nc = NATS()
    await nc.connect(servers=[nats_server])

    print("Fetching file from GitHub...")
    file_content = fetch_file_from_github(raw_url)

    print("Extracting anchored content...")
    extracted_code = extract_anchored_section(file_content)

    subject = "code.update"
    print(f"Publishing code to NATS subject '{subject}'...")
    await nc.publish(subject, extracted_code.encode())
    await nc.flush()
    await nc.close()

    print("✅ Published successfully!")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python publisher.py <nats_server> <raw_github_file_url>")
        sys.exit(1)

    nats_server = sys.argv[1]
    raw_url = sys.argv[2]
    asyncio.run(run_publisher(nats_server, raw_url))
