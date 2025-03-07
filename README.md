# CodeChat Documentation

## Summary
CodeChat is an AI-powered code analysis tool that leverages Claude (Anthropic's LLM) to help developers understand codebases, generate documentation, and analyze GitHub issues. It converts code repositories and issues into a structured XML format for better LLM comprehension and provides an interactive CLI interface for querying the codebase.

## Directory Structure

```
./chat/
├── CodeToXML.py        # Converts code repositories to XML format
├── IssueToXML.py       # Converts GitHub issues to XML format
├── XMLUtil.py          # Handles XML processing and compression
├── LLM.py             # Main Claude API interface and conversation management
├── LLM_utils.py       # Helper functions for LLM interactions
├── constants.py       # System configuration and prompts
└── main.py           # CLI application entry point
```

## Requirements

```
anthropic>=0.7.0
requests
nltk
xml.etree.ElementTree
```

Environment variables:
- `github_token`: GitHub Personal Access Token for repository access

## Installation

1. Clone the repository
2. Install required packages:
```bash
pip install anthropic requests nltk
```
3. Set up environment variables:
```bash
export github_token='your_github_token'
```

## Usage

1. Run the application:
```bash
python main.py
```

2. When prompted, provide either:
   - A local path to a code repository
   - A GitHub repository URL

3. Available commands:
   - `generate documentation`: Automatically generate markdown documentation
   - `investigate issue`: Analyze a GitHub issue (requires issue URL)
   - Any custom question about the code
   - `exit`: Quit the application

## Features

### 1. Code Repository Analysis
- Supports both local and GitHub repositories
- Converts code to structured XML format
- Maintains conversation context for follow-up questions

### 2. Documentation Generation
- Automatically generates comprehensive documentation
- Includes code structure and functionality analysis
- Provides usage instructions and requirements

### 3. GitHub Issue Investigation
- Analyzes issue content and comments
- Extracts and processes code snippets
- Provides resolution suggestions

### 4. XML Processing
- Compresses code content to fit LLM context windows
- Removes unnecessary whitespace and stop words
- Maintains code structure and meaning

## Error Handling

The application includes error handling for:
- Invalid repository paths/URLs
- GitHub API rate limiting
- XML parsing errors
- LLM API communication issues

## Technical Details

### XML Format Structure
```xml
<source type="[github_repository|local_directory]" url/path="...">
    <file name="...">
        [file_content]
    </file>
    ...
</source>
```

### Issue XML Structure
```xml
<source type="github_issue" url="...">
    <issue_info>
        <title>...</title>
        <description>...</description>
        <comments>
            <comment>
                <author>...</author>
                <content>...</content>
                <code_snippet>...</code_snippet>
            </comment>
        </comments>
    </issue_info>
</source>
```

## Limitations

1. File type restrictions: Only processes certain file extensions (.py, .txt, .md, .html, .json, .yaml)
2. GitHub API rate limiting may affect repository access
3. Large repositories may require additional processing time
4. Context window limitations may affect very large files

## Security Considerations

1. GitHub tokens should be kept secure
2. Local file access is restricted to specified file types
3. XML processing includes escape character handling
4. API keys should be properly managed through environment variables
