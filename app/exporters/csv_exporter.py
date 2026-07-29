import csv
from pathlib import Path

from app.models.family_office import FamilyOffice


class CSVExporter:

    HEADERS = [
        "id",
        "name",
        "website",
        "description",
        "email",
        "phone",
        "country",
        "city",
        "investment_focus",
        "aum",
        "principal_name",
        "principal_title",
        "principal_linkedin",
        "verification_status",
        "verification_notes",
        "discovery_source",
        "verification_source",
        "discovered_at",
    ]

    def export(self, offices: list[FamilyOffice], output_file: str):

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(self.HEADERS)

            for office in offices:

                writer.writerow([
                    office.id,
                    office.name,
                    office.website,
                    office.description,
                    office.email,
                    office.phone,
                    office.country,
                    office.city,
                    office.investment_focus,
                    office.aum,
                    office.principal_name,
                    office.principal_title,
                    office.principal_linkedin,
                    office.verification_status,
                    office.verification_notes,
                    office.discovery_source,
                    office.verification_source,
                    office.discovered_at.isoformat(),
                ])