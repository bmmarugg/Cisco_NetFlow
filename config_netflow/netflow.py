import netmiko
import json
from pprint import pprint
import ios_netflow
import iosxe_netflow
import nxos_netflow


with open("Path/to/credentials") as credentials:
    creds = json.load(credentials)


name = creds["username"]
passwrd = creds["passwrd"]
ios = "cisco_ios"


with open("Path/to/device/list") as f:
    device_line = f.read().splitlines()
while("" in device_line):
    device_line.remove("")
device_list = device_line


def main():
    print("Now connecting to: {}".format(device))
    connect = netmiko.ConnectHandler(username=name, password=passwrd, device_type=ios, ip=device)
    print("Successfully connected to: {}".format(device))

    connect.send_command("terminal length 0")
    show_version = connect.send_command("show version")
    version_line = show_version.splitlines()[0]

    if "IOS" in version_line:
        ios_netflow.ios_netflow(connect)

    elif "IOS-XE" in version_line:
        iosxe_netflow.iosxe_netflow(connect)

    elif "NX-OS" in version_line:
        nxos_netflow.nxos_netflow(connect)


for device in device_list:
    main()
