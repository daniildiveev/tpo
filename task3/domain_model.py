from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Building:
    name: str

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Building name must not be empty.")


@dataclass
class Floor:
    number: int
    building: Building

    def __post_init__(self) -> None:
        if self.number < 1:
            raise ValueError(
                f"Floor number must be ≥ 1, got {self.number}."
            )
        if not isinstance(self.building, Building):
            raise TypeError("floor.building must be a Building instance.")


@dataclass
class Window:
    floor: Floor
    is_magnificent: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.floor, Floor):
            raise TypeError("window.floor must be a Floor instance.")


@dataclass
class Platform:
    window: Window

    def __post_init__(self) -> None:
        if not isinstance(self.window, Window):
            raise TypeError("platform.window must be a Window instance.")


@dataclass
class People:
    name: str = "народ"

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("People.name must not be empty.")


@dataclass
class Speaker:
    name: str
    platform: Platform

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Speaker.name must not be empty.")
        if not isinstance(self.platform, Platform):
            raise TypeError("speaker.platform must be a Platform instance.")

    def address(self, audience: People) -> str:
        if not isinstance(audience, People):
            raise TypeError("audience must be a People instance.")
        return f"{self.name} обращается к {audience.name}."


@dataclass
class Arthur:
    name: str
    target_window: Optional[Window] = None
    is_sliding: bool = False

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Arthur.name must not be empty.")

    def slide_toward(self, window: Window) -> None:
        if not isinstance(window, Window):
            raise TypeError("window must be a Window instance.")
        if not window.is_magnificent:
            raise ValueError(
                "Arthur can only glide toward a magnificent window."
            )
        self.target_window = window
        self.is_sliding = True


@dataclass
class Crowd:
    size: int
    is_cheering: bool = False

    def __post_init__(self) -> None:
        if self.size < 0:
            raise ValueError(
                f"Crowd size must be ≥ 0, got {self.size}."
            )

    def erupt(self) -> None:
        if self.size == 0:
            raise ValueError("An empty crowd cannot erupt.")
        self.is_cheering = True
