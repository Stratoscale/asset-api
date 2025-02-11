import os
import yaml
from asset.tcp import client
from asset.tcp import config


_CONFIG_FILE_NAME = "/etc/asset.conf"
_VAR_NAME = "ASSET_CONFIG_FILE"


def factory(document=None):
    configFile = os.environ.get(_VAR_NAME, _CONFIG_FILE_NAME)
    with open(configFile) as f:
        config.Config(yaml.safe_load(f))
    return client.Client(config.config.provider(), document=document)
