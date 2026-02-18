import requests
import re

# Given in the exam – do NOT modify this
url = "http://ip-api.com/json/syntra.be"


def get_api_data(api_url: str) -> dict:
    """Fetch JSON data from the API."""
    response = requests.get(api_url, timeout=5)
    response.raise_for_status()
    return response.json()


def extract_as_number(as_field: str) -> str:
    """
    Extract the AS number using regex.
    Example input: 'AS34762 Combell NV'
    Output: 'AS34762'
    """
    match = re.search(r"\bAS\d+\b", as_field)
    return match.group(0) if match else ""


def build_yaml_output(data: dict) -> str:
    """Build YAML output matching the exam example exactly."""

    land = data.get("countryCode", "")
    ip = data.get("query", "")
    isp = data.get("isp", "")
    organisation = data.get("org", "")
    as_field = data.get("as", "")

    as_number = extract_as_number(as_field)

    # DNS provider: take first word of organisation, lowercase
    provider = organisation.split()[0].lower() if organisation else ""

    yaml_lines = [
        "infra:",
        f"  isp: '{isp}'",
        f"  organisation: '{organisation}'",
        f"  as: '{as_number}'",
        f"ip: {ip}",
        f"land: {land}",
        f"provider: {provider}",
    ]

    return "\n".join(yaml_lines)


def main():
    data = get_api_data(url)
    yaml_output = build_yaml_output(data)
    print(yaml_output)


if __name__ == "__main__":
    main()