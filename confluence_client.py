from atlassian import Confluence
from config import (
    CONFLUENCE_URL,
    CONFLUENCE_USERNAME,
    CONFLUENCE_API_TOKEN,
    CONFLUENCE_PERSONAL_SPACE
)
from typing import Optional, Dict, List, Union
import json

class ConfluenceTools:
    def __init__(self):
        self.client = self._initialize_client()
        self.personal_space_key = self._get_personal_space_key()

    def _initialize_client(self) -> Confluence:
        """Initialize Confluence client with credentials from config."""
        return Confluence(
            url=CONFLUENCE_URL,
            username=CONFLUENCE_USERNAME,
            password=CONFLUENCE_API_TOKEN,
            cloud=True  # Set to False if using Confluence Server
        )

    def _get_personal_space_key(self) -> str:
        """Get the personal space key for the authenticated user."""
        if not CONFLUENCE_PERSONAL_SPACE:
            raise ValueError("CONFLUENCE_PERSONAL_SPACE environment variable is not set")
        return CONFLUENCE_PERSONAL_SPACE

    def get_page(self, page_id: str) -> Dict:
        """Get a Confluence page by its ID."""
        return self.client.get_page_by_id(page_id, expand='body.storage,version,space')

    def create_page(self, space_key: str, title: str, body: str, parent_id: Optional[str] = None) -> Dict:
        """Create a new Confluence page in the user's personal space.
        
        Args:
            space_key: The key of the space where the page will be created (must be user's personal space)
            title: The title of the page
            body: The content of the page in storage format (HTML)
            parent_id: Optional ID of the parent page
        
        Returns:
            Dict containing the created page information
        
        Raises:
            ValueError: If attempting to create a page outside the user's personal space
        """
        if space_key != self.personal_space_key:
            raise ValueError(f"Pages can only be created in your personal space ({self.personal_space_key})")
            
        return self.client.create_page(
            space=space_key,
            title=title,
            body=body,
            parent_id=parent_id,
            type='page'
        )

    def update_page(self, page_id: str, title: str, body: str) -> Dict:
        """Update an existing Confluence page.
        
        Args:
            page_id: The ID of the page to update
            title: The new title of the page
            body: The new content of the page in storage format (HTML)
        
        Returns:
            Dict containing the updated page information
        """
        page = self.get_page(page_id)
        return self.client.update_page(
            page_id=page_id,
            title=title,
            body=body,
            version_number=page['version']['number'] + 1
        )

    def delete_page(self, page_id: str) -> bool:
        """Delete a Confluence page.
        
        Args:
            page_id: The ID of the page to delete
        
        Returns:
            bool indicating success
        """
        return self.client.remove_page(page_id)

    def get_page_children(self, page_id: str) -> List[Dict]:
        """Get all child pages of a given page.
        
        Args:
            page_id: The ID of the parent page
        
        Returns:
            List of child page information
        """
        return self.client.get_page_child_by_type(page_id)

    def search_content(self, cql_query: str) -> List[Dict]:
        """Search for content using CQL (Confluence Query Language).
        
        Args:
            cql_query: The CQL query string
        
        Returns:
            List of matching content items
        """
        return self.client.cql(cql_query)

    def get_space_content(self, space_key: str, content_type: str = 'page', limit: int = 100) -> List[Dict]:
        """Get all content of a specific type in a space.
        
        Args:
            space_key: The key of the space to get content from
            content_type: The type of content to get (page, blogpost, etc.)
            limit: Maximum number of items to return
        
        Returns:
            List of content items
        """
        return self.client.get_all_pages_from_space(space_key, start=0, limit=limit)

    def add_comment(self, page_id: str, comment: str) -> Dict:
        """Add a comment to a page.
        
        Args:
            page_id: The ID of the page to comment on
            comment: The comment text
        
        Returns:
            Dict containing the created comment information
        """
        return self.client.add_comment(page_id, comment)

    def get_page_comments(self, page_id: str) -> List[Dict]:
        """Get all comments on a page.
        
        Args:
            page_id: The ID of the page
        
        Returns:
            List of comments
        """
        return self.client.get_page_comments(page_id)

    def get_space_list(self) -> List[Dict]:
        """Get list of all accessible spaces.
        
        Returns:
            List of space information
        """
        return self.client.get_all_spaces()

    def attach_file(self, page_id: str, file_path: str) -> Dict:
        """Attach a file to a page.
        
        Args:
            page_id: The ID of the page to attach the file to
            file_path: Path to the file to attach
        
        Returns:
            Dict containing the attachment information
        """
        return self.client.attach_file(file_path, page_id)

    def get_attachments(self, page_id: str) -> List[Dict]:
        """Get all attachments on a page.
        
        Args:
            page_id: The ID of the page
        
        Returns:
            List of attachment information
        """
        return self.client.get_attachments_from_content(page_id)

    def export_page_as_pdf(self, page_id: str, output_path: str) -> bool:
        """Export a page as PDF.
        
        Args:
            page_id: The ID of the page to export
            output_path: Path where to save the PDF file
        
        Returns:
            bool indicating success
        """
        try:
            pdf_data = self.client.export_page(page_id)
            with open(output_path, 'wb') as f:
                f.write(pdf_data)
            return True
        except Exception as e:
            print(f"Failed to export page as PDF: {str(e)}")
            return False 