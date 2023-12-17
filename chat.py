import asyncio
import json
import roman
import re

from client import query

def sanitize(jsonish):
    jsonish = jsonish.replace('\n', '').replace('json', '')
    
    search = re.search('`(.+)`', jsonish)
    if search:
        jsonish = search.group()

    return jsonish.replace('\'', '"').replace('`', '')


def get_lines(references):
    context = ''
    for entry in references:
        canto_number = roman.toRoman(entry["canto"])

        file = open(f'cantos/{canto_number}.txt', 'r')
        canto = file.readlines()

        has_negatives = False
        building = ''

        for line_number in entry['lines']:
            if line_number < 0:
                line_number = len(canto) + line_number + 1
                has_negatives = True
            line = canto[line_number - 1]
            line = line.replace('\n', '')
            building += f'{canto_number}:{line_number}. {line}\n'

        if has_negatives:
            context += f'Canto {canto_number} is {len(canto)} lines long.'
        context += building

    return context


async def make_line_context(text):
    response = await query(text, json=True)

    references = []
    try:
        references = json.loads(sanitize(response))
    except json.decoder.JSONDecodeError:
        print(response)

    context = get_lines(references)
    return context


async def main():
    while True:
        text = input('Input text: ')
        text = f'\"{text}\"'
        context = await make_line_context(text)
        print('Context', context)
        response = await query(text, context=context)
        print(response)

asyncio.run(main())