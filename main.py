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
    
    
    """
Opdracht:

Bepalingen:
 - Je moet gebruik maken van de aangeleverde variable(n)
 - Je mag deze variable(n) niet aanpassen
 - Het is de bedoeling dat je op het einde 1 programma hebt
 - Als inlever formaat wordt een PUBLIEKE git url verwacht die gecloned kan worden
 - Je hoofd bestand dat uitgevoerd dient te worden moet `main.py` noemen
 - Jouw repository mag enkel jouw python bestanden en eventuele mappen te bevatten.
 - Jouw repository mag enkel de bestanden bevatten die nodig zijn voor jouw examen uit te voeren; dus geen onnodige/overbodige bestanden
 - Alle map en bestandsnamen mogen GEEN spaties bevatten, enkel underscores
 - Alle map en bestandsnamen mogen GEEN hoofdletters bevatten, enkel kleine letters
    
LET OP! Indien het examen dat je indient niet aan deze bepalingen voldoet wordt dit geacht niet in orde te zijn en is dit per definitie 0

/ 5 ptn 1 - Maak een public repository aan op jouw gitlab of github account voor dit project
/10 ptn 2 - Gebruik python om de gegeven api url aan te spreken
/20 ptn 3 - Gebruik regex om de volgende data te extracten:
    - De AS nummmer van de provider
/15 ptn 4 - Verzamel onderstaande data en output alles als yaml. Een voorbeeld vind je hieronder.
    - Het land van het domein
    - Het ip van het domain
    - De DNS provider van het domein
    - Aparte isp naam, organisation en AS nummer van de hoster


Totaal  /50ptn
"""

""" voorbeeld yaml output

infra:
  isp: 'Unix-Solutions BV'
  organisation: 'Unix-Solutions BV'
  as: 'AS39923'
ip: 185.58.96.99
land: BE
provider: combell

"""