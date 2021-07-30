import csv
import requests


url1 = "https://s3-eu-west-1.amazonaws.com/course.oc-static.com/projects/Python+FR/845+Maitrise+Algorithmes+Python/dataset1_Python+P7.csv"
url2 = "https://s3-eu-west-1.amazonaws.com/course.oc-static.com/projects/Python+FR/845+Maitrise+Algorithmes+Python/dataset2_Python+P7.csv"

def extract_csv_url(url):
    """Extract data csv into a dictionary"""
    data_url = requests.get(url)
    decoded_content = data_url.content.decode('utf-8')
    file = decoded_content.splitlines()

    cr = csv.DictReader(file, delimiter=',')
    list_shares_csv = list(cr)
    return list_shares_csv


def create_shares_csv(list_shares_csv):
    """Create shares instance from csv rows"""
    for i in range(len(list_shares_csv)):
        list_shares_csv[i]["name"] = Share(list_shares_csv[i]["name"], list_shares_csv[i]["price"], list_shares_csv[i]["profit"])


class Share:
    """Company Share class"""
    instances = []
    def __init__(self, name, price, profit, availability=True):
        self.name = name
        self.price = abs(int(float(price)*100))
        self.profit = abs(int(float(profit)*100))
        self.nominal_profit = abs(int(float(price)*100)) * abs(int(float(profit)*100)) / 100
        self.availability = availability
        self.instances.append(self)

    def __str__(self):
        return f"{self.name} - {self.price} - {self.profit} - {self.nominal_profit} - {self.availability}"

def get_list_available_shares():
    list_available_shares = []
    for share in Share.instances:
        if share.availability:
            list_available_shares.append(share)
    return list_available_shares


def create_share_from_csv(data):
    """Storing shares from csv url data in Share class"""
    for i in range(len(data)):
        list_shares[i]["share"] = Share(list_shares[i]["share"], list_shares[i]["price"], list_shares[i]["profit"])


list_shares_csv = extract_csv_url(url1)
create_shares_csv(list_shares_csv)
list_shares = get_list_available_shares()
print(len(list_shares))
