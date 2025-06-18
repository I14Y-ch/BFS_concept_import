import json
import requests
from typing import Optional, Dict, Any

import os
from dotenv import load_dotenv
load_dotenv()

def _api_get_request(url: str, token) -> Optional[Dict[str, Any]]:
    """Make a GET request to the API and return JSON response."""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    response = requests.get(url, verify=False, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content)
    return None

def _api_post_request(url, token, payload):

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload, verify=False)
    return response

def _api_post_request_file(url, token, payload):

    headers = {
        "Authorization": token
    }

    response = requests.post(url, headers=headers, files=payload, verify=False)
    return response


def get_DV(dv_id: str, token) -> Optional[Dict[str, Any]]:
    """gets the DV metadata"""
    url = f"https://sms-be.sis.bfs.admin.ch/api/DefinedVariables/{dv_id}"
    return _api_get_request(url, token)


def get_CL(cl_id: str, token) -> Optional[Dict[str, Any]]:
    """gets the CL metadata"""
    url = f"https://sms-be.sis.bfs.admin.ch/api/CodeLists/{cl_id}"
    return _api_get_request(url, token)


def get_CLE(cl_id: str, token) -> Optional[Dict[str, Any]]:
    """gets the CLE metadata"""
    url = f"https://sms-be.sis.bfs.admin.ch/api/CodeLists/{cl_id}/codeListEntries"
    return _api_get_request(url, token)

def map_CLE(CLE):
    annotations = []
    if CLE.get("type") is not None:
        annotations = [
            {
                "identifier": CLE.get("annotations[id]", None),
                "text": CLE.get("text", None),
                "title": CLE.get("title", None),
                "type": CLE.get("type", None),
                "uri": CLE.get("uri", None),
            }
        ]

    return {
        "annotations": annotations,
        "code": CLE.get("value"),
        "description": CLE.get("description", None),
        "name": CLE.get("name", None),
        "parentCode": CLE.get("parentCode", None)
    }

# Variables
SMS2_token = os.environ.get("SMS2_token")
I14Y_token = os.environ.get("I14Y_token")
# dv_id = "08d9e176-b0cf-c0fe-abab-861d6026f0ac" # does not work: user e-mail does not exist in I14Y
dv_id = "08dac62e-ab42-57fc-8db1-9e36ad2655c1" # works because user e-mail exist in I14Y

## Get the variables from SMS2
DV = get_DV(dv_id, SMS2_token)
# json.dump(DV, open("SMS2_concept_importer/output/DV.json", "w"), indent=4)

## TODO: make this a function map_DV
# Create the JSON object to write to I14Y. The object is different depending on the type of the defined variable
if DV['definedVariableType'] == "CodeList":
    cl_id = DV["codeListId"]
    CL = get_CL(cl_id, SMS2_token)
    json.dump(CL, open("SMS2_concept_importer/output/CL.json", "w"), indent=4)
    CLE = get_CLE(cl_id, SMS2_token)
    json.dump(CLE, open("SMS2_concept_importer/output/CLE.json", "w"), indent=4)

    concept_data = {
        "data": {
            "conceptType": DV["definedVariableType"],
            "codeListEntryValueType": CL["codeListEntryValueType"],
            "codeListEntryValueMaxLength": CL["codeListEntryValueMaxLength"],
            "conformsTo": DV["conformsTo"],
            "description": DV["description"],
            "identifier": DV["identifier"],
            "keywords": [],
            "name": DV["name"],
            "publisher": {
                "identifier": "i14y-test-organisation"  # Change organisation to BFS
            },
            "responsibleDeputy": {
                "email": DV["responsibleDeputy"]["identifier"]
            },
            "responsiblePerson": {
                "email": DV["responsiblePerson"]["identifier"]
            },
            "themes": [],
            "validFrom": DV["validFrom"],
            "validTo": DV.get("validTo", None),
            "version": DV["version"],
        }
    }

    CLE_data = {"data": [map_CLE(obj) for obj in CLE]}
    json.dump(CLE_data, open("SMS2_concept_importer/output/I14Y_codelistentries.json", "w"), indent=4)

