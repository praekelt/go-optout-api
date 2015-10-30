from api_methods import API
from store.memory import MemoryOptOutCollection

app = API(MemoryOptOutCollection())

app.app.run('localhost', 8080)
