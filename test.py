from bs4 import BeautifulSoup
import requests
url='https://en.wikipedia.org/wiki/Python_(programming_language)'
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/137.0.0.0 Safari/537.36",
}

response=requests.get(url,headers=headers)
soup=BeautifulSoup(response.text,'html.parser')
table=soup.find(class_='wikitable')
body=table.find('tbody')
rows=body.find_all('tr')[1:]
mutable_type=[]
imutable_type=[]
for row in rows:
    data=row.find_all('td')
    if data[1].get_text() == "mutable\n":
        mutable_type.append(data[0].get_text().strip())
    else:
        imutable_type.append(data[0].get_text().strip())

print("Mutable Data Types in Python:", mutable_type)  
print("Immutable Data Types in Python:", imutable_type)
