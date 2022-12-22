class Config(object):
SUDO_USERS = "5667156680"
OWNER_ID = 5667156680

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True  # Create a new config.py or rename this to config.py file in same dir and import, then extend this class.


