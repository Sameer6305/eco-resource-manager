"""
resource.py — Base and derived resource classes for the Sustainable Resource
Management System.

Design Decisions
────────────────
• The **Resource** base class encapsulates common attributes and provides a
  uniform interface (`report_usage`, `update_availability`).
• Three concrete subclasses — `WaterResource`, `EnergyResource`,
  `WasteResource` — each add *minimal, realistic* attributes and **override**
  `report_usage()` to demonstrate polymorphism.
• All methods return plain dicts / strings so they can be consumed by *any* UI
  (console, Streamlit, REST API) without coupling to a framework.
"""

from __future__ import annotations
from datetime import datetime


# ──────────────────────────────────────────────────────────────────────────────
# Base Class
# ──────────────────────────────────────────────────────────────────────────────
class Resource:
    """
    Abstract representation of a natural resource in an urban area.

    Attributes
    ----------
    name : str
        Human‑readable resource name (e.g. "Water", "Electricity").
    total_available : float
        Current quantity available (units depend on the resource type).
    renewable : bool
        Whether the resource is classified as renewable.
    """

    def __init__(self, name: str, total_available: float, renewable: bool) -> None:
        self._name: str = name
        self._total_available: float = total_available
        self._initial_amount: float = total_available  # snapshot for reports
        self._renewable: bool = renewable
        self._usage_log: list[dict] = []  # tracks every consumption event

    # ── Property-based encapsulation ──────────────────────────────────────

    @property
    def name(self) -> str:
        """Return the resource name."""
        return self._name

    @property
    def total_available(self) -> float:
        """Return the current available quantity."""
        return self._total_available

    @property
    def renewable(self) -> bool:
        """Return whether the resource is renewable."""
        return self._renewable

    @property
    def usage_log(self) -> list[dict]:
        """Return a copy of the usage log (prevents external mutation)."""
        return list(self._usage_log)

    # ── Core methods ─────────────────────────────────────────────────────

    def report_usage(self) -> dict:
        """
        Return a dictionary summarising current availability and consumption.

        Returns
        -------
        dict
            Keys: name, total_available, consumed, renewable, utilisation_pct.
        """
        consumed = self._initial_amount - self._total_available
        utilisation = (consumed / self._initial_amount * 100) if self._initial_amount > 0 else 0.0

        return {
            "name": self._name,
            "total_available": round(self._total_available, 2),
            "consumed": round(consumed, 2),
            "renewable": self._renewable,
            "utilisation_pct": round(utilisation, 2),
        }

    def update_availability(self, amount: float) -> str:
        """
        Reduce available quantity after consumption.

        Parameters
        ----------
        amount : float
            Quantity to consume (must be > 0 and ≤ available).

        Returns
        -------
        str
            Success or error message.
        """
        if amount <= 0:
            return f"⚠ Invalid amount ({amount}). Must be positive."
        if amount > self._total_available:
            return (
                f"⚠ Insufficient {self._name}! "
                f"Requested {amount}, but only {self._total_available:.2f} available."
            )

        self._total_available -= amount
        self._usage_log.append({
            "resource": self._name,
            "amount": amount,
            "remaining": round(self._total_available, 2),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        })
        return (
            f"✔ {amount} units of {self._name} consumed. "
            f"Remaining: {self._total_available:.2f}"
        )

    # ── Dunder helpers ───────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name='{self._name}', "
            f"available={self._total_available}, renewable={self._renewable})"
        )


# ──────────────────────────────────────────────────────────────────────────────
# Subclass — Water
# ──────────────────────────────────────────────────────────────────────────────
class WaterResource(Resource):
    """
    Represents a municipal water supply.

    Extra Attributes
    ----------------
    source : str
        Origin of water (e.g. "River", "Groundwater", "Reservoir").
    """

    def __init__(
        self,
        total_available: float,
        source: str = "Reservoir",
        renewable: bool = True,
    ) -> None:
        super().__init__(name="Water", total_available=total_available, renewable=renewable)
        self._source: str = source

    @property
    def source(self) -> str:
        return self._source

    # ── Polymorphic override ─────────────────────────────────────────────
    def report_usage(self) -> dict:
        """Extend base report with water-specific metadata."""
        report = super().report_usage()
        report["unit"] = "litres"
        report["source"] = self._source
        return report


# ──────────────────────────────────────────────────────────────────────────────
# Subclass — Energy
# ──────────────────────────────────────────────────────────────────────────────
class EnergyResource(Resource):
    """
    Represents an energy grid supply (electricity).

    Extra Attributes
    ----------------
    energy_type : str
        Generation method (e.g. "Solar", "Wind", "Thermal").
    """

    def __init__(
        self,
        total_available: float,
        energy_type: str = "Solar",
        renewable: bool = True,
    ) -> None:
        super().__init__(name="Electricity", total_available=total_available, renewable=renewable)
        self._energy_type: str = energy_type

    @property
    def energy_type(self) -> str:
        return self._energy_type

    # ── Polymorphic override ─────────────────────────────────────────────
    def report_usage(self) -> dict:
        """Extend base report with energy-specific metadata."""
        report = super().report_usage()
        report["unit"] = "kWh"
        report["energy_type"] = self._energy_type
        return report


# ──────────────────────────────────────────────────────────────────────────────
# Subclass — Waste
# ──────────────────────────────────────────────────────────────────────────────
class WasteResource(Resource):
    """
    Represents urban waste management capacity.

    Here `total_available` denotes the **remaining capacity** of the waste
    processing facility.  Consumption *reduces* that capacity.

    Extra Attributes
    ----------------
    waste_category : str
        Type of waste handled (e.g. "Organic", "Recyclable", "Hazardous").
    """

    def __init__(
        self,
        total_available: float,
        waste_category: str = "Recyclable",
        renewable: bool = False,
    ) -> None:
        super().__init__(name="Waste", total_available=total_available, renewable=renewable)
        self._waste_category: str = waste_category

    @property
    def waste_category(self) -> str:
        return self._waste_category

    # ── Polymorphic override ─────────────────────────────────────────────
    def report_usage(self) -> dict:
        """Extend base report with waste-specific metadata."""
        report = super().report_usage()
        report["unit"] = "kg"
        report["waste_category"] = self._waste_category
        # For waste, 'consumed' capacity means waste already deposited
        report["label_consumed"] = "waste_deposited"
        return report
