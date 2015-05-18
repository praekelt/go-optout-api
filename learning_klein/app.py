# Hello World
import json

from klein import Klein


class App(object):
    app = Klein()

    def __init__(self):
        self._info = {"Contact": [
            {"msg": "Hello", "Cell_No": 712345678, "Email": "trev@gmail.com"},
            {"msg": "Hello2", "Cell_No": 849485738, "Email": "oct@gmail.com"}
        ]}

    @app.route('/Hello')
    def hello(self, request):
        return 'Hello, world!'

# Adding Routes

    @app.route('/AR')
    def pg_root(self, request):
        return 'I am the root page!'

# Variable Routes

    @app.route('/VR/<username>')
    def pg_vr(self, request, username):
        return 'Hi %s!' % (username,)

# Route Order Matters-

    @app.route('/ROM/bob')
    def pg_user_bob(self, request):
        return 'Hello there bob!'

# Using Non-Global State

    @app.route('/')
    def items(self, request):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self._info)

    @app.route('/<string:name>', methods=['PUT'])
    def save_item(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        body = json.loads(request.content.read())
        self._info[name] = body
        return json.dumps({'success': True})

    @app.route('/infor/<string:name>', methods=['GET'])
    def get_item(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self._info.get(name))
