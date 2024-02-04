import json
import os

from dotenv import load_dotenv
import requests

### CONSTANTS
load_dotenv()
API_KEY = os.getenv("API_KEY")
LIMIT = 50 # default 20, max 250

def get_bills():
    offset = 0
    bills = []
    while True:
        print(f"Getting bills [{offset}, {offset + LIMIT})")
        r = requests.get("https://api.congress.gov/v3/bill", params={"api_key": API_KEY, "offset": offset, "limit": LIMIT})
        if r.status_code != 200:
            print("Error with API request")
        r_bills = r.json()["bills"]
        if not r_bills:
            break
        for r_bill in r_bills:
            bills.append({
                "congress": r_bill.get("congress"),
                "type": r_bill.get("type"),
                "number": r_bill.get("number")
            })
        offset += 250
        if offset > 50: break # TODO: remove this later

    with open("bills.json", "w") as f:
        f.write(json.dumps(bills))

    bills_with_details = []
    for bill in bills:
        bills_with_details.append(get_bill_details(bill["congress"], bill["type"], bill["number"]))
    
    for bill in bills_with_details:
        bill["actions"] = get_bill_actions(bill["congress"], bill["bill_type"], bill["bill_number"])
        bill["committees"] = get_bill_committees(bill["congress"], bill["bill_type"], bill["bill_number"])
        bill["cosponsors"] = get_bill_cosponsors(bill["congress"], bill["bill_type"], bill["bill_number"])
        bill["relatedbills"] = get_bill_relatedbills(bill["congress"], bill["bill_type"], bill["bill_number"])
        bill["subjects"] = get_bill_subjects(bill["congress"], bill["bill_type"], bill["bill_number"])

    with open("bills_with_details.json", "w") as f:
        f.write(json.dumps(bills_with_details))

def get_bill_details(congress, bill_type, bill_number):
    print(f"Getting details for {congress}/{bill_type}/{bill_number}")
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}", params={"api_key": API_KEY})
    if r.status_code != 200:
        print("Error with API request")
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

def get_bill_actions(congress, bill_type, bill_number):
    print(f"Getting actions for {congress}/{bill_type}/{bill_number}")
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/actions", params={"api_key": API_KEY})
    if r.status_code != 200:
        print("Error with API request")
    r_actions = r.json()["actions"]
    actions = []
    for action in r_actions:
        # NOTE: conflicts with actions_count if we remove dupes, review this
        action_date_type = {"date": action["actionDate"], "type": action["type"]}
        if action_date_type not in actions:
            actions.append(action_date_type)
    return actions

def get_bill_committees(congress, bill_type, bill_number):
    print(f"Getting committees for {congress}/{bill_type}/{bill_number}")
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/committees", params={"api_key": API_KEY})
    if r.status_code != 200:
        print("Error with API request")
    r_committees = r.json()["committees"]
    committees = []
    for committee in r_committees:
        committees.append({"name": committee["name"], "system_code": committee["systemCode"]})
    return committees

def get_bill_cosponsors(congress, bill_type, bill_number):
    print(f"Getting cosponsors for {congress}/{bill_type}/{bill_number}")
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/cosponsors", params={"api_key": API_KEY})
    if r.status_code != 200:
        print("Error with API request")
    r_cosponsors = r.json()["cosponsors"]
    cosponsors = []
    for cosponsor in r_cosponsors:
        cosponsors.append({"bioguide_id": cosponsor["bioguideId"], "party": cosponsor["party"], "state": cosponsor["state"], "district": cosponsor.get("district")})
    return cosponsors

def get_bill_relatedbills(congress, bill_type, bill_number):
    print(f"Getting related bills for {congress}/{bill_type}/{bill_number}")
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/relatedbills", params={"api_key": API_KEY})
    if r.status_code != 200:
        print("Error with API request")
    r_relatedbills = r.json()["relatedBills"]
    relatedbills = []
    for relatedbill in r_relatedbills:
        relatedbills.append({"related_bill_congress": relatedbill["congress"], "related_bill_number": relatedbill["number"], "related_bill_type": relatedbill["type"]})
    return relatedbills

def get_bill_subjects(congress, bill_type, bill_number):
    print(f"Getting subjects for {congress}/{bill_type}/{bill_number}")
    r = requests.get(f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/subjects", params={"api_key": API_KEY})
    if r.status_code != 200:
        print("Error with API request")
    r_subjects = r.json()["subjects"]
    subjects = {"legislative_subjects": [x["name"] for x in r_subjects["legislativeSubjects"]], "policy_area": r_subjects.get("policyArea", {}).get("name")}
    return subjects

if __name__ == "__main__":
    get_bills()
