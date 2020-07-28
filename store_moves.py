#! /bin/python
import json
import uuid
import argparse
import sys
from os import path

STORE_FILE = '../moves.json'


def load_store():
    if path.exists(STORE_FILE):
        with open(STORE_FILE) as file:
            return json.load(file)
    else:
        return []


def save_store(store):
    with open(STORE_FILE, 'w') as file:
        json.dump(store, file)


def enter_move():
    move = {}

    move['id'] = uuid.uuid4()
    move['playbook'] = input('Playbook: ')
    move['title'] = input('Title: ')
    move['description'] = input('Description: ')

    return move


def add(playbook, title, description, lines, **kwargs):
    store = load_store()
    move = {}
    move['id'] = str(uuid.uuid4())

    move['playbook'] = playbook
    move['title'] = title
    move['description'] = description

    if lines:
        elements = lines.split('\n')
        move['playbook'] = elements[0]
        move['title'] = elements[1]
        move['description'] = elements[2]

    while move['playbook'] == '':
        move['playbook'] = input('Playbook: ')

    while move['title'] == '':
        move['title'] = input('Title: ')

    while move['description'] == '':
        move['description'] = input('Description: ')

    store.append(move)
    save_store(store)


def remove(id, playbook, title, all, **kwargs):
    store = load_store()
    moves_to_delete = []
    if id is None and playbook is None and title is None:
        sys.exit('At least one of the parameters id, playbook and title needs to be provided so the moves for deletion can be selected.')

    for move in store:
        if ((id is None or id == move['id'])
                and (playbook is None or playbook == move['playbook'])
                and (title is None or title == move['title'])):
            moves_to_delete.append(move)

    if len(moves_to_delete) == 0:
        sys.exit('None of the available moves matches the criteria.')

    if all:
        store = [move for move in store if move['id']
                 not in [move['id'] for move in moves_to_delete]]
    else:
        for index in range(len(moves_to_delete)):
            print('{0}:\tid: {m[id]}\n\tplaybook: {m[playbook]}\n\ttitle: {m[title]}\n\tdescription: {m[description]}\n'.format(
                index, m=moves_to_delete[index]))
        choice = -1
        while choice not in range(len(moves_to_delete)):
            try:
                choice = int(input('Enter index to delete: '))
            except ValueError:
                pass
        del store[choice]

    save_store(store)


def show(id, playbook, title, **kwargs):
    store = load_store()
    moves_to_show = []

    for move in store:
        if ((id is None or id == move['id'])
                and (playbook is None or playbook == move['playbook'])
                and (title is None or title == move['title'])):
            moves_to_show.append(move)

    if len(moves_to_show) == 0:
        sys.exit('None of the available moves matches the criteria.')

    for index in range(len(moves_to_show)):
        print('{0}:\tid: {m[id]}\n\tplaybook: {m[playbook]}\n\ttitle: {m[title]}\n\tdescription: {m[description]}\n'.format(
            index, m=moves_to_show[index]))


def edit(id, playbook, title, description, **kwargs):
    store = load_store()
    moves = [move for move in store if move['id'] == id]
    if len(moves) == 0:
        sys.exit('No move with that id could be found.')
    move = moves[0]
    index = store.index(move)

    if playbook:
        move['playbook'] = playbook
    if title:
        move['title'] = title
    if description:
        move['description'] = description

    store[index] = move
    save_store(store)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('-p', '--playbook', type=str, default='')
    add_parser.add_argument('-t', '--title', type=str, default='')
    add_parser.add_argument('-d', '--description', type=str, default='')
    add_parser.add_argument('-l', '--lines', type=str)
    add_parser.set_defaults(command=add)

    remove_parser = subparsers.add_parser('remove')
    remove_parser.add_argument('-i', '--id', type=str)
    remove_parser.add_argument('-p', '--playbook', type=str)
    remove_parser.add_argument('-t', '--title', type=str)
    remove_parser.add_argument(
        '-a', '--all', type=bool, default=False, const=True, nargs='?')
    remove_parser.set_defaults(command=remove)

    show_parser = subparsers.add_parser('show')
    show_parser.add_argument('-i', '--id', type=str)
    show_parser.add_argument('-p', '--playbook', type=str)
    show_parser.add_argument('-t', '--title', type=str)
    show_parser.set_defaults(command=show)

    edit_parser = subparsers.add_parser('edit')
    edit_parser.add_argument('-i', '--id', type=str, required=True)
    edit_parser.add_argument('-p', '--playbook', type=str)
    edit_parser.add_argument('-t', '--title', type=str)
    edit_parser.add_argument('-d', '--description', type=str)
    edit_parser.set_defaults(command=edit)

    args = parser.parse_args()
    args.command(**vars(args))
