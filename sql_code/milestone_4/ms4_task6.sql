SELECT 
	dim_date_times.year,
	dim_date_times.month,
	SUM(orders_table.product_quantity * dim_products.product_price) AS total_sales
	FROm orders_table
	JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
	JOIN dim_products ON orders_table.product_code = dim_products.product_code
	JOIN dim_store_details on orders_table.store_code = dim_store_details.store_code
GROUP BY
	dim_date_times.month,dim_date_times.year
ORDER BY total_sales  DESC
LIMIT 10;