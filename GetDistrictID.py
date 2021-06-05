#Get State ID From GetStateID.py
import requests

headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}

#Change StateID
response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}".format(state_id = 21), headers=headers)
# print(response.status_code)
a = response.json()
print(a)

#Get Your District ID
districtName = input("Enter Your District Name : ")
def findDistrict():
  print([[districti['district_name'],districti['district_id']] for districti in a['districts'] if districtName in districti['district_name']])

findDistrict()