UNDER DEVELOPMENT
=================

.. image:: https://travis-ci.org/eliangcs/stockcrawler.png?branch=master
    :target: https://travis-ci.org/eliangcs/stockcrawler

.. image:: https://coveralls.io/repos/eliangcs/stockcrawler/badge.png?branch=master
    :target: https://coveralls.io/r/eliangcs/stockcrawler

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

Install ``pytest`` and ``pytest-cov`` if you don't have them::

    pip install pytest pytest-cov

Run the test suites::

    py.test
