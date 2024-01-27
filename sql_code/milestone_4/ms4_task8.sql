SELECT 
	dim_store_details.country_code,
	dim_store_details.store_type,
	SUM ( orders_table.product_quantity * dim_products.product_price) AS total_sales
	FROM orders_table
	JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
	JOIN dim_products ON orders_table.product_code = dim_products.product_code
WHERE 
	dim_store_details.country_code = 'de'
GROUP BY
	dim_store_details.country_code, dim_store_details.store_type