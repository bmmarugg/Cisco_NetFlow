def nxos_netflow(connection):


    def trunk_interfaces():
        config = []
        interface_list = connection.send_command("show int status | in trunk")
        lines = interface_list.split()
        for line in lines:
            if "Po" in line:
                continue
            interface = line.split()[0]
            config.append("interface " + interface)
            config.append(" ip flow monitor MONITOR_NAME input sampler SAMPLER_NAME")
            config.append("!")
        "\n".join(config)
        connection.send_config_set(config)
        print("Configuring trunk interfaces now... ")
        print("Saving configuration now... ")
        connection.send_command("wr mem")
        print("Finished")


    def routed_interfaces():
        config = []
        interface_list = connection.send_command("show int status | in routed")
        lines = interface_list.split()
        for line in lines:
            if "Po" in line:
                continue
            interface = line.split()[0]
            config.append("interface " + interface)
            config.append(" ip flow monitor MONITOR_NAME input sampler SAMPLER_NAME")
            config.append("!")
        "\n".join(config)
        connection.send_config_set(config)
        print("Configuring trunk interfaces now... ")
        print("Saving configuration now... ")
        connection.send_command("wr mem")
        print("Finished")

    host = connection.send_command("sh hostname")
    nxos_netflow_config = "Path/to/NX-OS/config/file"
    connection.send_config_from_file(nxos_netflow_config)

    netflow_source = []
    ip_int = connection.send_command("show run | in source-interface")
    ip_int_list = ip_int.split()


    source_int = ip_int_list[-1]
    netflow_source.append("flow exporter EXPORTER_NAME")
    netflow_source.append("source {}".format(source_int))
    "\n".join(netflow_source)
    connection.send_config_set(netflow_source)


    hostname = connection.send_command("sh hostname")

    dest_config = []
    if "CONDITION" in hostname.lower():
        dest_config.append("flow exporter EXPORTER_NAME")
        dest_config.append("destination XXX.XXX.XXX.XXX")
        dest_config.append("!")
        "\n".join(dest_config)
        connection.send_config_set(dest_config)
    elif "CONDITION" in hostname.lower():
        dest_config.append("flow exporter EXPORTER_NAME")
        dest_config.append("destination XXX.XXX.XXX.XXX")
        dest_config.append("!")
        "\n".join(dest_config)
        connection.send_config_set(dest_config)

    trunk_interfaces()
    routed_interfaces()
