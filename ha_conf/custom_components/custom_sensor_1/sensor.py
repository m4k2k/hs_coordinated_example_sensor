"""Example integration using DataUpdateCoordinator."""


"""
What is handled - and what is not:

NOT:
- delete orphaned entities (Currently no orphaned or old/outdated entities are detected and removed)

HANDLED:



"""

import logging
from datetime import timedelta
import async_timeout
from enum import Enum
from homeassistant.const import TEMP_CELSIUS
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import (callback, HomeAssistant)
from homeassistant.exceptions import (ConfigEntryAuthFailed, PlatformNotReady)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (CoordinatorEntity, DataUpdateCoordinator, UpdateFailed)
DOMAIN = "custom_sensor_1"

_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("Starting %s", __file__)

#from .const import DOMAIN

_managed_entity_ids: list[str] = []

#raise "last position"
# TODO: Find the issue why only dd is updated after a few tries (ee is LOST)
# Hint: maybe the for loop or the coord.data return
# Hint: be aware the dd is the last added entry


async def async_setup_platform(hass: HomeAssistant, config, async_add_entities, discovery_info=None) -> None:
    """Set up platform."""
    _LOGGER.debug("async_setup_platform of sensor.py")

    _managed_entity_ids.append("ee")
    _managed_entity_ids.append("dd")

    _LOGGER.debug("managed entity ids: %s", _managed_entity_ids)

    my_api = MyApiClient(username="", password="")
    coordinator = MyCoordinator(hass, my_api)

    await coordinator.async_refresh()
    if not coordinator.last_update_success:
        raise PlatformNotReady

    async_add_entities(CoordinatedExampleSensor(
        _coordinator=coordinator, _unique_id=_uid) for _uid in _managed_entity_ids)

    _LOGGER.debug("current coordinator data:")
    _LOGGER.debug(coordinator.data)


class MyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""
    _my_api: MyApiClient
    _LOGGER.debug("Class MyCoordinator")
    #data: dict

    def __init__(self, hass: HomeAssistant, my_api: MyApiClient):
        """Initialize my coordinator."""
        _LOGGER.debug("__init__ of MyCoordinator")
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=DOMAIN,
            # Polling interval. Will only be polled if there are subscribers.
            # default is usually 30 seconds
            update_interval=timedelta(seconds=40),
        )
        self._my_api = my_api
        _LOGGER.debug("managed entity ids: %s", _managed_entity_ids)

    async def _async_update_data(self) -> dict[DummyClass]:
        """Fetch data from API endpoint.
        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        _LOGGER.debug("_async_update_data of MyCoordinator")
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                # return await self.my_api.get_dummy_data()
                _LOGGER.debug("start self.my_api.get_dummy_data()")
                # call api to get the data object
                # put the dataobject into the HA-store
                coordinator_data: dict[DummyClass] = {}
                for __uid in _managed_entity_ids:
                    _LOGGER.debug("calling api for id: %s", __uid)
                    # here you could also do an if id = "abc" then talk to api-a else api-b
                    dummy_data: DummyClass = self._my_api.get_dummy_data()
                    coordinator_data[__uid] = dummy_data
                _LOGGER.debug("returning cordinator_data:")
                _LOGGER.debug(coordinator_data)
                return coordinator_data

        except ConfigEntryAuthFailed as err:
            # Raising ConfigEntryAuthFailed will cancel future updates
            # and start a config flow with SOURCE_REAUTH (async_step_reauth)
            raise ConfigEntryAuthFailed from err
        except UpdateFailed as err:
            raise UpdateFailed(f"Error communicating with API: {err}")


class CoordinatedExampleSensor(CoordinatorEntity, SensorEntity):
    """An entity using CoordinatorEntity.
    The CoordinatorEntity class provides:
        should_poll
        async_update
        async_added_to_hass
        available
    """
    __coordinator: CoordinatorEntity

    _LOGGER.debug("""Class of CoordinatedExampleSensor""")

    _attr_name = "Example Temperature Sensor Dummy"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    # declare keys for easier use
    _attr_system_state = "system_state"
    _attr_id = "id"
    # use the keys and assign an empty value
    # its content will be visible in HA
    extra_attributes: dict = {
        _attr_system_state: "",
        _attr_id: ""
    }

    def get_sensor_value(self) -> int:
        """Retrieve the current sensor value from the coordinator
        :return: The current value
        :rtype: int
        """
        _LOGGER.debug("_get_data of CoordinatedExampleSensor")
        _LOGGER.debug("getting sensor value for id: %s",
                      self.extra_attributes[self._attr_id])
        entity_id = self.extra_attributes[self._attr_id]
        __dummy_data: DummyClass = self.__coordinator.data[entity_id]
        value = __dummy_data.dummyvalue
        value = self.__coordinator.data[self.extra_attributes[self._attr_id]].dummyvalue
        _LOGGER.debug("current  self.__coordinator data:")
        _LOGGER.debug(self.__coordinator)
        _LOGGER.debug("returning %i", value)
        return value

    def get_sensor_system_state(self) -> str:
        _LOGGER.debug("_get_sensor_system_state of CoordinatedExampleSensor")
        _LOGGER.debug("getting sensor system state for id: %s",
                      self.extra_attributes[self._attr_id])
        # value = "fixed-offline"
        value = self.__coordinator.data[self.extra_attributes[self._attr_id]].dummystate
        _LOGGER.debug("returning %s", value)
        return value

    def update_all_data(self) -> None:
        # not rquired, but recommended updates all properties and values of the entity(sensor)
        _LOGGER.debug("update_all_data of CoordinatedExampleSensor")
        _LOGGER.debug("current  self.__coordinator data:")
        _LOGGER.debug(self.__coordinator)
        self._attr_native_value = self.get_sensor_value()
        self.extra_attributes[self._attr_system_state] = self.get_sensor_system_state(
        )

    @property
    def extra_state_attributes(self) -> dict:
        """Return entity specific state attributes."""
        # required to store your own attributes, like _attr_testprop
        # should only be done the state is of the own attributes are not changed frequently
        # else you should use another sensor
        _LOGGER.debug("extra_state_attributes of CoordinatedExampleSensor")
        return self.extra_attributes

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("_handle_coordinator_update of CoordinatedExampleSensor")
        # gets triggered, triggers the pull of the data from the coordinator
        # gets triggered after the coordinator has finished getting updates
        _LOGGER.debug("current  self.__coordinator data:")
        _LOGGER.debug(self.__coordinator)
        self.update_all_data()
        # self.async_write_ha_state()
        return super()._handle_coordinator_update()

    def __init__(self, _coordinator: CoordinatorEntity, _unique_id: str):
        """Pass coordinator to CoordinatorEntity."""
        _LOGGER.debug("__init__ of CoordinatedExampleSensor")
        _LOGGER.debug("current _coordinator data:")
        _LOGGER.debug(_coordinator)
        super().__init__(_coordinator)
        self.__coordinator = _coordinator
        _LOGGER.debug("current  self.__coordinator data:")
        _LOGGER.debug(self.__coordinator)
        self._attr_name = self._attr_name.replace("Dummy", _unique_id)
        self.extra_attributes[self._attr_id] = _unique_id
        self.update_all_data()
