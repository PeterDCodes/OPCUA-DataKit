
#import the rel
#https://opcua-asyncio.readthedocs.io/en/latest/usage/get-started/minimal-server.html

import asyncio

from asyncua import Server, ua
from asyncua.common.methods import uamethod


@uamethod
def func(parent, value):
    return value * 2


async def main():
    # setup our server
    server = Server() #server object is created
    await server.init() #server is initialized
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/") #the 'endpoint' is created. This is per OPC IA and defines how a server may be accessed by clients
                        #protocol://IPaddress:port/Namespace/path/


    # setting a namespace is not technically required but is recommended per OPCUA
    #A namespace is used to identify OPCUA nodes. My server is not a 'node' however it is the 'host' that provides the address space containing nodes
    #The details of this are related to indexing, node organization, and other specifics to the OPCUA standard
    uri = "http://examples.freeopcua.github.io" #uniform resource identifier (uri) is a unique identifier for the namespace. OPCUA best practices recommend using uri that represents a domain/URL
    idx = await server.register_namespace(uri)



    # populating our address space that was defined above
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, "MyObject") #an object is created. This object node is added to my server
    myvar = await myobj.add_variable(idx, "MyVariable", 6.7) #a variable is created and added to myobj that was just created
    # Set MyVariable to be writable by clients
    await myvar.set_writable()
    await server.nodes.objects.add_method(
        ua.NodeId("ServerMethod", idx),
        ua.QualifiedName("ServerMethod", idx),
        func,
        [ua.VariantType.Int64],
        [ua.VariantType.Int64],
    )
    async with server:
        while True:
            await asyncio.sleep(1)
            new_val = await myvar.get_value() + 0.1
            await myvar.write_value(new_val)


if __name__ == "__main__":
    asyncio.run(main(), debug=True)