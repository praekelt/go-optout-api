Opt Outs HTTP API
=================

This API is used to retrieve and update opt out information for addresses.


API Methods
-----------

.. http:get:: /optouts/(str:address_type)/(str:address)

   Retrieve the opt out for an address.

   **Request**

   .. sourcecode:: http

      GET /optouts/msisdn/%2B273121100
      Host: example.com
      Accept: application/json

   **Response**

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: accept
      Content-type: application/json

      {
        "id": "2468"",
        "address_type": "msisdn",
        "address": "+273121100"
      }

   :statuscode 200: no error
   :statuscode 404: there's no opt out for this contact


.. http:put:: /optouts/(str:address_type)/(str:address)

   Store a record of an opt out for an address.

   **Request**

   .. sourcecode:: http

      PUT /optouts/facebook/fb-app
      Host: example.com
      Accept: application/json

   **Response**

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: accept
      Content-type: application/json

      {
        "id": "1234",
        "address": "fb-app",
        "address_type": "facebook"
      }

   :statuscode 200: opt out created
   :statuscode 404: opt out already exists


.. http:delete:: /optouts/(str:address_type)/(str:address)

   Remove an opt out for an address.

   **Request**

   .. sourcecode:: http

      DELETE /optouts/twitter/%40twitter_handle
      Host: example.com
      Accept: application/json

   **Response**

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: accept
      Content-type: application/json

      {
        "id": "5678",
        "address": "@twitter_handle",
        "address_type": "twitter"
      }

   :statuscode 200: opt out deleted
   :statuscode 404: there's nothing to delete
