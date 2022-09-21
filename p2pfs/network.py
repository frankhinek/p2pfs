"""This module manages serving and downloading data between peers.

The module contains the following classes:
- `ContentService` - Serves files to other peers using a simple HTTP server and downloads files via HTTP GET requests.
"""
import logging
from pathlib import Path
import shutil
import urllib
from aiohttp import web

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

        self.http_app = None
        self.http_site = None
        self.configure_server()

    def configure_server(self) -> None:
        """Instantiate AIOHTTP web application and configure routes.
        """
        self.http_app = web.Application()
        self.http_app.router.add_get('/health', self.health)
        self.http_app.router.add_static(f'/{self.host_url_prefix}', self.host_root_dir)

    def decode_url(self, encoded_url: str) -> str:
        """Utility function uses URLLIB to decode encoded URL.

        Args:
            encoded_url (str): Encoded URL.

        Returns:
            str: Decode URL.
        """
        return urllib.parse.unquote(encoded_url)

    async def delete(self, file_name: str) -> None:
        """Utility function to delete files that are being hosted.

        Args:
            file_name (str): File name to be deleted.
        """
        Path(self.host_root_dir).joinpath(Path(file_name).name).unlink()

    def get_encoded_url_path(self) -> str:
        """Returns the base URL path for files hosted by this peer.

        Returns:
            str: URL encoded base path.
        """
        url = f'http://{self.host_ip}:{self.host_port}/{self.host_url_prefix}/'
        return urllib.parse.quote(url)

    async def health(self, request: dict) -> web.Response:
        """Health endpoint to check if the HTTP service is running.

        Args:
            request (dict): HTTP request object.

        Returns:
            web.Response: HTTP response object.
        """
        return web.json_response({"status":"OK"})

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

    async def start_serving(self) -> None:
        """Start AIOHTTP server and listen for requests.
        """
        runner = web.AppRunner(self.http_app)
        await runner.setup()
        self.http_site = web.TCPSite(runner, self.host_ip, self.host_port)
        await self.http_site.start()

    async def stop_serving(self) -> None:
        """Stop AIOHTTP server.
        """
        await self.http_site.stop()