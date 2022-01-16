import requests

# pip install requests

zipcode = input("\nEnter the zipcode : ")
url = "https://wttr.in/{}".format(zipcode)
try:
    res = requests.get(url)
    print(res.text)
except:
    print("Error occure Please try again later...")
