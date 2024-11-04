"""Config flow for HTTP Heartbeat integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    CONF_NAME,
    CONF_TARGET_URL,
    CONF_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
    MAX_SCAN_INTERVAL,
    ERROR_CANNOT_CONNECT,
    ERROR_INVALID_URL,
    ERROR_INVALID_INTERVAL,
)
from .heartbeat import HeartbeatHandler

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Required(CONF_TARGET_URL): str,
        vol.Required(CONF_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int),
            vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL)
        ),
    }
)

class HttpHeartbeatConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HTTP Heartbeat."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate URL format
            if not user_input[CONF_TARGET_URL].startswith(("http://", "https://")):
                errors[CONF_TARGET_URL] = ERROR_INVALID_URL
            elif not MIN_SCAN_INTERVAL <= user_input[CONF_INTERVAL] <= MAX_SCAN_INTERVAL:
                errors[CONF_INTERVAL] = ERROR_INVALID_INTERVAL
            else:
                # Test connection
                session = async_get_clientsession(self.hass)
                handler = HeartbeatHandler(session)
                success, error = await handler.send_heartbeat(
                    user_input[CONF_TARGET_URL],
                    user_input[CONF_NAME]
                )

                if success:
                    return self.async_create_entry(
                        title=user_input[CONF_NAME],
                        data=user_input,
                    )
                else:
                    errors[CONF_TARGET_URL] = ERROR_CANNOT_CONNECT

        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
        )