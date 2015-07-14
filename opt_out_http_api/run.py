from api_methods import API
from opt_out_http_api.store.memory import OptOutMemory

app = API(backend_class=OptOutMemory)

app.app.run('localhost', 8080)
