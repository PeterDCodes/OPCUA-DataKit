
#import the rel
#https://opcua-asyncio.readthedocs.io/en/latest/usage/get-started/minimal-server.html

import asyncio

from asyncua import Server, ua
from asyncua.common.methods import uamethod





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
    myvar = await myobj.add_variable(idx, "MyVariable", "Hello") #a variable is created and added to myobj that was just created
    # Set the variable to be writable by clients. By default variables are 'read-only' so this is needed to enable writing.
    await myvar.set_writable()

    #The above code is sufficient to create a server to run and expose some basic data

    
    #This defines a method that is callable by clients connected to the server
    #Here a decorator function is used
    @uamethod
    def func(parent, value):
        return value
    #Here, the function that is decorated with uamethod decorator above is created and registered on the server
    await server.nodes.objects.add_method(
        ua.NodeId("ServerMethod", idx),
        ua.QualifiedName("ServerMethod", idx),
        func,
        [ua.VariantType.Int64],
        [ua.VariantType.Int64],
    )


    async with server: #server is used to be the context manager for async
        while True: #this is used to keep server alive and running
            await asyncio.sleep(1) #this line is the key for managing asyncronous tasks. 
            #It basically allows the infinite loop to keep running without using CPU resources. This main loop is infinite but "pauses" while not pausing other functions or tasks
            #this is a common design patter used in programming for applications that often do a lot of 'waiting' for external tasks to happen.

if __name__ == "__main__":
     asyncio.run(main(), debug=True)