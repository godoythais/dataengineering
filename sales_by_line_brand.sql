CREATE OR REPLACE TABLE `case-486819.case.gold_sales_by_line_brand`
AS
SELECT 
    marca, 
    linha, 
    SUM(qtd_venda) AS qtd_venda
FROM `case-486819.case.table_sales` 
GROUP BY 1, 2