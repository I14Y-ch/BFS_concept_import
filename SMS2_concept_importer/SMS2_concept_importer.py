import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from typing import Optional, Dict, Any

import os
from dotenv import load_dotenv
load_dotenv()


# TODO: Create user if it does not exist

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

def _api_put_request(url: str, token) -> Optional[Dict[str, Any]]:
    """Make a PUT request to the API and return JSON response."""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    response = requests.put(url, headers=headers, verify=False)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    return response


def _api_post_request(url, token, payload):

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload, verify=False)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    return response


def _api_post_request_file(url, token, payload):

    headers = {
        "Authorization": token
    }
    response = requests.post(url, headers=headers, files=payload, verify=False)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
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

def get_Person(email: str, token, environment="DEV") -> Optional[Dict[str, Any]]:
    """gets the person metadata"""
    base_urls = {
        "DEV": f"https://dcat-d.app.cfap02.atlantica.admin.ch/api/Persons/{email}",
        "REF": f"https://dcat-r.app.cfap02.atlantica.admin.ch/api/Persons/{email}",
        "ABN": f"https://dcat-a.app.cfap02.atlantica.admin.ch/api/Persons/{email}",
        "PROD": f"https://dcat.app.cfap02.atlantica.admin.ch/api/Persons/{email}"
    }

    base_url = base_urls.get(environment.upper())
    if not base_url:
        raise ValueError(
            f"Invalid environment: {environment}. Choose from DEV, ABN, or PROD.")

    return _api_get_request(base_url, token)

def put_registrationStatus(conceptId, token, environment="DEV"):
    base_urls = {
        #"DEV": f"https://api-d.i14y.admin.ch/api/partner/v1/concepts/{conceptId}/registration-status?status=Recorded",
        #"REF": f"https://api-r.i14y.admin.ch/api/partner/v1/concepts/{conceptId}/registration-status?status=Recorded",
        #"ABN": f"https://api-a.i14y.admin.ch/api/partner/v1/concepts/{conceptId}/registration-status?status=Recorded",
        #"PROD": f"https://api.i14y.admin.ch/api/partner/v1/concepts/{conceptId}/registration-status?status=Recorded"
        "DEV": f"https://api-d.app.cfap02.atlantica.admin.ch/api/concepts/{conceptId}/registration-status?status=Recorded",
        "REF": f"https://api-r.app.cfap02.atlantica.admin.ch/api/concepts/{conceptId}/registration-status?status=Recorded",
        "ABN": f"https://api-a.app.cfap02.atlantica.admin.ch/api/concepts/{conceptId}/registration-status?status=Recorded",
        "PROD": f"https://api.app.cfap02.atlantica.admin.ch/api/concepts/{conceptId}/registration-status?status=Recorded"
    }

    base_url = base_urls.get(environment.upper())
    if not base_url:
        raise ValueError(
            f"Invalid environment: {environment}. Choose from DEV, ABN, or PROD.")

    # Put registrationStatus for concept
    response = _api_put_request(base_url, token)
    return response

def put_publicationLevel(conceptId, token, environment="DEV"):
    base_urls = {
        "DEV": f"https://api-d.app.cfap02.atlantica.admin.ch/api/concepts/{conceptId}/publication-level?level=Public",
        "REF": f"https://api-r.app.cfap02.atlantica.admin.ch/api/concepts/{conceptId}/publication-level?level=Public",
        "ABN": f"https://api-a.app.cfap02.atlantica.admin.ch/api/concepts/{conceptId}/publication-level?level=Public",
        "PROD": f"https://api.app.cfap02.atlantica.admin.ch/api/concepts/{conceptId}/publication-level?level=Public"
    }

    base_url = base_urls.get(environment.upper())
    if not base_url:
        raise ValueError(
            f"Invalid environment: {environment}. Choose from DEV, ABN, or PROD.")

    # Put registrationStatus for concept
    response = _api_put_request(base_url, token)
    return response

def post_Person(iopPerson, token, environment="DEV") -> Optional[Dict[str, Any]]:
    """gets the peron metadata"""
    base_urls = {
        "DEV": "https://dcat-d.app.cfap02.atlantica.admin.ch/api/Persons/",
        "REF": "https://dcat-r.app.cfap02.atlantica.admin.ch/api/Persons/",
        "ABN": "https://dcat-a.app.cfap02.atlantica.admin.ch/api/Persons/",
        "PROD": "https://dcat.app.cfap02.atlantica.admin.ch/api/Persons/"
    }

    base_url = base_urls.get(environment.upper())
    if not base_url:
        raise ValueError(
            f"Invalid environment: {environment}. Choose from DEV, ABN, or PROD.")

    return _api_post_request(base_url, token, iopPerson)


