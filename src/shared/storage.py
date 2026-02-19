"""
Storage Service Module to handle interaction with Azure Blob Storage Container

Uploads the final markdown reports for historical information.
"""
from azure.storage.blob import BlobServiceClient

from src.shared.config import settings
import os


class StorageService:
    def __init__(self):
        # Initialize the connection base on the value from the .env
        self.service_client = BlobServiceClient.from_connection_string(
            settings.azure_blob_storage_connection_string
        )

        self.container_name = "reports"
        # Verify container exists
        self._ensure_container_exists()

    def _ensure_container_exists(self):
        """
        Create the reports container if it doesn't exist
        """
        try:
            container_client = self.service_client.get_container_client(
                self.container_name)
            if not container_client.exists():
                container_client.create_container()
        except Exception as e:
            print(f"Error checking container: {e}")

    def upload_file(self, file_path: str, destination_name: str) -> str:
        """
        Uploads a local report file to the Azure Blob Container

        Args:
            file path and filename (e.g. report.md)

            destination_name: name of the file 
        """
        try:
            blob_client = self.service_client.get_blob_client(
                container=self.container_name,
                blob=destination_name,

            )
            # Read in the local version of the report and upload
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)

            return f"https://{self.service_client.account_name}.blob.core.windows.net/{self.container_name}/{destination_name}"

        except Exception as e:
            return f"Error uploading report to Azure Blob Storage Container: {str(e)}"
