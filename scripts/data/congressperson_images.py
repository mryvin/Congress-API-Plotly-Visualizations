import json
new_data = [

]

with open('members_with_details_all_updated.json', 'w') as f:
    json.dump(new_data, f)

import json
import requests
from bs4 import BeautifulSoup
import math

#############################################################################################################################################################################
##### State Name Abbreviation Function
#############################################################################################################################################################################

def get_state_name(state_code):
    """
    Returns the full name of a state given its abbreviation.
    """
    # Dictionary mapping state abbreviations to full names
    us_state_abbrev = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming',
        'AS': 'American Samoa',
        'DC': 'D.C.',
        'PR': 'Puerto Rico',
        'VI': 'U.S. Virgin Islands',
        'GU': 'Guam',
        'TT': 'Trust Territories'
    }
    return us_state_abbrev.get(state_code.upper())

#############################################################################################################################################################################
##### Collect Member Photos
#############################################################################################################################################################################
      
# Load the JSON file
with open('members_with_details_all.json', 'r') as f:
    data = json.load(f)  

success = 0
failure = 0

# Iterate over the data in chunks of 100
for i in range(math.ceil(len(data)/100)):
    min_index = i * 100
    max_index = min_index + 100 if i < 25 else 2515

    with open('members_with_details_all_updated.json', 'r') as f:
        new_data = json.load(f)  

    # Iterate over each object in the current chunk
    for obj in data[min_index:max_index]:
        full_name = f"{obj['first_name']} {obj['last_name']}"
        state = get_state_name(obj['state'])

        # Define the possible Wikipedia URL formats
        url_formats = [
            f'https://en.wikipedia.org/wiki/{full_name.replace(" ", "_")}',
            f'https://en.wikipedia.org/wiki/{full_name.replace(" ", "_")}_(politician)',
            f'https://en.wikipedia.org/wiki/{full_name.replace(" ", "_")}_(U.S._Senator)'
        ]

        # Try each URL format until a valid Wikipedia page is found
        for url_format in url_formats:
            response = requests.get(url_format)
            soup = BeautifulSoup(response.text, 'html.parser')
            infobox = soup.find('table', class_='infobox')

            if infobox:
                image_element = infobox.find('img')

                if image_element:
                    main_image_url = f'http:{image_element["src"]}'
                    main_image_url = main_image_url.rsplit('.', 1)[0] + '.jpg'  # Ensure it ends with jpg

                    obj['photo'] = main_image_url
                    success += 1
                else:
                    print(f"No main image found in the infobox for {full_name}.")
                    obj['photo'] = ""
                    failure += 1

                break  # Exit the loop if infobox found

        else:
            print(f"No article found for {full_name}.")
            obj['photo'] = ""
            failure += 1

        new_data.append(obj)

    # Write the updated data to a new JSON file
    with open('members_with_details_all_updated.json', 'w') as f:
        json.dump(new_data, f)

#############################################################################################################################################################################
##### Add the Missing Photos
#############################################################################################################################################################################
          
with open('members_with_details_all_updated.json') as f:
    data = json.load(f)

for item in data:
    if 'photo' not in item:
        item['photo'] = ""

# write the updated data back to the file
with open('members_with_details_all_updated.json', 'w') as f:
    json.dump(data, f)

import json

# Load data from the original JSON file
with open('members_with_details_all_updated.json', 'r') as f:
    data = json.load(f)

