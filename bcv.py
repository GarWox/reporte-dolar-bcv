import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def get_dolar_rate():
    url = "https://www.bcv.org.ve/"
    response = requests.get(url, verify=False)
    html = response.text 

    soup = BeautifulSoup(html, "html.parser")
    usd_div = soup.find("div", {"id": "dolar"}) or soup.find("div", {"id": "dolar-ref"})
    rate = usd_div.find("strong").text.replace(",", ".")

    return round(float(rate), 4)

def get_euro_rate():
    url = "https://www.bcv.org.ve/"
    response = requests.get(url, verify=False)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    euro_div = soup.find("div", {"id": "euro"}) or soup.find("div", {"id": "euro-ref"})
    rate = euro_div.find("strong").text.replace(",", ".")

    return round(float(rate), 4)

#print(get_dolar_rate())
#print(get_euro_rate())