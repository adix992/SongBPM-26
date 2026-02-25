"""Adds config flow for SongBPM."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.const import CONF_API_KEY

from .const import DOMAIN, NAME

_LOGGER = logging.getLogger(__name__)

class ComponentOptionsHandler(config_entries.OptionsFlow):
    """Handle options for the integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Pre-fill the menu with the currently saved data
        current_api = self.config_entry.options.get(
            CONF_API_KEY, self.config_entry.data.get(CONF_API_KEY, "")
        )
        current_player = self.config_entry.options.get(
            "media_player", self.config_entry.data.get("media_player", "")
        )

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY, default=current_api): str,
            vol.Required("media_player", default=current_player): selector.selector(
                {"entity": {"domain": "media_player"}}
            )
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
        )

class ComponentFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for SongBPM."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title=NAME, data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Required("media_player"): selector.selector(
                {"entity": {"domain": "media_player"}}
            )
        })

        return self.async_show_form(
            step_id="user", 
            data_schema=data_schema, 
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ComponentOptionsHandler(config_entry)
