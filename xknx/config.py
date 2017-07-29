import yaml
from xknx.knx import Address, AddressType
from .binary_sensor import BinarySensor
from .climate import Climate
from .time import Time
from .light import Light
from .switch import Switch
from .cover import Cover
from .sensor import Sensor

class Config:

    def __init__(self, xknx):
        """Initialize Config class."""
        self.xknx = xknx


    def read(self, file='xknx.yaml'):
        print("Reading {0}".format(file))
        with open(file, 'r') as filehandle:
            doc = yaml.load(filehandle)
            self.parse_general(doc)
            self.parse_groups(doc)


    def parse_general(self, doc):
        if "general" in doc:
            if "own_address" in doc["general"]:
                self.xknx.globals.own_address = \
                    Address(doc["general"]["own_address"],
                            AddressType.PHYSICAL)
            if "own_ip" in doc["general"]:
                self.xknx.globals.own_ip = doc["general"]["own_ip"]


    def parse_groups(self, doc):
        for group in doc["groups"]:
            if group.startswith("light"):
                self.parse_group_light(doc["groups"][group])
            elif group.startswith("switch"):
                self.parse_group_switch(doc["groups"][group])
            elif group.startswith("cover"):
                self.parse_group_cover(doc["groups"][group])
            elif group.startswith("climate"):
                self.parse_group_climate(doc["groups"][group])
            elif group.startswith("time"):
                self.parse_group_time(doc["groups"][group])
            elif group.startswith("sensor"):
                self.parse_group_sensor(doc["groups"][group])
            elif group.startswith("binary_sensor"):
                self.parse_group_binary_sensor(doc["groups"][group])

    def parse_group_light(self, entries):
        for entry in entries:
            light = Light.from_config(self.xknx,
                                      entry,
                                      entries[entry])
            self.xknx.devices.add(light)


    def parse_group_switch(self, entries):
        for entry in entries:
            switch = Switch.from_config(self.xknx,
                                        entry,
                                        entries[entry])
            self.xknx.devices.add(switch)


    def parse_group_binary_sensor(self, entries):
        for entry in entries:
            binary_sensor = BinarySensor.from_config(self.xknx,
                                                     entry,
                                                     entries[entry])
            self.xknx.devices.add(binary_sensor)


    def parse_group_cover(self, entries):
        for entry in entries:
            cover = Cover.from_config(self.xknx,
                                      entry,
                                      entries[entry])
            self.xknx.devices.add(cover)


    def parse_group_climate(self, entries):
        for entry in entries:
            climate = Climate.from_config(self.xknx,
                                          entry,
                                          entries[entry])
            self.xknx.devices.add(climate)


    def parse_group_time(self, entries):
        for entry in entries:
            time = Time.from_config(self.xknx,
                                    entry,
                                    entries[entry])
            self.xknx.devices.add(time)


    def parse_group_sensor(self, entries):
        for entry in entries:
            sensor = Sensor.from_config(self.xknx,
                                        entry,
                                        entries[entry])
            self.xknx.devices.add(sensor)

#TODO: Documentation
