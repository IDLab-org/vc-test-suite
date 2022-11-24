#!/bin/python3
import os
import json
from pprint import pprint
dir_list = os.listdir("allure-results")
for filename in dir_list:
    filepath = f"allure-results/{filename}"
    with open(filepath, "r") as f:
        file_data = f.read()
    file_data = json.loads(file_data)
    if "status" in file_data:
        if file_data["status"] == "skipped":
            os.remove(filepath)