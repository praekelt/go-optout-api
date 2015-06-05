import json

from klein import Klein


class API(object):
    app = Klein()

    def __init__(self):
        self._optouts = [
            {"id": "2468", "address_type": "msisdn", "address": "+273121100"},
            {"id": "1234", "address_type": "facebook", "address": "fb-app"},
            {"id": "5678", "address_type": "twitter",
             "address": "@twitter_handle"}
        ]

    def get_opt_out(self, addresstype, address):
        opt_outs = [
            o for o in self._optouts
            if o["address_type"] == addresstype and o["address"] == address
        ]
        if opt_outs:
            return opt_outs[0]
        return None

    def save_opt_out(self, addresstype, address):
        opt_out = {
            "id": "2211",
            "address_type": addresstype,
            "address": address,
        }
        self._optouts.append(opt_out)
        return opt_out

    @app.route('/')
    def addresses(self, request):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self._info)

# GET Method

    @app.route('/optouts/<string:addresstype>/<string:address>',
               methods=['GET'])
    def get_address(self, request, addresstype, address):
        opt_out = self.get_opt_out(addresstype, address)
        if opt_out is None:
            # TODO: return 404
            return "Eep."
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(opt_out)

# PUT Method

    @app.route('/optouts/<string:addresstype>/<string:address>',
               methods=['PUT'])
    def save_address(self, request, addresstype, address):
        opt_out = self.save_opt_out(addresstype, address)
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(opt_out)
