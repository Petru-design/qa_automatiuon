import asyncio
from websockets.server import serve
from websockets import WebSocketServerProtocol
import json
import subprocess
import os
import webbrowser


CLIENTS = {}


async def run_test(websocket, catalog_name, subject_path, reference_path, test_type, output_path):

    cmd = ['python', r'C:\Costum\Work\qa_automation\run_stiEF_test.py',
           '--name', catalog_name,
           '--subject', subject_path,
           '--reference', reference_path,
           '--prefix', f'{catalog_name}_',
           '--test', f"test_{test_type}",
           '--results', output_path,
           '--junitxml',  os.path.join(output_path, f'{catalog_name}_{test_type}.xml')]
    print(cmd)

    try:
        output = subprocess.check_output(cmd)
        exit_code = 0
    except subprocess.CalledProcessError as e:
        output = e.output
        exit_code = e.returncode
    print(output)

    print(exit_code)
    message = {'origin': 'server',
               'action': 'test result',
               'destination': 'frontend',
               'data': {'exit_code': exit_code,
                        "catalog_name": catalog_name, }
               }
    await websocket.send(json.dumps(message))


async def echo(websocket: WebSocketServerProtocol,):
    async for message in websocket:
        decoded_message = json.loads(message)
        print(decoded_message)

        origin = decoded_message.get('origin')
        action = decoded_message.get('action')
        destination = decoded_message.get('destination')

        if origin == 'frontend':
            if destination == 'server' and action == 'hello':
                CLIENTS['frontend'] = websocket
                response = {'origin': 'server',
                            'action': 'hello',
                            'destination': 'frontend',
                            'data': 'Connected to server'
                            }
                await websocket.send(json.dumps(response))

            elif destination == 'server' and action == 'run test':
                # {'origin': 'frontend', 'action': 'run test', 'destination': 'MPS', 'data':
                # {'catalog_name': 'L2-test', 'subject_path': 'C:\\Costum\\Work\\stief\\testoutput\\L2-test/L2-test.docx', 'reference_path': 'C:\\Costum\\Work\\stief\\baseline\\L2-test/L2-test.docx', 'test_type': 'docxText', 'output_path': 'C:\\Costum\\Work\\stief\\results\\'}}
                print("running test...")
                data = decoded_message.get('data')
                await run_test(websocket,
                               catalog_name=data.get('catalog_name'),
                               subject_path=data.get('subject_path'),
                               reference_path=data.get('reference_path'),
                               test_type=data.get('test_type'),
                               output_path=data.get('output_path'))
            elif destination == 'MPS':
                # forward messages to MPS client
                mps_client = CLIENTS.get('MPS')
                if mps_client:
                    await mps_client.send(message)

        if origin == 'MPS':
            # handle MPS messages
            if destination == 'server' and action == 'hello':
                CLIENTS['MPS'] = websocket
                response = {'origin': 'server',
                            'action': 'hello',
                            'destination': 'MPS',
                            'data': 'Connected to server'
                            }
                await websocket.send(json.dumps(response))

            if destination == 'frontend':
                # forward messages to frontend client
                frontend_client = CLIENTS.get('frontend')
                if frontend_client:
                    await frontend_client.send(message)


async def main():
    url = "http://localhost:8100/"

    webbrowser.open(url, new=0, autoraise=True)
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

# asyncio.run(main()) # not needed from jupyter notebook, can just call main()
# await main()
asyncio.run(main())
