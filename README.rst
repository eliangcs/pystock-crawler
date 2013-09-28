StockCrawler
============

.. image:: https://travis-ci.org/eliangcs/stockcrawler.png?branch=master
    :target: https://travis-ci.org/eliangcs/stockcrawler

.. image:: https://coveralls.io/repos/eliangcs/stockcrawler/badge.png?branch=master
    :target: https://coveralls.io/r/eliangcs/stockcrawler

``StockCrawler`` is a utility for scraping stock historical data including
daily prices and fundamental figures such as revenues and EPS.


Project Status
--------------

``StockCrawler`` is still **UNDER DEVELOPMENT**, so expect bugs and design
changes. The plan is to be able to crawl both price data and financial
reports. I'm working on financial reports and will proceed to work on pirce
data after that.


Installation (For Developers)
-----------------------------

A good Python developer always uses `virtualenv`_, so you should, too. I also
recommend you to use `virtualenvwrapper`_. This is how you install them::

    pip install virtualenv virtualenvwrapper

``StockCrawler`` is based on an awesome web crawling framework `Scrapy`_,
which is listed in ``requirements.txt``. Install it and other dependencies
like this::

    pip install -r requirements.txt

Notice on Windows, it isn't that easy to install `Scrapy`_. Please refer to
`Scrapy`_ documentation for detail.


Usage
-----

Crawl data from `SEC EDGAR`_ database::

    scrapy crawl edgar -a symbols=./symbols.txt -o output.json -t json

where ``symbols.txt`` stores a list of trading symbols you want to crawl.


Running Tests
-------------

Install ``pytest``, ``pytest-cov``, and ``requests`` if you don't have them::

    pip install pytest pytest-cov requests

Then running the tests is a simple command::

    py.test

This downloads the test data from the internet on the fly, so it will take
some time and disk space.


.. _virtualenv: http://www.virtualenv.org/
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/
.. _Scrapy: http://scrapy.org/
.. _SEC EDGAR: http://www.sec.gov/edgar/searchedgar/companysearch.html
