import asyncio
from websockets.server import serve
from websockets import WebSocketServerProtocol
import json
import subprocess
import os
import webbrowser
import logging
from typing import Callable
from utility import (create_config_file, check_baselines,
                     kill_all_pythons, read_config_file,
                     start_serving_frontend, update_config_file)


logging.basicConfig(level=logging.INFO)
CLIENTS = {}
MESSAGE_MAP: dict[str, Callable] = {}
__catalogs = [
    # {
    #     "name": "Test1",
    #     "baselines": ["docx", "pdf", "jpg", "png", "xlsx", "pptx", ],
    # },
    # {
    #     "name": "Test2",
    #     "baselines": ["docx", "pdf", "jpg", "png",  "pptx", ],
    # },
    # {
    #     "name": "Test3",
    #     "baselines": ["docx", "pdf", "png", "xlsx", "pptx", ],
    # }
]
__paths_config = {}


async def send_message(websocket: WebSocketServerProtocol,
                       action: str,
                       destination: str, data: dict):
    message = {'origin': 'server',
               'action': action,
               'destination': destination,
               'data': data
               }
    await websocket.send(json.dumps(message))


def subscribe_to_message(action: str, message_handler: Callable):
    MESSAGE_MAP[action] = message_handler


def unsubscribe_from_message(action: str):
    del MESSAGE_MAP[action]


async def handle_message(websocket: WebSocketServerProtocol, message: dict):
    action = message.get('action')
    handler = MESSAGE_MAP.get(action)
    if handler:
        await handler(websocket, message)


async def on_mps_catalogs(websocket: WebSocketServerProtocol, message: dict):
    data = message.get('data')
    if data:
        catalogs = data.get('catalogs')
        # print(catalogs)
        if catalogs:
            extensions = ["docx", "pdf", "jpg", "png", "xlsx", "pptx"]
            for catalog in catalogs:
                processed_catalog = {
                    "name": catalog,
                    "baselines": []
                }
                for extension in extensions:
                    if check_baselines(__paths_config['baselineDirectory'],
                                       catalog, extension):
                        processed_catalog['baselines'].append(extension)

                global __catalogs
                __catalogs.append(processed_catalog)


async def on_mps_first_connection(websocket: WebSocketServerProtocol):
    await send_message(websocket, "get-catalogs", "mps", {})
    # await send_message(websocket, "get-paths", "mps", {})


async def on_frontend_first_connection(websocket: WebSocketServerProtocol):
    global __catalogs
    await send_message(websocket, "set-catalogs", "frontend", {
        'catalogs': __catalogs
    })
    global __paths_config
    await send_message(websocket, "set-paths", "frontend", {
        'paths': __paths_config
    })


async def on_update_paths(websocket: WebSocketServerProtocol, message: dict):
    data = message.get('data')
    if data:
        paths = data.get('paths')
        if paths:
            global __paths_config
            __paths_config = paths
            update_config_file(os.path.join(os.path.dirname(
                __file__), "config.json"), paths)

            await send_message(websocket, "set-paths", "frontend", {
                'paths': __paths_config
            })


async def hadle_ping(websocket: WebSocketServerProtocol, message: dict):
    origin = message.get('origin')
    await send_message(websocket, 'pong', message['origin'], {})
    CLIENTS.setdefault(origin, websocket)

    if origin == 'frontend':
        await on_frontend_first_connection(websocket)
    elif origin == 'mps':
        await on_mps_first_connection(websocket)


async def run_test(websocket, data: dict):
    test_data = data.get('data')
    if test_data:
        catalog_name = test_data.get('catalog_name')
        subject_path = test_data.get('subject_path')
        reference_path = test_data.get('reference_path')
        test_type = test_data.get('test_type')
        output_path = test_data.get('output_path')
        cmd = ['python', os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      r'run_stiEF_test.py'),
               '--name', catalog_name,
               '--subject', subject_path,
               '--reference', reference_path,
               '--prefix', f'{catalog_name}_',
               '--test', f"test_{test_type}",
               '--results', output_path,
               '--junitxml',  os.path.join(output_path,
                                           f'{catalog_name}_{test_type}.xml')]

        try:
            output = subprocess.check_output(cmd)
            exit_code = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            exit_code = e.returncode

        message = {'exit_code': exit_code,
                   "catalog_name": catalog_name,
                   "test_type": test_type,
                   "output": output.decode("utf-8") if output else ""}

        await send_message(websocket, 'test-result', 'frontend', message)


async def echo(websocket: WebSocketServerProtocol,):
    async for message in websocket:
        logging.info(message)
        decoded_message = json.loads(message)
        # print(decoded_message)

        destination = decoded_message.get('destination')

        if destination != "server":
            coresponding_socket = CLIENTS.get(destination)
            if coresponding_socket:
                await coresponding_socket.send(message)

        else:
            await handle_message(websocket, decoded_message)


async def main():
    # kill_all_pythons()
    # start_serving_frontend()

    config_file_path = os.path.join(
        os.path.dirname(__file__), "config.json")

    if not os.path.exists(config_file_path):
        create_config_file()

    global __paths_config
    __paths_config = read_config_file(config_file_path)

    url = "http://localhost:8100/"

    MESSAGE_MAP['ping'] = hadle_ping
    MESSAGE_MAP['run-test'] = run_test
    MESSAGE_MAP['set-catalogs'] = on_mps_catalogs
    MESSAGE_MAP['update-paths'] = on_update_paths

    # webbrowser.open(url, new=0, autoraise=True)
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

# asyncio.run(main()) # not needed from jupyter notebook, can just call main()
# await main()
if __name__ == "__main__":
    asyncio.run(main())
