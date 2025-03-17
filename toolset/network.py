import platform
import socket
import subprocess

import psutil
import requests
import scapy.all as scapy


def get_local_ip() -> str:
    """Get the local IP address of the machine.

    Returns:
        str: The local IP address, e.g., '192.168.1.100'.
    """

    return socket.gethostbyname(socket.gethostname())


def get_network_interfaces() -> dict:
    """Returns a dictionary of network interfaces and their IP addresses.

    Returns:
        dict: A mapping of interface names to their IP addresses.
    """
    interfaces = {}
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # IPv4
                interfaces[interface] = addr.address
    return interfaces


def ping_device(host: str) -> bool:
    """Ping a device to check if it's reachable.

    Args:
        host: The IP or hostname to ping.

    Returns:
        True if the device responds, False otherwise.
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    result = subprocess.run(["ping", param, "1", host], capture_output=True)
    return result.returncode == 0


def get_active_connections() -> list:
    """Get a list of active network connections.

    Returns:
        A list of tuples (local_address, remote_address, status).
    """

    connections = []
    for conn in psutil.net_connections(kind="inet"):
        if conn.raddr:  # Ignore listening ports
            connections.append((conn.laddr.ip, conn.laddr.port, conn.raddr.ip, conn.raddr.port, conn.status))
    return connections


def scan_network(ip_range: str) -> list:
    """Get connected devices by scanning the local network.

    Args:
        ip_range: The subnet range to scan (e.g., '192.168.1.0/24').

    Returns:
        list: A list of dictionaries with IP and MAC addresses.
    """

    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    response = scapy.srp(broadcast / arp_request, timeout=2, verbose=False)[0]

    devices = []
    for sent, received in response:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})

    return devices


def get_public_ip() -> str:
    """Returns the public IP address of the machine.

    Returns:
        str: The external IP address, e.g., '203.0.113.45'.
    """
    return requests.get("https://api64.ipify.org?format=text").text
