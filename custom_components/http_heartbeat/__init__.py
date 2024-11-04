"""The HTTP Heartbeat integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval

from .const import (
    DOMAIN,
    CONF_NAME,
    CONF_TARGET_URL,
    DEFAULT_SCAN_INTERVAL,
)
from .heartbeat import HeartbeatHandler

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HTTP Heartbeat from a config entry."""
    name = entry.data[CONF_NAME]
    target_url = entry.data[CONF_TARGET_URL]
    
    session = async_get_clientsession(hass)
    handler = HeartbeatHandler(session)

    async def async_send_heartbeat(now=None) -> None:
        """Send periodic heartbeat."""
        await handler.send_heartbeat(target_url, name)

    # Schedule periodic heartbeat
    entry.async_on_unload(
        async_track_time_interval(
            hass,
            async_send_heartbeat,
            timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
    )

    # Store handler for cleanup
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = handler

    # Send initial heartbeat
    await async_send_heartbeat()

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return True