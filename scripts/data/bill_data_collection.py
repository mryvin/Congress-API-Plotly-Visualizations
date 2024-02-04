import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key and limit constants
API_KEY = os.getenv("API_KEY")
LIMIT = 50 # default 20, max 250

###############################################################################################################################################################
##### Bills
###############################################################################################################################################################

def get_bills():
    """
    Fetches bills from the API and writes their details to a JSON file.
    """
    offset = 0
    bills = []

    # Fetch bills in batches of size LIMIT
    while True:
        print(f"Fetching bills [{offset}, {offset + LIMIT})")

        # Make API request
        r = requests.get("https://api.congress.gov/v3/bill", params={"api_key": API_KEY, "offset": offset, "limit": LIMIT})

        # Check for successful request
        if r.status_code != 200:
            print("Error with API request")
            break

        # Extract bill details
        r_bills = r.json()["bills"]
        if not r_bills:
            break
        for r_bill in r_bills:
            bills.append({
                "congress": r_bill.get("congress"),
                "type": r_bill.get("type"),
                "number": r_bill.get("number")
            })

        # Update offset for next batch
        offset += LIMIT

    # Write bill details to file
    with open("bills.json", "w") as f:
        f.write(json.dumps(bills))

    # Fetch and write detailed bill information
    bills_with_details = [get_bill_details(bill["congress"], bill["type"], bill["number"]) for bill in bills]
    with open("bills_with_details.json", "w") as f:
        f.write(json.dumps(bills_with_details))

###############################################################################################################################################################
##### Bill Details
###############################################################################################################################################################

def get_bill_details(congress, bill_type, bill_number):
    """
    Fetches and returns details for a specific bill.
    """
    print(f"Fetching details for {congress}/{bill_type}/{bill_number}")

    # Make API request
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}", params={"api_key": API_KEY})

    # Check for successful request
    if r.status_code != 200:
        print("Error with API request")
        return {}

    # Extract bill details
    r_bill = r.json()["bill"]
    return {
        "actions_count": r_bill.get("actions", {}).get("count"),
        "amendments_count": r_bill.get("amendments", {}).get("count"),
        "committees_count": r_bill.get("committees", {}).get("count"),
        "cosponsors_count": r_bill.get("cosponsors", {}).get("count"),
        "introduced_date": r_bill.get("introducedDate"),
        "latest_action_date": r_bill.get("latestAction", {}).get("actionDate"),
        "latest_action_text": r_bill.get("latestAction", {}).get("text"),
        "origin_chamber": r_bill.get("originChamber"),
        "policy_area": r_bill.get("policyArea", {}).get("name"),
        "related_bills_count": r_bill.get("relatedBills", {}).get("count"),
        "sponsors": [{"bioguideId": s.get("bioguideId"), "party": s.get("party"), "state": s.get("state"), "district": s.get("district")} for s in r_bill.get("sponsors")],
        "subjects_count": r_bill.get("subjects", {}).get("count"),
        "text_versions_count": r_bill.get("textVersions", {}).get("count"),
        "title": r_bill.get("title"),
        "title_count": r_bill.get("titles", {}).get("count"),
        "congress": congress,
        "bill_type": bill_type,
        "bill_number": bill_number
    }

###############################################################################################################################################################
##### Bill Actions
###############################################################################################################################################################

def get_bill_actions(congress, bill_type, bill_number):
    """
    Fetches and returns actions for a specific bill.
    """
    print(f"Fetching actions for {congress}/{bill_type}/{bill_number}")

    # Make API request
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/actions", params={"api_key": API_KEY})

    # Check for successful request
    if r.status_code != 200:
        print("Error with API request")
        return []

    # Extract and return action details
    r_actions = r.json()["actions"]
    return [{"date": action["actionDate"], "type": action["type"]} for action in r_actions]

###############################################################################################################################################################
##### Bill Committees
###############################################################################################################################################################

def get_bill_committees(congress, bill_type, bill_number):
    """
    Fetches and returns committees for a specific bill.
    """
    print(f"Fetching committees for {congress}/{bill_type}/{bill_number}")

    # Make API request
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/committees", params={"api_key": API_KEY})

    # Check for successful request
    if r.status_code != 200:
        print("Error with API request")
        return []

    # Extract and return committee details
    r_committees = r.json()["committees"]
    return [{"name": committee["name"], "system_code": committee["systemCode"]} for committee in r_committees]

###############################################################################################################################################################
##### Bill Cosponsors
###############################################################################################################################################################

def get_bill_cosponsors(congress, bill_type, bill_number):
    """
    Fetches and returns cosponsors for a specific bill.
    """
    print(f"Fetching cosponsors for {congress}/{bill_type}/{bill_number}")

    # Make API request
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/cosponsors", params={"api_key": API_KEY})

    # Check for successful request
    if r.status_code != 200:
        print("Error with API request")
        return []

    # Extract and return cosponsor details
    r_cosponsors = r.json()["cosponsors"]
    return [{"bioguide_id": cosponsor["bioguideId"], "party": cosponsor["party"], "state": cosponsor["state"], "district": cosponsor.get("district")} for cosponsor in r_cosponsors]

###############################################################################################################################################################
##### Related Bills
###############################################################################################################################################################

def get_bill_relatedbills(congress, bill_type, bill_number):
    """
    Fetches and returns related bills for a specific bill.
    """
    print(f"Fetching related bills for {congress}/{bill_type}/{bill_number}")

    # Make API request
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/relatedbills", params={"api_key": API_KEY})

    # Check for successful request
    if r.status_code != 200:
        print("Error with API request")
        return []

    # Extract and return related bill details
    r_relatedbills = r.json()["relatedBills"]
    return [{"related_bill_congress": relatedbill["congress"], "related_bill_number": relatedbill["number"], "related_bill_type": relatedbill["type"]} for relatedbill in r_relatedbills]

###############################################################################################################################################################
##### Bill Subjects
###############################################################################################################################################################

def get_bill_subjects(congress, bill_type, bill_number):
    """
    Fetches and returns subjects for a specific bill.
    """
    print(f"Fetching subjects for {congress}/{bill_type}/{bill_number}")

    # Make API request
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/subjects", params={"api_key": API_KEY})

    # Check for successful request
    if r.status_code != 200:
        print("Error with API request")
        return {}

    # Extract and return subject details
    r_subjects = r.json()["subjects"]
    return {"legislative_subjects": [x["name"] for x in r_subjects["legislativeSubjects"]], "policy_area": r_subjects.get("policyArea", {}).get("name")}

if __name__ == "__main__":
    get_bills()
