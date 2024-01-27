ALTER TABLE dim_card_details 
    -- SELECT MAX(LENGTH(card_number::TEXT)) FROM dim_card_details;
    ALTER COLUMN card_number TYPE VARCHAR(19),
    -- SELECT MAX(LENGTH(expiry_date::TEXT)) FROM dim_card_details;
    ALTER COLUMN expiry_date TYPE VARCHAR(25), -- i think it should be TYPE DATE
    ALTER COLUMN date_payment_confirmed TYPE DATE;


-- ALTER TABLE dim_card_details  -- datat n orders table not in card_details
--     -- SELECT MAX(LENGTH(card_number::TEXT)) FROM dim_card_details;
--     ALTER COLUMN card_number TYPE VARCHAR(27),
--     -- SELECT MAX(LENGTH(expiry_date::TEXT)) FROM dim_card_details;
--     ALTER COLUMN expiry_date TYPE VARCHAR(25); -- i think it should be TYPE DATE
--     -- ALTER COLUMN date_payment_confirmed TYPE DATE;


