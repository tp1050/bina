
]=[-P09I87f barcodes are unknown still an unknown product with the barcode as gtin and none for rest should be added to the the system
use mysql for the db and json for file use docker and provide compose files 
index page:
    create invoice:
        barcode scanner scanns barcode looks up in our inventory and if it is there it will issue an invoice`   +
    
    update inventory:
        barcode scanner scanns the barcode if it is in our invebtory adds one 
        if it is not there it will look it up using any of the lokk up methods and returns the 
        result allows the user to enter a price and last known seller and then add or reject and go back
        
    just info
        barcode scanner scanns the barcode and presnets the data if from cache and if retirved it would cache it
    view inventory:
        a page to show the number of items of each barcode and small thumbnail allows clicking and editing
        allow export of each product or all products in csv format or Basalamteplate.xlcwelcome page

    
welcome page:
scan barcode
    look up the barcode in the local mysql db and if it is not there look it up online via lookup method lu() and 
    present the user with the results allow them to then choose to
        1- adding a price quote by adding price date and seller name/ or show older qoutes
        2- add the item to the inventory allow user to give the name of the inventory to add to and the price
        3  add the item to an invoice by getting inoice number make new ones for new numbers or show the invoices with this item in them
see inventory list ordered and  paginated (possibly by html5)
see invoice listpaginated allow for edition of the inoivce
see price qoute list
buyers and sellers are people in person table
product table has gtin description name source brand company and its price should come from a price tbale that records the procut id and price and date


choices:
add product  by scanning barcode if the product data was in mysql bring it up allow the user to add quanity source name price

add price qoute
