Com certeza\! Abaixo está um `README.md` completo que detalha o projeto, desde a análise dos dados e do esquema do banco de dados até a implementação dos scripts de extração em Python e os próximos passos recomendados.

-----

# Projeto de Extração e Estruturação de Dados de Clientes

## 1\. Introdução e Objetivos

Este projeto tem como objetivo principal extrair dados de clientes de arquivos HTML semi-estruturados e organizá-los em um formato JSON padronizado, pronto para ser carregado em um banco de dados relacional. A solução foi desenvolvida utilizando Python, com as bibliotecas `BeautifulSoup` para a análise e extração de dados do HTML (parsing) e `pandas` para a manipulação e estruturação dos dados.

O esquema do banco de dados fornecido serviu como um guia para a modelagem dos objetos JSON, garantindo que os dados extraídos estejam alinhados com a estrutura final de armazenamento.

## 2\. Arquitetura da Solução

O processo de extração e estruturação de dados segue a seguinte arquitetura:

1.  **Fontes de Dados:** Arquivos HTML contendo informações de clientes.
2.  **Extração (Extraction):** Um script em Python utiliza a biblioteca `BeautifulSoup` para analisar a estrutura HTML e extrair os dados relevantes.
3.  **Transformação (Transformation):** Os dados extraídos são limpos, formatados e organizados em uma estrutura de dicionários em Python.
4.  **Estruturação (Structuring):** Os dicionários são convertidos para o formato JSON, seguindo a estrutura definida pelo esquema do banco de dados.
5.  **Carga (Load):** Os arquivos JSON gerados podem ser utilizados para popular o banco de dados (ETL).

## 3\. Esquema do Banco de Dados

O banco de dados foi projetado para ser robusto e flexível, suportando múltiplos endereços e telefones por cliente e garantindo a integridade dos dados. As principais tabelas que guiaram a estruturação dos dados são:

  * **CLIENTES:** Tabela principal com os dados cadastrais do cliente.
  * **ENDERECOS:** Armazena múltiplos endereços para cada cliente.
  * **TELEFONES:** Armazena múltiplos telefones para cada cliente.
  * **EMAILS:** Armazena múltiplos emails para cada cliente.
  * **DADOS\_PROFISSIONAIS:** Contém informações sobre a ocupação e cargo do cliente.
  * **DADOS\_FINANCEIROS:** Armazena dados de renda e limites de crédito.

## 4\. Análise dos Arquivos HTML

Foram analisados três arquivos HTML distintos, cada um com um layout e conjunto de informações diferentes:

  * **`paginaDadosCliente07339054553.html`**: Contém dados cadastrais, múltiplos e-mails, telefones e endereços.
  * **`paginaTelefonesCliente03375498500.html`**: Apresenta dados cadastrais, um endereço e múltiplos telefones.
  * **`paginaDadosCliente02337487504.html`**: Rico em informações profissionais e financeiras, além dos dados cadastrais básicos.

## 5\. Estrutura do JSON Gerado

Para cada cliente, é gerado um objeto JSON consolidado, que agrupa todas as informações relacionadas. Este formato facilita o manuseio dos dados antes da inserção no banco. A estrutura é a seguinte:

```json
{
  "cliente": {
    "cpf": "...",
    "nome_completo": "...",
    "data_nascimento": "...",
    "genero": "...",
    "nome_mae": "..."
  },
  "enderecos": [
    {
      "logradouro": "...",
      "bairro": "...",
      "cidade": "...",
      "estado": "...",
      "cep": "...",
      "tipo": "..."
    }
  ],
  "telefones": [
    {
      "ddd": "...",
      "numero": "...",
      "tipo": "..."
    }
  ],
  "emails": [
    {
      "email": "...",
      "tipo": "..."
    }
  ],
  "dados_profissionais": {
    "ocupacao": "...",
    "cargo": "..."
  },
  "dados_financeiros": {
    "renda_mensal": "...",
    "limite_credito": "..."
  }
}
```

