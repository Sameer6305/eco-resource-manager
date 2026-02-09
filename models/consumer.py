"""
consumer.py — Consumer class for the Sustainable Resource Management System.

A **Consumer** represents any urban entity (household, factory, office) that
is assigned one or more `Resource` objects and can consume from them.

Design Decisions
────────────────
• The class delegates actual availability checks to `Resource.update_availability`,
  keeping Consumer thin and respecting the Single‑Responsibility Principle.
• `generate_usage_report()` returns structured data (list of dicts) so any UI
  layer can render it without parsing strings.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.resource import Resource


class Consumer:
    """
    An entity that consumes urban resources.

    Attributes
    ----------
    consumer_id : str | int
        Unique identifier for the consumer.
    name : str
        Human‑readable name (e.g. "Residential Block A").
    assigned_resources : list[Resource]
        Resources this consumer is allowed to draw from.
    """

    def __init__(
        self,
        consumer_id: str | int,
        name: str,
        assigned_resources: list[Resource] | None = None,
    ) -> None:
        self._consumer_id = consumer_id
        self._name: str = name
        self._assigned_resources: list[Resource] = assigned_resources or []
        self._consumption_history: list[dict] = []

    # ── Properties ────────────────────────────────────────────────────────

    @property
    def consumer_id(self) -> str | int:
        return self._consumer_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def assigned_resources(self) -> list[Resource]:
        """Return a shallow copy to prevent external list mutation."""
        return list(self._assigned_resources)

    @property
    def consumption_history(self) -> list[dict]:
        """Return a copy of this consumer's consumption history."""
        return list(self._consumption_history)

    # ── Resource management ───────────────────────────────────────────────

    def assign_resource(self, resource: Resource) -> str:
        """
        Assign a new resource to this consumer.

        Returns
        -------
        str
            Confirmation or duplicate-warning message.
        """
        if resource in self._assigned_resources:
            return f"⚠ {resource.name} is already assigned to {self._name}."
        self._assigned_resources.append(resource)
        return f"✔ {resource.name} assigned to {self._name}."

    def use_resource(self, resource: Resource, amount: float) -> str:
        """
        Consume a given amount from an assigned resource.

        Parameters
        ----------
        resource : Resource
            The resource to consume from (must be in assigned list).
        amount : float
            Quantity to consume.

        Returns
        -------
        str
            Success or error message forwarded from the Resource.
        """
        if resource not in self._assigned_resources:
            return (
                f"⚠ {resource.name} is not assigned to {self._name}. "
                "Please assign it first."
            )

        result: str = resource.update_availability(amount)

        # Log successful consumption only
        if result.startswith("✔"):
            self._consumption_history.append({
                "consumer": self._name,
                "resource": resource.name,
                "amount": amount,
                "remaining": resource.total_available,
            })

        return result

    # ── Reporting ─────────────────────────────────────────────────────────

    def generate_usage_report(self) -> dict:
        """
        Produce a structured summary of this consumer's resource usage.

        Returns
        -------
        dict
            Keys: consumer_id, name, resources (list of per-resource reports),
            total_consumption_events.
        """
        resource_reports = [res.report_usage() for res in self._assigned_resources]

        return {
            "consumer_id": self._consumer_id,
            "name": self._name,
            "resources": resource_reports,
            "consumption_history": self._consumption_history,
            "total_consumption_events": len(self._consumption_history),
        }

    # ── Dunder helpers ────────────────────────────────────────────────────

    def __repr__(self) -> str:
        res_names = [r.name for r in self._assigned_resources]
        return (
            f"Consumer(id={self._consumer_id}, name='{self._name}', "
            f"resources={res_names})"
        )
