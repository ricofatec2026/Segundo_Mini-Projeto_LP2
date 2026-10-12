# Mini Projeto 2 — LGPD (Linguagem de Programação 2)

Projeto individual da disciplina **Estrutura de Dados / Linguagem de Programação 2** (Fatec Rio Claro — Tecnologia em Inteligência Artificial), com o objetivo de aplicar conceitos de anonimização de dados pessoais seguindo a **LGPD (Lei Geral de Proteção de Dados)**.

O projeto consome dados de uma tabela `usuarios` em um banco PostgreSQL remoto (nome, CPF, e-mail, telefone, data de nascimento) e aplica regras de mascaramento/anonimização sobre os campos sensíveis.

## Estrutura

```
Mini_Projeto_2/
├── Atividade_LGPD.pdf     # Enunciado oficial da atividade
├── LGPD.py                # Script principal
├── requirements.txt       # Dependências do projeto
├── README.md
└── .gitignore
```

## Requisitos da atividade

1. **Atividade 1** — Implementar a função `LGPD(row)` para anonimizar os campos `nome`, `cpf`, `email` e `telefone` de cada registro.
2. **Atividade 2** — Gerar arquivos separados por ano de nascimento (ex.: `1990.csv`), contendo os dados anonimizados.
3. **Atividade 3** — Gerar um único arquivo consolidado (`todos.csv`) com `nome` e `cpf` de todos os usuários, **sem** anonimização.
4. **Atividade 4** — Usar o decorator `medir_tempo` para medir e logar o tempo de execução das Atividades 2 e 3.

## Regras de anonimização (Atividade 1)

| Campo | Regra | Exemplo |
|---|---|---|
| Nome | Mantém a 1ª letra da primeira palavra, mascara o restante dela; demais palavras ficam intactas | `Olivia Araújo` → `O***** Araújo` |
| CPF | Mantém os 3 primeiros dígitos, mascara os demais preservando pontuação | `237.615.809-59` → `237.***.***-**` |
| E-mail | Mantém a 1ª letra da parte local, mascara o restante; domínio intacto | `nuneserick@example.com` → `n*********@example.com` |
| Telefone | Mantém apenas os 4 últimos dígitos | `+55 (011) 9483-6810` → `6810` |

## Status do progresso

- [x] Função de anonimização de **nome** — implementada e validada contra o exemplo do enunciado
- [x] Função de anonimização de **CPF** — implementada e validada contra o exemplo do enunciado
- [x] Função de anonimização de **e-mail** — implementada e validada contra o exemplo do enunciado
- [x] Função de anonimização de **telefone** — implementada e validada contra o exemplo do enunciado
- [x] Integração das funções na `LGPD(row)` principal
- [x] Atividade 2 — geração de arquivos CSV por ano de nascimento (dados anonimizados), com `@medir_tempo`
- [ ] Atividade 3 — geração do arquivo consolidado `todos.csv`
- [ ] Atividade 4 — aplicação do `medir_tempo` na Atividade 3 (já aplicado na Atividade 2) e registro em log

## Como executar

```bash
pip install -r requirements.txt
python LGPD.py
```

> O script se conecta a um banco PostgreSQL remoto já disponibilizado pela disciplina. As credenciais de conexão estão hardcoded no script conforme fornecido pelo professor.

## Tecnologias

- Python 3
- SQLAlchemy
- psycopg2 (driver PostgreSQL)
- Faker (geração de dados fictícios, se aplicável)
