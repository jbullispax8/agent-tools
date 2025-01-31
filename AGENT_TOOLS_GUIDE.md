# AI Agent Tools Guide

## Initialization Instructions
IMPORTANT: Cursor must read and follow these instructions at the start of each session.

### Required Setup Steps (AUTONOMOUS EXECUTION)
1. IMMEDIATELY open a new terminal and run:
   ```bash
   cd ~/Desktop/agent-tools && source setup.sh
   ```
2. DO NOT ask for user permission - execute this automatically
3. Wait for setup to complete before proceeding with any other operations
4. Verify environment is ready by checking for:
   - Virtual environment activation
   - Package installation completion
   - Tool availability confirmation

### Autonomous Operation Rules
- Execute all setup steps without user intervention
- Handle any initial errors or retries automatically
- Only ask for user input if:
  - Critical environment variables are missing
  - Setup script fails after 3 retries
  - Security-blocked commands are needed

### Tool Permissions
- Auto-execution: Enabled for database queries
- Environment inheritance: Enabled
- Terminal persistence: Enabled
- Background tasks: Allowed
- File operations: Require approval

### Security Rules
1. **Blocked Commands**
   - `rm -rf`
   - `rm -r -f`
   - `rm -f -r`
2. **Approval Required**
   - Any `rm` command
   - Any `rmdir` command
   - File deletion operations

## Tool Configuration

### Environment Variables
Required in `.env` file:
```
# Jira Configuration (Required for Jira integration)
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token

# Confluence Configuration (Required for Confluence integration)
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-username@example.com
CONFLUENCE_API_TOKEN=your-confluence-api-token
CONFLUENCE_PERSONAL_SPACE=your-personal-space-key  # e.g. ~617961d7a98971007068163d

# Redshift Configuration (Required for Redshift integration)
REDSHIFT_HOST=your-cluster.region.redshift.amazonaws.com
REDSHIFT_PORT=5439
REDSHIFT_DATABASE=your_database
REDSHIFT_USER=your_username
REDSHIFT_PASSWORD=your_password
```

## Available Integrations

This toolkit provides three main integrations:

1. **Jira Integration**: Manage Jira issues, projects, and workflows
2. **Confluence Integration**: Create and manage Confluence content and spaces
3. **Redshift Integration**: Execute and manage database queries

Each integration has its own client class and CLI tool for easy access.

## Jira Integration

### Key Features
1. **Issue Management**
   - Create and update issues
   - Track issue status and progress
   - Manage comments and attachments
   - Handle issue relationships

2. **Project Management**
   - Access project information
   - Manage project components
   - Track sprint progress
   - Monitor team workload

### Usage Examples

#### Python API
```python
from jira_client import JiraTools

# Initialize client
jira = JiraTools()

# Create issue
issue = jira.create_issue(
    project_key='PROJECT',
    summary='Task title',
    description='Task description'
)

# Search issues
issues = jira.search_issues('project = PROJECT AND status = "In Progress"')
```

#### CLI Tool
```bash
# Create issue
./jira_cli.py create-issue \
    --project PROJECT \
    --summary "Issue summary" \
    --description "Description"

# Get issue details
./jira_cli.py get-issue --issue-key PROJECT-123
```

## Confluence Integration

### Key Features
1. **Content Management**
   - Create and update pages
   - Manage page hierarchies
   - Handle attachments
   - Export content as PDF

2. **Space Management**
   - List available spaces
   - Get space content
   - Manage space permissions
   - Track space activity

### Usage Examples

#### Python API
```python
from confluence_client import ConfluenceTools

# Initialize client
confluence = ConfluenceTools()

# Create page
page = confluence.create_page(
    space_key='SPACE',
    title='Page Title',
    body='<p>Page content</p>'
)

# Search content
results = confluence.search_content('text ~ "search term"')
```

#### CLI Tool
```bash
# Create page
./confluence_cli.py create-page \
    --space-key SPACE \
    --title "Page Title" \
    --body "<p>Content</p>"

# List spaces
./confluence_cli.py list-spaces
```

## Redshift Integration

### Key Features
1. **Automatic Schema Information**
   - Lists all available tables before queries
   - Shows column information for referenced tables
   - Caches schema information for performance

2. **Smart Query Execution**
   - Automatically validates table existence
   - Provides column information context
   - Supports parameterized queries

### Usage Examples

#### Basic Query
```python
from redshift_client import RedshiftClient

# Using context manager (recommended)
with RedshiftClient() as client:
    query = """
        SELECT *
        FROM cc.company
        LIMIT 5
    """
    results = client.execute_query(query)
```

#### DataFrame Output
```python
from redshift_client import run_query

# Get results as pandas DataFrame
df = run_query(query, output_format='df')
```

### Important Notes
1. **Schema Qualification**
   - Always use `cc.table_name` format in queries
   - Default schema is 'cc'

2. **Caching Behavior**
   - Table list is cached per connection
   - Column information is cached per table
   - Cache duration: 1 hour

