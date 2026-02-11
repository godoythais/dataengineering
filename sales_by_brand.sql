CREATE OR REPLACE TABLE `{project_id}.case.gold_sales_by_brand`
AS 
SELECT 
    marca, 
    EXTRACT(YEAR FROM data_venda) AS ano, 
    EXTRACT(MONTH FROM data_venda) AS mes, 
    SUM(qtd_venda) AS qtd_venda
FROM `{project_id}.case.table_sales` 
GROUP BY ALL
ORDER BY ano DESC, mes DESC