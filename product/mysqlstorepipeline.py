import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request
import MySQLdb.cursors

class MySQLStorePipeline(object):
  def __init__(self):
    self.conn = MySQLdb.connect( host='80.241.222.76', user='root', passwd='@dm1n45er', db='bizdashboard', charset='utf8', use_unicode=True )
    self.cursor = self.conn.cursor()

  def process_item(self, item, spider):
    try:
	 if isinstance(item['item_supplier_rate'], (list, tuple)):
             	itm_supplier_rt = item['item_supplier_rate'][0]
   	 else:
             	itm_supplier_rt = item['item_supplier_rate'];
	 self.cursor.execute("""INSERT INTO amazon_item_scan (item_site,item_supplier_bprice, item_supplier_offer,item_price,item_name,item_sku,item_img,item_supplier_rate,item_supplier,subcategory,item_rating,total_review) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)""",(item['item_site'],item['item_supplier_bprice'],item['item_supplier_offer'],item['item_price'], item['item_name'], item['item_sku'], item['item_img'],itm_supplier_rt, item['item_supplier'],item['item_cat'],item['item_rating'],item['item_review']))
	 self.conn.commit()

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    return item