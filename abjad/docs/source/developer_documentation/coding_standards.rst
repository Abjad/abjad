Coding standards
================

Abjad's coding standards are rigorous, but unambiguous. Code should be written
in a clear and consistent manner. This allows not only for long-term
legibility, but also facilitates our large collection of codebase tools, which
we use to refactor and maintain the system.

We follow `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_ whenever possible,
and our coding standards are quite similar to `Google's
<http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>`_, which
should be considered required reading.


General philosophy
------------------

Public is better than private. Explicit is better than implicit. Brevity is
almost always acquired along with ambiguity. You're probably only going to type
it once, so why make it vaguer than it needs to be?  Clarity in purpose and
style frees us up to think about more important things... like making music.
With that in mind, let's keep our code as clear as possible.


Codebase layout
---------------

Avoid private classes.

Avoid private functions. (But use private class methods as necessary.)

Implement only one statement per line of code.

Implement only one class per module.

Implement only one function per module.


Tests
-----

Author one ``pytest`` test file for every module-level function.

Author one ``pytest`` test file for every bound method in the public interface
of a class.

Author one ``doctest`` for every public function, method or property.


Casing and naming
-----------------

Name classes in upper camelcase:

::

    def FooBar(object):
        ...
        ...

Name bound methods in lower snakecase:

::

    def Foo(object):

        def bar_blah(self):
            ...

        def bar_baz(self):
            ...

Name module-level functions in lower snakecase:

::

    def foo_bar():
        ...

    def foo_blah():
        ...

Name all variables in lower snakecase:

::

    variable_one = 1
    variable_two = 2

Do not abbreviate variable names, but do use ``expr`` for 'expression',
``i`` or ``j`` for loop counters, and ``x`` for list comprehensions:

::
    
    def foo(expr):
        result = []
        for i in range(7):
            for j in range(23):
                result.extend(x for x in expr[i][j])

Name variables that represent a list or other collection of objects in the
plural:

::

    some_strings = (
        'one',
        'two',
        'three',
        )

Name functions beginning with a verb. (But use ``noun_to_noun`` for conversion
functions and ``mathtools.noun`` for some ``mathtools`` functions.)

Preceed private class attributes with a single underscore.



Imports
-------

Avoid ``from``. Instead of ``from fractions import Fraction`` use:

::

    import fractions

and then qualify the desired classes and functions with the imported module:

::

    my_fraction = fractions.Fraction(23, 7)

Favor early imports at the head of each module. Only one ``import`` per line.

Arrange standard library imports alphabetically at the head of each module:

::

    import fractions
    import types

Follow standard library imports with intrapackage Abjad imports arranged
alphabetically:

::

    import footools
    import bartools
    import blahtools

Include two blank lines after ``import`` statements before the rest of the
module:

::

    import fractions
    import types
    import footools
    import bartools
    import blahtools

    class Foo(object):
        ...
        ...

Use late imports to prevent circular imports problems, especially when
importing functionality from within the same tools package.


Whitespace and indentation
--------------------------

Indent with spaces, not with tabs. Use four spaces at a time:

::

    def foo(x, y):
        return x + y

When enumerating lists, tuples or dictionaries, place each item on its own
line, with every item having a trailing comma. Place the final brace on its own
line, indented like this:

::

    my_tuple = (
        'one',
        'two',
        'three',
        )

    my_dictionary = {
        'bar': 2,
        'baz': 3,
        'foo': 1,
        }

When a function or method call contains many arguments, prefer to place each
argument on its own line as well, with trailing parenthesis:

::

    result = my_class.do_something(
        expr,
        keyword_1=True,
        keyword_2=True,
        keyword_3=True,
        )

..  note::

    Python (unlike PHP, Java, Javascript etc.) allows for final trailing commas
    in collections and argument lists. We take advantage of this by placing
    each item on its own line whenever possible, along with its own trailing
    comma.
    
    Why? It actually helps us read and write more code.
    
    When adding, subtracting or reordering items in a collection or argument
    list defined across multiple lines, we never have to think about which item
    needs to have a comma added, and which needs to have one removed.
    Similarly, the resulting diffs are much simpler to read. If you keep
    everything on the same line, the diff will show that the entire line has
    changed, and you'll have to take time carefully comparing the old and new
    version to see what (if anything) has been altered. When each item has its
    own line, the diff will show only the insertion or deletion of a single
    item.

Use one space around operators:

::

    1 + 1

instead of:

::

    1+1

Use no spaces around the ``=`` for keyword arguments:

::

    my_function(keyword=argument)

instead of:

::

    my_function(keyword = argument)

Line length
-----------

Prefer 80 characters whenever possible.

Limit docstring lines to 99 characters.

Limit source lines to 110 characters and use ``\`` to break lines where
necessary.


