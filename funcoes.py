from time import sleep
from rich.console import Console
from rich import print
from rich.panel import Panel
import sqlite3
from datetime import date, datetime

def status(prompt:str, time:int):
    console = Console()
    def main():
        sleep(time)
    with console.status(prompt):
        main()

def print_(prompt, color, title_color = None,value=30, return_str = False ):
    if title_color is None:
        title_color = color
    string_ = f'[{color}]-[/]'*value
    string = f'{f"[{title_color}]{prompt}[/]":^{value+ len(title_color)+4}}'
    string__ = f'{string_}\n{string}\n{string_}'
    if return_str:
        return string__
    print(string__)
    return None

def public_interface():
    title = print_('Sistema Acordeon', 'blue', 'purple', 70,return_str=True)
    string = '''1 - Gatilhos
2 - Dias que você ficou sem fazer o vicio
3 - Diário de responsabilidade'''
    everyone = f'{title}\n{string}'
    painel = Panel(everyone, expand=False)
    print(painel)

def create():
    with sqlite3.Connection('dados.db') as banco:
        curso = banco.cursor()
        curso.execute('''CREATE TABLE IF NOT EXISTS gatilhos
(nome TEXT,
solucao TEXT)''')
        curso.execute('''CREATE TABLE IF NOT EXISTS ofensiva 
(nome TEXT,
data DATE)''')
        curso.execute('''CREATE TABLE IF NOT EXISTS diario(
data DATE,
texto TEXT)''')

def banco_(prompt, parametro = None):
    with sqlite3.Connection('dados.db') as banco:
        curso = banco.cursor()
        if parametro is None:
            curso.execute(prompt)
        else:
            curso.execute(prompt, parametro)
        return curso

def ninput(prompt):
    while True:
        nome = input(prompt).strip()
        if bool(nome):
            return nome
        print('[red]O nome está vazio![/]')

def buscar(nome,prompt, table):
    dado = banco_(f'''SELECT * FROM {table}
    WHERE {prompt} LIKE ?''', (f'{nome}',))
    return dado

def tabular(prompt, value = 15):
    space = ' '*(value - len(prompt))
    return prompt+space

def super_string(lista):
    string = ''
    for c in  lista:
        substr = ''
        for p in c:
            substr += tabular(p)
        string += f'{substr}\n'
    return string

def all_to_list(fetchall, lista):
    for c in fetchall:
        lista.append(c)

def list_to_panel(c1, c2, fetchall):
    lista = [(c1, c2)]
    all_to_list(fetchall, lista)
    string = super_string(lista)
    painel = Panel(string, expand=False)
    print(painel)
    return len(lista)

def validador(nome, filtro, tabela):
    busca = buscar(nome,filtro, tabela)
    lista = busca.fetchall()
    if len(lista) >0:
        return False
    else:
        return True

def delete(c1, c2 ,tabela):
    busca = buscar(c1, c2, tabela)
    lista = busca.fetchall()
    if len(lista) == 1:
        atualizar = banco_(f'''DELETE FROM {tabela} WHERE ?''', (f'%{c1}%',))
        return atualizar
    else:
        return None

def rinput(prompt):
    while True:
        try:
            numero = int(input(prompt))
            return numero
        except ValueError:
            print('[red]Valor invalido. Tente Novamente[/]')

class Gatilhos:
    @staticmethod
    def salvar():
        while True:
            nome = ninput('O nome do gatilho: ')
            if validador(nome, 'nome', 'gatilhos'):
                print('[red]Tente novamente, nome já inserido.')
            else:
                break
        solucao = input('Digite a solução do problema: ')
        banco_('''INSERT INTO gatilhos
            (nome, solucao)
        Values
            (?, ?)''',
               (f'{nome}', f'{solucao}',))
    @staticmethod
    def busca():
        interface = banco_('''SELECT nome FROM gatilhos''')
        list_to_panel('[blue]Nome[/]', '', interface)
        while True:
            nome = ninput('O nome que você quer buscar: ')
            busca_ = buscar(nome,'nome','gatilhos')
            lista = busca_.fetchall()
            tam = list_to_panel('nome', 'solução', lista)
            if tam > 2:
                try:
                    pergunta = input('deseja continuar: ').strip().upper()[0]
                except IndexError:
                    pergunta = ''
                if pergunta == 'N':
                    print('Fim de Busca.')
                    break
            else:
                string = '''[yellow]1. Você deseja continuar?[/]
[blue]2. Você deseja atualizar?[/]
[red bold]3. Você deseja deletar?[/]'''
                painel = Panel(string)
                print(painel)
                escolha = rinput('Escolha um desses valores: ')
                match escolha:
                    case 1:
                        pass
                    case 2:
                        banco_('''UPDATE gatilhos SET solucao = ?
                        WHERE nome = ?''', (input('Digite uma nova solução: '), lista[0][0]))
                    case 3:
                        delete(nome, 'nome', 'gatilhos')
                input('Aperte ENTER: ')
                break

class Diario:
    @staticmethod
    def escrever():
        data = datetime.today().date()
        fstring = f'{data:%d/%m/%Y}'
        buscar()