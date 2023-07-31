


<details>
  <summary><strong>English</strong></summary><br />

# Welcome to **countries_dw**

- [Welcome to **countries\_dw**](#welcome-to-countries_dw)
    - [Description](#description)
    - [How to use](#how-to-use)
    - [Next steps](#next-steps)

### Description
This project consumes [REST Countries](https://restcountries.com/) API and parses its data into dataframes. 
There are several informations available and it was chosen for being open source to practice data engineering techniques. 

Data from all countries are recieved as a list of dictionaries in a json response. 

[Country class](https://github.com/canutera/countries_dw/blob/master/src/country.py) is responsible for parsing and assembling tables for
each country contained in the response.

[CountriesHook](https://github.com/canutera/countries_dw/blob/master/src/countries_hook.py) makes a GET request at [All countries endpoint](https://restcountries.com/v3.1/all)
and save a json file with information. Then parses and concatenates information from every country to save all tables at the [data folder](https://github.com/canutera/countries_dw/tree/master/data). This project uses Pandas for manipulating data, so all pandas files formats are supported.


### How to use

To start using this repository, create a project folder, open a terminal and Git Clone using the [countries_dw url](https://github.com/canutera/countries_dw.git).
```bash
git clone https://github.com/canutera/countries_dw.git
```
This project uses [Poetry](https://python-poetry.org/) to manage its dependencies. 
To use Poetry, make sure you have this python package installed. If you don't, run the following command:
```bash
pip install poetry
```
Then run:
```bash
poetry config virtualenvs.in-project true
poetry install
```
To install the project dependencies inside the current folder. After installing run:
```bash
poetry shell
activate
```
Your brand new virtual envinroment should be setup and ready to use after these steps.

The example below, shows a simple usage for countries_dw project which can be found in main.py file:
```python
from src.countries_hook import CountriesHook
file_format = 'parquet'
hook = (CountriesHook()
            .parse_countries()
            .parse_tables()
            .save_tables(file_format, index=False)
        )
```
If you run the following code in a Jupyter Notebook, make sure you are connected to the created virtual environment for this project.
After running the code above, all tables should appear in the data folder. Just make sure, a valid format was passed.
You can check [pandas.DataFrame Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) to look for valid formats.

### Next steps

- [ ] Set up a WSL 
- [ ] Set up a PostgreSQL database to store table
- [ ] Create data model and documentation














<h1 align="center">Hi 👋, I'm Gabriel Canuto</h1>
<h3 align="center">Another curious person on a data journey</h3>

<h3 align="left">Connect with me:</h3>
<p align="left">
<a href="https://linkedin.com/in/gabriel-canuto0" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="gabriel-canuto0" height="30" width="40" /></a>
<a href="https://instagram.com/gabriel_canuto" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="gabriel_canuto" height="30" width="40" /></a>
</p>

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/> </a> <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>


</details>
<details>
  <summary><strong>Português</strong></summary><br />
  
- [Bem-vindo ao **countries\_dw**](#bem-vindo-ao-countries_dw)
    - [Descrição](#descrição)
    - [Como usar](#como-usar)
    - [Próximos passos](#próximos-passos)
  
# Bem-vindo ao **countries_dw**

### Descrição
Este projeto consome a API [REST Countries](https://restcountries.com/) e transforma seus dados em dataframes.
Há várias informações disponíveis e foi escolhida por ser de código aberto para praticar técnicas de engenharia de dados.

Os dados de todos os países são recebidos como uma lista de dicionários em uma resposta json.

A classe [Country](https://github.com/canutera/countries_dw/blob/master/src/country.py) é responsável por transformar e montar tabelas para cada país contido na resposta.

O [CountriesHook](https://github.com/canutera/countries_dw/blob/master/src/countries_hook.py) faz uma requisição GET no [endpoint de todos os países](https://restcountries.com/v3.1/all) e salva um arquivo json com as informações. Em seguida, ele transforma e concatena as informações de cada país para salvar todas as tabelas na [pasta de dados](https://github.com/canutera/countries_dw/tree/master/data). Este projeto usa o Pandas para manipular dados, portanto, todos os formatos de arquivos do Pandas são suportados.

### Como usar

Para começar a usar este repositório, crie uma pasta de projeto, abra um terminal e clone o repositório Git usando a [URL do countries_dw](https://github.com/canutera/countries_dw.git).
```bash
git clone https://github.com/canutera/countries_dw.git
```
Este projeto usa o [Poetry](https://python-poetry.org/) para gerenciar suas dependências. 
Para usar o Poetry, certifique-se de ter esse pacote Python instalado. Se não tiver, execute o seguinte comando:
```bash
pip install poetry
```
Em seguida, execute:
```bash
poetry config virtualenvs.in-project true
poetry install
```
Para instalar as dependências do projeto dentro da pasta atual. Após a instalação, execute:
```bash
poetry shell
activate
```
Seu novo ambiente virtual deve estar configurado e pronto para uso após essas etapas.

O exemplo abaixo mostra um uso simples do projeto countries_dw, que pode ser encontrado no arquivo main.py:
```python
from src.countries_hook import CountriesHook
file_format = 'parquet'
hook = (CountriesHook()
            .parse_countries()
            .parse_tables()
            .save_tables(file_format, index=False)
        )
```
Se você executar o código acima em um Jupyter Notebook, verifique se está conectado ao ambiente virtual criado para este projeto.
Depois de executar o código acima, todas as tabelas devem aparecer na pasta de dados. Apenas certifique-se de passar um formato válido.
Você pode consultar a [documentação do pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) para ver os formatos válidos.

### Próximos passos

- [ ] Configurar um WSL
- [ ] Configurar um banco de dados PostgreSQL para armazenar tabelas
- [ ] Criar modelo de dados e documentação

<h1 align="center">Olá 👋, Eu sou o Gabriel Canuto</h1>
<h3 align="center">Mais uma pessoa curiosa em uma jornada de dados</h3>

<h3 align="left">Conecte-se comigo:</h3>
<p align="left">
<a href="https://linkedin.com/in/gabriel-canuto0" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="gabriel-canuto0" height="30" width="40" /></a>
<a href="https://instagram.com/gabriel_canuto" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="gabriel_canuto" height="30" width="40" /></a>
</p>

<h3 align="left">Linguagens e Ferramentas:</h3>
<p align="left"> <a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/> </a> <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>

</details>