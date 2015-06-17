import json
import uuid

from klein import Klein


class OptOutNotFound(Exception):
    """ Raised when no opt out is found. """


class OptOutAlreadyExists(Exception):
    """ Raised when opt out already exists. """


class OptOutNotDeleted(Exception):
    """ Raised when opt out not deleted. """


class API(object):
    app = Klein()

    def __init__(self):
        self._optouts = [
            {"id": "2468", "address_type": "msisdn", "address": "+273121100"},
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

# Save Opt Out Address

    def save_opt_out(self, addresstype, address):
        opt_id = str(uuid.uuid4())
        opt_out = {
            "id": opt_id,
            "address_type": addresstype,
            "address": address,
        }
        self._optouts.append(opt_out)
        return opt_out

    def response(self, request, status_code=200, status_reason="OK", **data):
        request.setResponseCode(status_code)
        request.setHeader('Content-Type', 'application/json')
        data.update({
            "status": {
                "code": status_code,
                "reason": status_reason,
            },
        })
        return json.dumps(data)

# Error Handling

    @app.handle_errors(OptOutNotFound)
    def opt_out_not_found(self, request, failure):
        return self.response(
            request, status_code=404, status_reason="Opt out not found.")

    @app.handle_errors(OptOutAlreadyExists)
    def opt_out_already_exists(self, request, failure):
        return self.response(
            request, status_code=409, status_reason="Opt out already exists.")

    @app.handle_errors(OptOutNotDeleted)
    def opt_out_not_deleted(self, request, failure):
        return self.response(
            request, status_code=404,
            status_reason="There\'s nothing to delete.")


# Methods

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
        return self.response(request, opt_out=opt_out)

    @app.route('/optouts/<string:addresstype>/<string:address>',
               methods=['PUT'])
    def save_address(self, request, addresstype, address):
        opt_out = self.get_opt_out(addresstype, address)
        if opt_out is not None:
            raise OptOutAlreadyExists()
        opt_out = self.save_opt_out(addresstype, address)
        return self.response(request, opt_out=opt_out)

    @app.route('/optouts/<string:addresstype>/<string:address>',
               methods=['DELETE'])
    def delete_address(self, request, addresstype, address):
        opt_out = self.get_opt_out(addresstype, address)
        if opt_out is None:
            raise OptOutNotDeleted()
        return self.response(request, opt_out=opt_out)
