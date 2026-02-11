CREATE OR REPLACE TABLE `case-486819.case.gold_sales_by_brand`
AS 
SELECT 
    marca, 
    EXTRACT(YEAR FROM data_venda) AS ano, 
    EXTRACT(MONTH FROM data_venda) AS mes, 
    SUM(qtd_venda) AS qtd_venda
FROM `case-486819.case.table_sales` 
GROUP BY ALL
ORDER BY ano DESC, mes DESC