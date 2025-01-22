from jira import JIRA
from config import JIRA_SERVER, JIRA_EMAIL, JIRA_API_TOKEN
from datetime import datetime, timedelta

class JiraTools:
    def __init__(self):
        self.client = self._initialize_client()

    def _initialize_client(self):
        """Initialize Jira client with credentials from config."""
        return JIRA(
            server=JIRA_SERVER,
            basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
        )

    def get_issue(self, issue_key):
        """Get a Jira issue by its key."""
        return self.client.issue(issue_key)

    def create_issue(self, project_key, summary, description, issue_type='Task'):
        """Create a new Jira issue."""
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        return self.client.create_issue(fields=issue_dict)

    def search_issues(self, jql_query):
        """Search for issues using JQL."""
        return self.client.search_issues(jql_query)

    def add_comment(self, issue_key, comment):
        """Add a comment to an issue."""
        issue = self.client.issue(issue_key)
        return self.client.add_comment(issue, comment)

    def get_project(self, project_key):
        """Get project information."""
        return self.client.project(project_key)

    def get_all_projects(self):
        """Get all accessible projects."""
        return self.client.projects()

    def get_my_issues(self, status=None, priority=None):
        """Get all issues assigned to the authenticated user with optional filters."""
        jql = f"assignee = currentUser()"
        if status:
            jql += f" AND status = '{status}'"
        if priority:
            jql += f" AND priority = '{priority}'"
        return self.search_issues(jql)

    def get_issue_details(self, issue_key):
        """Get comprehensive details about an issue including acceptance criteria and requirements."""
        issue = self.get_issue(issue_key)
        details = {
            'summary': issue.fields.summary,
            'description': issue.fields.description,
            'status': issue.fields.status.name,
            'priority': issue.fields.priority.name if hasattr(issue.fields, 'priority') else None,
            'assignee': issue.fields.assignee.displayName if issue.fields.assignee else None,
            'created': issue.fields.created,
            'updated': issue.fields.updated,
            'comments': [{'author': c.author.displayName, 'body': c.body} for c in issue.fields.comment.comments],
            'acceptance_criteria': getattr(issue.fields, 'customfield_10000', None),  # Adjust field ID as needed
            'components': [c.name for c in issue.fields.components],
            'labels': issue.fields.labels,
            'linked_issues': [{'key': link.outwardIssue.key, 'type': link.type.name} 
                            for link in issue.fields.issuelinks if hasattr(link, 'outwardIssue')]
        }
        return details

    def get_overdue_issues(self):
        """Get all overdue issues assigned to the current user."""
        jql = "assignee = currentUser() AND duedate < now() AND status not in (Closed, Done, Resolved)"
        return self.search_issues(jql)

    def get_related_issues(self, issue_key):
        """Get all issues related to the specified issue."""
        issue = self.get_issue(issue_key)
        related = []
        for link in issue.fields.issuelinks:
            if hasattr(link, 'outwardIssue'):
                related.append(link.outwardIssue)
            elif hasattr(link, 'inwardIssue'):
                related.append(link.inwardIssue)
        return related

    def update_issue_status(self, issue_key, status_name):
        """Update the status of an issue."""
        issue = self.client.issue(issue_key)
        transitions = self.client.transitions(issue)
        
        # Find the transition that matches our target status
        for t in transitions:
            if t['name'].lower() == status_name.lower():
                self.client.transition_issue(issue, t['id'])
                return True
        return False

    def get_issue_history(self, issue_key):
        """Get the complete history of an issue."""
        issue = self.get_issue(issue_key)
        changelog = self.client.issue(issue_key, expand='changelog')
        history = []
        for history_item in changelog.changelog.histories:
            for item in history_item.items:
                history.append({
                    'date': history_item.created,
                    'author': history_item.author.displayName,
                    'field': item.field,
                    'from': item.fromString,
                    'to': item.toString
                })
        return history

    def get_sprint_issues(self, project_key):
        """Get all issues in the current sprint for a project."""
        jql = f"project = {project_key} AND sprint in openSprints()"
        return self.search_issues(jql)

    def get_issue_metrics(self, issue_key):
        """Get time tracking and other metrics for an issue."""
        issue = self.get_issue(issue_key)
        metrics = {
            'time_estimate': issue.fields.timeestimate,
            'time_spent': issue.fields.timespent,
            'created_date': issue.fields.created,
            'updated_date': issue.fields.updated,
            'resolution_date': issue.fields.resolutiondate if hasattr(issue.fields, 'resolutiondate') else None,
        }
        return metrics

    def update_issue_description(self, issue_key, description):
        """Update the description of an issue."""
        # Replace escaped newlines with actual newlines
        description = description.replace('\\n', '\n')
        issue = self.client.issue(issue_key)
        issue.update(fields={"description": description})
        return True 