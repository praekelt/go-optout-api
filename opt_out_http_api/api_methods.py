import json

from klein import Klein


class OptOutNotFound(Exception):
    """ Raised when no opt out is found. """


class OptOutFound(Exception):
    """ Raised when opt out is found. """


class API(object):
    app = Klein()

    def __init__(self):
        self._optouts = [
            {"id": "2468", "address_type": "msisdn", "address": "+273121100"},
            {"id": "1234", "address_type": "facebook", "address": "fb-app"},
            {"id": "5678", "address_type": "twitter",
             "address": "@twitter_handle"}
        ]

# Get Opt Out Address

    def get_opt_out(self, addresstype, address):
        opt_outs = [
            o for o in self._optouts
            if o["address_type"] == addresstype and o["address"] == address
        ]
        if opt_outs:
            return opt_outs[0]
        return None

    @app.handle_errors(OptOutNotFound)
    def opt_out_not_found(self, request, failure):
        request.setResponseCode(404)
        request.setHeader('Content-Type', 'application/json')
        return json.dumps({
            "status": {
                "code": 404,
                "reason": "Opt out not found.",
            },
        })

    @app.handle_errors(OptOutFound)
    def opt_out_found(self, request, failure):
        request.setResponseCode(200)
        request.setHeader('Content-Type', 'application/json')
        return json.dumps({
            "status": {
                "code": 200,
                "reason": "OK",
            },
            "optout": {
                "id": "2468",
                "address_type": "msisdn",
                "address": "+273121100",
            },
        })

# GET Method

    @app.route('/')
    def addresses(self, request):
            request.setHeader('Content-Type', 'application/json')
            return json.dumps(self._info)

    @app.route('/optouts/<string:addresstype>/<string:address>',
               methods=['GET'])
    def get_address(self, request, addresstype, address):
        opt_out = self.get_opt_out(addresstype, address)
        if opt_out is None:
            raise OptOutNotFound()

        # return 200 OK
        raise OptOutFound()
