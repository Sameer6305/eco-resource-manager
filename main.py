"""
main.py — Console‑based demonstration of the Sustainable Resource Management
System.

Run this file directly to see a sample interaction:

    python main.py

No external dependencies are required — only the standard library.
"""

from models.resource import WaterResource, EnergyResource, WasteResource
from models.consumer import Consumer


def separator(title: str = "") -> None:
    """Print a visual separator for console readability."""
    print(f"\n{'═' * 60}")
    if title:
        print(f"  {title}")
        print('═' * 60)


def print_report(report: dict) -> None:
    """Pretty‑print a consumer usage report to the console."""
    print(f"  Consumer ID   : {report['consumer_id']}")
    print(f"  Name          : {report['name']}")
    print(f"  Total Events  : {report['total_consumption_events']}")
    print("  ─── Resource Breakdown ───")
    for res in report["resources"]:
        print(f"    • {res['name']} ({res.get('unit', 'units')})")
        print(f"      Available : {res['total_available']}")
        print(f"      Consumed  : {res['consumed']}")
        print(f"      Utilisation : {res['utilisation_pct']}%")
        if "source" in res:
            print(f"      Source    : {res['source']}")
        if "energy_type" in res:
            print(f"      Type      : {res['energy_type']}")
        if "waste_category" in res:
            print(f"      Category  : {res['waste_category']}")


def main() -> None:
    """Execute a full sample workflow and print results to the console."""

    # ── 1. Create resource instances ─────────────────────────────────────
    separator("1. Creating Resources")

    water = WaterResource(total_available=10_000, source="River")
    energy = EnergyResource(total_available=5_000, energy_type="Solar")
    waste = WasteResource(total_available=2_000, waste_category="Recyclable")

    for r in (water, energy, waste):
        print(f"  Created → {r}")

    # ── 2. Create consumers and assign resources ─────────────────────────
    separator("2. Creating Consumers & Assigning Resources")

    household = Consumer(consumer_id="C-101", name="Residential Block A")
    factory = Consumer(consumer_id="C-202", name="Textile Factory B")

    # Assign resources
    print(f"  {household.assign_resource(water)}")
    print(f"  {household.assign_resource(energy)}")
    print(f"  {household.assign_resource(waste)}")

    print(f"  {factory.assign_resource(water)}")
    print(f"  {factory.assign_resource(energy)}")
    print(f"  {factory.assign_resource(waste)}")

    # ── 3. Simulate resource consumption ─────────────────────────────────
    separator("3. Consuming Resources")

    actions = [
        (household, water, 1500),
        (household, energy, 800),
        (household, waste, 300),
        (factory, water, 4000),
        (factory, energy, 2200),
        (factory, waste, 1000),
    ]

    for consumer, resource, amount in actions:
        result = consumer.use_resource(resource, amount)
        print(f"  {consumer.name} → {result}")

    # ── 4. Demonstrate safe guard — over‑consumption attempt ─────────────
    separator("4. Edge Case — Over‑consumption Attempt")

    result = factory.use_resource(water, 9999)
    print(f"  {factory.name} → {result}")

    # ── 5. Demonstrate safe guard — invalid amount ───────────────────────
    separator("5. Edge Case — Invalid (Negative) Amount")

    result = household.use_resource(energy, -50)
    print(f"  {household.name} → {result}")

    # ── 6. Demonstrate safe guard — unassigned resource ──────────────────
    separator("6. Edge Case — Unassigned Resource")

    extra_water = WaterResource(total_available=500, source="Groundwater")
    result = household.use_resource(extra_water, 100)
    print(f"  {household.name} → {result}")

    # ── 7. Generate usage reports (polymorphism in action) ───────────────
    separator("7. Usage Reports")

    for consumer in (household, factory):
        print(f"\n  ┌── Report: {consumer.name} ──┐")
        report = consumer.generate_usage_report()
        print_report(report)

    # ── 8. Show individual resource reports (polymorphic calls) ──────────
    separator("8. Individual Resource Reports (Polymorphism)")

    for resource in (water, energy, waste):
        info = resource.report_usage()
        print(f"  {info['name']:12s} | Available: {info['total_available']:>8} {info.get('unit', 'units'):5s} "
              f"| Consumed: {info['consumed']:>8} | Utilisation: {info['utilisation_pct']}%")

    separator("Demo Complete")
    print("  The system is ready for Streamlit integration — see app.py.\n")


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
