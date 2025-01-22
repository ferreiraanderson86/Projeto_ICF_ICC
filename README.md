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
   cp C:/Users/Desktop/Downloads/SA-andersonlf21.json src/SA-andersonlf21.json