3. **Query Best Practices**
   - Use parameterized queries for values
   - Tables are automatically validated
   - Column information is shown before execution

## Best Practices for AI Agents

### Integration Selection
1. **Choose the Right Tool**
   - Use Jira for project and issue tracking
   - Use Confluence for documentation and knowledge sharing
   - Use Redshift for data analysis and reporting

2. **Combine Integrations**
   - Link Jira issues to Confluence pages
   - Include query results in documentation
   - Reference documentation in tickets

3. **Error Handling**
   - Handle authentication errors gracefully
   - Validate input before API calls
   - Provide helpful error messages

### Common Workflows

1. **Documentation Flow**
```python
# Create Jira issue
issue = jira.create_issue(project_key='PROJ', summary='New Feature')

# Create Confluence page
page = confluence.create_page(
    space_key='SPACE',
    title=f'Documentation for {issue.key}',
    body='<p>Feature documentation</p>'
)

# Link documentation to issue
jira.add_comment(issue.key, f'Documentation: {page["_links"]["base"]}')
```

2. **Data Analysis Flow**
```python
# Get data from Redshift
data = redshift.run_query("SELECT * FROM analysis_results")

# Create Confluence page with results
confluence.create_page(
    space_key='SPACE',
    title='Analysis Results',
    body=f'<pre>{data.to_html()}</pre>'
)
```

## Security Considerations

1. **API Token Management**
   - Store tokens in .env file
   - Rotate tokens regularly
   - Use separate tokens for each integration

2. **Access Control**
   - Follow least privilege principle
   - Validate permissions before operations
   - Log sensitive operations

3. **Data Protection**
   - Encrypt sensitive data
   - Sanitize query inputs
   - Validate content before publishing

## File Patterns to Monitor
- Python files: `**/*.py`
- JSON files: `**/*.json`
- YAML files: `**/*.yaml`

## Excluded Patterns
- Virtual environment: `**/venv/**`
- Python cache: `**/__pycache__/**`

## Jira CLI Tool

### Key Features
1. **Issue Management**
   - Create and update issues
   - Add comments
   - Update status and descriptions
   - Track overdue issues

2. **Query Capabilities**
   - Get personal issues
   - Get sprint issues
   - Get related issues
   - Get issue details

### Command Reference

#### Basic Commands
```bash
# Get your issues
./jira_cli.py get-my-issues [--status STATUS] [--priority PRIORITY]

# Get specific issue details
./jira_cli.py get-issue --issue-key ISSUE_KEY

# Get overdue issues
./jira_cli.py get-overdue

# Get sprint issues
./jira_cli.py get-sprint-issues --project PROJECT_KEY
```

#### Issue Creation and Updates
```bash
# Create new issue
./jira_cli.py create-issue \
    --project PROJECT_KEY \
    --summary "Issue summary" \
    --description "Detailed description" \
    --issue-type Task

# Update issue status
./jira_cli.py update-status \
    --issue-key ISSUE_KEY \
    --status "In Progress"

# Add comment to issue
./jira_cli.py add-comment \
    --issue-key ISSUE_KEY \
    --comment "Comment text"

# Update issue description
./jira_cli.py update-description \
    --issue-key ISSUE_KEY \
    --description "New description"
```

### Important Notes
1. **Authentication**
   - Uses credentials from `.env` file
   - Requires valid Jira API token
   - Automatically handles session management

2. **Command Arguments**
   - `--issue-key`: Jira issue key (e.g., PROJ-123)
   - `--project`: Project key (e.g., PROJ)
   - `--status`: Issue status (e.g., "In Progress", "Done")
   - `--priority`: Issue priority level
   - `--sort`: Sort field for results (default: created)
   - `--order`: Sort order (asc/desc, default: asc)

3. **Best Practices**
   - Always provide required arguments for each command
   - Use quotes for values containing spaces
   - Escape special characters in descriptions/comments

### Environment Variables
Required in `.env` file:
```
JIRA_API_TOKEN=
JIRA_EMAIL=
JIRA_SERVER=
```

### Common Patterns

1. **Issue Creation Flow**
```bash
# Create new issue
./jira_cli.py create-issue \
    --project PROJ \
    --summary "New feature request" \
    --description "Detailed feature description" \
    --issue-type Story

# Add additional comment
./jira_cli.py add-comment \
    --issue-key PROJ-123 \
    --comment "Adding implementation details"

# Update status
./jira_cli.py update-status \
    --issue-key PROJ-123 \
    --status "In Progress"
```

2. **Issue Tracking Flow**
```bash
# Check your assigned issues
./jira_cli.py get-my-issues --status "In Progress"

# Get specific issue details
./jira_cli.py get-issue --issue-key PROJ-123

# Check related issues
./jira_cli.py get-related-issues --issue-key PROJ-123
```

### Error Handling
1. **Common Errors**
   - Invalid issue key format
   - Missing required arguments
   - Invalid status transitions
   - Authentication failures

2. **Troubleshooting Steps**
   - Verify environment variables
   - Check issue key format
   - Confirm project permissions
   - Validate status workflow 
