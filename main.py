import logging
from celery import Celery
from fastapi import FastAPI
from models.generla import Contact, ContactError, session_db
from process_end import process_exist_user_register, process_task_add

from hubspot_logic.create_contacs import create_contact_hubspot, extract_contacts_hubpot

# session interactive conecc database
session = session_db()

# Configurar el logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO
)

# init object with app fastapi
app = FastAPI()


# init object background applications
celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)


@celery.task
def process_data(data):
    # check exist or not name
    process_task_add(data)
    return {"status": 200}


@app.post("/create_hubspot_contact")
def create_contacts_hubspot(data: dict):

    # error default return with post requests intertan server error
    error = {"error": ""}

    # default list for compare with send for client by method post endpint
    compare_list_default = [
        "email",
        "firstname",
        "lastname",
        "phone",
        "website",
    ]

    # converting and avoiding loops is more efficient to confirm if no strange data has been injcted
    set_convert_compare_list_default = set(compare_list_default)
    set_convert_data = set(data.keys())

    if set_convert_compare_list_default != set_convert_data:
        return error

    # create contact in hubspot
    reasigned_send_contact_create = data

    # consul db
    existing_user = session.query(Contact)
    existing_user_filter = existing_user.filter(
        Contact.firstname == reasigned_send_contact_create['firstname']
    )
    existing_user_first_item = existing_user_filter.first()
    try:
        # se verifica si la persona no ha sido agregada anteriormente ala base de datos
        if not existing_user_first_item:
            api_response = create_contact_hubspot(
                contact=reasigned_send_contact_create
            )
            print(api_response)
            # se cuarda la informacion en una base de datos de igual forma sin el error
            new_contact = Contact(**reasigned_send_contact_create)
            # Agregar la instancia a la sesión
            session.add(new_contact)
            # Confirmar la transacción
            session.commit()
    except Exception as error_as:
        # si existe un error entonces terminar proceso y devolver el error de lado del servidor
        errro_save_conctac = ContactError(
            message=error_as,
        )
        # Agregar la instancia a la sesión
        session.add(errro_save_conctac)
        # Confirmar la transacción
        session.commit()

        # se registra en la base dedatos si no existe
        return error

    # Registrar información en el log
    logging.info("Hubspot API response: %s", data)

    return data


# Endpoint para crear una tarea en ClickUp
@app.post("/create/task")
def post_hubspot_pased_to_clickup():
    # Extraemos todos los contactos de Hubspot
    extract_all_hubspot = extract_contacts_hubpot()
    set_compare_clikup = process_exist_user_register()

    result_compare = [
        item_dict_filtered for item_dict_filtered in extract_all_hubspot
        if item_dict_filtered['firstname'] not in set_compare_clikup
    ]
    print(result_compare, "=>  comportamiento extrano")
    if result_compare != []:
        # Creamos una tarea en Celery para procesar los datos
        task_add_status = process_data.delay(result_compare)
        logging.info("Task status: %s", task_add_status.get())
        logging.info("Task created with data: %s", extract_all_hubspot)

    # Registrar información en el log

    return {"sattus": 200}
