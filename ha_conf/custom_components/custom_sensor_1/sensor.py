import logging
from collections.abc import MutableMapping
from datetime import timedelta
from typing import Any
import async_timeout
from custom_components.custom_sensor_1.my_api.client import (
    DummyClass, MyApiClient)
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator, UpdateFailed)
from homeassistant.components.sensor import (
    SensorDeviceClass, SensorEntity, SensorStateClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers import device_registry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

"""Example integration using DataUpdateCoordinator.


"""
# domain where all information of the sensor is found
_DOMAIN_ = "custom_sensor_1"
# get a logger object
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("Starting %s", __file__)

# holds ids for entities (not best solution)
_managed_entity_ids: list[str] = []


class MyCoordinator(DataUpdateCoordinator[Any]):
    # Initialize API Client
    _my_api: MyApiClient
    # Get logger with suffix
    _LOGLCL = logging.getLogger(__name__ + ".MyCoordinator")
    _LOGLCL.debug("Class MyCoordinator of %s", __file__)

    def __init__(self, hass: HomeAssistant, my_api: MyApiClient):
        """Initialize MyCoordinator Class"""
        self._LOGLCL.debug("__init__ of MyCoordinator Class")
        DataUpdateCoordinator.__init__(
            self=self,
            hass=hass,
            logger=_LOGGER,
            # Name of the data. For logging purposes.
            name=_DOMAIN_,
            update_method=self._async_update_data,
            # Polling interval. Will only be polled if there are subscribers.
            # default is usually 30 seconds
            update_interval=timedelta(seconds=40)
        )
        self._my_api = my_api
        self._LOGLCL.debug("managed entity ids: %s", _managed_entity_ids)

    async def _async_update_data(self) -> dict[Any, Any]:
        """Fetch data from API endpoint.
        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        self._LOGLCL.debug("_async_update_data of MyCoordinator")
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                self._LOGLCL.debug("start self.my_api.get_dummy_data()")
                # call api to get the data object
                # put the dataobject into the HA-store
                coordinator_data: dict[Any, Any] = {}
                for __uid in _managed_entity_ids:
                    self._LOGLCL.debug("calling api for id: %s", __uid)
                    # here you could also do an if id = "abc" then talk to api-a else api-b
                    dummy_data: DummyClass = self._my_api.get_dummy_data()
                    coordinator_data[__uid] = dummy_data
                self._LOGLCL.debug("returning cordinator_data:")
                self._LOGLCL.debug(coordinator_data)
                return coordinator_data
        except UpdateFailed as err:
            raise UpdateFailed(f"Error communicating with API: {err}")


class CoordinatedExampleSensor(CoordinatorEntity[Any], SensorEntity):
    """An entity using CoordinatorEntity.
    The CoordinatorEntity class provides:
        should_poll
        async_update
        async_added_to_hass
        available
    """
    _coord: MyCoordinator

    _LOGLCL = logging.getLogger(__name__ + ".CoordinatedExampleSensor")
    _LOGLCL.debug("Class of CoordinatedExampleSensor of %s", __file__)

    _attr_name = "Example Temperature Sensor Dummy"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def get_sensor_value(self) -> int:
        """Retrieve the current sensor value from the coordinator
        :return: The current value
        :rtype: int
        """
        # get custom id
        entity_idx = self.extra_state_attributes["idx"]
        self._LOGLCL.info(
            "get_sensor_value for CoordinatedExampleSensor from coordinator_data for id: %s", entity_idx)
        retval: int = self._coord.data[entity_idx].dummyvalue
        self._LOGLCL.info("returning %i", retval)
        return retval

    def get_sensor_system_state(self) -> str:
        # get custom id
        entity_idx = self.extra_state_attributes["idx"]
        self._LOGLCL.info(
            "get_sensor_system_state for CoordinatedExampleSensor from coordinator_data for id: %s", entity_idx)
        retval: str = self._coord.data[entity_idx].dummystate
        self._LOGLCL.info("returning %s", retval)
        return retval

    def update_all_data(self) -> None:
        self._LOGLCL.info("update_all_data of CoordinatedExampleSensor for id: %s",
                          self.extra_state_attributes["idx"])
        self._attr_native_value = self.get_sensor_value()
        self.extra_state_attributes["system_state"] = self.get_sensor_system_state(
        )

    @property
    def extra_state_attributes(self) -> MutableMapping[str, Any]:
        """Return extra state attributes."""
        return self._attr_extra_state_attributes

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update by the coordinator."""
        self._LOGLCL.debug(
            "_handle_coordinator_update of CoordinatedExampleSensor")
        self._LOGLCL.debug("enter for id: %s of entity %s",
                           self.extra_state_attributes["idx"], self.entity_id)
        # gets triggered, triggers the pull of the data from the coordinator
        # gets triggered after the coordinator has finished getting updates
        self.update_all_data()
        CoordinatorEntity[Any]._handle_coordinator_update(self)

    # Add device info, creates device if not exists.
    # Here we add more information which was not yet added to the device.
    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        self._LOGLCL.debug("ENTER: device_info")
        _device_id: str = "testdev01"  # test device id
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (_DOMAIN_, _device_id)
            },
            name="test dev xy",
            manufacturer="test manufacturer",
            model="test model",
            sw_version="0.01",
        )
    # All available device properties
    # configuration_url: str | None
    # connections: set[tuple[str, str]]     <<- required
    # default_manufacturer: str             <<- required
    # default_model: str                    <<- required
    # default_name: str                     <<- required
    # entry_type: DeviceEntryType | None
    # identifiers: set[tuple[str, str]]     <<- required
    # manufacturer: str | None
    # model: str | None
    # name: str | None
    # suggested_area: str | None
    # sw_version: str | None
    # hw_version: str | None
    # via_device: tuple[str, str]           <<- required

    def __init__(self, coord: MyCoordinator, _unique_id: str) -> None:
        # Pass self, coordinator and unique_id to CoordinatorEntity
        # pyright: reportUnknownMemberType=false
        CoordinatorEntity.__init__(self, coord)
        # Pass self to SensorEntity
        SensorEntity.__init__(self)

        self._LOGLCL.debug(
            "__init__ of CoordinatedExampleSensor %s", _unique_id)
        self._LOGLCL.debug("current _coordinator data:")
        self._LOGLCL.debug(coord.data)
        self._coord = coord
        if (self._attr_name is not None):
            dum: str = self._attr_name
        else:
            dum = ""
        self._attr_name = str(dum.replace("Dummy", _unique_id))
        self._attr_extra_state_attributes: MutableMapping[str, Any] = dict(
            {"idx": "", "system_state": ""})
        self._attr_extra_state_attributes["idx"] = _unique_id
        self._attr_unique_id = f"{_DOMAIN_}.{_unique_id}"
        self._LOGLCL.info("self.unique_id: %a", self.unique_id)
        self.update_all_data()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Main Setup File"""
    _LOGGER.debug("ENTER async_setup_entry %s", __file__)
    dr = device_registry.async_get(hass)
    _LOGGER.debug("create new device")

    # make sure device is created, even if no entity is present (usecase: show metadata like firmware version, etc.)
    # device doesnt need to be captured here, just create as many devices as required (e.g. in a loop)
    _device_id: str = "testdev01"  # test device id
    # create test device
    dev1: device_registry.DeviceEntry = dr.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(_DOMAIN_, _device_id)},
        name="my test device",
        sw_version="0.02",
    )

    _LOGGER.debug("my new device:")
    _LOGGER.debug(dev1)

    _LOGGER.debug("Set up platform Ex - async_setup_platform")

    # define test sensor ids
    _managed_entity_ids.append("test1")
    _managed_entity_ids.append("dest1")
    _managed_entity_ids.append("best1")

    # initialize api client
    my_api = MyApiClient(username="", password="")
    # initialize coordinator
    xcoordinator = MyCoordinator(hass, my_api)

    await xcoordinator.async_refresh()
    if not xcoordinator.last_update_success:
        raise PlatformNotReady

    _LOGGER.info("managed entity ids: %s", _managed_entity_ids)

    # add sensor entities to HA
    async_add_entities(CoordinatedExampleSensor(
        coord=xcoordinator, _unique_id=_uid) for _uid in _managed_entity_ids)

    _LOGGER.debug("EXIT async_setup_entry")
