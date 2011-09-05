Coding standards
================

Indent with spaces, not with tabs. Use four spaces at a time::

    def foo(x, y):
        return x + y

Introduce comments with one pound sign and a single space::

    # comment before foo
    def foo(x, y):
        return x + y

Favor early imports at the head of each module. Only one ``import`` per line::

       from foo import x
       from foo import y
       from foo import z

Include two blank lines after ``import`` statements before the rest of the module::

       from foo import x
       from foo import y
       from foo import z

    
       class Foo(object):
           ...
           ...

Wrap docstrings with triple apostrophes and align like this::

    def foo(x, y):
        '''This is the first line of the foo docstring.
        This is the second line of the foo docstring.
        And this is the last line of the foo docstring.
        '''

Use paired apostrophes to delimit strings::

    s = 'foo'

Use paired quotation marks to delimit strings within a string::

    s = 'foo and "bar"'

Name classes in upper camelcase::

    def FooBar(object):
        ...
        ...

Name bound methods in underscore-delimited lowercase::

    def Foo(object):

        def bar_blah(self):
            ...

        def bar_baz(self):
            ...

Name module-level functions in underscore-delimited lowercase::

    def foo_bar():
        ...

    def foo_blah():
        ...

Separate bound method definitions with a single empty line::

    class FooBar(object):

        def __init__(self, x, y):
            ...

        def bar_blah(self):
            ...

        def bar_baz(self):
            ...

Organize the definitions of core classes into the five following major sections plus initialization::

    class FooBar(object):

        def __init__(self, x, y):
            ...

        ### OVERLOADS ###

        def __repr__(self):
            ...

        def __str__(self):
            ...

        ### PRIVATE ATTRIBUTES ###

        @property
        def _foo(self):
            ...

        ### PUBLIC ATTRIBUTES ###

        @property
        def bar(self):
            ...

        ### PRIVATE METHODS ###

        def _blah(self, x, y):
            ...

        ### PUBLIC METHODS ###

        def baz(self, z):
            ...

Preceed private class attributes with a single underscore::

    class FooBar(object):

        ### PRIVATE ATTRIBUTES ###

        @property
        def _foo(self):
            ...

        ### PRIVATE METHODS ###

        def _blah(self, x, y):
            ...

Alphabetize method names.

Use ``<`` less-than signs in preference to greater-than signs::

    if x < y < z:
        ...

Limit lines to 110 characters and use ``\`` to break lines where necessary.

Eliminate trivial slice indices. Use ``s[:4]`` instead of ``s[0:4]``.

Do not abbreviate variable names.

Name variables that represent a list or other collection of objects in the plural.

Implement only one class per module.

Implement only one function per module.

Author one ``py.test`` test file for every module-level function.

Author one ``py.test`` test file for every bound method in the public interface of a class.
