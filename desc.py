import random
import json
desc = ['Красивый', 'Малый', 'Мегахорош', 'Чайник', 'Парапампам', 'Норм', 'Поховат',
        'Умывальник', 'Советский мультфильм', 'Советская изотерика', 'Совок', 'Красивая',
        'Просто калыч', 'Афигиваю', 'Хороший мультфильм']

d = {i: random.sample(desc, random.randint(1, 3)) for i in range(1, 99)}
with open('desc.json', 'w+', encoding='utf-8') as f:
        json.dump(d, f, indent=2)

