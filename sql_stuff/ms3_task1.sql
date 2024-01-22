ALTER TABLE orders_table
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
    -- SELECT MAX(LENGTH(card_number::TEXT)) FROM orders_table,
    ALTER COLUMN card_number TYPE VARCHAR(19),
    -- SELECT MAX(LENGTH(store_code::text)) FROM orders_table,
    ALTER COLUMN store_code TYPE VARCHAR(12),
    -- SELECT MAX(LENGTH(product_code::text)) FROM orders_table,
    ALTER COLUMN product_code TYPE VARCHAR(11),
    ALTER COLUMN product_quantity TYPE SMALLINT USING product_quantity::SMALLINT;

