use products;
CREATE TABLE brands (
    brand_id INT PRIMARY KEY AUTO_INCREMENT,
    brand_name VARCHAR(100) NOT NULL,
    UNIQUE KEY unique_brand_name (brand_name)
);
CREATE TABLE products (
    internal_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    gtin VARCHAR(14) NOT NULL,
    brand_id INT ,
    brand_name VARCHAR(100),
    image_src VARCHAR(2048),
    UNIQUE KEY unique_gtin (gtin)
);
CREATE TABLE images (
    image_id INT PRIMARY KEY AUTO_INCREMENT,
    url VARCHAR(2048) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Association table for products and images
CREATE TABLE product_images (
    product_id INT,
    image_id INT,
    display_order INT DEFAULT 0,
    PRIMARY KEY (product_id, image_id),
    FOREIGN KEY (product_id) REFERENCES products(internal_id),
    FOREIGN KEY (image_id) REFERENCES images(image_id)
);


-- SELECT p.name, i.url 
-- FROM products p 
-- JOIN product_images pi ON p.internal_id = pi.product_id 
-- JOIN images i ON pi.image_id = i.image_id 
-- ORDER BY pi.display_order;
