"""This module manages serving and downloading data between peers.

The module contains the following classes:
- `ContentService` - Serves files to other peers using a simple HTTP server and downloads files via HTTP GET requests.
"""
import logging
from pathlib import Path
import shutil
import urllib

log = logging.getLogger(__name__)

class ContentService:
    def __init__(self, ip: str, port: int, host_root_dir: str, host_url_prefix: str) -> None:
        """Initialize a ContentServer object.

        Args:
            ip (str): Interface IP address this peer should bind to.
            port (int): Port the HTTP server should listen on.
            host_root_dir (str): Local relative path to serve files from.
            host_url_prefix (str): URL path prefix for hosted files.
        """
        self.host_ip = ip
        self.host_port = port
        self.host_root_dir = host_root_dir
        self.host_url_prefix = host_url_prefix

    def get_encoded_url_path(self):
        url = f'http://{self.host_ip}:{self.host_port}/{self.host_url_prefix}/'
        return urllib.parse.quote(url)

    def put(self, src_file_path: str) -> bool:
        """Copies files from source content directory to the HTTP server's root
        directory to be served to peers that issue HTTP GET requests to download.

        Args:
            src_file_path (str): Path to the source file to be copied to the server root directory.

        Returns:
            bool: True if copy succeeded, False otherwise.
        """
        file_name = Path(src_file_path).name
        dst_file_path = Path(self.host_root_dir).joinpath(Path(file_name))
        result = shutil.copy2(src_file_path, dst_file_path)
        return True if result else False