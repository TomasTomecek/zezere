#!/usr/bin/python3
from typing import Optional

import json
import platform
from subprocess import run as sp_run
from tempfile import NamedTemporaryFile
from sys import stderr
import os


IGNITION_BINARY_PATH = "/usr/lib/dracut/modules.d/30ignition/ignition"


def get_primary_interface() -> Optional[str]:
    mask_to_iface = {}

    with open("/proc/net/route", "r") as routefile:
        for line in routefile.readlines():
            if not line.strip():
                # Pass over empty lines
                continue
            split = line.split()
            interface = split[0]
            mask = split[7]
            if split[0] == "Iface":
                # Pass over the file header
                continue
            mask_to_iface[mask] = interface

    # If there are no routes at all, just exit
    if len(mask_to_iface) == 0:
        # No routes at all
        return None
    # Determine the smallest mask in the table.
    # This will default to the default route, or go further down
    return mask_to_iface[min(mask_to_iface, key=lambda x: int(x, 16))]


def get_interface_mac(interface: Optional[str]) -> str:
    if interface is None:
        return None
    with open("/sys/class/net/%s/address" % interface, "r") as addrfile:
        return addrfile.read().strip()


def get_zezere_url():
    paths = ["/etc/zezere-ignition-url", "./zezere-ignition-url"]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as urlfile:
                return urlfile.read().strip()


def run_ignition_stage(config_file: str, stage: str):
    print("Running stage %s with config file %s" % (stage, config_file))
    cmd = [IGNITION_BINARY_PATH, "--platform", "file", "--stage", stage]
    procenv = os.environ.copy()
    procenv["IGNITION_CONFIG_FILE"] = config_file

    sp_run(cmd, env=procenv, check=True)


def run_ignition(config_url: str):
    with NamedTemporaryFile(
        "w", encoding="utf-8", prefix="zezere-ignition-config-", suffix=".ign"
    ) as ignfile:
        cfgobj = {
            "ignition": {
                "version": "3.0.0",
                "config": {"replace": {"source": config_url}},
            },
        }
        ignfile.write(json.dumps(cfgobj))
        for stage in ["disks", "fetch", "files", "mount", "umount"]:
            run_ignition_stage(ignfile.name, stage)


def main():
    zezere_url = get_zezere_url()
    if zezere_url is None:
        print("No Zezere URL configured, exiting", file=stderr)
        return

    def_intf = get_primary_interface()
    def_intf_mac = get_interface_mac(def_intf)
    if def_intf_mac is None:
        print("Unable to determine default interface, exiting", file=stderr)
        return

    arch = platform.machine()

    url = "%s/netboot/%s/ignition/%s" % (zezere_url, arch, def_intf_mac)

    run_ignition(url)


if __name__ == "__main__":
    main()