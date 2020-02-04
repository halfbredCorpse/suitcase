import time
import requests
import webbrowser
from math import sin, cos, atan2, sqrt, radians
import xml.etree.ElementTree as eT


class Victor:
    BUS_URL = 'http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22'
    STATIC_MAP_URL = 'https://static-maps.yandex.ru/1.x/?lang=en-US&ll='
    EARTH_R = 6378.100

    def __init__(self, his_lat, his_lon):
        self.lat = his_lat
        self.rad_lat = radians(self.lat)

        self.lon = his_lon
        self.rad_lon = radians(self.lon)

        self.buses = dict({})

        self.STATIC_MAP_URL += '{lon},{lat}&z=13&l=map&size=650,450&pt={lon},{lat},vkbkm'.format(lon=self.lon,
                                                                                                 lat=self.lat)

    def is_near(self, bus_lat, bus_lon):
        rad_bus_lon = radians(bus_lon)
        rad_bus_lat = radians(bus_lat)

        d_lon = rad_bus_lon - self.rad_lon
        d_lat = rad_bus_lat - self.rad_lat

        a = ((sin(d_lat / 2)) ** 2) + cos(self.rad_lat) * cos(rad_bus_lat) * (sin(d_lon / 2) ** 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = self.EARTH_R * c

        if distance <= 1.0:
            return True

        return False

    def get_buses(self):
        response = requests.get(self.BUS_URL)
        root = eT.fromstring(response.content)

        for bus in root:
            bus_id = lat = lon = 0
            d = ''

            for detail in bus:
                if detail.tag == 'id':
                    bus_id = int(detail.text)

                if detail.tag == 'd':
                    d = detail.text

                if detail.tag == 'lat':
                    lat = float(detail.text)

                if detail.tag == 'lon':
                    lon = float(detail.text)

            if bus_id and 'North' in d:
                self.buses[bus_id] = {
                    'lat': lat,
                    'lon': lon,
                }

    def check_nearest_bus(self):
        self.get_buses()

        bus_url = self.STATIC_MAP_URL

        for bus_id in self.buses:
            if self.is_near(self.buses[bus_id]['lat'], self.buses[bus_id]['lon']):
                print(self.buses[bus_id]['lat'])
                print(self.buses[bus_id]['lon'])

                bus_url += '~{},{},flag'.format(self.buses[bus_id]['lon'], self.buses[bus_id]['lat'])
                print("Look for Bus ID: {}".format(bus_id))

        webbrowser.open(bus_url, new=1, autoraise=True)


victor = Victor(41.980262, -87.668452)
while True:
    victor.check_nearest_bus()
    time.sleep(30)
