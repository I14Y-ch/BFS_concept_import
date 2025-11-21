import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from typing import Optional, Dict, Any, List

import os
from dotenv import load_dotenv
load_dotenv()

def _api_get_request(url: str, token) -> Optional[Dict[str, Any]]:
    """Make a GET request to the API and return JSON response."""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return json.loads(response.content)
    return None

def extract_identifiers_and_versions(data: Any, key: Optional[str] = None) -> Dict[str, List[str]]:
    """Extract identifier and version from a list of objects."""
    result = {}
    items = data.get(key, []) if isinstance(data, dict) and key else data
    for item in items:
        identifier = item.get("identifier")
        version = item.get("version")
        if identifier and version:
            result.setdefault(identifier, []).append(version)
    return result

# Variables
SMS2_token = os.environ.get("SMS2_token")
I14Y_token = os.environ.get("I14Y_token")

# API URLs to get list of concepts
i14y_url = "https://api.i14y.admin.ch/api/public/v1/concepts?publisherIdentifier=CH1&page=1&pageSize=10000"
sms2_url = "https://sms-be.sis.bfs.admin.ch/api/DefinedVariables?page=1&pageSize=10000"

# Fetch data from both APIs
i14y_data = _api_get_request(i14y_url, I14Y_token)
sms2_data = _api_get_request(sms2_url, SMS2_token)

# Save responses to files (useful for debugging)
if i14y_data:
    with open("SMS2_concept_importer/output/i14y_response.json", "w", encoding="utf-8") as f:
        json.dump(i14y_data, f, indent=2)

if sms2_data:
    with open("SMS2_concept_importer/output/sms2_response.json", "w", encoding="utf-8") as f:
        json.dump(sms2_data, f, indent=2)

print("API responses saved to 'output/i14y_response.json' and 'output/sms2_response.json'")


# Filter SMS2 data by agencyId (so we only keep the DVs of the Agency BFS, and not the other agencies)
filtered_sms2_data = [item for item in sms2_data if item.get("agencyId") == "6e7f0c77-97de-44db-a32c-87bc73fa21c3"]

# Extract identifier-version mappings
sms2_dict = extract_identifiers_and_versions(filtered_sms2_data)
#print(sms2_dict)
i14y_dict = extract_identifiers_and_versions(i14y_data, "data")
#print(i14y_dict)

# Compare the two dictionaries
only_in_i14y = {k: v for k, v in i14y_dict.items() if k not in sms2_dict}
only_in_sms2 = {k: v for k, v in sms2_dict.items() if k not in i14y_dict}
version_mismatches = {
    k: {"i14y_versions": sorted(i14y_dict[k]), "sms2_versions": sorted(sms2_dict[k])}
    for k in i14y_dict
    if k in sms2_dict and sorted(i14y_dict[k]) != sorted(sms2_dict[k])
}

# Save differences to files
with open("SMS2_concept_importer/output/only_in_i14y.json", "w", encoding="utf-8") as f:
    json.dump(only_in_i14y, f, indent=2)

with open("SMS2_concept_importer/output/only_in_sms2.json", "w", encoding="utf-8") as f:
    json.dump(only_in_sms2, f, indent=2)

with open("SMS2_concept_importer/output/version_mismatches.json", "w", encoding="utf-8") as f:
    json.dump(version_mismatches, f, indent=2)

print("Differences saved to 'output' folder.")
