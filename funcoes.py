from time import sleep
from rich.console import Console
from rich import print
from rich.panel import Panel
import sqlite3
from datetime import datetime

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

def cinput(prompt):
    while True:
        try:
            calendar = input(prompt)
            datetime.strptime(calendar, '%d/%m/%Y')
            return calendar
        except ValueError:
            print('[red bold]Tente novamente,tente escrever dia/mês/ano[/]')


class Gatilhos:
    @staticmethod
    def salvar():
        while True:
            nome = ninput('O nome do gatilho: ')
            if not validador(nome, 'nome', 'gatilhos'):
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
                        print(lista[0][0])
                        banco_('''DELETE FROM gatilhos WHERE nome LIKE ?''', (f'%{lista[0][0]}%',))
                input('Aperte ENTER: ')
                break

class Diario:
    @staticmethod
    def escrever():
        data = datetime.today().date()
        fstring = f'{data:%d/%m/%Y}'
        cursor = buscar(fstring, 'data', 'diario').fetchall()
        if len(cursor) > 0:
            lista = cursor
            string = lista[0][1]
            str_a_in = string + input('O que você quer escrever a mais em seu diário?: ')
            banco_('''UPDATE diario SET texto = ?
            WHERE data = ?''', (str_a_in, fstring))
        else:
            banco_(f'''INSERT INTO diario
            (data, texto)
            VALUES
            (?, ?)''', (fstring,input('O que você quer escrever em seu diário?: ')))
            print(fstring)
    @staticmethod
    def ler():
        data = cinput('Digite a data para você ler o que você escreveu no dia: ')
        lista = banco_('''SELECT texto FROM diario 
        WHERE data LIKE ?''', (data,)).fetchall()
        painel = Panel(lista[0][0], expand=False, title=data)
        print(painel)
        input('Aperte ENTER: ')


class Ofensiva:
    @staticmethod
    def quebra():
        data = datetime.today().date()
        fstring = f'{data:%d/%m/%Y}'
        banco_('''INSERT INTO ofensiva
        (nome, data)
        VALUES
        (?,?)''', ('quebra de ofensiva', fstring))
    @staticmethod
    def inicio():
        data = datetime.today().date()
        fstring = f'{data:%d/%m/%Y}'
        if len(buscar('inicio', 'nome', 'ofensiva').fetchall()) == 0:
            banco_('''INSERT INTO ofensiva
            (nome, data)
            VALUES
            (?,?)''', ('inicio', fstring))
        else:
            print('[red bold]Não pode escrever um novo inicio![/]')
    @staticmethod
    def dias():
        dataf = buscar('inicio', 'nome', 'ofensiva').fetchall()[0][1]
        split = dataf.split('/')
        data = datetime.fromisoformat(f'{split[2]}-{split[1]}-{split[0]}')
        delta = datetime.today().date() - data.date()
        lista = banco_('''SELECT * FROM ofensiva''').fetchall()
        print(f'[blue]Temos {str(delta).split()[0]} dias da sua longa caminhada para fugir do vício.[/]')
        try:
            dataf = buscar('quebra de ofensiva', 'nome', 'ofensiva').fetchall()[-1][1]
            split = dataf.split('/')
            data = datetime.fromisoformat(f'{split[2]}-{split[1]}-{split[0]}')
            delta = datetime.today().date() - data.date()
            print(f'[purple]Você tem {str(delta).split()[0]} dias desde da sua ultima quebra de ofensiva.[/]')
        except IndexError:
            dataf = str(delta).split()[0]
            print(f'[purple]Você tem {dataf} dias desde da sua ultima quebra de ofensiva.[/]')
        input('Aperte ENTER: ')

def limitador(prompt, min= 1, max =3):
    while True:
        try:
            dados = int(input(prompt))
            if min <= dados <= max:
                return dados
            else:
                print('Dados fora do limite')
                pass
        except ValueError:
            print('Valor incorreto')
            continue


def system():
    create()
    while True:
        public_interface()
        pergunta = limitador('Escolha um entre as opções: ')
        print('\n'*50)
        if pergunta == 1:
            painel = Panel('''1. Salvar
2. Buscar''')
            print(painel)
            pergunta = limitador('Escolha um entre as opções: ', max=2)
            if pergunta == 1:
                Gatilhos().salvar()
            else:
                Gatilhos().busca()
        elif pergunta == 2:
            painel = Panel('''1. inicio
2. Quebra de ofensiva
3. Dias de ofensiva''')
            print(painel)
            pergunta = limitador('Escolha um entre as opções: ')
            if pergunta == 1:
                Ofensiva().inicio()
            elif pergunta == 2:
                Ofensiva().quebra()
            else:
                Ofensiva().dias()
        else:
            painel = Panel('''1. Escrever
2. Ler''')
            print(painel)
            pergunta = limitador('Escolha um entre as opções: ', max=2)
            if pergunta == 1:
                Diario().escrever()
            else:
                Diario().ler()
        print('\n' * 50)