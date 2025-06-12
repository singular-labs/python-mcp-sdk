"""FastMCP - A more ergonomic interface for MCP servers."""

from importlib.metadata import version

from .server import Context, FastMCP
from .utilities.types import Image
from .redirect_fix import fix_redirects

__version__ = version("mcp")
__all__ = ["FastMCP", "Context", "Image", "fix_redirects"]
