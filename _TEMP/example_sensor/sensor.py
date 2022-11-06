"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from datetime import timedelta

import random
import logging

_LOGGER = logging.getLogger(__name__)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    _LOGGER.debug("""Set up the sensor platform.""")
    add_entities([ExampleSensor(), ExampleSensor2()])


class ExampleSensor(SensorEntity):
    _LOGGER.debug("""Representation Sensor 1""")

    _attr_name = "Example Temperature Sensor1"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    should_poll = True

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug("Update Sensor1")
        self._attr_native_value = random.randint(0, 100)


class ExampleSensor2(SensorEntity):
    _LOGGER.debug("""Representation of a Sensor2""")

    _attr_name = "Example Temperature Sensor2"
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _LOGGER.debug("Poll Disabled for Sensor2")
    should_poll = False

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug("Update Sensor2")
        self._attr_native_value = random.randint(0, 100)
