"""Example integration using DataUpdateCoordinator."""


"""
What is handled - and what is not:

NOT:
- delete orphaned entities (Currently no orphaned or old/outdated entities are detected and removed)

HANDLED:



"""


from typing import TypedDict
from dataclasses import replace
import logging
from datetime import timedelta
from tokenize import String
import async_timeout
from enum import Enum
from homeassistant.const import TEMP_CELSIUS
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.exceptions import (ConfigEntryAuthFailed, PlatformNotReady)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.template import device_entities
from homeassistant.helpers.template import integration_entities
from homeassistant.helpers.entity_registry import async_get
from custom_components.custom_sensor_1.my_api.client import (MyApiClient, DummyClass)
from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity, SensorStateClass)
from homeassistant.helpers.update_coordinator import (CoordinatorEntity, DataUpdateCoordinator, UpdateFailed)
_DOMAIN_ = "custom_sensor_1"

_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("Starting %s", __file__)

#from .const import DOMAIN

_managed_entity_ids: list[str] = []

#raise "last position"
# TODO: Find the issue why only dd is updated after a few tries (ee is LOST)
# Hint: maybe the for loop or the coord.data return
# Hint: be aware the dd is the last added entry

# def log_debug_all_items(__coordinator_data: dict[DummyClass]):
#     _LOGGER.debug("Log all coo data")
#     for key,value in __coordinator_data.items():
#         _LOGGER.debug(__coordinator_data[key].at_id)
#         _LOGGER.debug(__coordinator_data[key].extra_attributes)


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
        _coord=coordinator, _unique_id=_uid) for _uid in _managed_entity_ids)

    _LOGGER.debug("current coordinator data:")
    _LOGGER.debug(coordinator.data)

    _LOGGER.debug("hass-data")
    _LOGGER.debug(hass.data['integrations'][_DOMAIN_])

    log_entities_all(hass)
    # error: _LOGGER.debug(hass.data['integrations'][_DOMAIN_][_DOMAIN_])

    # _LOGGER.debug(hass.data)

    # raise "halt and catch fire"
    # hass.stop()
    # log_debug_all_items(coordinator.data)


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
            name=_DOMAIN_,
            update_method=self._async_update_data,
            # Polling interval. Will only be polled if there are subscribers.
            # default is usually 30 seconds
            update_interval=timedelta(seconds=40),
        )
        self._my_api = my_api
        _LOGGER.debug("managed entity ids: %s", _managed_entity_ids)
        log_entities_all(hass)

    # TODO: Replace dict[DummyClass] -> in this case, a list of dummyclass is stored - but it doesnt need to be a dict
    async def _async_update_data(self) -> dict:
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
                coordinator_data: dict = {}
                for __uid in _managed_entity_ids:
                    _LOGGER.debug("calling api for id: %s", __uid)
                    # here you could also do an if id = "abc" then talk to api-a else api-b
                    dummy_data: DummyClass = self._my_api.get_dummy_data()
                    coordinator_data[__uid] = dummy_data
                _LOGGER.debug("returning cordinator_data:")
                _LOGGER.debug(coordinator_data)
                # log_debug_all_items(coordinator_data)
                log_entities_all(self.hass)
                return coordinator_data

        except ConfigEntryAuthFailed as err:
            # Raising ConfigEntryAuthFailed will cancel future updates
            # and start a config flow with SOURCE_REAUTH (async_step_reauth)
            raise ConfigEntryAuthFailed from err
        except UpdateFailed as err:
            raise UpdateFailed(f"Error communicating with API: {err}")


class extra_coord_sens(TypedDict):
    system_state: str
    idx: str


