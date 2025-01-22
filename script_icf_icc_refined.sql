-- Criar tabela refinada icf_icc_refined
CREATE OR REPLACE TABLE `ps-eng-dados-ds3x.andersonlf21.icf_icc_refined` AS
WITH 
-- Calcular variação do ICC
icc_variation AS (
    SELECT
        -- Caso o campo mes já seja do tipo DATETIME, use FORMAT_DATETIME
        FORMAT_DATETIME('%Y-%m', mes) AS ano_mes,
        icc AS icc_indice,
        ROUND(((icc - LAG(icc) OVER (ORDER BY mes)) / LAG(icc) OVER (ORDER BY mes)) * 100, 2) AS icc_variacao,
        load_timestamp
    FROM
        `ps-eng-dados-ds3x.andersonlf21.icc_trusted`
),

-- Calcular variação do ICF
icf_variation AS (
    SELECT
        -- Caso o campo mes já seja do tipo DATETIME, use FORMAT_DATETIME
        FORMAT_DATETIME('%Y-%m', mes) AS ano_mes,
        icf AS icf_indice,
        ROUND(((icf - LAG(icf) OVER (ORDER BY mes)) / LAG(icf) OVER (ORDER BY mes)) * 100, 2) AS icf_variacao,
        load_timestamp
    FROM
        `ps-eng-dados-ds3x.andersonlf21.icf_trusted`
)

-- Realizar o JOIN entre as tabelas
SELECT
    icc.ano_mes,
    icc.icc_indice,
    icc.icc_variacao,
    icf.icf_indice,
    icf.icf_variacao,
    CURRENT_TIMESTAMP() AS load_timestamp
FROM
    icc_variation icc
INNER JOIN
    icf_variation icf
ON
    icc.ano_mes = icf.ano_mes;