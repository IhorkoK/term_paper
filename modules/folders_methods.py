import requests
from faker import Faker
fake = Faker()
myHeaders = {"Authorization": "pk_188609355_7L8T8DOVKGMEJW1K7YBPN7TB8IUPPDIJ"}
# workspaceID = 90151250171
spaceID = 90154394169


def get_folders():
    result = requests.get("https://api.clickup.com/api/v2/space/" + str(spaceID) + "/folder", headers = myHeaders)
    assert result.status_code == 200
    print(result)
    print(result.text)
    print("Test passed")
    return result
    # assert result.json()["lists"][0]["name"] == "Russell.Gorczany"
    # print("Test 2 passed")

def get_folder_by_id(folder_id):
    result = requests.get("https://api.clickup.com/api/v2/folder/" + folder_id, headers = myHeaders)
    # assert result.status_code == 200
    print(result)
    print(result.text)
    return result

def create_folder():
    random_name = fake.name()
    body = {
        "name": random_name
    }
    result = requests.post("https://api.clickup.com/api/v2/space/" + str(spaceID) + "/folder", headers = myHeaders, json = body)
    assert result.status_code == 200
    print(result)
    print(result.text)
    return result

def delete_folder(folder_id):
    result = requests.delete("https://api.clickup.com/api/v2/folder/" + folder_id, headers = myHeaders)
    print(result)
    print(result.text)
    return result

def update_folder(folder_id, updated_name):
    body = {
        "name": updated_name
    }
    result = requests.put("https://api.clickup.com/api/v2/folder/" + folder_id, headers = myHeaders,json = body)
    print(result)
    print(result.text)
    return result

def create_folder_by_name(current_name):
    body = {
        "name": current_name
    }
    result = requests.post("https://api.clickup.com/api/v2/space/" + str(spaceID) + "/folder", headers = myHeaders, json = body)
    assert result.status_code == 200
    print(result)
    print(result.text)
    return result




