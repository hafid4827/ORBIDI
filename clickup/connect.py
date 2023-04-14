import requests
import json

from clickup.key import API_KEY

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

def create_tastk_with_get_info_from_hubspot(list_id_param: str = "900200568557", name_task: str = "", description_task: str = "") -> None:
    url = "https://api.clickup.com/api/v2/list/{list_id}/task"

    payload = {
        'name': name_task,
        'description': description_task
    }

    response = requests.post(
        url.format(list_id=list_id_param),
        headers=headers,
        data=json.dumps(payload)
    )

    task_id = 0
    if response.ok:
        task_id = response.json()['id']
    else:
        task_id = response.json()['err']

    return task_id


def get_exist_user_register(list_id_param: str = "900200568557") -> None:
    url = "https://api.clickup.com/api/v2/list/{list_id}/task"

    response = requests.get(
        url.format(list_id=list_id_param),
        headers=headers,
    )
    data = response.json()

    return data
