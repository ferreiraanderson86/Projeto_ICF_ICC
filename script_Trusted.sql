-- Criar tabela icc_trusted
CREATE OR REPLACE TABLE `ps-eng-dados-ds3x.andersonlf21.icc_trusted` AS
SELECT
    DISTINCT
    mes,
    icc,
    icc_ate_10_sm,
    icc_mais_de_10_sm,
    icc_homens,
    icc_mulheres,
    icc_ate_35_anos,
    icc_mais_de_35_anos,
    icea,
    icea_ate_10_sm,
    icea_mais_de_10_sm,
    icea_homens,
    icea_mulheres,
    icea_ate_35_anos,
    icea_mais_de_35_anos,
    iec,
    iec_ate_10_sm,
    iec_mais_de_10_sm,
    iec_homens,
    iec_mulheres,
    iec_ate_35_anos,
    iec_mais_de_35_anos,
    load_timestamp
FROM
    `ps-eng-dados-ds3x.andersonlf21.icc_raw`
WHERE
    mes IS NOT NULL
ORDER BY mes;

-- Criar tabela icf_trusted
CREATE OR REPLACE TABLE `ps-eng-dados-ds3x.andersonlf21.icf_trusted` AS
SELECT
    DISTINCT
    mes,
    icf,
    icf_ate_10_sm,
    icf_mais_de_10_sm,
    emprego_atual,
    emprego_atual_ate_10_sm,
    emprego_atual_mais_de_10_sm,
    perspectiva_profissional,
    perspectiva_profissional_ate_10_sm,
    perspectiva_profissional_mais_de_10_sm,
    renda_atual,
    renda_atual_ate_10_sm,
    renda_atual_mais_de_10_sm,
    acesso_credito,
    acesso_credito_ate_10_sm,
    acesso_credito_mais_de_10_sm,
    nivel_consumo_atual,
    nivel_consumo_atual_ate_10_sm,
    nivel_consumo_atual_mais_de_10_sm,
    perspectiva_consumo,
    perspectiva_consumo_ate_10_sm,
    perspectiva_consumo_mais_de_10_sm,
    momento_duraveis,
    momento_duraveis_ate_10_sm,
    momento_duraveis_mais_de_10_sm,
    load_timestamp
FROM
    `ps-eng-dados-ds3x.andersonlf21.icf_raw`
WHERE
    mes IS NOT NULL
ORDER BY mes;
