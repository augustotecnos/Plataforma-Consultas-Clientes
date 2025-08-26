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