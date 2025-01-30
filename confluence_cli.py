#!/usr/bin/env python3
from confluence_client import ConfluenceTools
import argparse
import json
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Confluence CLI Tool')
    parser.add_argument('command', choices=[
        'get-page',
        'create-page',
        'update-page',
        'delete-page',
        'get-children',
        'search',
        'get-space-content',
        'add-comment',
        'get-comments',
        'list-spaces',
        'attach-file',
        'get-attachments',
        'export-pdf'
    ])
    parser.add_argument('--page-id', help='Page ID for specific page commands')
    parser.add_argument('--space-key', help='Space key for space-specific commands')
    parser.add_argument('--title', help='Title for page creation/update')
    parser.add_argument('--body', help='Content body for page creation/update')
    parser.add_argument('--parent-id', help='Parent page ID for page creation')
    parser.add_argument('--query', help='CQL query for search command')
    parser.add_argument('--comment', help='Comment text for add-comment command')
    parser.add_argument('--file-path', help='File path for attachment or PDF export')
    parser.add_argument('--limit', type=int, default=100, help='Limit for list operations')
    parser.add_argument('--output-format', choices=['json', 'text'], default='text', 
                       help='Output format (default: text)')
    
    args = parser.parse_args()
    confluence = ConfluenceTools()
    
    try:
        if args.command == 'get-page':
            if not args.page_id:
                print("Error: --page-id is required for get-page command")
                return
            result = confluence.get_page(args.page_id)
            
        elif args.command == 'create-page':
            if not all([args.space_key, args.title, args.body]):
                print("Error: --space-key, --title, and --body are required for create-page command")
                return
            result = confluence.create_page(args.space_key, args.title, args.body, args.parent_id)
            
        elif args.command == 'update-page':
            if not all([args.page_id, args.title, args.body]):
                print("Error: --page-id, --title, and --body are required for update-page command")
                return
            result = confluence.update_page(args.page_id, args.title, args.body)
            
        elif args.command == 'delete-page':
            if not args.page_id:
                print("Error: --page-id is required for delete-page command")
                return
            result = confluence.delete_page(args.page_id)
            
        elif args.command == 'get-children':
            if not args.page_id:
                print("Error: --page-id is required for get-children command")
                return
            result = confluence.get_page_children(args.page_id)
            
        elif args.command == 'search':
            if not args.query:
                print("Error: --query is required for search command")
                return
            result = confluence.search_content(args.query)
            
        elif args.command == 'get-space-content':
            if not args.space_key:
                print("Error: --space-key is required for get-space-content command")
                return
            result = confluence.get_space_content(args.space_key, limit=args.limit)
            
        elif args.command == 'add-comment':
            if not all([args.page_id, args.comment]):
                print("Error: --page-id and --comment are required for add-comment command")
                return
            result = confluence.add_comment(args.page_id, args.comment)
            
        elif args.command == 'get-comments':
            if not args.page_id:
                print("Error: --page-id is required for get-comments command")
                return
            result = confluence.get_page_comments(args.page_id)
            
        elif args.command == 'list-spaces':
            result = confluence.get_space_list()
            
        elif args.command == 'attach-file':
            if not all([args.page_id, args.file_path]):
                print("Error: --page-id and --file-path are required for attach-file command")
                return
            result = confluence.attach_file(args.page_id, args.file_path)
            
        elif args.command == 'get-attachments':
            if not args.page_id:
                print("Error: --page-id is required for get-attachments command")
                return
            result = confluence.get_attachments(args.page_id)
            
        elif args.command == 'export-pdf':
            if not all([args.page_id, args.file_path]):
                print("Error: --page-id and --file-path are required for export-pdf command")
                return
            result = confluence.export_page_as_pdf(args.page_id, args.file_path)
        
        # Output handling
        if args.output_format == 'json':
            print(json.dumps(result, indent=2))
        else:
            if isinstance(result, (list, dict)):
                if isinstance(result, dict):
                    for key, value in result.items():
                        print(f"{key}: {value}")
                else:
                    for item in result:
                        print("---")
                        if isinstance(item, dict):
                            for key, value in item.items():
                                print(f"{key}: {value}")
                        else:
                            print(item)
            else:
                print(result)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main() 