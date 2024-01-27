Select country_code,
Count (*) 
	From dim_store_details 
	Group BY country_code;

-- gb = 266
-- de = 141
-- us = 34