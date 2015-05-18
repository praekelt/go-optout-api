from app import App

# TODO use twistd instead
# http://klein.readthedocs.org/en/latest/introduction/2-twistdtap.html

app = App()

app.app.run('localhost', 8080)
