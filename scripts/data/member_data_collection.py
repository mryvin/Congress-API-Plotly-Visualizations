import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key and limit constants
API_KEY = os.getenv("API_KEY")
LIMIT = 250 # default 20, max 250

def get_members():
    """
    Fetches members from the API and writes their details to a JSON file.
    """
    offset = 0
    members = []

    # Fetch members in batches of size LIMIT
    while True:
        print(f"Fetching members [{offset}, {offset + LIMIT})")

        # Make API request
        r = requests.get("https://api.congress.gov/v3/member", params={"api_key": API_KEY, "offset": offset, "limit": LIMIT})

        # Check for successful request
        if r.status_code != 200:
            print("Error with API request")
            break

        # Extract member IDs
        r_members = r.json()["members"]
        if not r_members:
            break
        for r_member in r_members:
            members.append(r_member["member"]["bioguideId"])

        # Update offset for next batch
        offset += LIMIT

    # Write member IDs to file
    with open("members.json", "w") as f:
        f.write(json.dumps(members))

    # Fetch and write member details
    members_with_details = [get_member_details(member) for member in members]
    with open("members_with_details.json", "w") as f:
        f.write(json.dumps(members_with_details))

def get_member_details(bioguide_id):
    """
    Fetches and returns details for a specific member.
    """
    print(f"Fetching details for {bioguide_id}")

    # Make API request
    r = requests.get(f"https://api.congress.gov/v3/member/{bioguide_id}", params={"api_key": API_KEY})

    # Check for successful request
    if r.status_code != 200:
        print("Error with API request")
        return {}

    # Extract member details
    r_member = r.json()["member"]
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
