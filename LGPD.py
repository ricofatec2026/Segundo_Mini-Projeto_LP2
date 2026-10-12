from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime

import csv
import os
import time
from collections import defaultdict
from functools import wraps
def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        print(f"⏱ Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper

engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2", echo=False)
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)


# --- Funções de anonimização (Atividade 1) ---

def anonimizar_nome(nome: str) -> str:
    """Olivia Araújo -> O***** Araújo (mascara só a primeira palavra, mantém o restante)"""
    palavras = nome.split(" ", 1)
    primeira = palavras[0]
    resto = palavras[1] if len(palavras) > 1 else ""

    if len(primeira) <= 1:
        primeira_mascarada = primeira
    else:
        primeira_mascarada = primeira[0] + "*" * (len(primeira) - 1)

    return f"{primeira_mascarada} {resto}".strip()


def anonimizar_cpf(cpf: str) -> str:
    """237.615.809-59 -> 237.***.***-** (mantém os 3 primeiros dígitos, mascara o restante)"""
    partes = cpf.split(".")
    primeira = partes[0]

    resto_mascarado = []
    for parte in partes[1:]:
        if "-" in parte:
            bloco, sufixo = parte.split("-")
            resto_mascarado.append("*" * len(bloco) + "-" + "*" * len(sufixo))
        else:
            resto_mascarado.append("*" * len(parte))

    return primeira + "." + ".".join(resto_mascarado)


def anonimizar_email(email: str) -> str:
    """nuneserick@example.com -> n*********@example.com (mantém 1ª letra do usuário, mascara o resto; domínio intacto)"""
    usuario, dominio = email.split("@", 1)

    if len(usuario) <= 1:
        usuario_mascarado = usuario
    else:
        usuario_mascarado = usuario[0] + "*" * (len(usuario) - 1)

    return f"{usuario_mascarado}@{dominio}"


def anonimizar_telefone(telefone: str) -> str:
    """+55 (011) 9483-6810 -> 6810 (mantém só os últimos 4 dígitos)"""
    return telefone[-4:]


def LGPD(row):
    """Recebe um registro de 'usuarios' e retorna uma tupla com nome, CPF,
    e-mail e telefone anonimizados. id, data_nascimento, created_on e
    updated_on permanecem inalterados."""
    nome = anonimizar_nome(row[1])
    cpf = anonimizar_cpf(row[2])
    email = anonimizar_email(row[3])
    telefone = anonimizar_telefone(row[4])

    return (
        row[0],      # id - mantém
        nome,        # anonimizado
        cpf,         # anonimizado
        email,       # anonimizado
        telefone,    # anonimizado
        row[5],      # data_nascimento - mantém
        row[6],      # created_on - mantém
        row[7],      # updated_on - mantém
    )


# --- Atividade 2: gerar um CSV por ano de nascimento (dados anonimizados) ---

COLUNAS = ["id", "nome", "cpf", "email", "telefone", "data_nascimento", "created_on", "updated_on"]


@medir_tempo
def gerar_arquivos_por_ano(usuarios_anonimizados, pasta_saida="."):
    por_ano = defaultdict(list)
    for user in usuarios_anonimizados:
        ano = user[5].year  # data_nascimento está no índice 5
        por_ano[ano].append(user)

    for ano, registros in por_ano.items():
        nome_arquivo = os.path.join(pasta_saida, f"{ano}.csv")
        with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(COLUNAS)
            writer.writerows(registros)
        print(f"Arquivo {nome_arquivo} gerado com {len(registros)} registro(s).")


# --- Execução principal ---

users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios;"))
    for row in result:
        row = LGPD(row)
        users.append(row)

for user in users:
    print(user)

gerar_arquivos_por_ano(users)
