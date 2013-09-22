UNDER DEVELOPMENT
=================

``stockcralwer`` is a utility for scraping stock historical data including
daily prices and fundamental figures such as EPS.


Usage
-----

Crawl data from `SEC EDGAR`_ database::

    scrapy crawl edgar -a symbols=./symbols.txt -o output.json -t json

where ``symbols.txt`` stores a list of trading symbols you want crawl.

.. _SEC EDGAR: http://www.sec.gov/edgar/searchedgar/companysearch.html


Running Tests
-------------

Install ``nose`` and ``coverage`` if you don't have them::

    pip install nose
    pip install coverage

Run the test suites::

    nosetests -c scrapy.cfg
