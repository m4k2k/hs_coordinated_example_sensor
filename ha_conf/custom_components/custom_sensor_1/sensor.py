import logging
from collections.abc import MutableMapping
from datetime import timedelta
from typing import Any

import async_timeout
from custom_components.custom_sensor_1.my_api.client import (DummyClass,
                                                             MyApiClient)
from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity,
                                             SensorStateClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant, callback  # , State
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.exceptions import ConfigEntryAuthFailed, PlatformNotReady
from homeassistant.helpers import device_registry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (CoordinatorEntity,
                                                      DataUpdateCoordinator,
                                                      UpdateFailed)

"""Example integration using DataUpdateCoordinator.

What is handled - and what is not:

NOT:
- delete orphaned entities (Currently no orphaned or old/outdated entities are detected and removed)

HANDLED:


"""

#TODO: Do device registration 
#2 devices holds entitites
#3 refind entitites
#4 managed orphaned entities


_DOMAIN_ = "custom_sensor_1"
_LOGGER = logging.getLogger(__name__)
_LOEX = logging.getLogger(__name__ + ".experimental")
_LOGGER.debug("Starting %s", __file__)

_managed_entity_ids: list[str] = []


class MyCoordinator(DataUpdateCoordinator[Any]):
    _my_api: MyApiClient
    _LOGLCL = logging.getLogger(__name__ + ".MyCoordinator")
    _LOGLCL.debug("Class MyCoordinator of %s", __file__)

    def __init__(self, hass: HomeAssistant, my_api: MyApiClient):
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

    # TODO: Replace dict[DummyClass]
    # -> in this case a list of dummyclass is stored - but it doesnt need to be a dict
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
        #TODO: ConfigEntryAuthFailed seems no vaild excpection: Find alternative exception (or correct import)
        # except ConfigEntryAuthFailed as err:
        #     # Raising ConfigEntryAuthFailed will cancel future updates
        #     # and start a config flow with SOURCE_REAUTH (async_step_reauth)
        #     raise ConfigEntryAuthFailed from err
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
        entity_idx = self.extra_state_attributes["idx"]
        self._LOGLCL.info(
            "get_sensor_value for CoordinatedExampleSensor from coordinator_data for id: %s", entity_idx)
        retval: int = self._coord.data[entity_idx].dummyvalue
        self._LOGLCL.info("returning %i", retval)
        return retval

    def get_sensor_system_state(self) -> str:
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

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        self._LOGLCL.debug("ENTER: device_info")
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (_DOMAIN_, "testdev01")
            },
            name="test dev xy",
            manufacturer="test manufacturer",
            model="test model",
            sw_version="0.01",
        )

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
        "Pass self, coordinator to CoordinatorEntity."
        CoordinatorEntity.__init__(self, coord)  # pyright: reportUnknownMemberType=false
        "Pass self to SensorEntity."
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
    _LOEX.debug("ENTER async_setup_entry %s", __file__)
    dr = device_registry.async_get(hass)
    _LOEX.debug("create new device")

    # make sure device is created, even if no entity is present (usecase: show metadata like firmware version, etc.)
    dev1: device_registry.DeviceEntry = dr.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(_DOMAIN_, "testdev01")},
        name="my test device",
        sw_version="0.02",
    )

    """Set up platform."""
    _LOGGER.debug("async_setup_platform of %s", __file__)

    _managed_entity_ids.append("uzttra")
    _managed_entity_ids.append("f1")
    _managed_entity_ids.append("g1")

    my_api = MyApiClient(username="", password="")
    xcoordinator = MyCoordinator(hass, my_api)

    await xcoordinator.async_refresh()
    if not xcoordinator.last_update_success:
        raise PlatformNotReady

    _LOGGER.info("managed entity ids: %s", _managed_entity_ids)

    async_add_entities(CoordinatedExampleSensor(
        coord=xcoordinator, _unique_id=_uid) for _uid in _managed_entity_ids)

    _LOEX.debug("hass.data")
    _LOEX.debug(hass.states.async_all(_DOMAIN_))
    # from homeassistant.const import Platform
    # plat: list[Platform] = [Platform.SENSOR]
    
    # await hass.config_entries.async_forward_entry_setups(
    #     entry, plat
    # )


    _LOEX.debug("my new device:")
    _LOEX.debug(dev1)
    _LOEX.debug("EXIT async_setup_entry")

    #TODO: check    async_add_devices

    # dr.async_get_or_create(
    # config_entry_id=entry.entry_id,
    # connections={(device_registry.CONNECTION_NETWORK_MAC, config.mac)},
    # identifiers={(_DOMAIN_, config.bridgeid)},
    # manufacturer="Signify",
    # suggested_area="Kitchen",
    # name=config.name,
    # model=config.modelid,
    # sw_version=config.swversion,
    # hw_version=config.hwversion,
    # )

    # 'integrations': {
    # 'custom_components': {'custom_sensor_1': <Integration custom_sensor_1: custom_components.custom_sensor_1>}
    # 'custom_sensor_1': [<EntityPlatform domain=sensor platform_name=custom_sensor_1 config_entry=None>]}


def log_debug_coordinator_data(_coord: MyCoordinator) -> None:
    _LOGGER.debug("current self.__coordinator.data:")
    _LOGGER.debug(_coord.data)


def log_debug_domains(_hass: HomeAssistant):
    _LOGLCL = logging.getLogger(__name__ + ".debug_domains")
    _LOGLCL.debug("ENTER: log_domains")
    #_LOGLCL.debug("Start Domains:")
    #do: list[State] = _hass.states.async_all()
    #_LOGLCL.debug("Done Domains")
    _LOGLCL.debug("Start Domains2")
    count_all: int = 0
    domains: list[str] = []
    for entity_id in _hass.states.entity_ids():
        count_all = count_all + 1
        entity_domain = entity_id.split('.')[0]
        if entity_domain not in domains:
            domains.append(entity_domain)
    _LOGLCL.debug("found %i domains", count_all)
    _LOGLCL.debug(domains)
    _LOGLCL.debug("Done Domains2")
    _LOGLCL.debug("LEAVE: log_domains")


def log_debug_other(coo: MyCoordinator, hass: HomeAssistant):
    _LOGGER.debug("current coordinator data:")
    _LOGGER.debug(coo.data)
    _LOGGER.debug("hass-data")
    _LOGGER.debug(hass.data['integrations'][_DOMAIN_])


def log_debug_entity_ids(_hass: HomeAssistant):
    _LOGLCL = logging.getLogger(__name__ + ".debug_entity_ids")
    _LOGLCL.debug("ENTER: log_entity_ids")
    re = _hass.states.async_entity_ids()
    _LOGLCL.debug("print all:")
    for r in re:
        _LOGLCL.debug(r)
    _LOGLCL.debug("LEAVE: log_entity_ids")
    # ent = integration_entities(hass,_DOMAIN_)
    # _LOGGER.debug("entieees")
    # _LOGGER.debug(ent)


def log_debug_entities_all(_hass: HomeAssistant):
    # not sure if shows devices (not all entities!)
    _LOGLCL = logging.getLogger(__name__ + ".debug_entities_all")
    _LOGLCL.debug("ENTER: log_entities_all")
    _LOGLCL.debug("get all states/sensors")
    re = _hass.states.async_all()
    _LOGLCL.debug("show how many: %i", len(re))
    _LOGLCL.debug("show all:")
    for r in re:
        _LOGLCL.debug(r)
    _LOGLCL.debug("LEAVE: log_entities_all")
