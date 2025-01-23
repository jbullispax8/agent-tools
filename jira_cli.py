#!/usr/bin/env python3
from jira_client import JiraTools
import argparse
import json
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Jira CLI Tool')
    parser.add_argument('command', choices=[
        'get-my-issues',
        'get-issue',
        'get-overdue',
        'get-sprint-issues',
        'get-related-issues',
        'update-status',
        'create-issue',
        'update-description',
        'add-comment'
    ])
    parser.add_argument('--status', help='Filter by status or new status for update')
    parser.add_argument('--priority', help='Filter by priority')
    parser.add_argument('--issue-key', help='Issue key for specific issue commands')
    parser.add_argument('--project', help='Project key for project-specific commands')
    parser.add_argument('--sort', help='Sort field', default='created')
    parser.add_argument('--order', help='Sort order (asc/desc)', default='asc')
    parser.add_argument('--summary', help='Summary for new issue')
    parser.add_argument('--description', help='Description for new issue')
    parser.add_argument('--issue-type', help='Issue type (default: Task)', default='Task')
    parser.add_argument('--comment', help='Comment text for add-comment command. Use \\n for newlines.')
    
    args = parser.parse_args()
    jira = JiraTools()
    
    try:
        if args.command == 'add-comment':
            if not args.issue_key or not args.comment:
                print("Error: --issue-key and --comment are required for add-comment command")
                return
            # Process the comment text to handle newlines
            comment_text = args.comment.encode().decode('unicode_escape')
            comment = jira.add_comment(args.issue_key, comment_text)
            if comment:
                print(f"Successfully added comment to {args.issue_key}")
                print("Comment:", args.comment)
            else:
                print(f"Failed to add comment to {args.issue_key}")
                
        elif args.command == 'update-description':
            if not args.issue_key or not args.description:
                print("Error: --issue-key and --description are required for update-description command")
                return
            if jira.update_issue_description(args.issue_key, args.description):
                print(f"Successfully updated description for {args.issue_key}")
                details = jira.get_issue_details(args.issue_key)
                print(json.dumps(details, indent=2))
            else:
                print(f"Failed to update description for {args.issue_key}")

        elif args.command == 'create-issue':
            if not args.project or not args.summary or not args.description:
                print("Error: --project, --summary, and --description are required for create-issue command")
                return
            issue = jira.create_issue(
                project_key=args.project,
                summary=args.summary,
                description=args.description,
                issue_type=args.issue_type
            )
            if issue:
                print(f"Successfully created issue: {issue.key}")
            else:
                print("Failed to create issue")
        
        elif args.command == 'update-status':
            if not args.issue_key or not args.status:
                print("Error: --issue-key and --status are required for update-status command")
                return
            if jira.update_issue_status(args.issue_key, args.status):
                print(f"Successfully updated {args.issue_key} to status: {args.status}")
            else:
                print(f"Failed to update status. Available transitions may not include '{args.status}'")
        
        elif args.command == 'get-my-issues':
            # Get issues and filter for non-closed statuses
            issues = jira.get_my_issues(status=args.status, priority=args.priority)
            open_issues = [i for i in issues if i.fields.status.name.lower() not in ['done', 'completed', 'closed', 'resolved']]
            
            # Sort issues by creation date
            sorted_issues = sorted(open_issues, key=lambda x: datetime.strptime(x.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z'))
            
            for issue in sorted_issues:
                print(f"{issue.key}: {issue.fields.summary}")
                print(f"Status: {issue.fields.status.name}")
                print(f"Created: {issue.fields.created}")
                print("---")
        
        elif args.command == 'get-issue':
            if not args.issue_key:
                print("Error: --issue-key is required for get-issue command")
                return
            details = jira.get_issue_details(args.issue_key)
            print(json.dumps(details, indent=2))
        
        elif args.command == 'get-overdue':
            issues = jira.get_overdue_issues()
            for issue in issues:
                print(f"{issue.key}: {issue.fields.summary} (Due: {issue.fields.duedate})")
        
        elif args.command == 'get-sprint-issues':
            if not args.project:
                print("Error: --project is required for get-sprint-issues command")
                return
            issues = jira.get_sprint_issues(args.project)
            for issue in issues:
                print(f"{issue.key}: {issue.fields.summary}")
        
        elif args.command == 'get-related-issues':
            if not args.issue_key:
                print("Error: --issue-key is required for get-related-issues command")
                return
            issues = jira.get_related_issues(args.issue_key)
            for issue in issues:
                print(f"{issue.key}: {issue.fields.summary}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main() 