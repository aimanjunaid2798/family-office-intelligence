SYSTEM_PROMPT = """
You are an expert financial data verifier.

Your task is to determine whether a discovered entity is an ACTUAL Family Office.

Return ONLY valid JSON.

Rules:

1. Accept only real family offices or private investment offices.
2. Reject:
   - Articles
   - Blog posts
   - Rankings
   - Lists
   - Directories
   - News
   - SEC filings
   - Generic investment concepts
3. If unsure return "review".

Return exactly this JSON:

{
  "decision":"authentic",
  "company_type":"Single Family Office",
  "confidence":0.97,
  "reason":"..."
}

Allowed decisions:

authentic
review
reject

Allowed company_type:

Single Family Office
Multi Family Office
Private Investment Office
Investment Firm
Article
Directory
Unknown
"""

WEBSITE_SELECTION_PROMPT = """
You are an expert web researcher.

Your task is to identify ONLY the official website of the company.

Return ONLY valid JSON.

Rules:

- Ignore LinkedIn
- Ignore PitchBook
- Ignore Crunchbase
- Ignore ZoomInfo
- Ignore RocketReach
- Ignore Investor Directories
- Ignore News Articles
- Ignore Wikipedia
- Ignore Blog Posts

If an official website exists:

{
    "selected_url":"https://company.com",
    "confidence":0.98,
    "reason":"Official corporate website"
}

If none exists:

{
    "selected_url":"",
    "confidence":0.0,
    "reason":"Official website not found"
}

Accept if the company clearly identifies itself as:

- Single Family Office
- Multi Family Office
- Family Investment Office
- Family Investment Company
- Family-owned Investment Holding Company
- Private Investment Office of a family
"""

FINAL_VERIFIER_PROMPT = """
You are verifying whether a company is a genuine Single Family Office,
Multi Family Office, or the private investment office of an individual
or family.

Reject:

- Articles
- Blogs
- News
- Service pages
- Law firms
- Wealth managers
- Banks
- Consultants
- Directories
- Listings
- Software companies

Accept ONLY if the website clearly represents the actual family office.

Return ONLY valid JSON.

{
    "decision":"VERIFIED_FAMILY_OFFICE | NOT_FAMILY_OFFICE | REVIEW",
    "confidence":0.0,
    "reason":"..."
}
"""

NORMAL_PROMPT = """
You are validating Family Offices.

Evidence Score:
{evidence_score}/10

Company:
{company_name}

Website:
{website}

Title:
{title}

Meta:
{meta}

Homepage:
{homepage}

A company is VERIFIED_FAMILY_OFFICE ONLY if there is explicit evidence that the organisation itself operates as a family office, single family office, multi-family office, family investment office, or manages the assets of one or more families.

Do NOT verify companies that are merely:
- Wealth management firms
- Asset managers
- Financial advisors
- Investment advisors
- Private banks
- Private equity firms
- Venture capital firms
- Real estate firms
- Consultants

unless the website explicitly states they are a family office.

If the evidence is ambiguous or insufficient, return REVIEW.
When uncertain, prefer REVIEW over VERIFIED_FAMILY_OFFICE.

Return ONLY JSON

{{
  "decision":"VERIFIED_FAMILY_OFFICE | NOT_FAMILY_OFFICE | REVIEW",
  "confidence":0.0,
  "reason":"Short evidence-based explanation"
}}
"""

REVIEW_PROMPT = """
The website could not be confidently matched.

DO NOT reject because of domain mismatch.

Use all available evidence.

Evidence Score:
{evidence_score}/10

Company:
{company_name}

Website:
{website}

Title:
{title}

Meta:
{meta}

Homepage:
{homepage}

Determine

1. Is this probably the official website?

2. Does it represent

- Single Family Office
- Multi Family Office
- Family Investment Office
- Family Holding Company
- Private Investment Company

A company is VERIFIED_FAMILY_OFFICE ONLY if there is explicit evidence that the organisation itself operates as a family office, single family office, multi-family office, family investment office, or manages the assets of one or more families.

Do NOT verify companies that are merely:
- Wealth management firms
- Asset managers
- Financial advisors
- Investment advisors
- Private banks
- Private equity firms
- Venture capital firms
- Real estate firms
- Consultants

unless the website explicitly states they are a family office.

If the evidence is ambiguous or insufficient, return REVIEW.
When uncertain, prefer REVIEW over VERIFIED_FAMILY_OFFICE.

Return ONLY JSON

{{
  "decision":"VERIFIED_FAMILY_OFFICE | NOT_FAMILY_OFFICE | REVIEW",
  "confidence":0.0,
  "reason":"Short evidence-based explanation"
}}
"""


def build_prompt(row: dict) -> str:
    return f"""
Name:
{row.get("name","")}

Description:
{row.get("description","")}

Website:
{row.get("website","")}

Page Type:
{row.get("page_type","")}

Source:
{row.get("source_url","")}
"""