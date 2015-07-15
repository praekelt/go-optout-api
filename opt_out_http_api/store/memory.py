from zope.interface import implements
from interface import IOptOutStore
import uuid


class OptOutMemory(object):
    """
    This implements the IOptOutStore interface.

    It stores the opt out in a dictionary using the address type
    and address as the key. The values are opt out objects, for example::

        {
            "id": "2468",
            "address_type": "msisdn",
            "address": "+273121100",
        }
    """

    implements(IOptOutStore)

    def __init__(self):
        # _store maps (address_type, address) pairs to opt outs
        self._store = {}

    def get(self, address_type, address):
        key = (address_type, address)
        return self._store.get(key)

    def put(self, address_type, address):
        key = (address_type, address)
        opt_id = str(uuid.uuid4())
        self._store[key] = {
            'id': opt_id,
            'address_type': address_type,
            'address': address
        }
        return self._store.get(key)

    def delete(self, address_type, address):
        key = (address_type, address)
        return self._store.pop(key, None)

    def count(self):
        return len(self._store)
