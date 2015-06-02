Opt outs http api
-----------------

.. http:get:: /optouts/(str:address_type)/(str:address)

    :statuscode 200: no error
    :statuscode 404: there's no opt out for this contact
    
   **Request**

   .. sourcecode:: http

      GET /optouts/msisdn/"+273121100"
      Host: example.com 
      Accept: application/json

   **Response**

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: accept
      Content-type: application/json

      [
        {
        "id": 2468,
        "address-type": "msisdn",
        "address": "+273121100"
        },
        {
        "id": 8642,
        "address-type": "twitter",
        "address": "@vumi-app"
        }
      ]

    

.. http:put:: /optouts/(str:address_type)/(str:address)

    **Request**

    .. sourcecode:: http
    
       PUT /optouts/facebook/"@fb-app"
       Host: example.com 
       Accept: application/json

       {"address-type": "facebook", "address": "@fb-app"}

    **Response**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Vary: accept
       Content-type: application/json

       {..., "address": "@fb-app", ""address-type": "facebook", ...}

.. http:delete:: /optouts/(str:address_type)/01dfae6e5d4d90d9892622325959afbe
    
    **Request**

    .. sourcecode:: http

       DELETE /optouts/twitter/01dfae6e5d4d90d9892622325959afbe
       Host: axample.com
       Accept: application/json

    **Response**

    .. sourcecode:: http

       HTTP/1.1 200 OK
       Vary: accept
       Content-type: application/json

       {..., "id": "68e456a0c8da43bea162839a9a1669c0", ...}
