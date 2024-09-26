import json

def remove_item(name):
    with open('../world_generator/room.json') as f:
        room = json.load(f)

        for item in room['items']:
            if name in item:
                del item['name']


        for item in room['items']:
            print(item)

    



remove_item('Candle')