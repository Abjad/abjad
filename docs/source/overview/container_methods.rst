Basic operations on containers
==============================

Abjad containers work like Python lists.

----

..  rubric:: Container properties

The length of a container is defined equal to the number of components in the container:

::

    >>> container = abjad.Container("ds'16 cs'16 e'16 c'16 d'2 ~ d'8")
    >>> abjad.show(container)

::

    >>> len(container)

----

..  rubric:: Iteration

Containers iterate their contents like lists:

::

    >>> for item in container:
    ...     item

----

..  rubric:: Item getting

Item getting returns one component at a time:

::

    >>> container[0]

    >>> container[1]

    >>> container[2]

Slicing returns a selection of components:

::

    >>> container[:3]

----

..  rubric:: Containment testing
    
Containment testing and indexing work like lists:

::

    >>> note = container[0]
    >>> note in container

    >>> container.index(note)

    >>> rest = abjad.Rest("r4")
    >>> rest in container

----

..  rubric:: Adding components

Append, extend and insert work like lists:

::

    >>> container.append("af'32")
    >>> abjad.show(container)

    >>> container.extend("c''32 a'32")
    >>> abjad.show(container)

    >>> container.insert(-3, "g'32")
    >>> abjad.show(container)

----

..  rubric:: Removing components

And pop and remove work like lists, too:

::

    >>> note = container.pop(-1)
    >>> abjad.show(container)

    >>> note = container[-1]
    >>> container.remove(note)
    >>> abjad.show(container)

..  The musical example on this page derives from Xenakis's Jalons (1986) for contrabass.
