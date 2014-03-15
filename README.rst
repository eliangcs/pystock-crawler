pystock-crawler
===============

.. image:: https://travis-ci.org/eliangcs/pystock-crawler.png?branch=master
    :target: https://travis-ci.org/eliangcs/pystock-crawler

.. image:: https://coveralls.io/repos/eliangcs/pystock-crawler/badge.png?branch=master
    :target: https://coveralls.io/r/eliangcs/pystock-crawler

``pystock-crawler`` is a utility for scraping stock historical data including:

* Daily prices from `Yahoo Finance`_
* Fundamentals from 10-Q and 10-K filings on `SEC EDGAR`_


Installation
------------

Prerequisites:

* Linux or Mac OS
* Python 2.7

Install it in `virtualenv`_ (recommended)::

    pip install pystock-crawler

Or do system-wide installation::

    sudo pip install pystock-crawler


Quickstart
----------

**Example 1.** Google's and Yahoo's daily prices and sort::

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


.. _Yahoo Finance: http://finance.yahoo.com/
.. _virtualenv: http://www.virtualenv.org/
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/
.. _Scrapy: http://scrapy.org/
.. _SEC EDGAR: http://www.sec.gov/edgar/searchedgar/companysearch.html
