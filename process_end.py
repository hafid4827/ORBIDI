from clickup.connect import create_tastk_with_get_info_from_hubspot, get_exist_user_register


def process_task_add(data):
    for item_extract_all_hubspot in data:
        email = item_extract_all_hubspot['email']
        lastname = item_extract_all_hubspot['lastname']
        firstname = item_extract_all_hubspot['firstname']
        createdate = item_extract_all_hubspot['createdate']

        format_description = f"email: {email} \n"
        format_description += f"lastname: {lastname} \n"
        format_description += f"firstname: {firstname} \n"
        format_description += f"createdate: {createdate}"

        task_id = create_tastk_with_get_info_from_hubspot(
            name_task=firstname,
            description_task=format_description,
        )
    return {"status": 200, "task_id": task_id}


def process_exist_user_register() -> None:
    data = get_exist_user_register()
    list_task = data['tasks']
    names_list = [task['name'] for task in list_task]
    return names_list