## 6\. Scripts de Extração em Python

A seguir, o código Python desenvolvido para realizar a extração dos dados.

### Pré-requisitos

Para executar os scripts, é necessário ter o Python instalado e as seguintes bibliotecas:

```bash
pip install beautifulsoup4
pip install pandas
```

### Código Completo

```python
from bs4 import BeautifulSoup
import pandas as pd
import json

def extrair_dados_cliente_07339054553(html_content):
    """
    Extrai informações do cliente Abdias Souza Filho, que possui múltiplos 
    endereços, e-mails e telefones.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    cliente = {}
    enderecos = []
    telefones = []
    emails = []

    # Extração da Síntese Cadastral
    sintese_cadastral = soup.find('span', text='Síntese Cadastral')
    if sintese_cadastral:
        dados_cadastrais = sintese_cadastral.find_parent('div', class_='col-12').find_next_sibling('div')
        if dados_cadastrais:
            cliente['cpf'] = dados_cadastrais.find(string=lambda t: 'Documento' in t.find_parent().text).find_next('div').text.split('\xa0')[0].strip()
            cliente['nome_completo'] = dados_cadastrais.find(string=lambda t: 'Nome' in t.find_parent().text).find_next('div').text.strip()
            cliente['data_nascimento'] = dados_cadastrais.find(string=lambda t: 'Nascimento' in t.find_parent().text).find_next('div').text.split('\xa0')[0].strip()
            cliente['genero'] = dados_cadastrais.find(string=lambda t: 'Sexo' in t.find_parent().text).find_next('div').text.strip()
            cliente['nome_mae'] = dados_cadastrais.find(string=lambda t: 'Mãe' in t.find_parent().text).find_next('div').text.strip()

    # Extração de Emails
    secao_email = soup.find('span', text='Email')
    if secao_email:
        tabela_emails = secao_email.find_parent('div', class_='col-12').find_next_sibling('div')
        if tabela_emails:
            for email in tabela_emails.find_all('div', class_='col-12 mt-3 my-1'):
                emails.append({'email': email.text.strip(), 'tipo': 'Pessoal'})

    # Extração de Telefones
    secao_telefones = soup.find('span', text='Telefones')
    if secao_telefones:
        tabela_telefones = secao_telefones.find_parent('div', class_='col-12').find_next_sibling('div')
        if tabela_telefones:
            for telefone in tabela_telefones.find_all('div', class_='col-8 col-sm-6'):
                numero_completo = telefone.text.strip()
                ddd = numero_completo.split(')')[0].replace('(', '')
                numero = numero_completo.split(')')[1].strip()
                telefones.append({'ddd': ddd, 'numero': numero, 'tipo': 'Celular'})

    # Extração de Endereços
    secao_endereco = soup.find('span', text='Endereço')
    if secao_endereco:
        tabela_enderecos = secao_endereco.find_parent('div', class_='col-12').find_next_sibling('div')
        if tabela_enderecos:
            for row in tabela_enderecos.find_all('div', class_='row'):
                cols = row.find_all('div', class_='col-12')
                if len(cols) >= 2:
                    logradouro_bairro = cols[0].text.strip().split(',')
                    logradouro = logradouro_bairro[0]
                    bairro = logradouro_bairro[-1].strip() if len(logradouro_bairro) > 1 else None

                    cep_cidade_uf = cols[1].find_all('div', class_='col-6')
                    cep = cep_cidade_uf[1].text.strip() if len(cep_cidade_uf) > 1 else None
                    cidade_uf = cols[1].find('div', class_='col-12').text.strip().split('/')
                    cidade = cidade_uf[0] if len(cidade_uf) > 1 else None
                    uf = cidade_uf[1] if len(cidade_uf) > 1 else None

                    enderecos.append({
                        'logradouro': logradouro,
                        'bairro': bairro,
                        'cidade': cidade,
                        'estado': uf,
                        'cep': cep,
                        'tipo': 'Residencial'
                    })
    
    return {
        "cliente": cliente,
        "enderecos": enderecos,
        "telefones": telefones,
        "emails": emails
    }

def extrair_dados_cliente_03375498500(html_content):
    """
    Extrai informações do cliente Abdon Rozendo dos Santos, com foco em dados
    cadastrais, endereço e telefones.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    cliente = {}
    enderecos = []
    telefones = []

    cliente['nome_completo'] = soup.find('span', id='lblNome').text.strip()
    cliente['cpf'] = soup.find('span', id='lblCpf').text.strip()
    cliente['genero'] = soup.find('span', id='Frmdetalharcadastroclientecobranca1_lblSexo').text.strip()
    cliente['data_nascimento'] = soup.find('span', id='Frmdetalharcadastroclientecobranca1_lblData').text.strip()
    cliente['nome_mae'] = soup.find('span', id='Frmdetalharcadastroclientecobranca1_lblMae').text.strip()

    tabela_endereco = soup.find('table', id='Frmdetalharcadastroclientecobranca1_grdEnderecos')
    if tabela_endereco:
        linha_endereco = tabela_endereco.find_all('tr')[1]
        dados_endereco = [td.text.strip() for td in linha_endereco.find_all('td')]
        enderecos.append({
            'tipo': dados_endereco[0],
            'logradouro': dados_endereco[1],
            'numero': dados_endereco[2],
            'complemento': dados_endereco[3],
            'bairro': dados_endereco[4],
            'cidade': dados_endereco[5],
            'estado': dados_endereco[6],
            'cep': dados_endereco[7]
        })

    tabela_telefones = soup.find('table', id='Frmdetalharcadastroclientecobranca1_grdTelefones')
    if tabela_telefones:
        for linha in tabela_telefones.find_all('tr')[1:]:
            dados_telefone = [td.text.strip() for td in linha.find_all('td')]
            telefones.append({
                'ddd': dados_telefone[0],
                'numero': dados_telefone[1],
                'tipo': dados_telefone[2],
                'tipo_endereco': dados_telefone[3]
            })

    return {
        "cliente": cliente,
        "enderecos": enderecos,
        "telefones": telefones
    }

def extrair_dados_cliente_02337487504(html_content):
    """
    Extrai informações do cliente Abdias Gomes de Andrade, com dados
    profissionais e financeiros.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    cliente = {}
    enderecos = []
    dados_profissionais = {}
    dados_financeiros = {}

    cliente['nome_completo'] = soup.find('span', id='DadosTitularConta_lblNmTitular').text.strip()
    cliente['cpf'] = soup.find('span', id='DadosTitularConta_lblNrCpf').text.strip()
    cliente['data_cadastro'] = soup.find('span', id='DadosTitularConta_lblDataCadastro').text.strip()
    cliente['nome_mae'] = soup.find('span', id='DadosTitularConta_lblNmMae').text.strip()
    cliente['data_nascimento'] = soup.find('span', id='DadosTitularConta_lblDtNascimento').text.strip()

    endereco_completo = soup.find('div', id='DadosTitularConta_tipTitular_Tip').find('font').text.strip().split('\n')
    logradouro_numero_bairro = endereco_completo[0].split(',')
    cidade_uf_cep = endereco_completo[1].strip().split('-')
    
    enderecos.append({
        'logradouro': logradouro_numero_bairro[0] + "," + logradouro_numero_bairro[1],
        'bairro': logradouro_numero_bairro[2].strip(),
        'cidade': cidade_uf_cep[0].strip(),
        'estado': cidade_uf_cep[1].strip().split('  ')[1],
        'cep': cidade_uf_cep[1].strip().split('  ')[2]
    })

    dados_profissionais['ocupacao'] = soup.find('select', id='DadosProfissionais_ddlOcupacao').find('option', selected=True).text.strip()
    dados_profissionais['cargo'] = soup.find('input', id='DadosProfissionais_txtProfissao')['value'].strip()
    
    dados_financeiros['renda_mensal'] = soup.find('input', id='DadosProfissionais_txSalario')['value']
    dados_financeiros['limite_credito'] = soup.find('span', id='lblLimiteAtual').text.strip().replace('.', '').replace(',', '.')

    return {
        "cliente": cliente,
        "enderecos": enderecos,
        "dados_profissionais": dados_profissionais,
        "dados_financeiros": dados_financeiros
    }

# Dicionário para armazenar os dados de todos os clientes
todos_os_clientes = []

# Processando cada arquivo HTML
arquivos_html = {
    'paginaDadosCliente07339054553.html': extrair_dados_cliente_07339054553,
    'paginaDadosCliente03375498500.html': extrair_dados_cliente_03375498500,
    'paginaDadosCliente02337487504.html': extrair_dados_cliente_02337487504
}

for nome_arquivo, funcao_extracao in arquivos_html.items():
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        html_content = f.read()
    dados_cliente = funcao_extracao(html_content)
    todos_os_clientes.append(dados_cliente)

# Salvando a lista de clientes em um único arquivo JSON
with open('dados_consolidados_clientes.json', 'w', encoding='utf-8') as f:
    json.dump(todos_os_clientes, f, indent=4, ensure_ascii=False)

print("Dados extraídos e salvos em 'dados_consolidados_clientes.json'")
```

