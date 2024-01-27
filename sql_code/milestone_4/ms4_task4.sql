SELECT 	
	COUNT (orders_table.product_quantity) AS numbers_of_sales,
	SUM(orders_table.product_quantity) AS product_quantity_count,
	CASE 
		WHEN dim_store_details.store_code = 'WEB-1388012W' THEN 'web'
		ELSE 'offfline'
		END AS location
	FROM orders_table
	JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
	JOIN dim_products ON orders_table.product_code = dim_products.product_code
	JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY location;