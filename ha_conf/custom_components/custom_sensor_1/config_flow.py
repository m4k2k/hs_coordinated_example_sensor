import logging
from typing import Any, Mapping

from homeassistant import config_entries, data_entry_flow

# from .const import DOMAIN

_DOMAIN_ = "custom_sensor_1"

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("Enter: %s", __file__)


@config_entries.HANDLERS.register(_DOMAIN_)
class TestConfigFlow(config_entries.ConfigFlow):

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    # (this is not implemented yet)
    VERSION = 1
    _LOGGER.debug("Enter: TestConfigFlow of %s", __file__)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initiated by the user."""
        _LOGGER.debug("Enter: async_step_user")
        await self.async_set_unique_id("testdev01")
        self._abort_if_unique_id_configured()
        retval: Mapping[str, Any] = {}
        _LOGGER.debug("Create Config Entry")
        return self.async_create_entry(title="test", data=retval)
