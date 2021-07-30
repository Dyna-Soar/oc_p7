import csv
import requests
import time


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
        self.price = abs(int(float(price)*100))
        self.profit = abs(int(float(profit)*100))
        self.nominal_profit = abs(int(float(price)*100)) * abs(int(float(profit)*100)) / 100
        self.availability = availability
        self.instances.append(self)

    def __str__(self):
        return f"{self.name} - {self.price} - {self.profit} - {self.nominal_profit} - {self.availability}"


class Client:
    """Client class"""
    def __init__(self, name, portfolio=[], credit=500*100):
        self.name = name
        self.portfolio = portfolio
        self.credit = credit

# Intent is to get the highest profit over 2 years starting with 500€ investment


def create_share():
    for i in range(len(list_shares)):
        list_shares[i]["share"] = Share(list_shares[i]["share"], list_shares[i]["price"], list_shares[i]["profit"])


# V2 ALGORITHM

def get_list_available_shares():
    list_available_shares = []
    for share in Share.instances:
        if share.availability:
            list_available_shares.append(share)
    return list_available_shares


def sort_list_available_shares(list_available_shares):
    """Bubble sort algorithm"""
    infinite_loop_activated = True
    while infinite_loop_activated:
        nb_permutations = 0
        for i in range(1, len(list_available_shares)):
            #if list_available_shares[i-1].nominal_profit < list_available_shares[i].nominal_profit:
            if list_available_shares[i - 1].profit < list_available_shares[i].profit:
                permuted_share = list_available_shares[i-1]
                list_available_shares[i-1] = list_available_shares[i]
                list_available_shares[i] = permuted_share
                nb_permutations += 1
            if i == len(list_available_shares)-1 and nb_permutations == 0:
                infinite_loop_activated = False
    return list_available_shares


def get_list_share_by_price(list_available_shares):
    """Get a list of shares by descending price"""
    list_share_by_price = []
    infinite_loop_activated = True
    while infinite_loop_activated:
        nb_permutations = 0
        for i in range(1, len(list_available_shares)):
            if list_available_shares[i - 1].price < list_available_shares[i].price:
                permuted_share = list_available_shares[i - 1]
                list_available_shares[i - 1] = list_available_shares[i]
                list_available_shares[i] = permuted_share
                nb_permutations += 1
            if i == len(list_available_shares) - 1 and nb_permutations == 0:
                infinite_loop_activated = False
    return list_available_shares



class Cell_item:
    """cell_item Share class"""
    instances = []
    def __init__(self, item_reference, credit, remaining_profit, profit, actions = []):
        self.item_reference = item_reference
        self.actions = actions
        self.credit = credit
        self.remaining_profit = remaining_profit
        self.profit = profit
        self.instances.append(self)


def knapsack_v2():
    """Knapsack method v2"""
    cell_item = {"item_reference": "", "actions": [], "credit": "", "remaining_credit": "", "profit": ""}
    list_shares = get_list_available_shares()
    list_shares = get_list_share_by_price(list_shares)
    previous_list = loop_first_share_set(list_shares, cell_item)
    current_list = loop_share_set(list_shares, cell_item, previous_list)
    solution = current_list[-1]
    print(solution)
    cash_profit = profit_in_cash(solution, list_shares)
    cash_profit = cash_profit/10000
    solution = solution["price"]/100
    solution_shares = current_list[-1]["actions"]
    print(f"Client bought: {solution_shares}")
    print(f"Total Cost: {solution}")
    print(f"Total Return: {cash_profit}")


def total_money_after(solution, cash_profit):
    "Calculate the total return after 2 years"
    total_money = solution["remaining_credit"] + solution["price"] + cash_profit
    return total_money


def profit_in_cash(solution, list_shares):
    """Return total profit"""
    cash_profit = 0
    for share in solution["actions"]:
        for set_share in list_shares:
            if share == set_share.name:
                cash_profit += set_share.price * set_share.profit / 100
    return cash_profit


