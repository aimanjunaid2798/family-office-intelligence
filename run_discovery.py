from app.config.config import DISCOVERED_CSV
from app.discovery.manager import DiscoveryManager
from app.exporters.csv_exporter import CSVExporter


def main():

    print("=" * 80)
    print("Starting Family Office Discovery")
    print("=" * 80)

    manager = DiscoveryManager()

    offices = manager.discover()

    print(f"Discovered {len(offices)} candidate offices")

    exporter = CSVExporter()

    exporter.export(
        offices,
        str(DISCOVERED_CSV),
    )

    print()
    print(f"Dataset saved to:\n{DISCOVERED_CSV}")

    print()
    print("Preview")

    print("-" * 80)

    for office in offices[:10]:

        print(f"Name      : {office.name}")
        print(f"Website   : {office.website}")
        print(f"Status    : {office.verification_status}")
        print(f"Email     : {office.email}")
        print(f"Phone     : {office.phone}")
        print("-" * 80)


if __name__ == "__main__":
    main()