if DV['definedVariableType'] == "Numeric":
    concept_data = {
        "data": {
            "conceptType": DV["definedVariableType"],
            "maxValue": DV["maxValue"],
            "measurementUnit": DV["measurementUnit"],
            "minValue": DV["minValue"],
            "numberDecimals": DV["numberDecimals"],
            "conformsTo": DV["conformsTo"],
            "description": DV["description"],
            "identifier": DV["identifier"],
            "keywords": [],
            "name": DV["name"],
            "publisher": {
                "identifier": "test-organization"  # Change organisation to BFS
            },
            "responsibleDeputy": {
                "email": DV["responsibleDeputy"]["identifier"]
            },
            "responsiblePerson": {
                "email": DV["responsiblePerson"]["identifier"]
            },
            "themes": [],
            "validFrom": DV["validFrom"],
            "validTo": DV.get("validTo", None),
            "version": DV["version"],
        }
    }

if DV['definedVariableType'] == "String":
    concept_data = {
        "data": {
            "conceptType": DV["definedVariableType"],
            "maxLength": DV["maxLength"],
            "minLength": DV["minLength"],
            "pattern": DV["pattern"],
            "conformsTo": DV["conformsTo"],
            "description": DV["description"],
            "identifier": DV["identifier"],
            "keywords": [],
            "name": DV["name"],
            "publisher": {
                "identifier": "test-organization"  # Change organisation to BFS
            },
            "responsibleDeputy": {
                "email": DV["responsibleDeputy"]["identifier"]
            },
            "responsiblePerson": {
                "email": DV["responsiblePerson"]["identifier"]
            },
            "themes": [],
            "validFrom": DV["validFrom"],
            "validTo": DV.get("validTo", None),
            "version": DV["version"],
        }
    }

if DV['definedVariableType'] == "Date":
    concept_data = {
        "data": {
            "conceptType": DV["definedVariableType"],
            "pattern": DV["pattern"],
            "conformsTo": DV["conformsTo"],
            "description": DV["description"],
            "identifier": DV["identifier"],
            "keywords": [],
            "name": DV["name"],
            "publisher": {
                "identifier": "test-organization"  # Change organisation to BFS
            },
            "responsibleDeputy": {
                "email": DV["responsibleDeputy"]["identifier"]
            },
            "responsiblePerson": {
                "email": DV["responsiblePerson"]["identifier"]
            },
            "themes": [],
            "validFrom": DV["validFrom"],
            "validTo": DV.get("validTo", None),
            "version": DV["version"],
        }
    }

# Write the JSON object (concept) to a file
json.dump(concept_data, open("SMS2_concept_importer/output/concept.json", "w"), indent=4)

## TODO: make this a function post_DV
## POST concept data
# url = "https://iop-partner.app.cfap02.atlantica.admin.ch/api/concepts" #PRD
url = "https://iop-partner-d.app.cfap02.atlantica.admin.ch/api/concepts"  # DEV
response = _api_post_request(url, I14Y_token, concept_data)
concept_id = response.text.strip('"')
print("Migrated Defined Variable:", DV["identifier"])
print("Status Code:", response.status_code)
print("Response Text:", response.text)

## IF it is a codelist, post the codelist as well

if DV['definedVariableType'] == "CodeList":
    # url = f"https://iop-partner.app.cfap02.atlantica.admin.ch/api/concepts/{concept_id}/codelist-entries/imports/json" #PRD
    url = f"https://iop-partner-d.app.cfap02.atlantica.admin.ch/api/concepts/{concept_id}/codelist-entries/imports/json" #DEV
    print(url)
    
    with open("SMS2_concept_importer/output/I14Y_codelistentries.json", "rb") as f:
        files = {
            "file": ("SMS2_concept_importer/output/I14Y_codelistentries.json", f, "application/json")
        }
        response = _api_post_request_file(url, I14Y_token, files)
        print("Migrated codelist:", CL["identifier"])
        print("Status Code:", response.status_code)