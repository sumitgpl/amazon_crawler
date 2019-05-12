# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ProductDetails(Item):
   item_site=Field()
   item_cat=Field()
   item_name=Field()
   item_price=Field()
   item_img=Field()
   item_sku=Field()
   item_supplier=Field()
   item_supplier_rate=Field()
   item_supplier_bprice=Field()
   item_supplier_offer=Field()
   item_dtl=Field()
   item_rating=Field()
   item_review=Field()