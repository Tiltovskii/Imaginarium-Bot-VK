import json
import vk
from config import access_token
import random

session = vk.Session(access_token=access_token)
vkapi = vk.API(session, v='5.131')


async def find_unique_word(desc: dict, nums_of_subdict: dict) -> tuple:
    enum_nums = list(enumerate(nums_of_subdict, start=1))
    random.shuffle(enum_nums)
    for i, index in enum_nums:
        name = set(desc[str(index)].copy())
        for j in set(nums_of_subdict) - {index}:
            name -= set(desc[str(j)])
        if name:
            name = list(name)
            return name[0], i
    return 'Нет уникальных слов', 1


async def update_json(id: str):
    id = str(id)
    try:
        with open("stats.json", "r") as jsonFile:
            data = json.load(jsonFile)
    except:
        data = {}
    if id in data.keys():
        data[id] += 3
    else:
        data[id] = 3

    with open("stats.json", "w") as jsonFile:
        json.dump(data, jsonFile)


async def how_many_points(id):
    id = str(id)
    with open("stats.json", "r") as jsonFile:
        data = json.load(jsonFile)
    return data[id]


async def get_photos_ids(url, id):
    album_id = url.split('/')[-1].split('_')[1]
    owner_id = url.split('/')[-1].split('_')[0].replace('album', '')
    photos = vkapi.photos.get(owner_id=owner_id, album_id=album_id, count=1000)
    description = {}
    names_of_photos = []
    for photo in photos['items']:
        name = 'photo' + str(owner_id) + '_' + str(photo['id'])
        description[name] = photo['text'].split()
        names_of_photos.append(name)

    id2desc = {id: description}
    with open("desc.json", "w+") as jsonFile:
        json.dump(id2desc, jsonFile, indent=2)

    return names_of_photos


