StockCrawler
============

.. image:: https://travis-ci.org/eliangcs/stockcrawler.png?branch=master
    :target: https://travis-ci.org/eliangcs/stockcrawler

.. image:: https://coveralls.io/repos/eliangcs/stockcrawler/badge.png?branch=master
    :target: https://coveralls.io/r/eliangcs/stockcrawler

``StockCrawler`` is a utility for scraping stock historical data including
daily prices and fundamental figures such as revenues and EPS.


Development Status
------------------

``StockCrawler`` is still **UNDER DEVELOPMENT**, so expect bugs and design
changes. The plan is to be able to crawl both price data and financial
reports. I'm working on financial reports (10-Q and 10-K forms) and will
proceed to work on pirce data after that.


Installation (For Developers)
-----------------------------

A good Python developer always uses `virtualenv`_, so you should, too. I also
recommend you to use `virtualenvwrapper`_. This is how you install them::

    pip install virtualenv virtualenvwrapper

Then you can create an isolated Python environment with::

    mkvirtualenv stockcrawler

Clone this repository::

    git clone git@github.com:eliangcs/stockcrawler.git

Or you can just download the `ZIP file
<https://github.com/eliangcs/stockcrawler/archive/master.zip>`_ and extract
it.

``StockCrawler`` is based on an awesome web crawling framework `Scrapy`_,
which is listed in ``requirements.txt``. Install it and other dependencies
like this::

    pip install -r requirements.txt

Notice on Windows, it isn't that easy to install `Scrapy`_. Please refer to
`Scrapy`_ documentation for detail.


Usage
-----

Crawl data from `SEC EDGAR`_ database::

    scrapy crawl edgar -a symbols=SYMBOLS
                       -a startdate=YYYYMMDD
                       -a enddate=YYYYMMDD
                       -o OUTPUT_FILE
                       -t OUTPUT_FORMAT

* ``-a symbols``: Trading symbols you want to crawl. Can be a text file or a
  comma-separated string.
* ``-a startdate`` and ``-a enddate``: Optional. If specified, the crawler
  only collects the documents that were filed within
  this period.
* ``-o``: Output file path.
* ``-t``: Output file format, e.g., ``csv`` and ``json``.

Example 1::

    scrapy crawl edgar -a symbols=./symbols/nasdaq100.txt -a startdate=20130101 -a enddate=20130930 -o output.csv -t csv

Example 2::

    scrapy crawl edgar -a symbols=GOOG,AAPL,FB -o tech.csv -t csv


Running Tests
-------------

Install ``pytest``, ``pytest-cov``, and ``requests`` if you don't have them::

    pip install pytest pytest-cov requests

Then running the tests is a simple command::

    py.test

This downloads the test data from from `SEC EDGAR`_ on the fly, so it will
take some time and disk space.


.. _virtualenv: http://www.virtualenv.org/
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/
.. _Scrapy: http://scrapy.org/
.. _SEC EDGAR: http://www.sec.gov/edgar/searchedgar/companysearch.html


.. image:: https://d2weczhvl823v0.cloudfront.net/eliangcs/stockcrawler/trend.png
    :target: https://bitdeli.com/free
    :alt: Bitdeli Badge
