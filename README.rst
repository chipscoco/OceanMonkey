.. image:: https://raw.githubusercontent.com/chipscoco/OceanMonkey/main/artwork/logo.jpg

Overview
========

OceanMonkey is a High-Level Distributed Web Crawling and Web Scraping framework, used to
crawl websites and extract structured data from their pages. It can be used for
a wide range of purposes, from data mining to monitoring and automated testing.

OceanMonkey was brought to life and is maintained by chenzhengqiang(wechat:Pretty-Style, blog:http://www.chipscoco.com) while teaching the python's web scraping in 2021.

Requirements
============

* Python 3.5+
* Works on Linux, Windows, macOS, BSD

Install
=======

The quick way:
    pip install oceanmonkey


Quick start
=============
Firstly execute **monkeys startproject** in command line to create a OceanMonkey Project like the following:
    monkeys startproject BeBe

Then write your crawling logic in gibbons.py under the monkeys' directory and write your storing logic in orangutans.py.

Execute the **monkeys run** command under the project's directory finally when you finish your coding work:

    cd BeBe

    monkeys run
