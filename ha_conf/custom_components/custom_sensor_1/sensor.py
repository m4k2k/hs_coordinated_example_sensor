import logging
from collections.abc import MutableMapping
from datetime import timedelta
from typing import Any

import async_timeout
from custom_components.custom_sensor_1.my_api.client import (DummyClass,
                                                             MyApiClient)
from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity,
                                             SensorStateClass)
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryAuthFailed, PlatformNotReady
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (CoordinatorEntity,
                                                      DataUpdateCoordinator,
                                                      UpdateFailed)

"""
#from .const import DOMAIN
#from homeassistant.helpers.template import device_entities
#from homeassistant.config_entries import ConfigEntry
#from enum import Enum
#from typing import TypedDict
#from dataclasses import replace
#from homeassistant.helpers.template import integration_entities
#from homeassistant.helpers.entity_registry import async_get
#from collections.abc import Coroutine, Iterable, Mapping
#from tokenize import String
"""

"""Example integration using DataUpdateCoordinator."""


"""
What is handled - and what is not:

NOT:
- delete orphaned entities (Currently no orphaned or old/outdated entities are detected and removed)

HANDLED:


"""

_DOMAIN_ = "custom_sensor_1"
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("Starting %s", __file__)

_managed_entity_ids: list[str] = []


class MyCoordinator(DataUpdateCoordinator[Any]):
    _my_api: MyApiClient
    _LOGLCL = logging.getLogger(__name__ + ".MyCoordinator")
    _LOGLCL.debug("Class MyCoordinator of %s", __file__)

    def __init__(self, hass: HomeAssistant, my_api: MyApiClient):
        self._LOGLCL.debug("__init__ of MyCoordinator Class")
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=_DOMAIN_,
            update_method=self._async_update_data,
            # Polling interval. Will only be polled if there are subscribers.
            # default is usually 30 seconds
            update_interval=timedelta(seconds=40),
        )
        self._my_api = my_api
        self._LOGLCL.debug("managed entity ids: %s", _managed_entity_ids)
        log_entities_all(hass)

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
                    # await self.my_api.get_dummy_data()
                    dummy_data: DummyClass = self._my_api.get_dummy_data()
                    coordinator_data[__uid] = dummy_data
                self._LOGLCL.debug("returning cordinator_data:")
                self._LOGLCL.debug(coordinator_data)
                # log_debug_all_items(coordinator_data)
                log_entities_all(self.hass)
                return coordinator_data

        except ConfigEntryAuthFailed as err:
            # Raising ConfigEntryAuthFailed will cancel future updates
            # and start a config flow with SOURCE_REAUTH (async_step_reauth)
            raise ConfigEntryAuthFailed from err
        except UpdateFailed as err:
            raise UpdateFailed(f"Error communicating with API: {err}")


