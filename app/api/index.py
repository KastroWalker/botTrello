# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Script para automatizar tarefa no trello
    
    Utilizando a API do Trello:
    https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/

    Criado por: Victor Castro
    site: kastrowalker.github.io
"""

import json
import requests
from tqdm import tqdm
from config import *


def getID():
    """
        Função para pegar o idMember do usuario
        Retorna str(idMember)
    """
    global TOKEN
    global KEY

    url = f"https://api.trello.com/1/token/{TOKEN}"

    headers = {"Accept": "application/json"}

    query = {'key': KEY, 'token': TOKEN}

    response = requests.request(
        "GET", url, headers=headers, params=query).json()

    return response['idMember']


def getBoardID(id_member):
    """
        Função para pegar o id do quadro
        Recebe:
            str(id_member) - idMember do usuario
        Retorna:
            str(board_id) - id do quadro
    """
    global TOKEN
    global KEY

    url = f"https://api.trello.com/1/members/{id_member}/boards/"

    headers = {"Accept": "application/json"}

    query = {'key': KEY, 'token': TOKEN}

    response = requests.request(
        "GET", url, headers=headers, params=query).json()

    return response[1]['id']


def getListID(board_id):
    """
        Função para pegar o id da lista
        Recebe:
            str(boar_id) - id do quadro que vai pegar a lista
        Retorna:
            str(list_id) - id da lista
    """
    global TOKEN
    global KEY

    url = f"https://api.trello.com/1/boards/{board_id}/lists"

    headers = {"Accept": "application/json"}

    query = {'key': KEY, 'token': TOKEN}

    response = requests.request(
        "GET", url, headers=headers, params=query).json()

    return response[0]['id']


def createCard(card_name, list_id):
    """
        Função para criar o card
        Recebe:
            str(card_name) - nome do card
            str(list_id) - id da lista que vai ser criado o card
        Retorna:
            str(card_id) - id do card criado
    """
    global KEY
    global TOKEN

    url = f"https://api.trello.com/1/cards"

    query = {'name': card_name, 'idList': list_id, 'key': KEY, 'token': TOKEN}

    response = requests.request("POST", url, params=query).json()

    return response["id"]


def createCheckList(check_list_name, card_id):
    """
        Função para criar os checklist no card do curso
        Recebe:
            str(check_list_name) - nome do checklist a ser criado
            str(card_id) - id do card que vai ser criado os checklist
        Retorna:
            str(check_id) - id do checklist criado 
    """
    global KEY
    global TOKEN

    url = "https://api.trello.com/1/checklists"

    query = {'name': check_list_name, 'key': KEY,
             'token': TOKEN, 'idCard': card_id}

    response = requests.request("POST", url, params=query).json()

    return response["id"]


def createCheckItem(item_name, check_id):
    """
        Função para criar o item do checklist no checklist do modulo
        Recebe:
            str(item_name) - nome do item que vai ser criado
            str(check_id) - id do checklist que vai ser criado o item
        Retorna:
            str(check_id) - id do item criado
    """
    global KEY
    global TOKEN

    url = f"https://api.trello.com/1/checklists/{check_id}/checkItems"

    query = {'key': KEY, 'token': TOKEN, 'name': item_name}

    response = requests.request("POST", url, params=query).json()

    return response["id"]


def grava_aulas(file_aulas, card_id):
    """
        Função para criar os checklist no card do curso
        Recebe:
            json(file_aulas) - arquivo json com as aulas dentro
            str(card_id) - id do card que vai ser criado os checklist
    """
    print("Lendo aulas...")
    file_json = open(file_aulas, 'r')

    data = data = json.load(file_json)

    capitulo = None
    check_id = None

    print("Gravando aulas...")
    for aula in tqdm(range(len(data['results']))):
        if (data['results'][aula]['_class'] == 'chapter'):
            capitulo = f"Capítulo: {data['results'][aula]['title']}"
            check_id = createCheckList(capitulo, card_id)
            continue
        else:
            class_name = data['results'][aula]['title']
            createCheckItem(class_name, check_id)


def main():
    id_member = getID()
    card_id = "5eed893b6d23b3294c7656cc"
    grava_aulas(FILE_COURSE, card_id)

    # board_id = getBoardID(id_member)
    # list_id = getListID(board_id)
    # print(createCard('Teste 1', list_id))
    # ler_aulas(FILE_COURSE, card_id)
    # print(createCheckList('teste 2', card_id))
    # check_id = "5eed8aead241935b0dd06ed0"
    # print(createCheckItem('item 1', check_id))


main()
