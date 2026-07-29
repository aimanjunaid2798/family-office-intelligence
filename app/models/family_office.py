from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class FamilyOffice:

    # Identity
    id: str
    name: str
    office_type: Optional[str]
    website: Optional[str]

    # Location
    country: Optional[str]
    city: Optional[str]

    # Intelligence
    investment_focus: Optional[str]
    aum: Optional[str]
    description: Optional[str]

    # Decision Maker
    principal_name: Optional[str]
    principal_title: Optional[str]
    principal_linkedin: Optional[str]

    # Contact
    email: Optional[str]
    phone: Optional[str]

    # Signals
    recent_activity: Optional[str]

    # Verification
    discovery_source: str
    verification_source: Optional[str]
    verification_status: str
    verification_notes: Optional[str]

    # Metadata
    discovered_at: datetime

    @classmethod
    def create(
        cls,
        name: str,
        discovery_source: str,
        website: Optional[str] = None,
    ) -> "FamilyOffice":

        return cls(
            id=str(uuid4()),
            name=name.strip(),

            office_type=None,
            website=website,

            country=None,
            city=None,

            investment_focus=None,
            aum=None,
            description=None,

            principal_name=None,
            principal_title=None,
            principal_linkedin=None,

            email=None,
            phone=None,

            recent_activity=None,

            discovery_source=discovery_source,
            verification_source=None,
            verification_status="Pending",
            verification_notes=None,

            discovered_at=datetime.utcnow(),
        )