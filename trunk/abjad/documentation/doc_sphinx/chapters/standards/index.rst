Coding Standards
================

Indent with three spaces at a time. Do no indent with tabs::

   def foo(x, y):
      return x + y

Introduce comments with two pound signs and a single space::

   ## comment before foo
   def foo(x, y):
      return x + y

Limit lines to 80 characters and use ``\`` to break lines where necessary.

Favor early imports at the head of each module instead of late imports within the body of a module. Include only one ``import`` per line::

      from foo import x
      from foo import y
      from foo import z

Include two blank lines after ``import``` statements but before the class or method definitions::

      from foo import x
      from foo import y
      from foo import z

   
      class Foo(object):
         ...
         ...

Wrap docstrings with triple apostrophes instead of triple quotation marks. Align docstrings like this::

   def foo(x, y):
      '''This is the first line of the foo docstring.
         This is the second line of the foo docstring.
         And this is the last line of the foo docstring.'''

Use paired apostrophes to delimit strings instead of pair quotation marks::

   s = 'foo'

Use paired quotation marks only within pair apostrophes::

   s = 'foo and "bar"'

Eliminate trivial slice indices. Use ``s[:4]`` instead of ``s[0:4]``.

Name classes in upper camelcase::

   def FooBar(object):
      ...
      ...

Name bound methods in lower camelcase::

   def Foo(object):

      def barBlah(self):
         ...

      def barBaz(self):
         ...

Name module-level functions in underscore-delimited lowercase::

   def foo_bar( ):
      ...

   def foo_blah( ):
      ...

Separate bound method definitions with a single empty line::

   class FooBar(object):

      def __init__(self, x, y):
         ...

      def barBlah(self):
         ...

      def barBaz(self):
         ...

Organize the definitions of core classes into the five following major sections plus initialization::

   class FooBar(object):

      def __init__(self, x, y):
         ...

      ## OVERLOADS ##

      def __repr__(self):
         ...

      def __str__(self):
         ...

      ## PRIVATE ATTRIBUTES ##

      @property
      def _foo(self):
         ...

      ## PUBLIC ATTRIBUTES ##

      @property
      def bar(self):
         ...

      ## PRIVATE METHODS ##

      def _blah(self, x, y):
         ...

      ## PUBLIC METHODS ##

      def baz(self, z):
         ...

Preceed private class attributes with a single underscore::

   class FooBar(object):

      ## PRIVATE ATTRIBUTES ##

      @property
      def _foo(self):
         ...

      ## PRIVATE METHODS ##

      def _blah(self, x, y):
         ...

Include a single space in between empty parentheses::

   def foo( ):
      ...
      ...

Do not abbreviate variable names. Use ``container`` instead of ``cont`` and ``component`` instead of ``comp``.

Name variables that represent a list or other collection of object in the plural. For example, use ``components`` to name a variable that will most likely house a Python list of Abjad components.

Implement only one class per module.

Implement only one function per module.

Author one ``py.test`` test file for each module-level function or for each bound method in the public interface of a class.

Encapsulate, encapsulate, encapsulate.
