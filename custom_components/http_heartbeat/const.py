"""Constants for the HTTP Heartbeat integration."""
from typing import Final

DOMAIN: Final = "http_heartbeat"

CONF_NAME: Final = "name"
CONF_TARGET_URL: Final = "target_url"
CONF_INTERVAL: Final = "interval"

DEFAULT_SCAN_INTERVAL: Final = 60  # seconds
DEFAULT_TIMEOUT: Final = 10  # seconds
MIN_SCAN_INTERVAL: Final = 10  # minimum 10 seconds
MAX_SCAN_INTERVAL: Final = 3600  # maximum 1 hour

# Error messages
ERROR_CANNOT_CONNECT: Final = "cannot_connect"
ERROR_INVALID_URL: Final = "invalid_url"
ERROR_INVALID_AUTH: Final = "invalid_auth"
ERROR_INVALID_INTERVAL: Final = "invalid_interval"