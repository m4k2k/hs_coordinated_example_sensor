import logging
from homeassistant.core import HomeAssistant
from custom_components.custom_sensor_1.sensor import MyCoordinator


"""
Debug utils for Homeassistant
"""


_LOGGER = logging.getLogger(__name__ + ".debug")
_LOGGER.debug("Starting %s", __file__)


# Specific

def log_debug_coordinator_data(_my_coordinator: MyCoordinator) -> None:
    _LOGGER.debug("current self.__coordinator.data:")
    _LOGGER.debug(_my_coordinator.data)


# Generic

def log_debug_domains(_hass: HomeAssistant):
    _LOGLCL = logging.getLogger(__name__ + ".debug_domains")
    _LOGLCL.debug("ENTER: log_domains")
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


def log_debug_other(_my_coordinator: MyCoordinator, _hass: HomeAssistant, _domain: str):
    _LOGGER.debug("current coordinator data:")
    _LOGGER.debug(_my_coordinator.data)
    _LOGGER.debug("hass-data")
    _LOGGER.debug(_hass.data['integrations'][_domain])


def log_debug_entity_ids(_hass: HomeAssistant):
    _LOGLCL = logging.getLogger(__name__ + ".debug_entity_ids")
    _LOGLCL.debug("ENTER: log_entity_ids")
    re = _hass.states.async_entity_ids()
    _LOGLCL.debug("print all:")
    for r in re:
        _LOGLCL.debug(r)
    _LOGLCL.debug("LEAVE: log_entity_ids")


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


def log_debug_hass_states(_hass: HomeAssistant, _domain: str):
    _LOGGER.debug("hass.states")
    _LOGGER.debug(_hass.states.async_all(_domain))