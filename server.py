import asyncio
import logging

import aiocoap
import aiocoap.resource as resource


class ActiveThing(resource.Resource):
    """
    https://coap.whoisdeveloper.ru/things
    Activates a thing with an activation code. The result is a thing token.
    """
    async def render_post(self, request):
        text = ["Used protocol: %s." % request.remote.scheme]

        text.append("Request came from %s." % request.remote.hostinfo)
        text.append("The server address used %s." % request.remote.hostinfo_local)

        claims = list(request.remote.authenticated_claims)
        if claims:
            text.append("Authenticated claims of the client: %s." % ", ".join(repr(c) for c in claims))
        else:
            text.append("No claims authenticated.")

        return aiocoap.Message(content_format=0,
                               payload="\n".join(text).encode('utf8'))


class ThingWrite(resource.Resource):
    """
    https://coap.whoisdeveloper.ru/things/{THING_TOKEN}
    Writes the records of data from the thing to the specified THING_TOKEN.
    Only alphanumeric characters and ".", "-", "" symbols are admited for the resource name "key".
    """
    async def render_post(self, request):
        pass


class ThingRead(resource.Resource):
    """
    This method returns the values of the resource with the specified RESOURCE_KEY from the corresponding THING_TOKEN.
    To read data, use the operation GET /things/ with the thing token and
    the key that you are using to store the values.
    """
    async def render_get(self, request):
        pass


class ThingSubscribe(resource.Resource):
    """
    https://coap.whoisdeveloper.ru/things/{THING_TOKEN}
    With this method you can subscribe to the thing channel and get real-time updates from all the thing's keys (resources).
    The subscription endpoint creates a streaming channel and we keep the channel open depending on the keep alive that you send.
    If no keep alive is set, your router or our server will close the channel at its sole discretion.
    """
    async def render_get(self, request):
        pass


class GetResources(resource.Resource):
    """
    https://coap.whoisdeveloper.ru/things/{THING_TOKEN}/resources
    Returns the names of the resources of the thing.
    """
    async def render_get(self, request):
        pass

# logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(['things'], WhoAmI())

    await aiocoap.Context.create_server_context(root, bind=("0.0.0.0",1222))

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
