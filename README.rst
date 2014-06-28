pystock-crawler
===============

.. image:: https://badge.fury.io/py/pystock-crawler.png
    :target: http://badge.fury.io/py/pystock-crawler

.. image:: https://travis-ci.org/eliangcs/pystock-crawler.png?branch=master
    :target: https://travis-ci.org/eliangcs/pystock-crawler

.. image:: https://coveralls.io/repos/eliangcs/pystock-crawler/badge.png?branch=master
    :target: https://coveralls.io/r/eliangcs/pystock-crawler

``pystock-crawler`` is a utility for crawling historical data of US stocks,
including:

* Ticker symbols listed in NYSE and NASDAQ from `NASDAQ`_
* Daily prices from `Yahoo Finance`_
* Fundamentals from 10-Q and 10-K filings on `SEC EDGAR`_


Example Output
--------------

NYSE ticker symbols::

    DDD   3D Systems Corporation
    MMM   3M Company
    WBAI  500.com Limited
    ...

Apple's daily prices::

    symbol,date,open,high,low,close,volume,adj_close
    AAPL,2014-04-28,572.80,595.75,572.55,594.09,23890900,594.09
    AAPL,2014-04-25,564.53,571.99,563.96,571.94,13922800,571.94
    AAPL,2014-04-24,568.21,570.00,560.73,567.77,27092600,567.77
    ...

Google's fundamentals::

    symbol,end_date,amend,period_focus,doc_type,revenues,op_income,net_income,eps_basic,eps_diluted,dividend,assets,cur_assets,cur_liab,cash,equity,cash_flow_op,cash_flow_inv,cash_flow_fin
    GOOG,2009-06-30,False,Q2,10-Q,5522897000.0,1873894000.0,1484545000.0,4.7,4.66,0.0,35158760000.0,23834853000.0,2000962000.0,11911351000.0,31594856000.0,3858684000.0,-635974000.0,46354000.0
    GOOG,2009-09-30,False,Q3,10-Q,5944851000.0,2073718000.0,1638975000.0,5.18,5.13,0.0,37702845000.0,26353544000.0,2321774000.0,12087115000.0,33721753000.0,6584667000.0,-3245963000.0,74851000.0
    GOOG,2009-12-31,False,FY,10-K,23650563000.0,8312186000.0,6520448000.0,20.62,20.41,0.0,40496778000.0,29166958000.0,2747467000.0,10197588000.0,36004224000.0,9316198000.0,-8019205000.0,233412000.0
    ...


Installation
------------

Prerequisites:

* Python 2.7

``pystock-crawler`` is based on Scrapy_, so you will also need to install
prerequisites such as lxml_ and libffi_ for Scrapy and its dependencies. See
`Scrapy's installation guide`_ for more details.

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

**Example 5.** All ticker symbols in NYSE and NASDAQ::

    pystock-crawler symbols NYSE,NASDAQ -o out.txt


Usage
-----

Type ``pystock-crawler -h`` to see command help::

    Usage:
      pystock-crawler symbols <exchanges> (-o OUTPUT) [-l LOGFILE] [-w WORKING_DIR] [--sort]
      pystock-crawler prices <symbols> (-o OUTPUT) [-s YYYYMMDD] [-e YYYYMMDD] [-l LOGFILE] [-w WORKING_DIR] [--sort]
      pystock-crawler reports <symbols> (-o OUTPUT) [-s YYYYMMDD] [-e YYYYMMDD]  [-l LOGFILE] [-w WORKING_DIR] [--sort]
      pystock-crawler (-h | --help)
      pystock-crawler (-v | --version)

    Options:
      -h --help       Show this screen
      -o OUTPUT       Output file
      -s YYYYMMDD     Start date [default: ]
      -e YYYYMMDD     End date [default: ]
      -l LOGFILE      Log output [default: ]
      -w WORKING_DIR  Working directory [default: .]
      --sort          Sort the result

There are three commands available:

* ``pystock-crawler symbols`` grabs ticker symbol lists
* ``pystock-crawler prices`` grabs daily prices
* ``pystock-crawler reports`` grabs fundamentals

``<exchanges>`` is a comma-separated string that specifies the stock exchanges
you want to include. Only NYSE and NASDAQ are supported.

The output file of ``pystock-crawler symbols`` can be used for ``<symbols>``
argument in ``pystock-crawler prices`` and ``pystock-crawler reports``
commands.

``<symbols>`` can be an inline string separated with commas or a text file
that lists symbols line by line. For example, the inline string can be
something like ``AAPL,GOOG,FB``. And the text file may look like this::

    # This line is comment
    AAPL    Put anything you want here
    GOOG    Since the text here is ignored
    FB

Use ``-o`` to specify the output file. For ``pystock-crawler symbols``
command, the output format is a simple text file. For
``pystock-crawler prices`` and ``pystock-crawler reports`` the output format
is CSV.

``-l`` is where the crawling logs go to. If not specified, the logs go to
stdout.

By default, the crawler uses the current directory as the working directory.
If you don't want to use the current directoy, you can specify it with ``-w``
option. The crawler keeps HTTP cache in a directory named ``.scrapy`` under
the working directory. The cache can save your time by avoid downloading the
same web pages. However, the cache can be quite huge. If you don't need it,
just delete the ``.scrapy`` directory after you've done crawling.

The rows in the output file are in an arbitrary order by default. Use
``--sort`` option to sort them by symbols and dates. But if you have a large
output file, don't use --sort because it will be slow and eat a lot of memory.


Developer Guide
---------------

Installing Dependencies
~~~~~~~~~~~~~~~~~~~~~~~
::

    pip install -r requirements.txt


Running Test
~~~~~~~~~~~~

Install test requirements::

    pip install -r requirements-test.txt

Then run the test::

    py.test

This will download the test data (a lot of XML files) from from `SEC EDGAR`_
on the fly, so it will take some time and disk space. The test data is saved
to ``pystock_crawler/tests/sample_data`` directory. It can be reused on the
next time you run the test. If you don't need them, just delete the
``sample_data`` directory.


.. _libffi: https://sourceware.org/libffi/
.. _lxml: http://lxml.de/
.. _NASDAQ: http://www.nasdaq.com/
.. _Scrapy: http://scrapy.org/
.. _Scrapy's installation guide: http://doc.scrapy.org/en/latest/intro/install.html
.. _SEC EDGAR: http://www.sec.gov/edgar/searchedgar/companysearch.html
.. _virtualenv: http://www.virtualenv.org/
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/
.. _Yahoo Finance: http://finance.yahoo.com/
