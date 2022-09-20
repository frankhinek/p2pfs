"""This module implementations the Application layer of a 3-layer design that includes UI and Network layers.

The Application layer provides a UI layer client with services to search for files, publish files to share, and
initiate file downloads.  It manages the DHT and ContentService components that make up the Network layer.

The module contains the following classes:
- `QueryService` - Queries the DHT for files by file name or metadata tags.
- `IndexingService` - Extract metadata from files and inserts mappings from metadata tags to content IDs into the DHT.
"""