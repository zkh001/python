
import subprocess
import re

import command

class WifiConnector:
    def __init__(self):
        self.__cmd = command.Command

    def scan(self, wifi_if = 'wlan0'):
        cmd = ['iwlist', wifi_if, 'scan']
        return self.__cmd.execute(cmd)

    def find_essid(self, wifi_if = 'wlan0'):
        # return self.scan(wifi_if).grep(r"ESSID").get_result()
        return self.scan(wifi_if).pipe(['grep','ESSID']).strip().get_result()

    def ifdown(self, wifi_if = 'wlan0'):
        cmd = ['ifdown', wifi_if]
        return self.__cmd.execute(cmd)

    def ifup(self, wifi_if = 'wlan0'):
        cmd = ['ifup', wifi_if]
        return self.__cmd.execute(cmd)

    def connect_wifi(self, essid, wifi_if = 'wlan0'):
        # TODO: append to here
        cmd = ['iwconfig', wifi_if, 'essid', essid]
        return self.__cmd.execute(cmd)
    

class ARDroneWifiManager:

    def __init__(self):
        self.__wifi_manager = WifiConnector()
        self.__connected_tb = {}

    def scan_ardorne_wifi(self):
        pat = re.compile(r"ESSID:.*(?P<ardrone_essid>ardrone2_[0-9]+)")

        drone_essid_list = []
        for line in self.__wifi_manager.find_essid():
            m = pat.match(line)
            if m is None:
                continue
            drone_essid_list.append(m.group('ardrone_essid'))

        return drone_essid_list

    def connect_ardrone(self, drone_essid):
        self.__wifi_manager.connect_wifi(drone_essid)

    

if __name__ == '__main__':
    cmd = WifiConnector()
    print(cmd.find_essid())
