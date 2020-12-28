# TradeKit

Note: I am currently gathering feedback on what to include in this image, this is not "final". I will add more packages based on feedback and eventually freeze the versions. Let me know your thoughts. [Demo Video](https://www.youtube.com/watch?v=uiPMCJ0MEbM)

The goal of TradeKit is to maintain a collection of open source server components and Python libraries for building your own financial applications, data analysis tools, and trading bots. These tools are packaged in a Docker container so that anyone can easily get up and running locally and develop with these components regardless of their operating system. Once a developer has successfully built their project locally, the Docker container can easily be deployed to a server (such as VPS on DigitalOcean or a cloud provider like AWS) for production use. 

## Server Components

* [Debian Linux 10](https://www.debian.org/) - a stable and dependable linux distribution for servers
* [Python 3.8](https://www.python.org/) - the most popular language for data science, analysis, and machine learning
* [PostgreSQL 12](https://www.postgresql.org/) - the world's most advanced open source database
* [TimeScaleDB 2.0](https://www.timescale.com/) - open source time-series database built on top of PostgreSQL

## Web Frameworks

* [FastAPI](https://fastapi.tiangolo.com/) - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
* [Flask](https://flask.palletsprojects.com/) - a lightweight, easy to learn microframework for Python web apps

## Data Analysis

* [pandas](https://pandas.pydata.org/) - library for data analysis and manipulation of numerical tables and time series
* [NumPy](https://numpy.org/) - library for multi-dimensional arrays and matrices, mathematical functions
* [SciPy](https://www.scipy.org/) - modules for linear algebra, integration, FFT, signal and image processing
* [pandas-datareader](https://pandas-datareader.readthedocs.io/) - remote data access for pandas

# Data Visualization

* [matplotlib](https://matplotlib.org/) - comprehensive library for creating static, animated, and interactive visualizations in Python
* [plotly](https://pypi.org/project/plotly/) - provides online graphing, analytics, and statistics tools for individuals and collaboration, as well as scientific graphing libraries for Python
* [dash](https://plotly.com/dash/) - build & deploy beautiful analytic web apps using Python
* [mplfinance](https://github.com/matplotlib/mplfinance) - matplotlib utilities for the visualization, and visual analysis, of financial data
* [jupyterlab](https://jupyterlab.readthedocs.io/) - web-based interactive development environment for Jupyter notebooks, code, and data
pillow

## Technical Analysis

* [ta](https://technical-analysis-library-in-python.readthedocs.io/) - Technical Analysis Library in Python based on pandas
* [TA-Lib](https://mrjbq7.github.io/ta-lib/) - Python wrapper for TA-Lib
* [bta-lib](https://btalib.backtrader.com/) - backtrader ta-lib
* [pandas-ta](https://github.com/twopirllc/pandas-ta) - Pandas Technical Analysis (Pandas TA) is an easy to use library that leverages the Pandas library with more than 120 Indicators and Utility functions
* [tulipy](https://github.com/cirla/tulipy) - Python bindings for Tulip Indicators

# Database Libraries and Data Storage

* [psycopg2](https://pypi.org/project/psycopg2/) - most popular PostgreSQL database adapter for the Python programming language.
* [sqlalchemy](https://www.sqlalchemy.org/) - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
* [redis](https://redis.io/) - open source, in-memory data structure store, used as a database, cache, and message broker
* [h5py](https://www.h5py.org/) - Pythonic interface to the HDF5 binary data format

# Broker APIs

* [alpaca-trade-api](https://github.com/alpacahq/alpaca-trade-api-python) - python library for the Alpaca Commission Free Trading API. It allows rapid trading algo development easily, with support for both REST and streaming data interfaces.
* [python-binance](https://python-binance.readthedocs.io/) - unofficial Python wrapper for the Binance exchange REST API v3
* [tda-api](https://github.com/alexgolec/tda-api) - tda-api is an unofficial wrapper around the TD Ameritrade APIs. It strives to be as thin and unopinionated as possible, offering an elegant programmatic interface over each endpoint
* [ib_insync](https://github.com/erdewit/ib_insync) - The goal of the IB-insync library is to make working with the Trader Workstation API from Interactive Brokers as easy as possible.
* [robin-stocks](https://robin-stocks.readthedocs.io/) - simple to use functions to interact with the Robinhood Private API

# Data Providers

* [intrinio-sdk](https://docs.intrinio.com/documentation/python) - Intrinio provides US market data, company fundamentals data, options data and SEC data, powered by advanced data quality technology
* [polygon-api-client](https://pypi.org/project/polygon-api-client/) - python client for Polygon.io, provider of real-time and historical financial market data APIs
* [iexfinance](https://pypi.org/project/iexfinance/) - Python SDK for IEX Cloud. Easy-to-use toolkit to obtain data for Stocks, ETFs, Mutual Funds, Forex/Currencies, Options, Commodities, Bonds, and Cryptocurrencies
* [yfinance](https://pypi.org/project/yfinance/) - yfinance offers a reliable, threaded, and Pythonic way to download historical market data from Yahoo! finance.
* [quandl](https://www.quandl.com/tools/python) - source for financial, economic, and alternative datasets, serving investment professionals
* [alpha-vantage](https://alpha-vantage.readthedocs.io/) - The Alpha Vantage Stock API provides free JSON access to the stock market, plus a comprehensive set of technical indicators
* [sec-edgar-downloader](https://sec-edgar-downloader.readthedocs.io/en/latest/) - package for downloading company filings from the SEC EDGAR database

# Backtesting

* [backtrader](https://www.backtrader.com/) - feature-rich Python framework for backtesting and trading
* [pyalgotrade](https://gbeced.github.io/pyalgotrade/) - Python Algorithmic Trading Library with focus on backtesting and support for paper-trading and live-trading
* [bt](https://pmorissette.github.io/bt/) - bt is a flexible backtesting framework for Python used to test quantitative trading strategies
* [backtesting](https://kernc.github.io/backtesting.py/) - Backtesting.py is a Python framework for inferring viability of trading strategies on historical (past) data

# Portfolio and Performance Analysis

* [pyfolio](https://github.com/quantopian/pyfolio) - library for performance and risk analysis of financial portfolios developed by Quantopian
* [finquant](https://finquant.readthedocs.io/) - program for financial portfolio management, analysis and optimisation

# Web Server, Task Queue

* [uvicorn](https://www.uvicorn.org/) - lightning-fast ASGI server implementation
* [gunicorn](https://gunicorn.org/) - Python WSGI HTTP Server for UNIX
* [celery](https://docs.celeryproject.org/) - simple, flexible, distributed task queue

# Networking

* [requests](https://requests.readthedocs.io/) - elegant and simple HTTP library for Python
* [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - Amazon Web Services (AWS) SDK for Python. It enables Python developers to create, configure, and manage AWS services, such as EC2 and S3.
* [urllib3](https://urllib3.readthedocs.io/en/latest/) - powerful, user-friendly HTTP client for Python
* [websocket-client](https://pypi.org/project/websocket_client/) - websocket client for python. This provide the low level APIs for WebSocket
* [websockets](https://websockets.readthedocs.io/en/stable/intro.html) - library for building WebSocket servers and clients in Python

# Utilities

* [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) - library for screen-scraping
* [pendulum](https://pendulum.eustace.io/) - package to assist with date and time manipulation
* [click](https://click.palletsprojects.com/) - package for creating beautiful command line interfaces in a composable way with as little code as necessary
* [passlib](https://passlib.readthedocs.io/) - password hashing library

# Machine Learning

* [tensorflow](https://www.tensorflow.org/) - open source library to help you develop and train ML models
* [scikit-learn](https://scikit-learn.org/) - machine learning library
* [keras](https://keras.io/) - deep learning framework
* [pytorch](https://pytorch.org/) - optimized tensor library for deep learning using GPUs and CPUs
* [opencv-python](https://github.com/skvark/opencv-python) - open source computer vision library
