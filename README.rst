yieldfixture
========================================

.. image:: https://travis-ci.org/podhmo/yieldfixture.svg?branch=master
    :target: https://travis-ci.org/podhmo/yieldfixture

how to use
----------------------------------------

.. code-block:: python

  from yieldfixture import create
  run, yield_fixture = create()
  
  
  @yield_fixture
  def f():
      print(">>> f")
      yield 1
      print(">>> f")
  
  
  @yield_fixture
  def g():
      print("  >>> g")
      yield 2
      print("  >>> g")
  
  
  @run
  def use_it(x, y):
      print("{} + {} = {}".format(x, y, x + y))

output

.. code-block::

  >>> f
    >>> g
  1 + 2 = 3
    >>> g
  >>> f

with context
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  from yieldfixture import create, with_context
  run, yield_fixture = create()
  
  
  @yield_fixture
  @with_context
  def f(ctx):
      i = ctx["i"] = 0
      print("{}>>> f".format("  " * i))
      yield 1
      print("{}>>> f".format("  " * i))
  
  
  @yield_fixture
  @with_context
  def g(ctx):
      i = ctx["i"] = ctx["i"] + 1
      print("{}>>> g".format("  " * i))
      yield 2
      print("{}>>> g".format("  " * i))
  
  
  @run
  def use_it(x, y, *, i=0):
      print("{}{} + {} = {}".format("  " * (i + 1), x, y, x + y))

output

.. code-block::

  >>> f
    >>> g
      1 + 2 = 3
    >>> g
  >>> f

when a exception is raised
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  from yieldfixture import create, with_context
  run, yield_fixture = create()
  
  
  @yield_fixture
  @with_context
  def f(ctx):
      i = ctx["i"] = 0
      print("{}>>> f".format("  " * i))
      try:
          yield 1
      finally:
          print("{}>>> f".format("  " * i))
  
  
  @yield_fixture
  @with_context
  def g(ctx):
      i = ctx["i"] = ctx["i"] + 1
      print("{}>>> g".format("  " * i))
      try:
          yield 2
      finally:
          print("{}>>> g".format("  " * i))
  
  
  @run
  def use_it(x, y, *, i=0):
      print("{}{} + {} = {}".format("  " * (i + 1), x, y, x + y))
      1 / 0

output

.. code-block::

  >>> f
    >>> g
      1 + 2 = 3
    >>> g
  >>> f
  Traceback (most recent call last):
    File "examples/02withexception.py", line 28, in <module>
      def use_it(x, y, *, i=0):
    File "$HOME/vboxshare/venvs/my3/yieldfixture/yieldfixture/__init__.py", line 98, in run_with
      return fn(*ctx.args, **ctx.kwargs)
    File "examples/02withexception.py", line 30, in use_it
      1 / 0
  ZeroDivisionError: division by zero

selective fixture activation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  from yieldfixture import create, with_context
  run, yield_fixture = create()
  
  
  @yield_fixture
  @with_context
  def f(ctx):
      i = ctx["i"] = ctx.get("i", -1) + 1
      print("{}>>> f".format("  " * i))
      try:
          yield 1
      finally:
          print("{}>>> f".format("  " * i))
  
  
  @yield_fixture
  @with_context
  def g(ctx):
      i = ctx["i"] = ctx.get("i", -1) + 1
      print("{}>>> g".format("  " * i))
      try:
          yield 2
      finally:
          print("{}>>> g".format("  " * i))
  
  
  @run
  def use_it(x, y, *, i=0):
      print("{}{} + {} = {}".format("  " * (i + 1), x, y, x + y))
  
  
  @run([g, f])
  def use_it2(x, y, *, i=0):
      print("{}{} + {} = {}".format("  " * (i + 1), x, y, x + y))

output

.. code-block::

  >>> f
    >>> g
      1 + 2 = 3
    >>> g
  >>> f
  >>> g
    >>> f
      2 + 1 = 3
    >>> f
  >>> g
