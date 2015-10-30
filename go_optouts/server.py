from api import API
from store.memory import MemoryOptOutBackend

site = API(MemoryOptOutBackend())
resource = site.app.resource  # expose for twistd web

if __name__ == "__main__":
    site.app.run('localhost', 8080)
