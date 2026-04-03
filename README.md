# Analisador de Currículos
> Este projeto é apenas para treino, então esse texto é apenas uma explicação do projeto e não uma documentação

O projeto consiste em um sistema para análise de currículos, onde você pode conversar e tirar dúvidas sobre o currículo com um Agente IA que tem todo o contexto do currículo, podendo também gerar análises pré-prontas.

## Como o Agente da análise funciona
O sistema é bem simples, então ele não utiliza sistema de RAG ou algo do tipo, o que acontece é que quando você upa um currículo, o sistema coleta todo o conteúdo dele e armazena em um banco de dados, e então quando você gera uma análise por exemplo o Agente coleta o conteúdo no banco de dados, entende sobre o que é e gera a análise com uma estrutura pré-pronta. Após isso, ele armazena um resumo do currículo na própria memória, com uma técnica chamada "Memories" que o Agno utiliza.

## Como o Agente do chat funciona

O Agente do chat funciona quase da mesma forma que o anterior, mas tem algumas funcionalidades a mais.
Como ele funciona por mensagens, ele tem acesso a uma ferramenta que retorna o conteúdo do currículo que o usuário enviou, ou seja, ele pode consultar o conteudo do currículo quantas vezes quiser. Além disso, como a memória é compartilhada com o Agente de análise, o Agente do chat também tem acesso ao resumo que já foi feito antes. Isso evita consultas desnecessárias à ferramenta. Com isso, o consumo de tokens é menor, já que ele só precisa consultar a ferramenta em casos mais específicos.

## Tecnologias
As principais bibliotecas/frameworks que o projeto utiliza são:

1. `Streamlit`
2. `Agno`
3. `FastAPI`
4. `Requests`
5. `Groq`
6. `OpenAI`

## Como rodar o projeto localmente
> Atualmente o projeto só foi testado em Windows, então não posso afirmar que ele rodará com as mesmas instruções no Linux e MacOS

1. Instalar a versão mais recente do `Python`

2. Criar o venv (opcional):
```powershell

python -m venv .venv

.\.venv\Scripts\activate

```

3. Instalar as dependências:

```powershell

pip install -r requirements.txt

```

4. Rodar servidor da API:

```powershell

cd api

python -m uvicorn server:app --reload

```

5. Rodar front:

```powershell

cd interface

a streamlit run Index.py

```

