ALTER TABLE dim_date_times
    -- SELECT MAX(LENGTH(month::TEXT)) FROM dim_date_times;
    ALTER COLUMN month TYPE VARCHAR(10),
    -- SELECT MAX(LENGTH(year::TEXT)) FROM dim_date_times;
    ALTER COLUMN year TYPE VARCHAR(10),
    -- SELECT MAX(LENGTH(day::TEXT)) FROM dim_date_times;
    ALTER COLUMN day TYPE VARCHAR(10),
    -- SELECT MAX(LENGTH(time_period::TEXT)) FROM dim_date_times;
    ALTER COLUMN time_period TYPE VARCHAR(10),
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;
    