def extract_and_capitalize_first_name(text: str) -> str:
    # Find the position of the first period
    end_index = text.find(".")

    # If no period is found, use the whole string
    if end_index == -1:
        end_index = len(text)

    # Extract substring and capitalize the first letter
    result = text[:end_index].strip()
    return result.capitalize()


def extract_between_dot_and_at_last_name(text: str) -> str:
    start_index = text.find(".")
    end_index = text.find("@")

    # Ensure both characters are found and in the correct order
    if start_index == -1 or end_index == -1 or start_index >= end_index:
        return ""

    # Extract and clean the substring
    result = text[start_index + 1:end_index].strip()
    return result.capitalize()


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

# Create the JSON object to write to I14Y. The object is different depending on the type of the defined variable
def map_DV(DV):
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
        json.dump(CLE_data, open(
            "SMS2_concept_importer/output/I14Y_codelistentries.json", "w"), indent=4)

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
    json.dump(concept_data, open(
        "SMS2_concept_importer/output/concept.json", "w"), indent=4)
    return concept_data, CLE_data

def check_users(iopPerson, I14Y_token, environment="DEV"):
    iopPersonToCheck = get_Person(iopPerson, I14Y_token, environment)
    print(iopPersonToCheck)
    
    if iopPersonToCheck is None:
        new_iopPersonToCheck = [
            {
                "givenName": extract_between_dot_and_at_last_name(iopPerson),
                "familyName": extract_and_capitalize_first_name(iopPerson),
                "email": iopPerson
            }
        ]
        print(new_iopPersonToCheck)
        post_Person(new_iopPersonToCheck, I14Y_token, environment)
        return new_iopPersonToCheck
    else:
        print("User is found in the I14Y Database")
        return None

def post_DV(concept_data, CLE_data, DV, I14Y_token, environment="DEV"):
    base_urls = {
        "DEV": "https://iop-partner-d.app.cfap02.atlantica.admin.ch/api/concepts",
        "REF": "https://iop-partner-r.app.cfap02.atlantica.admin.ch/api/concepts",
        "ABN": "https://iop-partner-a.app.cfap02.atlantica.admin.ch/api/concepts",
        "PROD": "https://iop-partner.app.cfap02.atlantica.admin.ch/api/concepts"
    }

    base_url = base_urls.get(environment.upper())
    if not base_url:
        raise ValueError(
            f"Invalid environment: {environment}. Choose from DEV, ABN, or PROD.")

    # Post concept data
    response = _api_post_request(base_url, I14Y_token, concept_data)
    concept_id = response.text.strip('\"')

    print("Migrated Defined Variable:", DV["identifier"])
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    # If it's a CodeList, post the codelist entries
    if DV['definedVariableType'] == "CodeList":
        url = f"{base_url}/{concept_id}/codelist-entries/imports/json"
        print(url)

        with open("SMS2_concept_importer/output/I14Y_codelistentries.json", "rb") as f:
            files = {
                "file": ("SMS2_concept_importer/output/I14Y_codelistentries.json", f, "application/json")
            }
            response = _api_post_request_file(url, I14Y_token, files)
            print("Migrated codelist:", DV["codeListId"])
            print("Status Code:", response.status_code)
    return concept_id


def Copy_DV_to_I14Y(dv_id, SMS2_token, I14Y_token, I14Y_environment="DEV"):
    #Get the DV from SMS2
    DV = get_DV(dv_id, SMS2_token)

    # Map the DV to objects compatible with I14Y
    concept_data, CLE_data = map_DV(DV)

    # Check if the users exist in the I14Y database, and create the user if it does not exist
    check_users(iopPerson = DV["responsibleDeputy"]["identifier"], I14Y_token = I14Y_token, environment=I14Y_environment)
    check_users(iopPerson = DV["responsiblePerson"]["identifier"], I14Y_token = I14Y_token, environment=I14Y_environment)

    # Post the new objects to I14Y
    concept_id = post_DV(concept_data, CLE_data, DV, I14Y_token,
            environment=I14Y_environment)
    
    return concept_id

# Variables
SMS2_token = os.environ.get("SMS2_token")
I14Y_token = os.environ.get("I14Y_token") # requires IOS token
I14Y_environment="DEV" # or "REF", "ABN", "PROD"

dv_id = "08d9e176-b0cf-c0fe-abab-861d6026f0ac"# LAND_TRADE_PARTNER
# dv_id = "08dac62e-ab42-57fc-8db1-9e36ad2655c1" # DV_COM_CHANNEL_EUROPASS

concept_id = Copy_DV_to_I14Y(dv_id, SMS2_token, I14Y_token, I14Y_environment=I14Y_environment)

response = put_registrationStatus(concept_id, I14Y_token, environment="DEV")
print(response.text)
put_publicationLevel(concept_id, I14Y_token, environment="DEV")