
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '');

ALTER TABLE dim_products
ADD COLUMN weight_class TEXT;

UPDATE dim_products
SET weight_class =
    CASE
        WHEN CAST(weight AS FLOAT) < 2 THEN 'Light'
        WHEN CAST(weight AS FLOAT) BETWEEN 2 AND 40 THEN 'Mid_size'
        WHEN CAST(weight AS FLOAT) BETWEEN 40 AND 140 THEN 'Heavy'
        WHEN CAST(weight AS FLOAT) >= 140 THEN 'Truck_required'
    END;

