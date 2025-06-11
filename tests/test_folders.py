import string
import random
import string

import requests
from faker import Faker
from pytest_steps import test_steps

from modules.folders_methods import \
    get_folders, get_folder_by_id, create_folder, delete_folder, update_folder, create_folder_by_name

#
# def test_get_folders():
#     result = get_folders()
#     assert result.status_code == 200
#
# def test_get_folder_by_id():
#     result = get_folder_by_id("90157327163")
#     assert result.status_code == 200
#
# def test_create_folder():
#     result = create_folder()
#     assert result.status_code == 200
#
# def test_delete_folder_by_id():
#     result = delete_folder("90157327811")
#     assert result.status_code == 200
#
# def test_update_folder_by_id():
#     updated_folder_name = "Igor Updated"
#     result = update_folder("90157327140", updated_folder_name)
#     assert result.status_code == 200

@test_steps("Create", "Create", "Get", "Delete", "Delete")
def test_get_folders_with_two_created_folders():
    response1 = create_folder()
    folder1_data = response1.json()
    folder1_id = folder1_data["id"]
    folder1_name = folder1_data["name"]
    print(f"First folder: {folder1_name} (ID: {folder1_id})")
    yield

    response2 = create_folder()
    folder2_data = response2.json()
    folder2_id = folder2_data["id"]
    folder2_name = folder2_data["name"]
    print(f"Second folder: {folder2_name} (ID: {folder2_id})")
    yield

    all_folders_response = get_folders()
    folders = all_folders_response.json()["folders"]
    yield

    folder_ids = [folder["id"] for folder in folders]

    assert folder1_id in folder_ids, "First folder is not in folders"
    assert folder2_id in folder_ids, "Second folder is not in folders"
    print("Both folders exist")

    del1 = delete_folder(folder1_id)
    assert del1.status_code == 200, "Can't delete first folder"
    print("First folder deleted.")
    yield

    del2 = delete_folder(folder2_id)
    assert del2.status_code == 200, "Can't delete second folder"
    print("Second folder deleted.")
    yield

@test_steps("Create", "Get by ID", "Get by wrong ID", "Delete")
def test_get_folder():
    response = create_folder()
    folder = response.json()
    folder_id = folder["id"]
    folder_name = folder["name"]
    print(f"Created folder: {folder_name} (ID: {folder_id})")
    yield

    get_folder_response = get_folder_by_id(folder_id)
    assert get_folder_response.status_code == 200, "Failed to get folder by valid ID"
    fetched_folder = get_folder_response.json()
    assert fetched_folder["id"] == folder_id, "Fetched folder ID does not match"
    print("Successfully fetched folder by ID")
    yield

    wrong_id = "invalid_id_3234343324"
    wrong_response = get_folder_by_id(wrong_id)
    assert wrong_response.status_code in [400, 404, 500], "Expected error for wrong ID"
    print(f"Correctly handled wrong ID (Status code: {wrong_response.status_code})")
    yield

    delete_response = delete_folder(folder_id)
    assert delete_response.status_code == 200, "Failed to delete folder"
    print("Folder successfully deleted")
    yield


@test_steps("Create", "Get", "Verify", "Delete")
def test_create_folder():
    random_char = random.choice(string.ascii_letters + string.digits)
    test_name = f"Igor Created {random_char}"

    response = create_folder_by_name(test_name)
    folder = response.json()
    folder_id = folder["id"]
    folder_name = folder["name"]
    print(f"Folder created: {folder_name} (ID: {folder_id})")
    yield

    fetched = get_folder_by_id(folder_id)
    assert fetched.status_code == 200, "Failed to fetch folder by ID"
    fetched_folder = fetched.json()
    yield

    fetched_name = fetched_folder["name"]
    assert fetched_name == test_name, f"Expected name '{test_name}', got '{fetched_name}'"
    print("Folder name verified")
    yield

    deleted = delete_folder(folder_id)
    assert deleted.status_code == 200, "Failed to delete folder"
    print("Folder deleted")
    yield


@test_steps("Create", "Update", "Get", "Verify", "Delete")
def test_update_folder():
    random_char = random.choice(string.ascii_letters + string.digits)
    original_name = f"Igor Folder {random_char}"

    response = create_folder_by_name(original_name)
    assert response.status_code == 200, "Folder creation failed"

    folder = response.json()
    folder_id = folder["id"]
    print(f"Folder created: {original_name} (ID: {folder_id})")
    yield

    updated_name = f"Updated Folder {random_char}"
    update_response = update_folder(folder_id, updated_name)
    assert update_response.status_code == 200, "Folder update failed"
    print(f"Folder updated to: {updated_name}")
    yield

    fetched = get_folder_by_id(folder_id)
    assert fetched.status_code == 200, "Failed to fetch folder by ID"
    fetched_folder = fetched.json()
    yield

    fetched_name = fetched_folder["name"]
    assert fetched_name == updated_name, f"Expected updated name '{updated_name}', got '{fetched_name}'"
    print("Folder name updated and verified successfully.")
    yield

    deleted = delete_folder(folder_id)
    assert deleted.status_code == 200, "Failed to delete folder"
    print("Folder deleted successfully.")
    yield


@test_steps("Create", "Delete", "Delete Again (Expect deleted=true)", "Get (Expect deleted=true)")
def test_delete_folder():
    random_char = random.choice(string.ascii_letters + string.digits)
    test_name = f"Delete Test {random_char}"

    response = create_folder_by_name(test_name)
    assert response.status_code == 200, "Folder creation failed"

    folder = response.json()
    folder_id = folder["id"]
    print(f"Folder created: {test_name} (ID: {folder_id})")
    yield

    del_response = delete_folder(folder_id)
    assert del_response.status_code in [200, 204], f"Failed to delete folder: {del_response.status_code}"
    print("Folder deleted (1st time).")
    yield

    del_again_response = delete_folder(folder_id)
    assert del_again_response.status_code in [200, 204], f"Second delete failed: {del_again_response.status_code}"
    print("Second delete succeeded or was no-op.")
    yield

    get_response = get_folder_by_id(folder_id)
    assert get_response.status_code == 200, "Expected 200 on get after delete"
    folder_data = get_response.json()
    assert folder_data.get("deleted") is True, "Expected folder to be marked as deleted"
    print("Get after delete returned folder with deleted=true")
    yield

