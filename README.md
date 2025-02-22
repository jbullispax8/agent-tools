# Jira Integration Tools for Cursor Agent

A Python toolkit that provides a simple interface for interacting with the Jira API, specifically designed for Cursor AI agent integration. This toolkit enables natural language interactions with your Jira workspace through the Cursor agent.

## Prerequisites

- Python 3.7+
- Jira account with API token access
- Access to a Jira instance (Cloud or Server)
- Confluence account with API token access (optional)
- Cursor IDE with AI agent enabled

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
# On Unix/macOS
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` file with your credentials:
```
# Jira Configuration
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token

# Confluence Configuration (optional)
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-username@example.com
CONFLUENCE_API_TOKEN=your-confluence-api-token

# Redshift Configuration (optional)
REDSHIFT_HOST=your-cluster.region.redshift.amazonaws.com
REDSHIFT_PORT=5439
REDSHIFT_DATABASE=your_database
REDSHIFT_USER=your_username
REDSHIFT_PASSWORD=your_password
```

### Getting Atlassian API Tokens

1. Log in to your Atlassian account at https://id.atlassian.com/manage/api-tokens
2. Click "Create API token"
3. Give your token a name and click "Create"
4. Copy the token and paste it in your `.env` file
5. Repeat the process for both Jira and Confluence if you plan to use both integrations

## Agent Interaction Examples

You can interact with your Jira workspace through natural language commands to the Cursor agent. Here are some example interactions:

### Ticket Management
- "Pull and prioritize all my active tickets"
- "Show me all high-priority tickets assigned to me"
- "What are my overdue tickets?"
- "Create a new bug ticket for the login issue"

### Ticket Analysis
- "Explain the requirements for ticket PROJECT-123"
- "Review the acceptance criteria for this ticket"
- "What's the current status of the authentication feature tickets?"
- "Show me all related tickets to PROJECT-123"

### Code Review Support
- "Does this code meet the requirements in ticket PROJECT-123?"
- "Check if my implementation matches the acceptance criteria"
- "List all tickets affected by changes in the auth module"

## Technical Implementation

The toolkit provides these core methods for agent operations:

```python
from jira_client import JiraTools

# Initialize the client
jira = JiraTools()

# Get a specific issue
issue = jira.get_issue('PROJECT-123')

# Create a new issue
new_issue = jira.create_issue(
    project_key='PROJECT',
    summary='New task title',
    description='Detailed description of the task'
)

# Search for issues using JQL
issues = jira.search_issues('project = PROJECT AND status = "In Progress"')

# Add a comment to an issue
jira.add_comment('PROJECT-123', 'This is a new comment')

# Get project information
project = jira.get_project('PROJECT')

# List all accessible projects
projects = jira.get_all_projects()
```

## Available Methods

### Basic Operations
- `get_issue(issue_key)`: Retrieve a specific issue
- `create_issue(project_key, summary, description, issue_type='Task')`: Create a new issue
- `search_issues(jql_query)`: Search for issues using JQL
- `add_comment(issue_key, comment)`: Add a comment to an issue
- `get_project(project_key)`: Get project information
- `get_all_projects()`: List all accessible projects

### Advanced Issue Management
- `get_my_issues(status=None, priority=None)`: Get all issues assigned to the current user with optional status and priority filters
- `get_issue_details(issue_key)`: Get comprehensive details about an issue including acceptance criteria and requirements
- `get_overdue_issues()`: Get all overdue issues assigned to the current user
- `get_related_issues(issue_key)`: Get all issues related to the specified issue
- `update_issue_status(issue_key, status_name)`: Update the status of an issue

### Analysis and Metrics
- `get_issue_history(issue_key)`: Get the complete change history of an issue
- `get_sprint_issues(project_key)`: Get all issues in the current sprint for a project
- `get_issue_metrics(issue_key)`: Get time tracking and other metrics for an issue

Each method returns structured data that the agent can use to:
- Analyze ticket requirements and acceptance criteria
- Track progress and identify bottlenecks
- Manage dependencies between tickets
- Monitor time estimates and actual time spent
- Review ticket history and changes
- Manage sprint planning and execution

## Security Notes

- Never commit your `.env` file to version control
- Keep your API token secure and rotate it regularly
- Use environment variables for sensitive information

# Redshift Integration for Cursor Agent

This toolkit also includes a Redshift integration that allows you to query your Redshift database through natural language interactions with the Cursor agent.

## Redshift Configuration

1. Ensure your `.env` file includes Redshift credentials:
```
# Redshift Configuration
REDSHIFT_HOST=your-cluster.region.redshift.amazonaws.com
REDSHIFT_PORT=5439
REDSHIFT_DATABASE=your_database
REDSHIFT_USER=your_username
REDSHIFT_PASSWORD=your_password
```

## Redshift Query Examples

You can interact with your Redshift database through natural language commands. Here are some example interactions:

- "Show me all active subscriptions for vendor X"
- "Query the total number of customers by product"
- "Find all transactions in the last 30 days"
- "Get the schema information for table Y"

## Technical Implementation

The toolkit provides these core methods for Redshift operations:

```python
from redshift_client import RedshiftClient, run_query

