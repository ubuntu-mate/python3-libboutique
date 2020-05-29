from dataclasses import dataclass


@dataclass(frozen=True)
class CuratedApp:
	name: str  # Name of the application, e.g. Brave
