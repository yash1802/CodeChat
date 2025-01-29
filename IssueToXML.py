import requests
import os
import nltk
from nltk.corpus import stopwords
import re
from XMLUtil import compress_XML

nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))

TOKEN = os.getenv('GITHUB_TOKEN', 'Enter your Github Personal Access Token')
headers = {"Authorization": f"token {TOKEN}"}

def escape_xml(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def convert_issue(issue_url):
    """
    Transforms a given github repository's issue into XML format (stored as .txt)
    """
    url_parts = issue_url.split("/")
    repo_owner = url_parts[3]
    repo_name = url_parts[4]
    issue_number = url_parts[-1]

    api_base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}"
    headers = {"Authorization": f"token {TOKEN}"}

    response = requests.get(api_base_url, headers=headers)
    issue_data = response.json()

    comments_url = issue_data["comments_url"]
    comments_response = requests.get(comments_url, headers=headers)
    comments_data = comments_response.json()

    xml_text = f'<source type="github_issue" url="{issue_url}">\n'
    xml_text += '<issue_info>\n'
    xml_text += f'<title>{escape_xml(issue_data["title"])}</title>\n'
    xml_text += f'<description>{escape_xml(issue_data["body"])}</description>\n'
    xml_text += '<comments>\n'

    for comment in comments_data:
        xml_text += '<comment>\n'
        xml_text += f'<author>{escape_xml(comment["user"]["login"])}</author>\n'
        xml_text += f'<content>{escape_xml(comment["body"])}</content>\n'

        code_snippets = re.findall(r'https://github.com/.*#L\d+-L\d+', comment['body'])
        for snippet_url in code_snippets:
            url_parts = snippet_url.split("#")
            file_url = url_parts[0].replace("/blob/", "/raw/")
            line_range = url_parts[1]
            start_line, end_line = map(int, line_range.split("-")[0][1:]), map(int, line_range.split("-")[1][1:])

            file_response = requests.get(file_url, headers=headers)
            file_content = file_response.text

            code_lines = file_content.split("\n")[start_line - 1:end_line]
            code_snippet = "\n".join(code_lines)

            xml_text += '<code_snippet>\n'
            xml_text += f'<![CDATA[{code_snippet}]]>\n'
            xml_text += '</code_snippet>\n'

        xml_text += '</comment>\n'

    xml_text += '</comments>\n'
    xml_text += '</issue_info>\n'
    xml_text += '</source>'

    return xml_text


def convert_issue_to_xml(input_path):
    XML_file = "Issue_XML_output.txt"
    XML_file_compressed = "compressed_Issue_XML_output.txt"

    print("\nProcessing the github issue data...")
    final_output = convert_issue(input_path)

    with open(XML_file, "w", encoding="utf-8") as file:
        file.write(final_output)

    compress_XML(XML_file, XML_file_compressed)
    print("processing complete.")