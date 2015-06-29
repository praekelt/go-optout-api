import zope.interface


class OptOutStore(zope.interface.Interface):

        def get(address_type, address):
            """ Retrieve the opt out for an address. """
            pass

        def put(address_type, address):
            """ Store a record of an opt out for an address. """
            pass

        def delete(address_type, address):
            """ Remove an opt out for an address. """
            pass

        def count(results):
            """ Return the number of opt outs. """
            pass