Comments
--------

Introduce comments with one pound sign and a single space:

::

    # comment before foo
    def foo(x, y):
        return x + y

Avoid inline comments.


Docstrings
----------

Wrap docstrings with triple apostrophes and align like this:

::

    def foo(x, y):
        r'''This is the first line of the foo docstring.

        This is the second line of the foo docstring.
        And this is the last line of the foo docstring.
        '''

Start each docstring with a single sentence explaining, in brief, what the
class, function, method or property does.

For class docstrings, and class properties, the article and noun is sufficient,
but for methods use a verb, unless that verb is "returns":

::

    class NamedPitch(Pitch):
        r'''A named pitch.
        ...
        '''

        ...

        @property
        def accidental(self):
            r'''An accidental.
            ...
            '''

        ...

        def transpose(self, expr):
            r'''Transpose by `expr`.
            ...
            '''

Phrase predicate docstrings like this:

::

    class Gesture(object):
    
        ...

        def is_pitched(self):
            r'''True if gesture is pitched, otherwise false.
            ...
            '''

Do not place restructured text double colon `::` symbols at the end of a line
of text. 

Instead, place all restructured text double colon `::` symbols on lines by
themselves, like this:

::

    def multiply(x, y):
        r'''Multiplies x by y:

        ::

            >>> foo(10, 11)
            110

        Returns integer.
        '''


Quotation
---------

Use paired apostrophes to delimit strings:

::

    s = 'foo'

Use paired quotation marks to delimit strings within a string:

::

    s = 'foo and "bar"'


Functions and methods
---------------------

Alphabetize keyword arguments:

::

    my_function(one=1, three=3, two=2)

::

    my_function(one=1, two=2, three=3)

Always include keyword argument names explicitly in function calls:

::

    my_function(expr, one=1, three=3, two=2)

But not:

::

    my_function(expr, 1, 3, 2)

..  note::

    Python let's you write out the arguments to a function or method as though
    they were all positional:

    ::

        def foo(expr, first=None, second=None, third=None):
            ...

    ::

        foo(expr, 1, 2, 3)

    Do *not* do this.

    We ask that keyword arguments are always named explicitly because it
    makes function calls completely unambiguous, and therefore make it easier
    to refactor using automated tools. In the above function definition, what
    is our cognitive burden if we realize we need to rename the keyword
    ``third`` to ``alpha``, but we haven't named the keywords explicitly in our
    use of the function? 

    ::

        def foo(expr, first=None, second=None, alpha=None):
            ...

    The old function call ``foo(expr, 1, 2, 3)`` will still work correctly,
    because we haven't reordered the keywords in the function's signature. But
    that's burdensome for us, as we're now relying not on the *lexical*
    ordering of the keyword names, but on their *position*. They might as well
    be positional arguments.  Don't do this! Always explicitly name your
    keyword arguments, and assume that they can and will be renamed and
    re-alphabetized at any time. Typing a few extra character is not a burden,
    but intuiting context while proofreading old code is.

Classes and class file layout
-----------------------------

Organize the definitions of classes into the seven following major sections,
omitting sections if they contain no class members:

::

    class FooBar(object):

        ### CLASS VARIABLES ###

        special_enumeration = (
            'foo',
            'bar',
            'blah',
            )

        ### INITIALIZER ###

        def __init__(self, x, y):
            ...

        ### SPECIAL METHODS ###

        def __repr__(self):
            ...

        def __str__(self):
            ...

        ### PRIVATE PROPERTIES ###

        @apply
        def _bar():
            def fget(self):
                ...
            def fset(self, expr):
                ...
            return property(**locals())

        @property
        def _foo(self):
            ...

        ### PRIVATE METHODS ###

        def _blah(self, x, y):
            ...

        ### PUBLIC PROPERTIES ###

        @property
        def baz(self):
            ...

        @apply
        def quux():
            def fget(self):
                ...
            def fset(self, expr):
                ...
            return property(**locals())

        ### PUBLIC METHODS ###

        def wux(self, expr, keyword=None):
            ...

Separate bound method definitions with a single empty line:

::

    class FooBar(object):

        def __init__(self, x, y):
            ...

        def bar_blah(self):
            ...

        def bar_baz(self):
            ...

Alphabetize method names.


Operators
---------

Use ``<`` less-than signs in preference to greater-than signs::

    if x < y < z:
        ...


Miscellaneous
-------------

Eliminate trivial slice indices. Use ``s[:4]`` instead of ``s[0:4]``.

Prefer new-style string formatting to old-style string interpolation. Use
``'string {} content'.format(expr)`` instead of ``'string %s content' % expr``.

Prefer list comprehensions to ``filter()``, ``map()`` and ``apply()``.
