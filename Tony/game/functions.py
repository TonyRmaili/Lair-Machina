import json

def remove_item(name):
    name = name.lower()
    with open('../world_generator/room.json') as f:
        room = json.load(f)

    try:
        del room['items'][name]
        with open('../world_generator/room.json','w') as f:
            room = json.dump(room,f,indent=4)
    except KeyError:
        return 'No item found'
    


def add_item(name):
    name = name.lower()
    with open('../world_generator/room.json') as f:
        room = json.load(f)

    try:
        room['items'][name ] = 'New item'
        with open('../world_generator/room.json','w') as f:
            room = json.dump(room,f,indent=4)
            
    except KeyError:
        return 'No item to add found'



all_functions = {
    'remove_item':remove_item,
    'add_item':add_item
}



if __name__=='__main__':
    remove_item('table')