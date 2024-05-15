"""Test for the lib_helpers definitions."""

import pytest
from netutils import os_version
from netutils.constants import UPGRADE_PATHS


LOOSE_VERSION = [
    {"sent": {"current_version": "10.1", "comparison": ">=", "target_version": "10.2"}, "received": False},
    {"sent": {"current_version": "2.0.1", "comparison": "<", "target_version": "2.0.2"}, "received": True},
    {"sent": {"current_version": "1.0", "comparison": "==", "target_version": "1.0"}, "received": True},
    {"sent": {"current_version": "1.2.3", "comparison": "!=", "target_version": "1.2.3"}, "received": False},
    {"sent": {"current_version": "0.9.9", "comparison": ">", "target_version": "0.9.8"}, "received": True},
    {"sent": {"current_version": "3.3.3", "comparison": "<=", "target_version": "3.3.4"}, "received": True},
    {"sent": {"current_version": "2020.01.01", "comparison": ">=", "target_version": "2020.01.01"}, "received": True},
    {"sent": {"current_version": "2020.1.1", "comparison": "==", "target_version": "2020.01.01"}, "received": True},
    {"sent": {"current_version": "2.0.0a", "comparison": "<", "target_version": "2.0.1"}, "received": True},
    {"sent": {"current_version": "1.10", "comparison": ">", "target_version": "1.2"}, "received": True},
    {"sent": {"current_version": "3.3.3b", "comparison": "==", "target_version": "3.3.3b"}, "received": True},
    {"sent": {"current_version": "1.0.0", "comparison": "!=", "target_version": "2.0.0"}, "received": True},
]

STRICT_VERSION = [
    {"sent": {"current_version": "10.1", "comparison": ">=", "target_version": "10.2"}, "received": False},
    {"sent": {"current_version": "2.0.1", "comparison": "<", "target_version": "2.0.2"}, "received": True},
    {"sent": {"current_version": "1.0", "comparison": "==", "target_version": "1.0"}, "received": True},
    {"sent": {"current_version": "1.2.3", "comparison": "!=", "target_version": "1.2.3"}, "received": False},
    {"sent": {"current_version": "0.9.9", "comparison": ">", "target_version": "0.9.8"}, "received": True},
    {"sent": {"current_version": "3.3.3", "comparison": "<=", "target_version": "3.3.4"}, "received": True},
    {"sent": {"current_version": "2020.01.01", "comparison": ">=", "target_version": "2020.01.01"}, "received": True},
    {"sent": {"current_version": "1.10", "comparison": ">", "target_version": "1.2"}, "received": True},
    {"sent": {"current_version": "1.0.0", "comparison": "!=", "target_version": "2.0.0"}, "received": True},
]

PLATFORM_VERSION_METADATA = [
    # Cisco and Arista use the generic parsing
    {
        "sent": {"vendor": "cisco", "platform": "ios", "version": "15.7(2.0z)M"},
        "received": {
            "major": "15",
            "minor": "7",
            "vendor_metadata": False,
        },
    },
    {
        "sent": {"vendor": "arista", "platform": "eos", "version": "4.15.3f"},
        "received": {
            "major": "4",
            "minor": "15",
            "vendor_metadata": False,
        },
    },
    # Juniper Junos uses a custom parser
    {
        "sent": {"vendor": "juniper", "platform": "junos", "version": "12.4R"},
        "received": {
            "isservice": False,
            "ismaintenance": False,
            "isfrs": True,
            "isspecial": False,
            "main": "12",
            "minor": "4",
            "type": "R",
            "build": None,
            "service": None,
            "service_build": None,
            "service_respin": None,
            "vendor_metadata": True,
            "major": "12",
            "patch": None,
        },
    },
    {
        "sent": {"vendor": "juniper", "platform": "junos", "version": "12.3x48-d80"},
        "received": {
            "isservice": False,
            "ismaintenance": False,
            "isfrs": False,
            "isspecial": True,
            "main": "12",
            "minor": "3",
            "type": "x",
            "build": "48",
            "service": "d",
            "service_build": "80",
            "service_respin": None,
            "vendor_metadata": True,
            "major": "12",
            "patch": "48",
        },
    },
    {
        "sent": {"vendor": "juniper", "platform": "junos", "version": "12.3x48:d80"},
        "received": {
            "isservice": False,
            "ismaintenance": False,
            "isfrs": False,
            "isspecial": True,
            "main": "12",
            "minor": "3",
            "type": "x",
            "build": "48",
            "service": "d",
            "service_build": "80",
            "service_respin": None,
            "vendor_metadata": True,
            "major": "12",
            "patch": "48",
        },
    },
    {
        "sent": {"vendor": "juniper", "platform": "junos", "version": "12.3R12-S15"},
        "received": {
            "isservice": True,
            "ismaintenance": True,
            "isfrs": False,
            "isspecial": False,
            "main": "12",
            "minor": "3",
            "type": "R",
            "build": "12",
            "service": "S",
            "service_build": "15",
            "service_respin": None,
            "vendor_metadata": True,
            "major": "12",
            "patch": "12",
        },
    },
]


def test_get_upgrade_path():
    return_values = ["9.1.15-h1", "10.0.0", "10.0.12", "10.1.0", "10.1.9"]
    assert os_version.get_upgrade_path("9.1.6", "10.1.9", UPGRADE_PATHS["PANOS_OFFICIAL_V1"]) == return_values
    assert os_version.get_upgrade_path("9.1.6", "10.1.9", UPGRADE_PATHS["PANOS_MAJOR_ONLY_V1"]) == [
        "10.0.0",
        "10.1.0",
        "10.1.9",
    ]


def test_get_upgrade_path_current_greater_than_target():
    with pytest.raises(ValueError, match="Target version must be newer than current version."):
        os_version.get_upgrade_path("10.1.9", "9.1.6", UPGRADE_PATHS["PANOS_MAJOR_ONLY_V1"])


def test_get_upgrade_path_current_equals_target():
    with pytest.raises(ValueError, match="Target version equals current version. No upgrade necessary."):
        os_version.get_upgrade_path("10.1.9", "10.1.9", UPGRADE_PATHS["PANOS_MAJOR_ONLY_V1"])


@pytest.mark.parametrize("data", LOOSE_VERSION)
def test_compare_loose(data):
    assert os_version.compare_version_loose(**data["sent"]) == data["received"]


@pytest.mark.parametrize("data", STRICT_VERSION)
def test_compare_strict(data):
    assert os_version.compare_version_strict(**data["sent"]) == data["received"]


def test_compare_strict_bad_version():
    with pytest.raises(ValueError, match="invalid version number."):
        os_version.compare_version_strict("3.3.3b", "==", "3.3.3b")
    with pytest.raises(ValueError, match="Invalid comparison operator:"):
        os_version.compare_version_strict("3.3.3", "not-an-operator", "3.3.3")


# Testing the parsing of a Vendor, Platform, Version into vendor standardized sections
@pytest.mark.parametrize("data", PLATFORM_VERSION_METADATA)
def test_platform_parsing(data):
    assert (
        os_version.version_metadata(data["sent"]["vendor"], data["sent"]["platform"], data["sent"]["version"])
        == data["received"]
    )
