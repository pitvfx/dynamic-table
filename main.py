from fasthtml.common import *

db = database(":memory:", wal=True)
clients = db.t.clients
if clients not in db.t:
    clients.create(id=int, name=str, address=str, email=str, pk='id')
Client = clients.dataclass()

app, rt = fast_app(debug=True)


def create_row():
    return Tr(Th("Add", scope="col"), Th(Input(type="text", name="name", required=True, form="create-form", placeholder="Name"), scope="col"), Th(Input(type="text", name="address", required=True, form="create-form", placeholder="Address"), scope="col"), Th(Input(type="email", name="email", required=True, form="create-form", placeholder="Email"), scope="col"), Th(Input(type="submit", value="Add", form="create-form"), scope="col"), id="create-row", hx_swap_oob="true")


def client_row(client):
    _id = f"client-{client.id}"
    return Tr(Th(client.id, scope="row"), client_column_data(client.id, "name", client.name, "text"), client_column_data(client.id, "address", client.address, "text"), client_column_data(client.id, "email", client.email, "email"), Td(Button("Delete", hx_delete=f"/{client.id}", hx_confirm="Are you sure?", hx_target=f"#{_id}"),), id=_id)


def client_column_data(_id: int, name: str, value: str, _type: str, edit: bool = False):
    cell_id = f"client-{_id}-{name}"
    kwargs = {"id": cell_id, "hx_post": f"/swap/{_id}/{name}",
              "hx_swap": "outerHTML"}
    inner = value
    if edit:
        inner = Input(type=_type, name=name, value=inner, hx_post=f"/update/{_id}", target_id=f"client-{_id}",
                      hx_swap="outerHTML", hx_trigger="keyup[key=='Enter'] changed", required=True, placeholder=name)
        kwargs.update(hx_vals=f'{{"pre_value":"{value}"}}',
                      hx_trigger="keyup[key=='Escape']")
    else:
        kwargs.update(
            hx_vals=f'{{"pre_value":"{value}", "edit":true}}', hx_trigger="click")
    return Td(inner, **kwargs)


def client_table():
    return Form(hx_post="/", target_id="tbody", hx_swap="beforeend", id="create-form", cls="grid"), Table(Thead(Tr(Th("ID", scope="col"), Th("Name", scope="col"), Th("Address", scope="col"), Th("Email", scope="col"), Th("Action", scope="col")), create_row()), Tbody(*[client_row(client) for client in clients()], id="tbody"))


@rt("/")
def get():
    return Titled("Clients", client_table())


@rt("/")
def post(client: Client):
    return client_row(clients.insert(client)), create_row()


@rt("/{client_id:int}")
def delete(client_id: int):
    clients.delete(client_id)
    return


@rt("/swap/{_id:int}/{name:str}")
def post(_id: int, name: str, pre_value: str, edit: bool = False):
    return client_column_data(_id, name, pre_value, "email" if name == "email" else "text", edit=edit)


@rt("/update/{_id:int}")
def post(_id: int, client: Client):
    client.id = _id
    return client_row(clients.update(client))


serve()