# Define a dictionary for bioguide_id to photo mapping
bioguide_id_to_photo = {
    'V000137': 'https://upload.wikimedia.org/wikipedia/commons/8/83/Senator_Vance_official_portrait._118th_Congress.jpg',
    'R000122': 'https://upload.wikimedia.org/wikipedia/commons/d/d8/Jack_Reed_official_photo_%28cropped%29.jpg',
    'M001169': 'https://upload.wikimedia.org/wikipedia/commons/4/47/Chris_Murphy%2C_official_portrait%2C_113th_Congress_%28cropped%29.jpg',
    'L000570': 'https://upload.wikimedia.org/wikipedia/commons/b/b5/Ben_Ray_Lujan%2C_117th_Congress_portrait_2.jpg',
    'D000563': 'https://upload.wikimedia.org/wikipedia/commons/4/49/Dick_Durbin_117th_Congress_portrait_%281%29_%28cropped%29.jpeg',
    'C001070': 'https://commons.wikimedia.org/wiki/File:Bob_Casey_Jr._official_photo.jpg',
    'O000175': 'https://upload.wikimedia.org/wikipedia/commons/3/3b/Congressman_Andy_Ogles_2022.jpg',
    'N000193': 'https://upload.wikimedia.org/wikipedia/commons/0/05/Rep._Zach_Nunn_official_photo%2C_118th_Congress.jpg',
    'M001218': 'https://commons.wikimedia.org/wiki/File:Rep._Rich_McCormick_official_photo,_118th_Congress_(1).jpg',
    'L000600': 'https://upload.wikimedia.org/wikipedia/commons/c/cb/Nick_langworthy_portrait.jpg',
    'G000599': 'https://upload.wikimedia.org/wikipedia/commons/d/db/Daniel_Goldman_Portrait.jpg',
    'D000530': 'https://upload.wikimedia.org/wikipedia/commons/1/1b/Rep._Chris_Deluzio_-_118th_Congress.jpg',
    'C001132': 'https://upload.wikimedia.org/wikipedia/commons/2/2a/Rep._Eli_Crane_official_photo%2C_118th_Congress.jpg',
    'M000687': 'https://upload.wikimedia.org/wikipedia/commons/b/ba/Kweisi_Mfume%2C_official_portrait%2C_116th_Congress.jpg',
    'R000579': 'https://upload.wikimedia.org/wikipedia/commons/a/a8/Pat_Ryan_117th_Congress_portrait.jpeg',
    'S000168': 'https://upload.wikimedia.org/wikipedia/commons/e/e0/REP.MES_Headshot_%28cropped_2%29.jpg',
    'M001214': 'https://upload.wikimedia.org/wikipedia/commons/6/6a/Frank_Mrvan_117th_U.S_Congress.jpg',
    'G000593': 'https://upload.wikimedia.org/wikipedia/commons/e/ee/Rep._Carlos_Gimenez_official_photo%2C_117th_Congress.jpg',
    'F000472': 'https://upload.wikimedia.org/wikipedia/commons/6/64/Scott_Franklin%2C_117th_Congress_portrait.jpg',
    'T000165': 'https://upload.wikimedia.org/wikipedia/commons/d/d6/Tom_Tiffany.jpg',
    'M001210': 'https://upload.wikimedia.org/wikipedia/commons/f/fe/Rep._Greg_Murphy_116th_Congress_Portrait.jpg',
    'G000586': 'https://upload.wikimedia.org/wikipedia/commons/1/17/Chuy_Garcia_official_portrait.jpg',
    'S001214': 'https://upload.wikimedia.org/wikipedia/commons/5/57/Greg_Steube_117th_Congress.jpeg',
    'S001205': 'https://upload.wikimedia.org/wikipedia/commons/7/75/Mary_Gay_Scanlon%2C_official_portrait%2C_2018.jpg',
    'G000582': 'https://upload.wikimedia.org/wikipedia/commons/7/7a/Official_portrait_of_Resident_Commissioner_Jenniffer_Gonzalez.jpg',
    'F000466': 'https://upload.wikimedia.org/wikipedia/commons/3/3a/Brian_Fitzpatrick_official_congressional_photo.jpg',
    'F000465': 'https://upload.wikimedia.org/wikipedia/commons/e/e3/Drew_Ferguson_115th_Congress_2.jpeg',
    'C001110': 'https://upload.wikimedia.org/wikipedia/commons/3/30/J._Luis_Correa.jpg',
    'C001103': 'https://upload.wikimedia.org/wikipedia/commons/7/7b/Buddy_Carter%2C_Official_Portrait%2C_115th_Congress.jpg',
    'C001091': 'https://upload.wikimedia.org/wikipedia/commons/d/d5/Photo_of_Joaquin_Castro.jpg',
    'B001314': 'https://upload.wikimedia.org/wikipedia/commons/9/9a/Official_portrait_of_Resident_Commissioner_Jenniffer_Gonzalez.jpg',
    'A000360': 'https://upload.wikimedia.org/wikipedia/commons/5/5f/Mark_Amodei_Official_Portrait.jpg',
    'A000372': 'https://upload.wikimedia.org/wikipedia/commons/d/d0/Rep._Colin_Allred_official_portrait%2C_116th_Congress_%28cropped%29.jpg',
    'A000370': 'https://upload.wikimedia.org/wikipedia/commons/d/d0/Jodey_Arrington_official_portrait_%28cropped%29.jpg',
    'B001312': 'https://upload.wikimedia.org/wikipedia/commons/e/e3/James_R._Baird_115th_Congress_photo.jpg',
    'B001311': 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Troy_Balderson%2C_official_portrait%2C_116th_Congress_%28cropped%29.jpg',
    'B001290': 'https://upload.wikimedia.org/wikipedia/commons/4/48/Rep_Brandon_Banker.jpg',
    'B001281': 'https://upload.wikimedia.org/wikipedia/commons/3/3a/Lou_Barletta%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001278': 'https://upload.wikimedia.org/wikipedia/commons/2/21/Moe_Barnes_116th_Congress_portrait.jpg',
    'B001275': 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Joyce_Beatty_Official_Congressional_Portrait_%28cropped%29.jpg',
    'B001274': 'https://upload.wikimedia.org/wikipedia/commons/e/e1/Donald_Bacon%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001273': 'https://upload.wikimedia.org/wikipedia/commons/7/76/Aumua_Amata_Radewagen_official_portrait_%28cropped%29.jpg',
    'B001272': 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Buddy_Carter%2C_Official_Portrait%2C_115th_Congress.jpg',
    'B001270': 'https://upload.wikimedia.org/wikipedia/commons/4/47/Sanford_Bishop%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001269': 'https://upload.wikimedia.org/wikipedia/commons/6/63/Earl_Blumenauer%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001256': 'https://upload.wikimedia.org/wikipedia/commons/d/d2/Mark_Begich.jpg',
    'B001255': 'https://upload.wikimedia.org/wikipedia/commons/7/70/Ami_Bera%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001250': 'https://upload.wikimedia.org/wikipedia/commons/c/c2/Lou_Barletta%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001248': 'https://upload.wikimedia.org/wikipedia/commons/e/e3/John_Barrasso_official_portrait_112th_Congress.jpg',
    'B001245': 'https://upload.wikimedia.org/wikipedia/commons/c/ca/Andy_Barr_official_portrait_113th_Congress.jpg',
    'B001242': 'https://upload.wikimedia.org/wikipedia/commons/f/fb/Marsha_Blackburn_official_portrait_112th_Congress.jpg',
    'B001240': 'https://upload.wikimedia.org/wikipedia/commons/c/cf/Rodney_Blum%2C_Official_Portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001237': 'https://upload.wikimedia.org/wikipedia/commons/c/ca/Suzanne_Bonamici%2C_Official_Portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001236': 'https://upload.wikimedia.org/wikipedia/commons/4/45/Joaquin_Castro%2C_115th_Congress_official_photo_%28cropped%29.jpg',
    'B001234': 'https://upload.wikimedia.org/wikipedia/commons/7/70/Rob_Bishop%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001233': 'https://upload.wikimedia.org/wikipedia/commons/e/e5/Gus_Bilirakis%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001232': 'https://upload.wikimedia.org/wikipedia/commons/8/8a/Earl_Blumenauer%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001230': 'https://upload.wikimedia.org/wikipedia/commons/f/fe/Gus_Bilirakis%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001229': 'https://upload.wikimedia.org/wikipedia/commons/8/8a/Earl_Blumenauer%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001227': 'https://upload.wikimedia.org/wikipedia/commons/8/80/Tom_Brady_official_photo_%28cropped%29.jpg',
    'B001226': 'https://upload.wikimedia.org/wikipedia/commons/1/18/Susan_Brooks_official_photo_%28cropped%29.jpg',
    'B001225': 'https://upload.wikimedia.org/wikipedia/commons/7/71/Dave_Bratt_official_portrait_114th_Congress_%28cropped%29.jpg',
    'B001224': 'https://upload.wikimedia.org/wikipedia/commons/3/30/Kevin_Brady_official_portrait_%28cropped%29.jpg',
    'B001223': 'https://upload.wikimedia.org/wikipedia/commons/5/50/Anthony_Brown%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001222': 'https://upload.wikimedia.org/wikipedia/commons/f/f9/Sherrod_Brown_official_portrait_%28cropped%29.jpg',
    'B001243': 'https://upload.wikimedia.org/wikipedia/commons/6/65/Marsha_Blackburn_official_portrait%2C_115th_Congress.jpg',
    'B001206': 'https://upload.wikimedia.org/wikipedia/commons/d/d9/Rodney_Blum%2C_Official_Portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001205': 'https://upload.wikimedia.org/wikipedia/commons/c/c7/David_Beauregard_2015.jpg',
    'B001204': 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Andy_Barr_official_portrait_%28cropped%29.jpg',
    'B001270': 'https://upload.wikimedia.org/wikipedia/commons/4/47/Sanford_Bishop%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001269': 'https://upload.wikimedia.org/wikipedia/commons/6/63/Earl_Blumenauer%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001268': 'https://upload.wikimedia.org/wikipedia/commons/3/39/Tom_Brady_official_photo_%28cropped%29.jpg',
    'B001267': 'https://upload.wikimedia.org/wikipedia/commons/1/18/Susan_Brooks_official_photo_%28cropped%29.jpg',
    'B001266': 'https://upload.wikimedia.org/wikipedia/commons/7/71/Dave_Bratt_official_portrait_114th_Congress_%28cropped%29.jpg',
    'B001265': 'https://upload.wikimedia.org/wikipedia/commons/3/30/Kevin_Brady_official_portrait_%28cropped%29.jpg',
    'B001264': 'https://upload.wikimedia.org/wikipedia/commons/5/50/Anthony_Brown%2C_official_portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001263': 'https://upload.wikimedia.org/wikipedia/commons/f/f9/Sherrod_Brown_official_portrait_%28cropped%29.jpg',
    'B001262': 'https://upload.wikimedia.org/wikipedia/commons/6/65/Marsha_Blackburn_official_portrait%2C_115th_Congress.jpg',
    'B001260': 'https://upload.wikimedia.org/wikipedia/commons/d/d9/Rodney_Blum%2C_Official_Portrait%2C_115th_Congress_%28cropped%29.jpg',
    'B001259': 'https://upload.wikimedia.org/wikipedia/commons/c/c7/David_Beauregard_2015.jpg',
    'B001258': 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Andy_Barr_official_portrait_%28cropped%29.jpg',
}

# Iterate through the data and update photos based on bioguide_id
for item in data:
    bioguide_id = item.get('bioguide_id', '')
    
    # Update photos based on bioguide_id
    if item.get('current_member') == True:
        if bioguide_id in bioguide_id_to_photo:
            item['photo'] = bioguide_id_to_photo[bioguide_id]

# Save the updated JSON file
with open('members_with_details_all_updated2.json', 'w') as f:
    json.dump(data, f)

