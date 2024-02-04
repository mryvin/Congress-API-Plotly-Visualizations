import json
import os

from dotenv import load_dotenv
import requests

### CONSTANTS
load_dotenv()
API_KEY = os.getenv("API_KEY")
LIMIT = 250 # default 20, max 250

def get_members():
    offset = 0
    members = []
    while True:
        print(f"Getting members [{offset}, {offset + LIMIT})")
        r = requests.get("https://api.congress.gov/v3/member", params={"api_key": API_KEY, "offset": offset, "limit": LIMIT})
        if r.status_code != 200:
            print("Error with API request")
        r_members = r.json()["members"]
        # print(r_members)
        if not r_members:
            break
        for r_member in r_members:
            members.append(r_member["member"]["bioguideId"])
        offset += 250
        if offset >= 500: break # TODO: remove this later

    with open("members.json", "w") as f:
        f.write(json.dumps(members))

    members_with_details = []
    for member in members:
        members_with_details.append(get_member_details(member))

    with open("members_with_details.json", "w") as f:
        f.write(json.dumps(members_with_details))

def get_member_details(bioguide_id):
    print(f"Getting details for {bioguide_id}")
    r = requests.get(f"https://api.congress.gov/v3/member/{bioguide_id}", params={"api_key": API_KEY})
    if r.status_code != 200:
        print("Error with API request")
    r_member = r.json()["member"]
    # NOTE: double check how to accurately get party, district, state
    # print(r_member)
    # print(r_member.get("terms", [{}])[-1].get("termBeginYear"))
    # print(int(r_member.get("deathYear", "2023")) - int(r_member.get("birthYear")))
    return {
        "bioguide_id": bioguide_id,
        "birth_year": r_member.get("birthYear"),
        "sponsored_legislation_count": r_member.get("sponsoredLegislation", {}).get("count"),
        "cosponsored_legislation_count": r_member.get("cosponsoredLegislation", {}).get("count"),
        "current_member": r_member.get("currentMember"),
        "death_year": r_member.get("deathYear"),
        "full_name": r_member.get("directOrderName"),
        "honorific_name": r_member.get("honorificName"),
        "first_name": r_member.get("firstName"),
        "last_name": r_member.get("lastName"),
        "party": r_member.get("partyHistory", [{}])[0].get("partyName"),
        "state": r_member.get("terms", [{}])[-1].get("stateCode"),
        "years_served": sum([x.get("termEndYear", 2023) - x["termBeginYear"] for x in r_member.get("terms")]),
        "year_of_first_term": r_member.get("terms", [{}])[0].get("termBeginYear")
    }

if __name__ == "__main__":
    get_members()
