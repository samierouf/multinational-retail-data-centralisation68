ALTER TABLE dim_products
    RENAME COLUMN removed to still_avaiable;

UPDATE dim_products
    SET still_avaiable = CASE
                        WHEN still_avaiable = 'TRUE' THEN TRUE
                        WHEN still_avaiable = 'FALSE' THEN FALSE
                        END;


ALTER TABLE dim_products
    ALTER COLUMN product_price TYPE FLOAT USING product_price::FLOAT,
    ALTER COLUMN weight TYPE FLOAT USING weight::FLOAT,
    -- SELECT MAX(LENGTH("EAN"::TEXT)) FROM dim_products;
    ALTER COLUMN "EAN" TYPE VARCHAR(17),
    -- SELECT MAX(LENGTH(product_code::TEXT)) FROM dim_products;
    ALTER COLUMN product_code TYPE VARCHAR(11),
    ALTER COLUMN date_added TYPE DATE,
    ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
    ALTER COLUMN still_avaiable DROP DEFAULT, 
    ALTER COLUMN still_avaiable TYPE BOOLEAN USING still_avaiable::BOOLEAN,
    -- SELECT MAX(LENGTH(weight_class::TEXT)) FROM dim_products;
    ALTER COLUMN weight_class TYPE VARCHAR(14);






