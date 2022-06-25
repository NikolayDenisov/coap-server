import asyncio
import logging
import json

import aiocoap
import aiocoap.resource as resource

from db.db import write_temp


class ActiveThing(resource.Resource):
    """
    https://coap.whoisdeveloper.ru/things
    Activates a thing with an activation code. The result is a thing token.
    """

    @staticmethod
    async def render_post(request):
        logging.info(request.remote.hostinfo)
        payload = request.payload.decode('utf8')
        parse_payload(payload)
        logging.info(payload)
        text = "Hello world"
        return aiocoap.Message(code=aiocoap.CREATED,
                               payload=text.encode('utf8'))




class ThingWrite(resource.Resource, resource.PathCapable):
    """
    https://coap.whoisdeveloper.ru/things/{THING_TOKEN}
    Writes the records of data from the thing to the specified THING_TOKEN.
    Only alphanumeric characters and ".", "-", "" symbols are admited for the resource name "key".
    """

    async def render_post(self, request):
        device_token = request.opt.uri_path[0]
        if not device_token:
            return aiocoap.Message(code=aiocoap.UNAUTHORIZED)
        dev_ip_addr = request.remote.sockaddr[0]
        uri_query = request.opt.uri_query
        logging.info(f'Receive token {device_token}, dev_ip_addr {dev_ip_addr}, uri_query {uri_query}')
        payload = request.payload.decode('utf8')
        # convert string to  object
        json_object = json.loads(payload)
        for data in json_object['values']:
            if data['key'] == 'temp':
                write_temp(data['value'])
        return aiocoap.Message(code=aiocoap.CREATED,
                               payload=payload.encode('utf8'))


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
    site = resource.Site()

    site.add_resource(['things'], ActiveThing())
    site.add_resource(['things'], ThingWrite())

    await aiocoap.Context.create_server_context(site, bind=("0.0.0.0", 1222))

    # Run forever
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())