class CoordinatedExampleSensor(CoordinatorEntity, SensorEntity):
    """An entity using CoordinatorEntity.
    The CoordinatorEntity class provides:
        should_poll
        async_update
        async_added_to_hass
        available
    """
    _coord: MyCoordinator

    _LOGGER.debug("""Class of CoordinatedExampleSensor""")

    _attr_name = "Example Temperature Sensor Dummy"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    # use the keys and assign an empty value
    # its content will be visible in HA
    extra_attrib: extra_coord_sens = {"idx": "", "system_state": ""}

    def get_sensor_value(self) -> int:
        """Retrieve the current sensor value from the coordinator
        :return: The current value
        :rtype: int
        """
        _LOGGER.debug("_get_data of CoordinatedExampleSensor")
        _LOGGER.debug("getting sensor value for id: %s",
                      self.extra_attrib["idx"])
        entity_id = self.extra_attrib["idx"]
        __dummy_data: DummyClass = self._coord.data[entity_id]
        value = __dummy_data.dummyvalue
        value = self._coord.data[self.extra_attrib["idx"]].dummyvalue
        _LOGGER.debug("current self.__coordinator.data:")
        _LOGGER.debug(self._coord.data)
        _LOGGER.debug("returning %i", value)
        return value

    def get_sensor_system_state(self) -> str:
        _LOGGER.debug("_get_sensor_system_state of CoordinatedExampleSensor")
        _LOGGER.debug("getting sensor system state for id: %s",
                      self.extra_attrib["idx"])
        # value = "fixed-offline"
        value = self._coord.data[self.extra_attrib["idx"]].dummystate
        _LOGGER.debug("returning %s", value)
        return value

    def update_all_data(self) -> None:
        # not rquired, but recommended updates all properties and values of the entity(sensor)
        _LOGGER.debug("update_all_data of CoordinatedExampleSensor")
        _LOGGER.debug("enter for id: %s", self.extra_attrib["idx"])
        _LOGGER.debug("current self.__coordinator.data:")
        _LOGGER.debug(self._coord.data)
        self._attr_native_value = self.get_sensor_value()
        self.extra_attrib["idx"] = self.get_sensor_system_state()
        # not working: log_entities(self.hass)

    @property
    def extra_state_attributes(self) -> extra_coord_sens:
        """Return entity specific state attributes."""
        _LOGGER.debug("enter for id: %s", self.extra_attrib["idx"])
        # required to store your own attributes, like _attr_testprop
        # should only be done the state is of the own attributes are not changed frequently
        # else you should use another sensor
        _LOGGER.debug("extra_state_attributes of CoordinatedExampleSensor")
        return self.extra_attrib

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("_handle_coordinator_update of CoordinatedExampleSensor")
        _LOGGER.debug("enter for id: %s", self.extra_attrib["idx"])
        # gets triggered, triggers the pull of the data from the coordinator
        # gets triggered after the coordinator has finished getting updates
        _LOGGER.debug("current self.__coordinator data:")
        _LOGGER.debug(self._coord.data)
        self.update_all_data()
        # self.async_write_ha_state()
        log_entities_all(self.hass)
        return super()._handle_coordinator_update()

    def __init__(self, _coord: MyCoordinator, _unique_id: str) -> None:
        """Pass coordinator to CoordinatorEntity."""
        _LOGGER.debug("__init__ of CoordinatedExampleSensor %s", _unique_id)
        _LOGGER.debug("current _coordinator data:")
        _LOGGER.debug(_coord.data)
        # log_debug_all_items(_coordinator.data)
        self._coord = _coord
        _LOGGER.debug("current self.__coordinator data:")
        _LOGGER.debug(self._coord.data)
        # log_debug_all_items(self.__coordinator.data)
        if (self._attr_name is not None):
            dum: str = self._attr_name
        else:
            dum = ""
        self._attr_name = dum.replace("Dummy", _unique_id)
        # self.extra_attrib["idx"] = _unique_id
        # AttributeError: 'CoordinatedExampleSensor' object has no attribute 'extra_attrib'
        # TODO: solve issue where object not existing (needs to be created / new)

        #self.extra_attrib = extra_coord_sens()

        self.extra_attrib["idx"] = _unique_id
        self.update_all_data()
        super().__init__(_coord)
        # log_debug_all_items(_coordinator.data)
        #raise "hier"
        # TODO: Find issue why the second attribute gets overwriten
        #!check the attribute_name / and attribute id of both objects

        # in coordinator.data sind dummyclass objekte und nicht CoordinatedExampleSensor Objekte
        # TODO: For debug purpose write functions which finds and logs all info
        # of CoordinatedExampleSensor Objects in HA entities store
        # not working, producing error log_entities(self.hass)
