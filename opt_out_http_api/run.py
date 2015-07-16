from api_methods import API
from store.memory import OptOutMemory

app = API(OptOutMemory())

app.app.run('localhost', 8080)
