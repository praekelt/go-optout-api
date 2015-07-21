""" Riak opt out backend. """

from twisted.internet.defer import inlineCallbacks, returnValue
from zope.interface import implements

from go.vumitools.opt_out import OptOutStore, OptOut

from .interface import IOptOutCollection


class RiakOptOutBackend(object):
    """ Riak opt out backend.

    :type riak_manager:
        `vumi.persist.txriak_manager.TxRiakManager`
    :param riak_manager:
        A Riak manager for the opt out stores.
    """

    # TODO: this should declare that it implements the
    #       opt out backend interface

    def __init__(self, riak_manager):
        self.riak_manager = riak_manager

    def get_opt_out_collection(self, owner_id):
        """ Return the opt out collection for the specified owner.

        :param str owner_id:
            The id of the owner of the opt out store.
        """
        opt_out_store = OptOutStore(self.riak_manager, owner_id)
        return RiakOptOutCollection(opt_out_store)


class RiakOptOutCollection(object):
    """ Riak opt out collection for a particular opt out store.

    :type opt_out_store:
        `go.vumitools.opt_out.models.OptOutStore`
    :param opt_out_store:
        The opt out store to provide access to.
    """

    implements(IOptOutCollection)

    def __init__(self, opt_out_store):
        self.store = opt_out_store

    @classmethod
    def _pick_fields(cls, data, keys):
        """
        Return a sub-dictionary of all the items from ``data`` whose
        keys are listed in ``keys``.
        """
        return dict((k, data[k]) for k in keys if k in data)

    @classmethod
    def _opt_out_to_dict(cls, opt_out):
        """
        Return a sub-dictionary of the items from ``data`` that are valid
        contact fields.
        """
        return cls._pick_fields(
            opt_out.get_data(), OptOut.field_descriptors.keys())

    @inlineCallbacks
    def get(self, addresstype, address):
        opt_out = yield self.store.get_opt_out(addresstype, address)
        if opt_out is None:
            returnValue(None)
        returnValue(self._opt_out_to_dict(opt_out))

    @inlineCallbacks
    def put(self, addresstype, address):
        opt_out = yield self.store.new_opt_out(
            addresstype, address, message={
                'message_id': None,  # TODO: fix opt out store
            })
        returnValue(self._opt_out_to_dict(opt_out))

    @inlineCallbacks
    def delete(self, addresstype, address):
        opt_out = yield self.store.get_opt_out(addresstype, address)
        if opt_out is None:
            returnValue(None)
        yield opt_out.delete()
        returnValue(opt_out)

    @inlineCallbacks
    def count(self):
        count = yield self.store.count()
        returnValue(count)
