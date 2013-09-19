UNDER DEVELOPMENT
=================

``stockcralwer`` is a utility for scraping stock historical data including
daily prices and fundamental figures such as EPS.


Usage
-----

Crawl data from `SEC EDGAR`_ database::

    scrapy crawl edgar -a symbols=./symbols.txt -o output.csv -t csv

where ``symbols.txt`` stores a list of trading symbols you want crawl. The
crawled data stored in ``output.csv`` is raw and hard to read. To sort them
out, use the following command::

    scrapy aggregate ./output.csv -o output2.csv

.. _SEC EDGAR: http://www.sec.gov/edgar/searchedgar/companysearch.html
