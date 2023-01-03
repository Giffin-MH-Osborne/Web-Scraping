import geocoder
import json

def write_user_data():
    geo_data = geocoder.ip('me')

    file = open('user.txt', 'w')

    address = geo_data.address.split(',')

    user_data = {
    "IP": geo_data.ip, 
    "Locale": geo_data.latlng, 
    "City": address[0],
    "Province": address[1].strip()
    }

    user_data_json = json.dumps(user_data, indent=4)

    print(user_data_json)

    file.write(user_data_json)