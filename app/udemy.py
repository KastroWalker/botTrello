#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Script para automatizar tarefa no trello
    
    Criado por: Victor Castro
    site: kastrowalker.github.io
"""
from tqdm import tqdm
from selenium import webdriver
import json
import time
from config import *

def ler_aulas(file_aulas):
    """
        Função para ler o nome das aulas
        Recebe:
            json(file_aulas) - arquivo json com as aulas dentro
        Retorna:
            uma lista com os nome das aulas
    """
    print("Lendo aulas...")
    file_json = open(file_aulas, 'r')

    data = data = json.load(file_json)

    aulas = []

    print("Salvando aulas...")
    for aula in range(len(data['results'])):
        aulas.append(data['results'][aula]['title'])

    return aulas


def escreveAula(driver, titulo):
    """
        Função para inserir a aula no trello
        Recebe: 
            drive - driver do webdriver
            str(titulo) - nome do modulo
    """

    driver.find_element_by_class_name('checklist-new-item-text').send_keys(titulo)
    driver.find_element_by_class_name('js-add-checklist-item').click()


def realizaLogin(driver, email, senha):
    """
        Função para realizar login no trello
        Recebe: 
            drive - driver do webdriver
            str(email) - email do trello
            str(senha) - senha do trello
    """
    driver.get('https://trello.com/login')
    dar_nome_login = driver.find_element_by_id('user')
    dar_nome_senha = driver.find_element_by_id('password')
    dar_nome_botao = driver.find_element_by_id('login')
    dar_nome_login.send_keys(email)
    dar_nome_senha.send_keys(senha)
    dar_nome_botao.click()


def main():
    # Lendo o nome das aulas
    aulas = ler_aulas(ARQUIVO_AULAS)

    # Acessando o Trello
    print("Acessando Trello...")
    driver = webdriver.Chrome(CHROME_DRIVER)

    # Realizando login no trello
    print("Realizando login no Trello...")
    realizaLogin(driver, USER, SENHA)
    time.sleep(1)

    # Inicando Cadastro de aulas
    print("Acessando página do curso...")
    driver.get(CARTAO_TRELLO)

    # Salvando aulas no Trello
    print("Salvando aulas no Trello...")
    driver.find_element_by_class_name('js-new-checklist-item-button').click()

    for i in tqdm(range(len(aulas))):
        escreveAula(driver, aulas[i])


main()
