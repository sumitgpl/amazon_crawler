##########################
Amazon Crawler
##########################

Points :- 

> *  main "exec_amazon.sh" shell script to initiate crawling. This script read target category and Start URL from file "amazon_data.csv"

> *  this script initiating scrapy to start crawling spider "amazonitem" 

> *  Because amazon stopping normal HTTP hists , so added user-agent into middleware. Amazon feel like a read browser opening pages.

> *  Based on internet connection speed and amazon response , added some parameters to tune crawling. These parameters are ...

CONCURRENT_REQUESTS = 64

CONCURRENT_REQUESTS_PER_DOMAIN = 8

CONCURRENT_ITEMS = 200

> *  Added pipeline to store all crawl values directly to Mysql database.
> *  During data crawling from amazon , need to take care of 3 points. 1-> have to open and crawl all product of a pages and move next. 
	2-> on each product page capture product related info like sku,description etc. 3-> also have to capture all supplier details for 
	each product. So to achive this added 3 layer of parsing. In "amazon.py" file , "parse_nextpage" to achive point 1. "parse_item" 
	for point 2 and "parse_supplier" for point 3.
	
