CREATE OR REPLACE TABLE `{project_id}.case.gold_sales_by_line_brand`
AS
SELECT 
    marca, 
    linha, 
    SUM(qtd_venda) AS qtd_venda
FROM `{project_id}.case.table_sales` 
GROUP BY 1, 2