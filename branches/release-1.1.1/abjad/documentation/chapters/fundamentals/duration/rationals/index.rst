Rational values
===============

Abjad models musical duration with rational numbers. Standard Python
distributions include built-in classes for integers, floats and many
other types of number. But no rational. So Abjad implements the custom
rational class described here.

The Abjad :class:`Rational <abjad.rational.rational.Rational>` class initializes with integer numerator and integer denominator.

.. sourcecode:: python

    
    abjad> Rational(4, 5)
    Rational(4, 5)


Negative values are allowed.

.. sourcecode:: python

    
    abjad> Rational(-4, 5)
    Rational(-4, 5)


.. sourcecode:: python

    
    abjad> Rational(-4, -5)
    Rational(4, 5)


Zero-valued numerators are allowed but zero-valued denominators
aren't.

.. sourcecode:: python

    
    abjad> Rational(0, 1)
    Rational(0, 1)


Numerator and denominator both simplify on input.

.. sourcecode:: python

    
    abjad> Rational(8, 10)
    Rational(4, 5)


Arithmetic operators work as expected.

.. sourcecode:: python

    
    abjad> Rational(4, 5) + Rational(2, 3)
    Rational(22, 15)


.. sourcecode:: python

    
    abjad> Rational(4, 5) ** 2
    Rational(16, 25)


Comparison operators work, too.

.. sourcecode:: python

    
    abjad> Rational(4, 5) >= Rational(2, 3)
    True


Type coercion works with ``float( )``.

.. sourcecode:: python

    
    abjad> float(Rational(4, 5))
    0.80000000000000004



.. note::

   Rational-to-rational exponentiation is not supported. `Rational(4, 5)
   ** Rational(2, 3)` will raise an `AssertionError`.


.. note::

   The Abjad :class:`Rational <abjad.rational.rational.Rational>` exists only
   because current versions of Python contain no such functionality.
   Previous Python enhancement proposals, including `PEP 239
   <http://www.python.org/dev/peps/pep-0239/>`__, have proposed the
   addition of a rational type to Python. Guido van Rossum has rejected
   all such proposals up to now. However, it looks like Python 2.6
   implements a `Fraction` type with most of the functionality we need.
   Should this turn out to be the case, then the Abjad 
   :class:`Rational <abjad.rational.rational.Rational>`
   class will be deprecate and then
   remove from the distribution. Abjad users and contributors should
   therefore avoid special customization or extension of the Abjad
   :class:`Rational <abjad.rational.rational.Rational>` class and consider
   adding helpers for novel uses of rational arithmetic instead.

.. note::

   Other third-party implementations of rational arithmetic abound on the
   web. LilyPond distributions include a rational class that corresponds
   closely to the Abjad :class:`Rational <abjad.rational.rational.Rational>`.
   Other good examples show up readily in search results.

.. todo:: Migrate to the rational type available in Python 2.6.
