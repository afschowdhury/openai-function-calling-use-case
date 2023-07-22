import json


def get_branch_names():
    with open("db/store_info.json", "r") as file:
        data = json.load(file)

    branch_names = []
    stores = data["Stores"]
    for store in stores:
        branches = store["branches"]
        for branch in branches:
            branch_name = (
                branch["branch_name"]
                if "branch_name" in branch
                else list(branch.keys())[0]
            )
            branch_names.append(branch_name)

    return json.dumps({"branch_locations": branch_names})


def get_delivery_areas(branch_name=None):
    with open("db/store_info.json", "r") as file:
        data = json.load(file)

    delivery_areas = []

    stores = data["Stores"]
    for store in stores:
        branches = store["branches"]
        for branch in branches:
            if branch_name:
                if branch_name in branch or branch.get("branch_name") == branch_name:
                    delivery_location = branch[branch_name]["Delivery Location"]
                    delivery_areas.extend(
                        [list(location.keys())[0] for location in delivery_location]
                    )
            else:
                delivery_location = list(branch.values())[0]["Delivery Location"]
                delivery_areas.extend(
                    [list(location.keys())[0] for location in delivery_location]
                )

    return json.dumps({"delivery_areas": delivery_areas})


def extract_menu(branch_name):
    with open("db/store_info.json", "r") as file:
        data = json.load(file)
    for store in data["Stores"]:
        for branch in store["branches"]:
            for branch_key in branch:
                if branch_key.lower() == branch_name.lower():
                    return json.dumps({"menu": store["menu"]})
    return "invalid branch_name"


function_descriptions = [
    {
        "name": "get_delivery_areas",
        "description": "Get the delivery areas for a given branch or all branches if no branch name is specified and validate the delivery location asked by user",
        "parameters": {
            "type": "object",
            "properties": {
                "branch_name": {
                    "type": "string",
                    "description": "The name of the branch. It is optional parameter",
                }
            },
        },
    },
    {
        "name": "get_branch_names",
        "description": "Get the names of all branches in the store and validate for branch locations asked by user",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "extract_menu",
        "description": "Get the menu and validate if a food item is available or not from the menu",
        "parameters": {
            "type": "object",
            "properties": {
                "branch_name": {
                    "type": "string",
                    "description": "branch name whose menu is requested",
                }
            },
            "required": ["branch_name"],
        },
    },
]
