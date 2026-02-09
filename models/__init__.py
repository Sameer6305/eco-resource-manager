"""
models package — Core business logic for the Sustainable Resource Management System.

This package contains all domain classes (Resource, Consumer) and is
completely independent of any UI framework (Streamlit, Flask, etc.).
"""

from models.resource import Resource, WaterResource, EnergyResource, WasteResource
from models.consumer import Consumer

__all__ = [
    "Resource",
    "WaterResource",
    "EnergyResource",
    "WasteResource",
    "Consumer",
]
