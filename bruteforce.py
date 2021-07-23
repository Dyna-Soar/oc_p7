import time
from itertools import combinations
import csv
import requests

start_time = time.time()

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


list_shares = [
    {"share": "Action-1", "price": 20, "profit": 5},
    {"share": "Action-2", "price": 30, "profit": 10},
    {"share": "Action-3", "price": 50, "profit": 15},
    {"share": "Action-4", "price": 70, "profit": 20},
    {"share": "Action-5", "price": 60, "profit": 17},
    {"share": "Action-6", "price": 80, "profit": 25},
    {"share": "Action-7", "price": 22, "profit": 7},
    {"share": "Action-8", "price": 26, "profit": 11},
    {"share": "Action-9", "price": 48, "profit": 13},
    {"share": "Action-10", "price": 34, "profit": 27},
    {"share": "Action-11", "price": 42, "profit": 17},
    {"share": "Action-12", "price": 110, "profit": 9},
    {"share": "Action-13", "price": 38, "profit": 23},
    {"share": "Action-14", "price": 14, "profit": 1},
    {"share": "Action-15", "price": 18, "profit": 3},
    {"share": "Action-16", "price": 8, "profit": 8},
    {"share": "Action-17", "price": 4, "profit": 12},
    {"share": "Action-18", "price": 10, "profit": 14},
    {"share": "Action-19", "price": 24, "profit": 21},
    {"share": "Action-20", "price": 114, "profit": 18},
]


class Share:
    """Company Share class"""
    instances = []
    def __init__(self, name, price, profit, availability=True):
        self.name = name
        self.price = price
        self.profit = profit
        self.nominal_profit = price * profit / 100
        self.availability = availability
        self.instances.append(self)

    def __str__(self):
        return f"{self.name} - {self.price} - {self.profit} - {self.nominal_profit} - {self.availability}"


class Client:
    """Client class"""
    def __init__(self, name, portfolio=[], credit=500):
        self.name = name
        self.portfolio = portfolio
        self.credit = credit


def create_share():
    for i in range(len(list_shares)):
        list_shares[i]["share"] = Share(list_shares[i]["share"], list_shares[i]["price"], list_shares[i]["profit"])



def get_list_available_shares():
    list_available_shares = []
    for share in Share.instances:
        if share.availability:
            if jean.credit >= share.price:
                list_available_shares.append(share)
    return list_available_shares


def main():
    """Main function Bruteforce"""
    list_available_shares = get_list_available_shares()
    list_combinations = []
    for r in range(1, len(list_available_shares)):
        combinations = bruteforce_simple(list_available_shares, r)
        list_combinations.extend(combinations)
    best_option = find_best_option(list_combinations)
    print(best_option)
    #print_results(best_option)


def print_results(best_option):
    """Print the best result at readable figures"""
    actions = best_option["actions"]
    profit = best_option["total_nominal_profit"]/10000
    price = best_option["total_price"]/100
    print(f"Client bought: {actions}")
    print(f"Total cost {price}")
    print(f"Total return {profit}")


def find_best_option(list_combinations):
    """Find the set of shares that returns the highest profit"""
    best_option = {"total_nominal_profit": 0, "actions": []}
    for i in range(len(list_combinations)):
        total_price = 0
        total_nominal_profit = 0
        actions = []
        for j in range(len(list_combinations[i])):
            total_nominal_profit += list_combinations[i][j].nominal_profit
            total_price += list_combinations[i][j].price
            actions.append(list_combinations[i][j].name)
        if total_price <= 500 and total_nominal_profit > best_option["total_nominal_profit"]:
            best_option["total_nominal_profit"] = total_nominal_profit
            best_option["total_price"] = total_price
            best_option["actions"] = actions
    return best_option


def bruteforce_simple(iterable, r):
    """Return a list of combinations for one index"""
    return list(combinations(iterable, r))


jean = Client("jean")
# Basic list of shares
create_share()
# Sienna shares
#list_shares_csv = extract_csv_url(url2)
#create_shares_csv(list_shares_csv)
# Main for running the algorithm
main()

print("--- %s seconds ---" % (time.time() - start_time))
