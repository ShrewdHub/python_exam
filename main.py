import requests
import re

# Given in the exam – do NOT change this
url = "http://ip-api.com/json/syntra.be"


def get_api_data(api_url: str) -> dict:
    response = requests.get(api_url, timeout=5)
    response.raise_for_status()
    return response.json()


def extract_as_number(as_field: str) -> str:
    """
    Use regex to extract the AS number from a string like:
    'AS34762 Combell NV'
    We want: 'AS34762'
    """
    match = re.search(r"\bAS\d+\b", as_field)
    if match:
        return match.group(0)
    return ""


def build_yaml_output(data: dict) -> str:
    """
    Build YAML output manually, matching the example structure.
    """

    # From ip-api.com typical fields:
    # - 'countryCode' -> e.g. 'BE'
    # - 'query' -> IP address
    # - 'isp' -> ISP name
    # - 'org' -> organisation name
    # - 'as' -> e.g. 'AS34762 Combell NV'

    land = data.get("countryCode", "")
    ip = data.get("query", "")
    isp = data.get("isp", "")
    organisation = data.get("org", "")
    as_field = data.get("as", "")

    as_number = extract_as_number(as_field)

    # For 'provider' (DNS provider of the domain), the example shows 'combell'.
    # We can derive this from the organisation name by taking the first word
    # and lowercasing it.
    provider = ""
    if organisation:
        provider = organisation.split()[0].lower()

    # Build YAML as a string
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
