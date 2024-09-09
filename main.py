from fasthtml.common import *

app, rt = fast_app(debug=True)

db = database(":memory:")
clients = db.t.clients

if clients not in db.t:
    clients.create(id=int, name=str, address=str, email=str, pk='id')

Client = clients.dataclass()


def create_form():
    return Form(id="create-form", hx_post="/", hx_target="#client-list", hx_swap="beforeend")


def create_row():
    return Tr(
        Th("Add"),
        Th(Input(name="name", type="text", placeholder="Name", form="create-form")),
        Th(Input(name="address", type="text",
           placeholder="Address", form="create-form")),
        Th(Input(name="email", type="email", placeholder="Email", form="create-form")),
        Th(Input(type="submit", value="Add", form="create-form")),
        id="create-row", hx_swap_oob="true"
    )


def client_cell(client_id: int, column_name: str, column_value: str, edit: bool = False):
    cell_id = f"client-{client_id}-{column_name}"
    attributes = {
        "id": cell_id,
        "hx_swap": "outerHTML",
        "hx_vals": {'pre_value': column_value},
    }
    if edit:
        # table cell after user clicks on it - Edit State
        inner_html = Input(name=column_name,
                           value=column_value,
                           type="email" if column_name == "email" else "text",
                           hx_post=f"/update/{client_id}/{column_name}",
                           target_id=cell_id,
                           hx_swap="outerHTML",
                           hx_trigger="keyup[key=='Enter'] changed",
                           )
        attributes["hx_trigger"] = "keyup[key=='Escape']"
        attributes["hx_post"] = f"/reset/{client_id}/{column_name}"
    else:
        # table cell in its Initial State
        inner_html = column_value
        attributes["hx_trigger"] = "click"
        attributes["hx_post"] = f"/swap/{client_id}/{column_name}"
    return Td(inner_html, **attributes)


def client_row(client: Client):
    return Tr(
        Td(client.id),
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
            map(client_row, clients()), id="client-list"
        )
    )


@rt("/")
def get():
    return Titled("Clients", create_form(), client_table())


@rt("/")
def post(client: Client):
    new_client = clients.insert(client)
    return client_row(new_client), create_row()


@ rt("/swap/{client_id:int}/{column_name:str}")
def post(client_id: int, column_name: str, pre_value: str):
    # table cell after user clicks on it - Edit State
    return client_cell(client_id, column_name, pre_value, edit=True)


@ rt("/update/{client_id:int}/{column_name:str}")
def post(client_id: int, column_name: str, client: Client):
    client.id = client_id
    client = clients.update(client)
    # table cell in its Initial State
    return client_cell(client_id, column_name, getattr(client, column_name))


@ rt("/reset/{client_id:int}/{column_name:str}")
def post(client_id: int, column_name: str, pre_value: str):
    # table cell in its Initial State
    return client_cell(client_id, column_name, pre_value)


@ rt("/{client_id:int}")
def delete(client_id: int):
    clients.delete(client_id)
    return


serve()
