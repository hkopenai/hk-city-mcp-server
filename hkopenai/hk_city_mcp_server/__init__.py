"""Hong Kong city MCP Server package."""

from .server import main
from .tool_ambulance_service import get_ambulance_indicators

__version__ = "0.1.0"
__all__ = ["main", "get_ambulance_indicators"]