# Using the context manager
with RedshiftClient() as client:
    # Execute a query and get results as dictionaries
    results = client.execute_query(
        "SELECT * FROM schema.table WHERE condition = %s",
        params={'condition': 'value'}
    )
    
    # Execute a query and get results as a pandas DataFrame
    df = client.query_to_dataframe(
        "SELECT * FROM schema.table WHERE condition = %s",
        params={'condition': 'value'}
    )

# Or use the convenience function
results = run_query(
    "SELECT * FROM schema.table WHERE condition = %s",
    params={'condition': 'value'},
    output_format='df'  # or 'dict' for dictionary output
)
```

### Available Methods

#### RedshiftClient Class
- `execute_query(query, params=None)`: Execute a query and return results as a list of dictionaries
- `query_to_dataframe(query, params=None)`: Execute a query and return results as a pandas DataFrame
- `close()`: Close the database connection

#### Convenience Functions
- `run_query(query, params=None, output_format='dict')`: Execute a query and return results in the specified format

### Features
- Automatic connection management with context manager
- Support for parameterized queries
- Multiple output formats (dictionaries or pandas DataFrames)
- Connection pooling and automatic cleanup
- Error handling and connection retry logic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

# Confluence Integration for Cursor Agent

This toolkit includes a Confluence integration that allows you to manage your Confluence workspace through natural language interactions with the Cursor agent.

## Confluence Configuration

Ensure your `.env` file includes Confluence credentials:
```
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-username@example.com
CONFLUENCE_API_TOKEN=your-confluence-api-token
```

## Confluence Interaction Examples

You can interact with your Confluence workspace through natural language commands or the CLI tool. Here are some example interactions:

### Content Management
- "Create a new page in the SPACE space"
- "Update the content of page with ID 123456"
- "Get all child pages of the parent page"
- "Export page as PDF"

### Search and Navigation
- "Search for pages containing 'keyword'"
- "List all available spaces"
- "Show me all pages in the SPACE space"
- "Get all attachments from page 123456"

### Collaboration
- "Add a comment to page 123456"
- "Get all comments from the page"
- "Attach a file to the page"

## Technical Implementation

The toolkit provides these core methods for Confluence operations:

```python
from confluence_client import ConfluenceTools

# Initialize the client
confluence = ConfluenceTools()

# Get a specific page
page = confluence.get_page('123456')

# Create a new page
new_page = confluence.create_page(
    space_key='SPACE',
    title='New Page Title',
    body='<p>Page content in HTML format</p>'
)

# Search for content
results = confluence.search_content('text ~ "search term"')

# Add a comment to a page
confluence.add_comment('123456', 'This is a new comment')

# List all spaces
spaces = confluence.get_space_list()
```

### CLI Usage

The toolkit includes a command-line interface for Confluence operations:

```bash
# List all spaces
./confluence_cli.py list-spaces

# Create a new page
./confluence_cli.py create-page --space-key SPACE --title "Page Title" --body "<p>Content</p>"

# Get page content
./confluence_cli.py get-page --page-id 123456

# Search content
./confluence_cli.py search --query "text ~ 'search term'"

# Export page as PDF
./confluence_cli.py export-pdf --page-id 123456 --file-path output.pdf
```

### Available Methods

#### Basic Operations
- `get_page(page_id)`: Retrieve a specific page
- `create_page(space_key, title, body, parent_id=None)`: Create a new page
- `update_page(page_id, title, body)`: Update an existing page
- `delete_page(page_id)`: Delete a page
- `get_page_children(page_id)`: Get all child pages

#### Search and Navigation
- `search_content(cql_query)`: Search using Confluence Query Language
- `get_space_content(space_key, limit=100)`: Get all content in a space
- `get_space_list()`: List all accessible spaces

#### Collaboration
- `add_comment(page_id, comment)`: Add a comment to a page
- `get_page_comments(page_id)`: Get all comments on a page
- `attach_file(page_id, file_path)`: Attach a file to a page
- `get_attachments(page_id)`: Get all attachments on a page
- `export_page_as_pdf(page_id, output_path)`: Export a page as PDF
