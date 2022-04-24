from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text
from config import token, default_album
from typing import Optional
import aiofiles
from my_tools import *
from urllib.parse import urlparse
import os.path

bot = Bot(token=token)


@bot.on.message(func=lambda m: urlparse(m.text).scheme == 'https')
async def other_album_handler(m: Message):
    async with aiofiles.open('ids2names.json', 'r') as f:
         content = await f.read()
    ids2names = json.loads(content)
    try:
        names_of_photos = await get_photos_ids(m.text, str(m.from_id))
        ids2names[str(m.from_id)] = names_of_photos
        with open("ids2names.json", "w+") as jsonFile:
            json.dump(ids2names, jsonFile, indent=2)

        await m.answer('Переключился на другой альбом')
    except:
        await m.answer('Ссылочка похоже не та')


@bot.on.message(text='Старт')
async def photos_handler(m: Message):
    async with aiofiles.open("ids2names.json", "r") as jsonFile:
        content = await jsonFile.read()
    ids2names = json.loads(content)

    async with aiofiles.open("pos.json", "r") as jsonFile:
        content = await jsonFile.read()
    positions = json.loads(content)

    if str(m.from_id) in ids2names.keys():
        names_of_photos = ids2names[str(m.from_id)]
    else:
        names_of_photos = await get_photos_ids(default_album)
        ids2names[str(m.from_id)] = names_of_photos

    if len(names_of_photos) < 5:
        await m.answer('Карточки кончились(')
        return

    rnd = random.sample(names_of_photos, 5)

    async with aiofiles.open('desc.json') as jsonFile:
        content = await jsonFile.read()
    description = json.loads(content)

    ids2names[str(m.from_id)] = list(set(names_of_photos) - set(rnd))

    await m.answer(attachment=rnd)

    word, pos = await find_unique_word(description[str(m.from_id)], rnd)
    positions[str(m.from_id)] = pos
    with open("pos.json", "w+") as jsonFile:
        json.dump(positions, jsonFile, indent=2)

    with open("ids2names.json", "w+") as jsonFile:
        json.dump(ids2names, jsonFile, indent=2)

    await m.answer(word, keyboard=(
                                    Keyboard(one_time=True, inline=False)
                                    .add(Text("Фотография 1"))
                                    .add(Text("Фотография 2"))
                                    .row()
                                    .add(Text("Фотография 3"))
                                    .add(Text("Фотография 4"))
                                    .add(Text("Фотография 5"))
                                    .get_json()
                                ))


@bot.on.message(text="Фотография <number>")
async def buttons_handler(m: Message, number: Optional[int]):
    async with aiofiles.open("pos.json", "r") as jsonFile:
        content = await jsonFile.read()
    positions = json.loads(content)
    number = int(number)
    if number == positions[str(m.from_id)]:
        await update_json(m.from_id)
        await m.answer(f'Правильно! +3 очка!\n'
                       f'У тебя очков в сумме: {await how_many_points(str(m.from_id))}')

    else:
        try:
            await m.answer(f'Неправильно(\n'
                           f'Правильный ответ был под номером {positions[str(m.from_id)]}\n'
                           f'У тебя очков в сумме: {await how_many_points(str(m.from_id))}')
        except:
            await m.answer(f'Неправильно(\n'
                           f'Правильный ответ был под номером {positions[str(m.from_id)]}\n'
                           f'У тебя очков в сумме: 0')
if __name__ == '__main__':
    if not os.path.isfile('ids2names.json'):
        ids2names = dict()
        with open("ids2names.json", "w") as jsonFile:
            json.dump(ids2names, jsonFile)

    if not os.path.isfile('pos.json'):
        positions = dict()
        with open("pos.json", "w") as jsonFile:
            json.dump(positions, jsonFile)

    bot.run_forever()