def loop_first_share_set(list_shares, cell_item):
    """Loop credit only for the first share"""
    previous_list = []
    # Loop every credit from 0 to 500
    for credit in range(jean.credit+1):
        cell_item = {"item_reference": "", "actions": [], "credit": "", "remaining_credit": "", "profit": "", "return_profit": ""}
        # if share price is less expensive append it to the solution
        if list_shares[0].price <= credit:
            cell_item["item_reference"] = list_shares[0].name
            cell_item["actions"].append(list_shares[0].name)
            cell_item["credit"] = credit
            cell_item["remaining_credit"] = credit-list_shares[0].price
            cell_item["profit"] = list_shares[0].profit
            cell_item["price"] = list_shares[0].price
            cell_item["return_profit"] = list_shares[0].profit * list_shares[0].price / 100
        else:
            cell_item["item_reference"] = list_shares[0].name
            cell_item["credit"] = credit
            cell_item["remaining_credit"] = credit
            cell_item["profit"] = 0
            cell_item["price"] = 0
            cell_item["return_profit"] = 0
        previous_list.append(cell_item)
    return previous_list


def build_temporary_cell(share, credit):
    """Build temporary first cell"""
    cell_item = {"item_reference": "", "actions": [], "credit": "", "remaining_credit": "", "profit": "", "return_profit": ""}
    if share.price <= credit:
        cell_item["item_reference"] = share.name
        cell_item["actions"].append(share.name)
        cell_item["credit"] = credit
        cell_item["remaining_credit"] = credit - share.price
        cell_item["profit"] = share.profit
        cell_item["price"] = share.price
        cell_item["return_profit"] = share.price * share.profit / 100
    else:
        cell_item["item_reference"] = share.name
        cell_item["credit"] = credit
        cell_item["remaining_credit"] = credit
        cell_item["profit"] = 0
        cell_item["price"] = 0
        cell_item["return_profit"] = 0
    return cell_item


def loop_share_set(list_shares, cell_item, previous):
    """Loop all shares minus the first one"""
    previous_list = previous
    for share in list_shares[1:]:
        current_list = []
        for credit in range(jean.credit+1):
            cell_item = build_temporary_cell(share, credit)
            cell_item = build_cl1_pl2(cell_item, previous_list[cell_item["remaining_credit"]])
            cell_item_up = build_pl1(previous_list[cell_item["credit"]], share)
            best_option = compare_both_option(cl1_pl2=cell_item, pl2=cell_item_up)
            current_list.append(best_option)
        previous_list = current_list
    return previous_list


def build_cl1_pl2(cell_item, pl2):
    """Build cell with current cell 1 and item of previous list"""
    cell_item["actions"].extend(pl2["actions"])
    cell_item["remaining_credit"] -= pl2["price"]
    cell_item["profit"] += pl2["profit"]
    cell_item["price"] += pl2["price"]
    cell_item["return_profit"] += pl2["return_profit"]
    return cell_item


def build_pl1(pl1, share):
    """Build cell with previous list 1 by changing item reference"""
    cell_item_up = pl1
    cell_item_up["item_reference"] = share.name
    return cell_item_up


def compare_both_option(cl1_pl2, pl2):
    """Compare two options by return profit after 2 years"""
    if cl1_pl2["return_profit"] > pl2["return_profit"]:
        return cl1_pl2
    else:
        return pl2


def create_share_from_csv(data):
    """Storing shares from csv url data in Share class"""
    for i in range(len(data)):
        list_shares[i]["share"] = Share(list_shares[i]["share"], list_shares[i]["price"], list_shares[i]["profit"])


jean = Client("jean")
#create_share()
list_shares_csv = extract_csv_url(url2)
create_shares_csv(list_shares_csv)

# V4 Knapsack V2
knapsack_v2()
print("--- %s seconds ---" % (time.time() - start_time))