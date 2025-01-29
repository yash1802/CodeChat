import requests
import os
import nltk
from nltk.corpus import stopwords
from XMLUtil import compress_XML

nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))

TOKEN = os.getenv('GITHUB_TOKEN', 'Enter your Github Personal Access Token')
headers = {"Authorization": f"token {TOKEN}"}

EXCLUDED_DIRS = [".git", "__pycache__"]

def download_file(url, target_path):
    """
    Fetches the data from the files in the repo
    """
    response = requests.get(url, headers=headers)
    with open(target_path, "wb") as f:
        f.write(response.content)

def convert_repo(repo_url):
    """
    Transforms a given github repository's code into a single, unified XML format (stored as .txt)
    """
    api_base_url = "https://api.github.com/repos/"
    repo_url_components = repo_url.split("https://github.com/")[-1].split("/")
    repo_name = "/".join(repo_url_components[:2])

    # Detect branch or tag references
    subdirectory = ""
    branch_or_tag = ""
    if len(repo_url_components) > 2 and repo_url_components[2] == "tree":
        if len(repo_url_components) > 3:
            branch_or_tag = repo_url_components[3]

        if len(repo_url_components) > 4:
            subdirectory = "/".join(repo_url_components[4:])
    
    contents_url = f"{api_base_url}{repo_name}/contents"
    if subdirectory:
        contents_url = f"{contents_url}/{subdirectory}"
    if branch_or_tag:
        contents_url = f"{contents_url}?ref={branch_or_tag}"

    repo_content = [f'<source type="github_repository" url="{repo_url}">']

    def process_directory(url, repo_content):
        response = requests.get(url, headers=headers)
        files = response.json()

        for file in files:
            if file["type"] == "dir" and file["name"] in EXCLUDED_DIRS:
                continue

            if file["type"] == "file" and is_allowed_filetype(file["name"]):

                temp_file = f"temp_{file['name']}"
                download_file(file["download_url"], temp_file)

                repo_content.append(f'<file name="{escape_xml(file["path"])}">') 
                with open(temp_file, "r", encoding='utf-8', errors='ignore') as f:
                    repo_content.append(escape_xml(f.read()))
                repo_content.append('</file>')
                os.remove(temp_file)

            elif file["type"] == "dir":
                process_directory(file["url"], repo_content)

    process_directory(contents_url, repo_content)
    repo_content.append('</source>')

    return "\n".join(repo_content)

def process_local_folder(local_path):
    """
    Transforms a local repository's code into a single, unified XML format (stored as .txt)
    """
    def process(local_path):
        content = [f'<source type="local_directory" path="{escape_xml(local_path)}">']
        for root, dirs, files in os.walk(local_path):

            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

            for file in files:
                if is_allowed_filetype(file):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, local_path)
                    content.append(f'<file name="{escape_xml(relative_path)}">')

                    with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                        content.append(escape_xml(f.read()))

                    content.append('</file>')

        content.append('</source>')
        return '\n'.join(content)

    formatted_content = process(local_path)
    return formatted_content

    
def escape_xml(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

def is_allowed_filetype(filename):
    """
    Check if a file should be processed.
    """
    return any(filename.endswith(ext) for ext in ['.py','.txt','.md','.html','.json','.yaml'])

def convert_code_to_xml(input_path):
    XML_file = "XML_output.txt"
    XML_file_compressed = "compressed_XML_output.txt"

    print("\nProcessing the code...")
    if "github.com" in input_path:
        final_output = convert_repo(input_path)
    else:
        final_output = process_local_folder(input_path)

    with open(XML_file, "w", encoding="utf-8") as file:
        file.write(final_output)

    compress_XML(XML_file, XML_file_compressed)
    print("Code processing complete.")