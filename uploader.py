# [START pubsub_code]
import os
import shutil
import sys

def add_anchors_to_file(input_file, output_file):
    """
    Adds START and END anchor markers around the content of the given file.
    """
    with open(input_file, 'r') as infile:
        content = infile.read()

    # Wrap with anchors if not already present
    if "# [START pubsub_code]" not in content:
        content = "# [START pubsub_code]\n" + content + "\n# [END pubsub_code]"

    with open(output_file, 'w') as outfile:
        outfile.write(content)

def push_file_to_git(local_repo_path, filename):
    """
    Adds, commits, and pushes the given file into the git repo.
    """
    os.chdir(local_repo_path)
    os.system(f"git add {filename}")
    os.system(f"git commit -m \"Add {filename} via uploader\" || echo 'No changes to commit'")
    os.system("git push origin main")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python uploader.py <input_file_path> <local_repo_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    local_repo_path = sys.argv[2]
    filename = os.path.basename(input_file)
    output_file = os.path.join(local_repo_path, filename)

    # Make sure repo folder exists
    if not os.path.exists(local_repo_path):
        print(f"Error: Repo folder '{local_repo_path}' does not exist.")
        sys.exit(1)

    # Add anchors to the file and save it into the repo
    add_anchors_to_file(input_file, output_file)

    # Push it to GitHub
    push_file_to_git(local_repo_path, filename)

    print(f"Uploaded and pushed '{filename}' to repo successfully.")

# [END pubsub_code]