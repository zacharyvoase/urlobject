URLObject 2
===========

|Build Status|

**URLObject** is a utility class for manipulating URLs. The latest incarnation of
this library builds upon the ideas of its predecessor, but aims for a clearer
API, focusing on proper method names over operator overrides. It's also being
developed from the ground up in a test-driven manner, and has full Sphinx
documentation.

If you're new to this library, take a look at the :doc:`quickstart
<quickstart>`. If you're just here for reference purposes, see the :doc:`API
documentation <api>`.

Installation
------------

Install using ``pip`` from `pypi <http://pypi.python.org/pypi/URLObject>`__.
There are no dependencies, and the package is pure Python.

.. code:: bash

    pip install URLObject

Contents
--------

.. toctree::
    :maxdepth: 2

    quickstart
    api


License
=======

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to http://unlicense.org/


Credits
=======

This library bundles `six <http://packages.python.org/six/>`__, which is
licensed as follows:

    Copyright (c) 2010-2012 Benjamin Peterson

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation files
    (the "Software"), to deal in the Software without restriction,
    including without limitation the rights to use, copy, modify, merge,
    publish, distribute, sublicense, and/or sell copies of the Software,
    and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
    BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
    ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

Many thanks go to `Aron Griffis <http://arongriffis.com/>`__ for porting
this library to Python 3, and to `vmalloc <https://github.com/vmalloc>`__ for
work on the comprehensive API documentation and Sphinx setup.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |Build Status| image:: https://secure.travis-ci.org/zacharyvoase/urlobject.png?branch=master
   :target: http://travis-ci.org/zacharyvoase/urlobject
