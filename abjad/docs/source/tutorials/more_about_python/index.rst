More about Python
==================

The tutorials earlier in this section showed basic ways to work with Python.
In this tutorial we'll use the interactive interpreter to find out
more about the language and library of tools that it contains.


Doing many things
-----------------

You can use the Python interpreter to do many things.

Simple math like addition looks like this::

    >>> 2 + 2
    4

Exponentiation looks like this::

    >>> 2 ** 38
    274877906944

Interacting with the Python interpreter means typing something as input
that Python then evaluates and prints as output.

As you learn more about Abjad you'll work more with Python files than with the Python interpreter.
But the Python interpreter's input-output loop makes it easy to see what Python is all about.


Looking around
--------------

Use ``dir()`` to see the things the Python interpreter knows about::

    >>> dir()
    ['__builtins__', '__doc__', '__name__', '__package__']

These four things are the only elements that Python loads into the so-called
global namespace when you start the interpreter.

Now let's define the variable ``x``::

    >>> x = 10

Which lets us do things with ``x``::
    
    >>> x ** 2
    100

When we call ``dir()`` now we see that the global namespace has changed::

    >>> dir()
    ['__builtins__', '__doc__', '__name__', '__package__', 'x']

Using ``dir()`` is a good way to check the variables Python knows about when it runs.

Now type ``__builtins__`` at the prompt::

    >>> __builtins__
    <module '__builtin__' (built-in)>

Python responds and tells us that ``__builtins__`` is the name of a module.

A module is file full of Python code that somebody has written to provide new functionality.

Use ``dir()`` to inspect the contents of ``__builtins__``::

    >>> dir(__builtins__)
    ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError', 'BytesWarning', 
    'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FloatingPointError', 
    'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 
    'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'NameError', 'None', 
    'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 
    'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError', 
    'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'True', 'TypeError', 'UnboundLocalError', 
    'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 
    'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError', '_', '__debug__', '__doc__', '__import__', 
    '__name__', '__package__', 'abs', 'all', 'any', 'apply', 'basestring', 'bin', 'bool', 'buffer', 
    'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile', 'complex', 'copyright', 
    'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 
    'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 
    'intern', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'long', 'map', 'max', 
    'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 
    'raw_input', 'reduce', 'reload', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 
    'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'unichr', 'unicode', 'vars', 'xrange', 'zip']

Python responds with a list of many names.

Use Python's ``len()`` command together with the last-output character ``_``
to find out how many names ``__builtins__`` contains::

    >>> len(_)
    144

These names make up the core of the Python programming language.

As you learn Abjad you'll use some Python built-ins all the time and others less often.

Before moving on, notice that both ``dir()`` and ``len()`` appear in the list above.
This explains why we've been able to use these commands in this tutorial.