### Como Utilizar

1.  **Salve o Código:** Salve o código acima como um arquivo Python (ex: `extrator_dados.py`).

2.  **Organize os Arquivos:** Coloque os três arquivos HTML (`paginaDadosCliente07339054553.html`, `paginaDadosCliente03375498500.html`, `paginaDadosCliente02337487504.html`) no mesmo diretório que o script Python.

3.  **Execute o Script:** Abra um terminal no diretório do projeto e execute o seguinte comando:

    ```bash
    python extrator_dados.py
    ```

4.  **Verifique a Saída:** Após a execução, um novo arquivo chamado `dados_consolidados_clientes.json` será criado no mesmo diretório, contendo todos os dados extraídos e estruturados.

## 7\. Próximos Passos e Recomendações

Com os dados extraídos e estruturados em formato JSON, os próximos passos para a implementação completa do sistema incluem:

1.  **Desenvolver um Módulo de Carga (ETL):**

      * Criar um script Python que leia o arquivo `dados_consolidados_clientes.json`.
      * Estabelecer uma conexão com o banco de dados PostgreSQL.
      * Para cada cliente no JSON, executar as seguintes operações:
          * Verificar se o cliente já existe na tabela `CLIENTES` (pelo CPF).
          * Se não existir, inserir os dados na tabela `CLIENTES` e obter o `cliente_id` gerado.
          * Utilizar o `cliente_id` para inserir os registros correspondentes nas tabelas `ENDERECOS`, `TELEFONES`, `EMAILS`, etc.
          * Se o cliente já existir, aplicar uma lógica de atualização (UPDATE) para os dados que podem ter sido alterados.

2.  **Implementar Validações e Tratamento de Erros:**

      * Adicionar validações aos dados (ex: formato de CPF, data de nascimento) antes da inserção no banco.
      * Implementar um sistema de logs para registrar o sucesso ou falha de cada operação de inserção.

3.  **Automatizar o Processo:**

      * Criar um pipeline que monitore um diretório de entrada para novos arquivos HTML e execute automaticamente o processo de extração e carga.

## 8\. Conclusão

Este projeto demonstra uma solução eficaz para a extração de dados de fontes HTML e sua estruturação para a integração com um banco de dados. A abordagem modular e o uso de bibliotecas consagradas como `BeautifulSoup` e `pandas` garantem a flexibilidade e a robustez da solução, que pode ser facilmente expandida para processar outros layouts de arquivos e integrar-se a diferentes sistemas de banco de dados.