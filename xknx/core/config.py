"""
Module for reading configfiles (xknx.yaml).

* it will parse the given file
* and add the found devices to the devies vector of XKNX.
"""

import yaml

from xknx.devices import (BinarySensor, Climate, Cover, DateTime, ExposeSensor,
                          Light, Notification, Scene, Sensor, Switch)
from xknx.exceptions import XKNXException
from xknx.knx import PhysicalAddress


class Config:
    """Class for parsing xknx.yaml."""

    prefix_map = {
        'light': Light,
        'switch': Switch,
        'cover': Cover,
        'climate': Climate,
        'datetime': DateTime,
        'sensor': Sensor,
        'expose_sensor': ExposeSensor,
        'binary_sensor': BinarySensor,
        'notification': Notification,
        'scene': Scene
    }

    def __init__(self, xknx):
        """Initialize Config class."""
        self.xknx = xknx

    def read(self, file='xknx.yaml'):
        """Read config."""
        self.xknx.logger.debug("Reading %s", file)
        try:
            with open(file, 'r') as filehandle:
                doc = yaml.load(filehandle)
                self.parse_general(doc)
                self.parse_groups(doc)
        except FileNotFoundError as ex:
            self.xknx.logger.error("Error while reading %s: %s", file, ex)

    def parse_general(self, doc):
        """Parse the general section of xknx.yaml."""
        if "general" in doc:
            if "own_address" in doc["general"]:
                self.xknx.own_address = \
                    PhysicalAddress(doc["general"]["own_address"])

    def parse_groups(self, doc):
        """Parse the group section of xknx.yaml."""
        for group in doc["groups"]:
            self.parse_group(doc, group)

    def parse_group(self, doc, group):
        """Parse a group entry of xknx.yaml."""
        try:
            for prefix, clazz in Config.prefix_map.items():
                if group.startswith(prefix):
                    self.create_device(clazz, doc["groups"][group])
        except XKNXException as ex:
            self.xknx.logger.error("Error while reading config file: Could not parse %s: %s", group, ex)

    def create_device(self, clazz, entries):
        """Parse a section of xknx.yaml."""
        for entry in entries:
            device = clazz.from_config(
                self.xknx,
                entry,
                entries[entry])
            self.xknx.devices.add(device)
