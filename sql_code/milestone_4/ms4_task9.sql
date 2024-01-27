WITH full_timestamp_table AS( ------Final final
SELECT
	dim_date_times.date_uuid,
	dim_date_times.year,
	CAST(CONCAT(dim_date_times.year, '-', dim_date_times.month, '-', dim_date_times.day, ' ', dim_date_times.timestamp) AS TIMESTAMP) AS full_time_stamp
	FROM 
		dim_date_times
),
lead_full_timestamp_table AS (
	SELECT
		full_timestamp_table.full_time_stamp,
		full_timestamp_table.year,
		full_timestamp_table.date_uuid,
	CAST(LEAD(full_timestamp_table.full_time_stamp) OVER(ORDER BY full_timestamp_table.full_time_stamp) AS TIMESTAMP) AS lead_full_timestamp
	FROM 
		full_timestamp_table
),
difference_between_timestamp_table AS (
	SELECT
		lead_full_timestamp_table.year,
		lead_full_timestamp_table.date_uuid,
		lead_full_timestamp - full_time_stamp AS difference_between_times
	FROM 
		lead_full_timestamp_table
)
SELECT
difference_between_timestamp_table.year,
    CONCAT(
        'hours: ', EXTRACT(HOUR FROM AVG(difference_between_times)),
        ', minutes: ', EXTRACT(MINUTE FROM AVG(difference_between_times)),
        ', seconds: ', EXTRACT(SECOND FROM AVG(difference_between_times)),
        ', milliseconds: ', EXTRACT(MILLISECOND FROM AVG(difference_between_times))
    ) AS actual_time_taken

	FROM
		difference_between_timestamp_table
GROUP BY
	difference_between_timestamp_table.year
ORDER BY
    actual_time_taken DESC;
	