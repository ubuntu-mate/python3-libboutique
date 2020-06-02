from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class CuratedApp:
    """
    Dataclass to hold the JSON metadata into a read-only object
    """
    name: str  # Name of the application, e.g. Brave
    listed: bool  # TODO Document the use of listed
    summary: str  # A little summary of the application
    developer_name: str
    developer_url: str  # The developer website
    description: str  # Complete description of the application
    launch_cmd: str  # The command to use from the terminal
    proprietary: bool
    alternate_to: str = field(init=True)  # Always get init.
    urls: dict  # More like links
    arch: List[str]  # List of architecture e.g. amd64, i386, arm
    releases: List[str]  # List of release codenames, e.g. : xenial, bionic, focal
    # TODO Define most accurate type here for methods
    methods: List  # Installation Method, it can be APT or SNAP
    # TODO Validate current structure and come with propositions.
