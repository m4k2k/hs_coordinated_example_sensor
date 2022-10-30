"""Custom Sensor 1"""

# TODO: inti coordinator here
# TODO: see: https://github.com/jgriss/FusionSolarHA/blob/2549d3d490c8eb187e08ae0efa6c4de02df5dc02/custom_components/fusion_solar/__init__.py


_DOMAIN_ = "custom_sensor_1"
import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("Starting %s", __file__)



# from homeassistant.config_entries import ConfigEntry
# # from homeassistant.const import Platform
# from homeassistant.core import HomeAssistant

# import logging

# # from fusion_solar_py.client import FusionSolarClient
# # from fusion_solar_py.exceptions import AuthenticationException, FusionSolarException


# from my_api.client import MyApiClient
# import my_api.client


# _LOGGER = logging.getLogger(__name__)


# Integration -> Plattform -> SensorType -> Entity


# #TODO: Needs to be edited, just copied 1:1
# async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
#     """Set up the platform.

#     @NOTE: `config` is the full dict from `configuration.yaml`.

#     :returns: A boolean to indicate that initialization was successful.
#     """
#     conf = config[DOMAIN]
#     country = conf[CONF_COUNTRY].name
#     wishlist = conf[CONF_WISHLIST]
#     scan_interval = conf[CONF_SCAN_INTERVAL]
#     eshop = EShop(country, async_get_clientsession(hass), wishlist)
#     coordinator = DataUpdateCoordinator(
#         hass,
#         _LOGGER,
#         # Name of the data. For logging purposes.
#         name=DOMAIN,
#         update_method=eshop.fetch_on_sale,
#         # Polling interval. Will only be polled if there are subscribers.
#         update_interval=scan_interval,
#     )

#     # Fetch initial data so we have data when entities subscribe
#     await coordinator.async_refresh()

#     hass.data[DOMAIN] = {
#         "conf": conf,
#         "coordinator": coordinator,
#     }
#     hass.async_create_task(async_load_platform(
#         hass, "sensor", DOMAIN, {}, conf))
#     hass.async_create_task(async_load_platform(
#         hass, "binary_sensor", DOMAIN, {}, conf))
#     return True
