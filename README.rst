pystock-crawler
===============

.. image:: https://badge.fury.io/py/pystock-crawler.png
    :target: http://badge.fury.io/py/pystock-crawler

.. image:: https://travis-ci.org/eliangcs/pystock-crawler.png?branch=master
    :target: https://travis-ci.org/eliangcs/pystock-crawler

.. image:: https://coveralls.io/repos/eliangcs/pystock-crawler/badge.png?branch=master
    :target: https://coveralls.io/r/eliangcs/pystock-crawler

``pystock-crawler`` is a utility for scraping stock historical data including:

* Daily prices from `Yahoo Finance`_
* Fundamentals from 10-Q and 10-K filings on `SEC EDGAR`_

Example output::

    symbol,date,open,high,low,close,volume,adj_close
    AAPL,2014-03-14,528.79,530.89,523.00,524.69,8453600,524.69
    AAPL,2014-03-13,537.44,539.66,529.16,530.65,9191200,530.65
    AAPL,2014-03-12,534.51,537.35,532.00,536.61,7118800,536.61
    AAPL,2014-03-11,535.45,538.74,532.59,536.09,9972300,536.09

    symbol,end_date,amend,period_focus,doc_type,revenues,net_income,eps_basic,eps_diluted,dividend,assets,cash,equity
    GOOG,2013-03-31,False,Q1,10-Q,13969000000.0,3346000000.0,10.13,9.94,0.0,96692000000.0,15375000000.0,75473000000.0
    GOOG,2013-06-30,False,Q2,10-Q,14105000000.0,3228000000.0,9.71,9.54,0.0,101182000000.0,16164000000.0,78852000000.0
    GOOG,2013-09-30,False,Q3,10-Q,14893000000.0,2970000000.0,8.9,8.75,0.0,105068000000.0,15242000000.0,82989000000.0
    GOOG,2013-12-31,False,FY,10-K,59825000000.0,12920000000.0,38.82,38.13,0.0,110920000000.0,18898000000.0,87309000000.0


Installation
------------

Prerequisites:

* Python 2.7

``pystock-crawler`` is based on Scrapy_, so you will also need to install
prerequisites such as lxml_ and libffi_ for Scrapy and its dependencies.

Install with `virtualenv`_ (recommended)::

    pip install pystock-crawler

Or do system-wide installation::

    sudo pip install pystock-crawler


Quickstart
----------

**Example 1.** Google's and Yahoo's daily prices ordered by date::

    pystock-crawler prices GOOG,YHOO -o out.csv --sort

**Example 2.** Daily prices of all companies listed in ``./symbols.txt``::

    pystock-crawler prices ./symbols.txt -o out.csv

**Example 3.** Facebook's fundamentals during 2013::

    pystock-crawler reports FB -o out.csv -s 20130101 -e 20131231

**Example 4.** Fundamentals all companies in ``./nyse.txt`` and direct the
logs to ``./crawling.log``::

    pystock-crawler reports ./nyse.txt -o out.csv -l ./crawling.log


Usage
-----

Type ``pystock-crawler -h`` to see command help::

    Usage:
      pystock-crawler prices <symbols> (-o OUTPUT) [-s YYYYMMDD] [-e YYYYMMDD] [-l LOGFILE] [--sort]
      pystock-crawler reports <symbols> (-o OUTPUT) [-s YYYYMMDD] [-e YYYYMMDD]  [-l LOGFILE] [--sort]
      pystock-crawler (-h | --help)
      pystock-crawler (-v | --version)

    Options:
      -h --help     Show this screen
      -o OUTPUT     Output file
      -s YYYYMMDD   Start date [default: ]
      -e YYYYMMDD   End date [default: ]
      -l LOGFILE    Log output [default: ]
      --sort        Sort the result

Use ``prices`` to crawl price data and ``reports`` to crawl fundamentals.

``<symbols>`` can be an inline string separated with commas or a text file
that lists symbols line by line. For example, the inline string can be
something like ``AAPL,GOOG,FB``. And the text file may look like this::

    # Comment to be ignored
    AAPL    Put anything you want here
    GOOG    Since the text here is ignored
    FB

Use ``-o`` to specify the output file. CSV is the only supported output format
for now.

``-l`` is where the crawling logs go to. If not specified, the logs go to
stdout.

The rows in the output CSV file are in an arbitrary order by default. Use
``--sort`` to sort them by symbols and dates. But if you have a large output
file, don't use ``--sort`` because it will be slow and eat a lot of memory.


Developer Guide
---------------

Installing Dependencies
~~~~~~~~~~~~~~~~~~~~~~~
::

    pip install -r requirements.txt


Running Test
~~~~~~~~~~~~

Install ``pytest``, ``pytest-cov``, and ``requests`` if you don't have them::

    pip install pytest pytest-cov requests

Then run the test::

    py.test

This downloads the test data from from `SEC EDGAR`_ on the fly, so it will
take some time and disk space. If you want to delete test data, just delete
``pystock_crawler/tests/sample_data`` directory.


.. _libffi: https://sourceware.org/libffi/
.. _lxml: http://lxml.de/
.. _Scrapy: http://scrapy.org/
.. _SEC EDGAR: http://www.sec.gov/edgar/searchedgar/companysearch.html
.. _virtualenv: http://www.virtualenv.org/
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/
.. _Yahoo Finance: http://finance.yahoo.com/
