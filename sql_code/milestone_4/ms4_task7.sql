SELECT
	dim_store_details.country_code,
	SUM (dim_store_details.staff_numbers)
FROM dim_store_details
GROUP BY dim_store_details.country_code;
