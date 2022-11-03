"""my_api client"""

import logging
import random

# global logger object
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("Starting %s", __file__)


class DummyClass:
    """Class representing the object which will be returned by the client"""
    """All attributes which should be returned will be listed here"""
    dummystate: str
    dummyvalue: int

    _LOGGER.debug("Class DummyClass")

    def __init__(
        self,
        dummystate: str,
        dummyvalue: int,
    ):
        _LOGGER.debug("__init__ of DummyClass")
        self.dummystate = dummystate
        self.dummyvalue = dummyvalue

    def get_dummystate(self) -> str:
        return self.dummystate

    def get_dummyvalue(self) -> int:
        return self.dummyvalue


class MyApiClient:
    def __init__(self, username: str, password: str) -> None:
        """  """
        _LOGGER.debug("__init__ of MyApiClient")
        self._user = username
        self._password = password
        _LOGGER.debug("check if login credentials are working, tryout login")
        self._login()

    def _login(self):
        """  """
        _LOGGER.debug("_login of MyApiClient")
        # self._user
        # self._password
        _LOGGER.debug("Logging into the service")

    def get_dummy_data(self) -> DummyClass:
        _LOGGER.debug("get_dummy_data of MyApiClient")

        _LOGGER.debug("Getting dummy data")
        # mockup, at this the API connects to the device and fetches the data
        _dummystate = "online"
        _dummydata = random.randint(0, 100)

        # now the data will be packed into a returnable formatted object
        dummy_data_object = DummyClass(
            dummystate=_dummystate, dummyvalue=_dummydata)

        return dummy_data_object
