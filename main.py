# main.py
from fasthtml.common import *

db = database(":memory:")  # database
clients = db.t.clients  # table
if clients not in db.t:  # if table not in database
    clients.create(id=int, name=str, address=str, email=str, pk='id')
Client = clients.dataclass()  # dataclass

app, rt = fast_app(debug=True)


def create_row():
    return Tr(
        Th("Add", scope="col"),
        Th(
            Input(type="text", name="name", required=True, form="create-form", placeholder="Name"), scope="col"
        ),
        Th(
            Input(type="text", name="address", required=True, form="create-form", placeholder="Address"), scope="col"
        ),
        Th(
            Input(type="email", name="email", required=True, form="create-form", placeholder="Email"), scope="col"
        ),
        Th(
            Input(type="submit", value="Add", form="create-form"), scope="col"
        ),
        id="create-row", hx_swap_oob="true"
    )


def client_cell(client_id: int, column_name: str, column_value: str):
    return Td(column_value,
              id=f"client-{client_id}-{column_name}",
              hx_post=f"/swap/{client_id}/{column_name}",
              hx_trigger="click",
              hx_swap="outerHTML",
              hx_vals=f'{{"pre_value":"{column_value}"}}'
              )


def client_row(client: Client):
    return Tr(
        client_cell(client.id, "id", client.id),
        client_cell(client.id, "name", client.name),
        client_cell(client.id, "address", client.address),
        client_cell(client.id, "email", client.email),
        Td(
            Button("Delete",
                   hx_delete=f"/{client.id}",
                   hx_confirm="Are you sure?",
                   hx_swap="outerHTML",
                   target_id=f"client-{client.id}"
                   ),
        ),
        id=f"client-{client.id}"
    )


def client_table():
    return Table(
        Thead(
            Tr(
                Th("ID", scope="col"),
                Th("Name", scope="col"),
                Th("Address", scope="col"),
                Th("Email", scope="col"),
                Th("Action", scope="col")
            ),
            create_row()
        ),
        Tbody(
            map(client_row, clients()), id="tbody"
        )
    )


def create_form():
    return Form(
        hx_post="/",
        target_id="tbody",
        hx_swap="beforeend",
        id="create-form"
    )


@ rt("/")
def get():
    return Titled("Clients", create_form(), client_table())


@ rt("/")
def post(client: Client):
    new_client = clients.insert(client)
    return client_row(new_client), create_row()


@ rt("/swap/{client_id:int}/{column_name:str}")
def post(client_id: int, column_name: str, pre_value: str):
    return Td(
        Input(name=column_name,
              value=pre_value,
              hx_post=f"/update/{client_id}/{column_name}",
              target_id=f"client-{client_id}-{column_name}",
              hx_swap="outerHTML",
              hx_trigger="keyup[key=='Enter'] changed",
              ),
        hx_vals={"pre_value": pre_value},
        hx_trigger="keyup[key=='Escape']",
        hx_swap="outerHTML",
        hx_post=f"/reset/{client_id}/{column_name}",
        id=f"client-{client_id}-{column_name}",
    )


@ rt("/update/{client_id:int}/{column_name:str}")
def post(client_id: int, column_name: str, client: Client):
    client.id = client_id
    client = clients.update(client)
    return client_cell(client_id, column_name, getattr(client, column_name))


@ rt("/reset/{client_id:int}/{column_name:str}")
def post(client_id: int, column_name: str, pre_value: str):
    return client_cell(client_id, column_name, pre_value)


@ rt("/{client_id:int}")
def delete(client_id: int):
    clients.delete(client_id)
    return


serve()
