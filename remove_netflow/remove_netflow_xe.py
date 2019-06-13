import netmiko
import json
from pprint import pprint


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


    def trunk_interfaces():
        config = []
        interface_list = connect.send_command("show int status | in trunk")
        lines = interface_list.split()
        for line in lines:
            if "Po" in line:
                continue
            interface = line.split()[0]
            config.append("interface " + interface)
            config.append(" no ip flow monitor MONITOR_NAME input")
            config.append("!")
        "\n".join(config)
        connect.send_config_set(config)
        print("Removing NetFlow from trunk interfaces now... ")
        print("Finished removing NetFlow from trunk interfaces. ")
        print("Saving configuration now... ")
        connect.send_command("wr mem")



    def routed_interfaces():
        config = []
        interface_list = connect.send_command("show ip int br | ex un")
        lines = interface_list.split()
        for line in lines:
            if "Po" in line:
                continue
            interface = line.split()[0]
            config.append("interface " + interface)
            config.append(" no ip flow monitor MONITOR_NAME input")
            config.append("!")
        "\n".join(config)
        connect.send_config_set(config)
        print("Removing NetFlow from routed interfaces now... ")
        print("Finished removing NetFlow from routed interfaces. ")
        print("Saving configuration now... ")
        connect.send_command("wr mem")
        print("Finished")


    trunk_interfaces()
    routed_interfaces()

    connect.send_config_set("no Sampler SAMPLER_NAME")
    connect.send_config_set("no flow monitor MONITOR_NAME")
    connect.send_config_set("no flow exporter EXPORTER_NAME")
    connect.send_config_set("no flow record RECORD_NAME")
    connect.send_command("wr mem")



for device in device_list:
    main()