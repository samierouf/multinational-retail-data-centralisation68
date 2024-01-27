ALTER TABLE dim_card_details 
    -- SELECT MAX(LENGTH(card_number::TEXT)) FROM dim_card_details;
    ALTER COLUMN card_number TYPE VARCHAR(19),
    -- SELECT MAX(LENGTH(expiry_date::TEXT)) FROM dim_card_details;
    ALTER COLUMN expiry_date TYPE VARCHAR(25),
    ALTER COLUMN date_payment_confirmed TYPE DATE;