# class extra_coord_sens(TypedDict):
#     system_state: str
#     idx: str

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
    _attr_extra_state_attributes: MutableMapping[str, Any]
    #extra_attrib: extra_coord_sens = {"idx": "", "system_state": ""}

    def log_debug_coordinator_data(self) -> None:
        self._LOGLCL.debug("current self.__coordinator.data:")
        self._LOGLCL.debug(self._coord.data)

    def get_sensor_value(self) -> int:
        """Retrieve the current sensor value from the coordinator
        :return: The current value
        :rtype: int
        """
        entity_idx = self.extra_state_attributes["idx"]
        self._LOGLCL.info(
            "get_sensor_value for CoordinatedExampleSensor from coordinator_data for id: %s", entity_idx)
        retval: int = self._coord.data[entity_idx].dummyvalue
        self.log_debug_coordinator_data()
        self._LOGLCL.info("returning %i", retval)
        return retval

    def get_sensor_system_state(self) -> str:
        entity_idx = self.extra_state_attributes["idx"]
        self._LOGLCL.info(
            "get_sensor_system_state for CoordinatedExampleSensor from coordinator_data for id: %s", entity_idx)
        retval: str = self._coord.data[entity_idx].dummystate
        self.log_debug_coordinator_data()
        self._LOGLCL.info("returning %s", retval)
        return retval

    def update_all_data(self) -> None:
        self._LOGLCL.info("update_all_data of CoordinatedExampleSensor for id: %s",
                          self.extra_state_attributes["idx"])
        self.log_debug_coordinator_data()
        self._attr_native_value = self.get_sensor_value()
        self.extra_state_attributes["system_state"] = self.get_sensor_system_state(
        )

    # def extra_state_attributes(self) -> extra_coord_sens:
    # @property
    # def extra_state_attributes(self) -> dict:
    #     """Return entity specific state attributes."""
    #     _LOGGER.debug("enter for id: %s", self.extra_attrib["idx"])
    #     # required to store your own attributes, like _attr_testprop
    #     # should only be done the state is of the own attributes are not changed frequently
    #     # else you should use another sensor
    #     _LOGGER.debug("extra_state_attributes of CoordinatedExampleSensor")
    #     #return {"idx": self.extra_attrib["idx"], "system_state": self.extra_attrib["system_state"]}
    #     #return self.extra_attrib
    #     return super().extra_state_attributes

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
        self.log_debug_coordinator_data()
        self.update_all_data()
        # self.async_write_ha_state()
        log_entities_all(self.hass)
        return super()._handle_coordinator_update()

    def __init__(self, coord: MyCoordinator, _unique_id: str) -> None:
        super().__init__(coord)
        """Pass coordinator to CoordinatorEntity."""
        self._LOGLCL.debug(
            "__init__ of CoordinatedExampleSensor %s", _unique_id)
        self._LOGLCL.debug("current _coordinator data:")
        self._LOGLCL.debug(coord.data)
        # log_debug_all_items(_coordinator.data)
        self._coord = coord
        self.log_debug_coordinator_data()
        # log_debug_all_items(self.__coordinator.data)
        if (self._attr_name is not None):
            dum: str = self._attr_name
        else:
            dum = ""
        self._attr_name = str(dum.replace("Dummy", _unique_id))
        # TODO: solve issue where object not existing (needs to be created / new)
        #self._attr_extra_state_attributes: MutableMapping[str, Any] = MutableMapping()
        self._attr_extra_state_attributes: MutableMapping[str, Any] = dict(
            {"idx": "", "system_state": ""})
        #
        #self._attr_extra_state_attributes: dict[str, Any] = dict()
        self._attr_extra_state_attributes["idx"] = _unique_id
        self.update_all_data()
        # log_debug_all_items(_coordinator.data)


async def async_setup_platform(hass: HomeAssistant, config: ConfigType, async_add_entities: AddEntitiesCallback, discovery_info: DiscoveryInfoType | None = None) -> None:
    """Set up platform."""
    _LOGGER.debug("async_setup_platform of %s", __file__)

    _managed_entity_ids.append("e1")
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

    _LOGGER.debug("current coordinator data:")
    _LOGGER.debug(xcoordinator.data)

    _LOGGER.debug("hass-data")
    _LOGGER.debug(hass.data['integrations'][_DOMAIN_])

    log_entities_all(hass)


def log_domains(_hass: HomeAssistant):
    _LOGGER.debug("ENTER: log_domains")
    _LOGGER.debug("DOMAIN LOGGIN DISABLED")
    # _LOGGER.debug("Start Domains:")
    # do = _hass.states.async_all()
    # _LOGGER.debug(do.domain)
    # _LOGGER.debug("Done Domains")
    # _LOGGER.debug("Start Domains2:")
    # for entity_id in _hass.states.entity_ids():
    #     count_all = count_all + 1
    #     entity_domain = entity_id.split('.')[0]
    #     if entity_domain not in domains:
    #         domains.append(entity_domain)
    # _LOGGER.debug(domains)
    # _LOGGER.debug("Done Domains2:")
    _LOGGER.debug("LEAVE: log_domains")


def log_entity_ids(_hass: HomeAssistant):
    _LOGGER.debug("ENTER: log_entity_ids")
    re = _hass.states.async_entity_ids()
    _LOGGER.debug("print all:")
    for r in re:
        _LOGGER.debug(r)
    _LOGGER.debug("LEAVE: log_entity_ids")
    # ent = integration_entities(hass,_DOMAIN_)
    # _LOGGER.debug("entieees")
    # _LOGGER.debug(ent)


def log_entities_all(_hass: HomeAssistant):
    _LOGGER.debug("ENTER: log_entities_all")
    _LOGGER.debug("get all states/sensors")
    re = _hass.states.async_all()
    _LOGGER.debug("show how many:")
    _LOGGER.debug(len(re))
    _LOGGER.debug("print all:")
    for r in re:
        _LOGGER.debug(r)
    _LOGGER.debug("LEAVE: log_entities_all")
    log_entity_ids(_hass)
    log_domains(_hass)
