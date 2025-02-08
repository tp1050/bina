this is a flask project

it is inteded for a product database
it should allow for inventory management of separate warehouses.
it should have a centersl database of products:
    all products have gtin, name, description, country of origin,brand 
    a ware house is essentially just an id which in a table of associations between products and warehouse could be recorded
    or an warehouse object may have an list indide it that holds the  gtins and number of each items witing it

it should have  routes
         that allows for the creation of a new product
        either by scanning the barcode and trying to load the information from the web or the local database or by manually entering the information
        gtin feild allow for scanning from a barcode camera


flask routes:
    /products/view/gtin/<barcode>
    /products/add
    /products/edit/<barcode>
    /brands/view/<brand_name>
    /brands/add
    /brands/edit/<brand_name>
    /warehouses/view/<warehouse_name>
    /warehouses/add
    /warehouses/edit/<warehouse_name>




the db structer:

brand table: 
    brand_id
    brand_name
product table:
    product_id
    gtin
    product_name
    description
    brand_id
warehouse table:
    warehouse_id
    warehouse_name
inventory table:
    inventory_id
    product_id
    warehouse_id
    quantity
    date_added