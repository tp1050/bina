from models import db, Product, Price, Person, Inventory, Invoice

class ProductService:
    @staticmethod
    def lookup_product(barcode):
        product = Product.query.filter_by(gtin=barcode).first()
        if not product:
            # Implement online lookup logic here
            product_data = lookup_online(barcode)
            product = Product(
                gtin=barcode,
                name=product_data['name'],
                description=product_data['description'],
                brand=product_data['brand'],
                company=product_data['company']
            )
            db.session.add(product)
            db.session.commit()
        return product

class PriceService:
    @staticmethod
    def add_quote(product_id, price, seller_id, date):
        quote = Price(
            product_id=product_id,
            price=price,
            seller_id=seller_id,
            date=date
        )
        db.session.add(quote)
        db.session.commit()
        return quote

class InventoryService:
    @staticmethod
    def add_item(inventory_id, product_id, quantity, price):
        item = InventoryItem(
            inventory_id=inventory_id,
            product_id=product_id,
            quantity=quantity,
            price=price
        )
        db.session.add(item)
        db.session.commit()
        return item

class InvoiceService:
    @staticmethod
    def create_invoice(number, buyer_id, date):
        invoice = Invoice(
            number=number,
            buyer_id=buyer_id,
            date=date
        )
        db.session.add(invoice)
        db.session.commit()
        return invoice
