WORDS = {
    'ru': {
        'ПРОФЕССИЯ': ['СВАРЩИК', 'СПАСАТЕЛЬ', 'ПОВАР'],
        'ЖИВОТНОЕ': ['ЛИЧИНКА', 'МЕДУЗА', 'ОРАНГУТАН'],
        'ТРАНСПОРТ': ['ПОЕЗД', 'ВЕЛОСИПЕД', 'ЛОКОМОТИВ']
    },
    'en': {
        'PROFESSION': ['WELDER', 'RESCUER', 'COOK'],
        'ANIMAL': ['LARVA', 'MEDUSA', 'ORANGUTAN'],
        'TRANSPORT': ['TRAIN', 'BIKE', 'LOCOMOTIVE']
    }
}


lng = input('Язык: ').lower()
category = input('Категория: ').upper()
word = input('Слово: ').upper()

WORDS[lng].setdefault(category, []).append(word)

print(WORDS[lng])