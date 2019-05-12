from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from product.items import ProductDetails
from scrapy import log
import urlparse 
import json
import string
from scrapy.http.request import Request
 
class DmozSpider(CrawlSpider):
   name = "amazonitem"
   base_url = "http://www.amazon.in"
   itemsarray = []
   burl = ""
   nextpagenum = int(1)
   start_urls=[]	
   itemcat = ""
   itemsite = "amazon"
   prm = ''
   itemtotsupplier = []


   def __init__(self, category='', url=None, prm='',pgnum=''):
	  self.burl = url
	  self.nextpagenum = int(pgnum)
	  url = url + '&page=' + str(self.nextpagenum) + prm
	  self.start_urls.append(url)
	  self.itemcat = category
	  self.prm = prm

   def parse(self, response):
	   return self.parse_nextpage(response)


   def parse_nextpage(self, response):
	   fnd = False
	   sel = Selector(response)
	   if not sel.xpath('//div[@class="image imageContainer"]/a/@href').extract():
	   	productlist = sel.xpath('//div[@class="s-item-container"]/div/div/div/a/@href').extract()
	   else:
	   	productlist = sel.xpath('//div[@class="image imageContainer"]/a/@href').extract()

	   for prod in productlist:
		fnd = True
		yield Request(prod, callback=self.parse_item)

	   try:
		if fnd:
			if sel.xpath('//a[@id="pagnNextLink"]/@href').extract():
				nextpage = sel.xpath('//a[@id="pagnNextLink"]/@href').extract()[0]
				self.log('NEXT url : ' + nextpage, log.ERROR)
				nextpage = self.base_url + nextpage
				yield Request(nextpage, callback=self.parse_nextpage)
	   except:
		self.log('Whole category parsed: ', log.DEBUG)
	   return

   def parse_item(self, response):
	   sel = Selector(response)
	   itemallsupplier = []
	   pass_flg = 0
	   supplierlist = []
	   itemcat = self.itemcat
	   if not sel.xpath('//*[@id="productTitle"]//text()').extract():
	   	itemname = ''
	   else:
	   	itemname = sel.xpath('//*[@id="productTitle"]//text()').extract()[0]

	   item_dtl = "" 

	   if not sel.xpath('//*[@id="priceblock_saleprice"]/text()').extract():
		if not sel.xpath('//*[@id="olp_feature_div"]/div/span/span/text()').extract():
			itemprice = 0
		else:
			itemprice = sel.xpath('//*[@id="olp_feature_div"]/div/span/span/text()').extract()[0]
	   else:
	   	itemprice = sel.xpath('//*[@id="priceblock_saleprice"]/text()').extract()[0]

	   if not sel.xpath('//*[@id="landingImage"]/@data-a-dynamic-image').extract():
		itemimg = "img"
	   else:
	    	itemimg = sel.xpath('//*[@id="landingImage"]/@data-a-dynamic-image').extract()[0]

	   if not sel.xpath('//*[@id="ASIN"]/@value').extract():
   	   	itemsku = 'Out of Stock!'
	   else:
   	   	itemsku = sel.xpath('//*[@id="ASIN"]/@value').extract()[0]

	   if not sel.xpath('//a[@class="seller-name"]/text()').extract():
	   	if not sel.xpath('//*[@id="merchant-info"]/a/text()').extract():
			itemsupplier = ""
			itemsupplierrate = 0	
		else:
			itemsupplier = sel.xpath('//*[@id="merchant-info"]/a/text()').extract()[0]
			itemsupplierrate = sel.xpath('//*[@id="merchant-info"]/text()').extract()[1]
	   else:
	   	itemsupplier = sel.xpath('//a[@class="seller-name"]/text()').extract()[0]
		itemsupplierrate = sel.xpath('//a[@class="seller-name"]/text()').extract()[1]

	   if not sel.xpath('//*[@id="averageCustomerReviews"]/span/span[1]/a/i/@class').extract():
	   	itemrate = 0
	   else:
		itemrate = sel.xpath('//*[@id="averageCustomerReviews"]/span/span[1]/a/i/@class').extract()[0].replace('a-icon a-icon-star a-star-','')

	   if not sel.xpath('//*[@id="acrCustomerReviewText"]//text()').extract():
	   	item_review = 0
	   else:
		item_review = sel.xpath('//*[@id="acrCustomerReviewText"]//text()').extract()[0].replace('customer reviews','')


	   if not sel.xpath('//*[@id="olp_feature_div"]/div/span/a//@href').extract():
	   	supplierlist = []
		itslist = ProductDetails()
		itslist['item_cat'] = itemcat
		itslist['item_site'] = self.itemsite
	   	itslist['item_name'] = itemname
	   	itslist['item_price'] = itemprice
	   	itslist['item_img'] = itemimg
	   	itslist['item_sku'] =  itemsku
	   	itslist['item_supplier'] = itemsupplier.replace('\r\n\t\t\t','')
	   	itslist['item_supplier_rate'] = itemsupplierrate
	   	itslist['item_supplier_bprice'] = itemprice	
	   	itslist['item_supplier_offer'] = ""
	   	itslist['item_dtl'] = item_dtl
		itslist['item_rating'] = itemrate
		itslist['item_review'] = item_review
   		itemallsupplier.append(itslist)
		return itemallsupplier
	   else:
		nextpage = sel.xpath('//*[@id="olp_feature_div"]/div/span/a//@href').extract()[0]
		nextpage = self.base_url + nextpage
		item_data = []
		#return Request(nextpage, callback=self.parse_supplier)
		request = Request(nextpage, callback=self.parse_supplier)
		request.meta['item_data'] = item_data
		return request

   def parse_supplier(self, response):
	   sel = Selector(response)
	   item_data = response.meta.get('item_data',{})
	   pass_flg = 0
	   supplierlist = []
	   itemcat = self.itemcat

	   if not sel.xpath('//*[@id="olpProductDetails"]/h1/text()').extract():
		itemname = ''
	   else:
	   	itemname = sel.xpath('//*[@id="olpProductDetails"]/h1/text()').extract()[1]

	   if not sel.xpath('//div[@class="a-column a-span2 olpBuyColumn a-span-last"]/div/form/input[5]//@name').extract():
   	   	itemsku = 'Out of Stock!'
	   else:
   	   	itemsku = sel.xpath('//div[@class="a-column a-span2 olpBuyColumn a-span-last"]/div/form/input[5]//@name').extract()[0]
		itemsku = itemsku.replace('metric-asin.','')
   
	   if not sel.xpath('//*[@id="olpProductImage"]/a/img//@src').extract():
   	   	itemimg = 'img'
	   else:
   	   	itemimg = sel.xpath('//*[@id="olpProductImage"]/a/img//@src').extract()[0]

	   if not sel.xpath('//*[@id="olpProductDetails"]/div[2]/span/span[3]/a//text()').extract():
   	   	item_review = ''
	   else:
   	   	item_review = sel.xpath('//*[@id="olpProductDetails"]/div[2]/span/span[3]/a//text()').extract()[0]

	   if not sel.xpath('//*[@id="olpProductDetails"]/div[2]/span/span[1]/a[2]/i//@class').extract():
   	   	itemrate = '0'
	   else:
   	   	itemrate = sel.xpath('//*[@id="olpProductDetails"]/div[2]/span/span[1]/a[2]/i//@class').extract()[0].replace('a-icon a-icon-star a-star-','')

	   if not sel.xpath('//div[@class="a-row a-spacing-mini olpOffer"]').extract():
		supplierlist = []
		pass_flg = 0
	   else:
  	   	supplierlist = sel.xpath('//div[@class="a-row a-spacing-mini olpOffer"]')
		pass_flg = 1

	
	   if pass_flg == 1:
	   	for onesupplier in supplierlist:
			itslist = ProductDetails()
			itslist['item_cat'] = itemcat
			itslist['item_site'] = self.itemsite	
	   		itslist['item_name'] = itemname
		   	itslist['item_img'] = itemimg
	   		sup_itm_price = onesupplier.xpath('div[@class="a-column a-span2"]/span/span/text()').extract()[0].replace(',','')
	   		itslist['item_price'] = sup_itm_price
	   		itslist['item_sku'] =  itemsku

			if not onesupplier.xpath('div[@class="a-column a-span2 olpSellerColumn"]/p[2]/i//@class').extract():
				itslist['item_supplier_rate'] = 0
			else:
		   		itslist['item_supplier_rate'] = onesupplier.xpath('div[@class="a-column a-span2 olpSellerColumn"]/p[2]/i//@class').extract()[0].replace('a-icon a-icon-star a-star-','').replace('-','.')
	   		itslist['item_supplier_bprice'] = sup_itm_price
   			itslist['item_supplier_offer'] = ""
			#if not onesupplier.xpath('div[@class="a-column a-span2 olpSellerColumn"]/p[1]/span/a//@href').extract():
		   	#	itslist['item_supplier'] = onesupplier.xpath('div[@class="a-column a-span2 olpSellerColumn"]/p[1]/a//@href').extract()[0]
			#else:
			#	itslist['item_supplier'] = onesupplier.xpath('div[@class="a-column a-span2 olpSellerColumn"]/p[1]/span/a//text()').extract()[0]
			if onesupplier.xpath('div[@class="a-column a-span2 olpSellerColumn"]/h3/span/a/text()').extract():
		   		itslist['item_supplier'] = onesupplier.xpath('div[@class="a-column a-span2 olpSellerColumn"]/h3/span/a/text()').extract()[0]
			else:
				if onesupplier.xpath('div[@class="a-column a-span2 olpSellerColumn"]/h3/a/@href').extract():
					itslist['item_supplier'] = onesupplier.xpath('div[@class="a-column a-span2 olpSellerColumn"]/h3/a/@href').extract()[0].replace('http://www.amazon.in/shops/','')
				else:
					itslist['item_supplier'] = onesupplier.xpath('div[@class="a-column a-span2 olpSellerColumn"]/p[1]/span/a//text()').extract()[0]

			itslist['item_rating'] = itemrate
			itslist['item_review'] = item_review
   			#self.itemtotsupplier.append(itslist)
			item_data.append(itslist)
			#yield item_data

	   try:
		nextpage = sel.xpath('//li[@class="a-last"]/a//@href').extract()[0]
		self.log('NEXT url : ' + nextpage, log.ERROR)
		nextpage = self.base_url + nextpage
		request = Request(nextpage, callback=self.parse_supplier)
		request.meta['item_data'] = item_data
		return request
		#return Request(nextpage, callback=self.parse_supplier)
	   except:
		self.log('Whole category supplier parsed: ', log.DEBUG)
	   	#return self.itemtotsupplier
		return item_data