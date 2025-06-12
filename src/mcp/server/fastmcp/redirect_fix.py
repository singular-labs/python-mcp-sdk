"""
Simple wrapper to fix 307 redirects for MCP StreamableHTTP apps.
"""

from typing import Callable, Awaitable


class NoRedirectWrapper:
    """ASGI wrapper that handles both /path and /path/ to avoid 307 redirects."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        # If the path doesn't end with / and the method is POST/GET/DELETE, 
        # add trailing slash to avoid redirect
        if scope["type"] == "http":
            path = scope["path"]
            method = scope["method"]
            
            # For MCP endpoints, ensure trailing slash to avoid redirects
            if method in ["GET", "POST", "DELETE"] and not path.endswith("/"):
                # Modify the scope to add trailing slash
                scope = scope.copy()
                scope["path"] = path + "/"
        
        # Pass to the wrapped app
        await self.app(scope, receive, send)


def fix_redirects(mcp_app):
    """
    Wrap an MCP streamable HTTP app to fix 307 redirects.
    
    Usage:
        mcp_http_app = mcp.streamable_http_app()
        app.mount("/mcp-server", fix_redirects(mcp_http_app))
    """
    return NoRedirectWrapper(mcp_app) 