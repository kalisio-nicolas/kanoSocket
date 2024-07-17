

import socketio # pip install "python-socketio[asyncio_client]"
import asyncio  # pip install asyncio
import random


'''
KANO_BASE_URL : The base URL of the Kano instance
WEBSOCKET_PATH : The path of the websocket
JWT_TOKEN : The JWT token to authenticate the user
'''

KANO_BASE_URL = ""   
WEBSOCKET_PATH = "/apiws"                               
JWT_TOKEN=""
sio = socketio.AsyncClient(engineio_logger=True, logger=True)


def generateRandomGeometry():
    '''Generate a random geometry inside a bounding box (France)'''
    return {
        "type": "Point",
        "coordinates": [
            random.uniform(-5, 10),
            random.uniform(40, 52)
        ]
    }



async def main():
    headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
    # By default socketio uses the path /socket.io but Kano uses /apiws
    await sio.connect(KANO_BASE_URL, socketio_path=WEBSOCKET_PATH, headers=headers)

    # Example of sending a patch message to the server
    # Update the geometry of the features with properties.deviceId = 3 every 100ms  with a random geometry
    for i in range(0,1000): 
        newGeometry = generateRandomGeometry()
        
        await sio.emit(
            'patch',                            # The event of the operation
                (                               # The rest of the arguments are sent as a tuple
                    'api/features',             # [0] The path/name of the service
                    None,                       # [1] The document id (null for a all documents)
                    {"geometry": newGeometry},  # [2] The patch to apply
                    {                           # [3] The query to select the documents to patch
                        "upsert": True,             # Create the document if it does not exist 
                        "properties.deviceId":3     # Select the document with the deviceId
                    },  
                ),
            callback=print                       # The callback to call when the operation is finished
        )

        await asyncio.sleep(0.1)

    await sio.wait() # block the main thread until the connection is closed


if __name__ == '__main__':
    asyncio.run(main())




