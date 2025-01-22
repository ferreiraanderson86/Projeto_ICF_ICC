# Projeto ICC e ICF

Este projeto realiza a automação do download, processamento e carga de dados do ICC e ICF para o BigQuery, além da criação de tabelas `trusted` e `refined` para análise.

## Estrutura do Projeto

python-docker-project/
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
├── src/
│   ├── Script_ICC_ICF.py          # Automação Python
│   ├── script_Trusted.sql         # Criação das tabelas trusted
│   └── Script_icf_icc_refined.sql # Criação da tabela refinada
├── tests/                         # Scripts de teste (opcional)

## Requisitos

- Python 3.8+
- Docker e Docker Compose instalados.
- Conta no Google Cloud Platform (GCP) com permissões para usar o BigQuery.
- Um arquivo de credenciais do GCP (`SA-andersonlf21.json`).

## Configuração do Ambiente com Docker

1. Certifique-se de ter o Docker e o Docker Compose instalados.
2. No diretório do projeto, copie suas credenciais do GCP:
   ```bash
   cp C:/Users/Desktop/Downloads/SA-andersonlf21.json src/credentials.json```
3. Construa a imagem Docker:

docker-compose build

4. Execute o script Python com:

docker-compose up

## Scripts SQL

- script_Trusted.sql: Cria tabelas trusted com dados organizados e sem duplicatas.
- Script_icf_icc_refined.sql: Cria a tabela refined com métricas calculadas e join entre as tabelas trusted.

## Execução do Projeto

- Configure o ambiente conforme instruções acima.
- Execute o script Python para baixar e processar os dados.
- Rode os scripts SQL no BigQuery para criar as tabelas trusted e refined.

## Decisões Técnicas

- Os dados são processados no Python e enviados ao BigQuery.
- O Docker é usado para garantir a reprodutibilidade do ambiente.
- O projeto é versionado no GitHub para facilitar a colaboração.

## Estrutura de Dependências

As dependências do projeto são gerenciadas pelo Dockerfile e incluem:

- Python 3.8
- Bibliotecas necessárias (listadas em requirements.txt)

## Contato

Para dúvidas ou contribuições, entre em contato pelo repositório GitHub.

---

### **2. `Dockerfile`**

```dockerfile
# Usar a imagem oficial do Python
FROM python:3.8-slim

# Diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos para o container
COPY src/ /app/

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão para rodar o script Python
CMD ["python", "Script_ICC_ICF.py"]

