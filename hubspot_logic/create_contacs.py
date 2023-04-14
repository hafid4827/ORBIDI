from hubspot.crm.contacts.exceptions import ApiException
from hubspot import HubSpot

from hubspot_logic.key import TOKEN_HUBSPOT


api_client = HubSpot()
api_client.access_token = TOKEN_HUBSPOT


def create_contact_hubspot(contact: dict) -> None:
    api_response = {}
    try:
        registro = api_client.create(data=contact)
        api_response = registro
    except ApiException as error:
        api_response = {"send": "error", "type_error": error}
    return api_response


def extract_contacts_hubpot():
    all_contacts = api_client.crm.contacts.get_all()
    all_contacts_map = map(lambda extract : extract.properties, all_contacts)
    all_contacts_map_to_list = list(all_contacts_map)
    return all_contacts_map_to_list