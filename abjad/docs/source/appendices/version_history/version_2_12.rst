:orphan:

Abjad 2.12
----------

Released 2013-03-24. Built from r9810.
Implements 559 public classes and 1045 functions totaling 216,000 lines of code.

Performance increases
^^^^^^^^^^^^^^^^^^^^^

Abjad 2.12 introduces a number of performance optimizations. ``LilyPondFile``
objects format four times faster than before. ``Duration`` objects initialize
faster.  ``NonreducedFraction`` arithmetic operations are faster.  Context
marks like dynamics and tempo indications now attach and detach much faster.

Duration property renames
^^^^^^^^^^^^^^^^^^^^^^^^^

You may now use ``note.duration``, ``rest.duration``, ``staff.duration`` and so
on to access the duration of all objects in the system. The previous term
``prolated_duration`` has been removed from all objects in the system.

Timespan integration
^^^^^^^^^^^^^^^^^^^^

You may now use ``note.timespan.start_offset`` and
``note.timespan.stop_offset`` to access the start- and stop-offsets of notes.
The previous ``note.start_offset`` and ``note.stop_offset`` properties have
been removed from the system. Note that the same is true for all other durated
objects systemwide.

Deepcopy changes
^^^^^^^^^^^^^^^^

You may now use Python's built-in ``copy.deepcopy()`` to copy any object in the
system.  Previous versions of Abjad aliased Python's deepcopy. In Abjad 2.12
deepcopy copies all attributes of a score component and all references the
component holds. This result is that deepcopying a note will result in the note
being copied as well as the entire score tree in which the note is embedded.

Measure classes
^^^^^^^^^^^^^^^

Abjad 2.12 features only a single ``Measure`` class. The anonymous measure and
dynamic measures have been removed from the system.

The string format of ``Measure`` objects has been updated to indicate ties:

::

    >>> m = Measure((5, 4), "c'4 ~ c' d' ~ d' e'")
    >>> str(m)
    "|5/4 c'4 ~ c'4 d'4 ~ d'4 e'4|"

Other new features
^^^^^^^^^^^^^^^^^^

Extended ``lilypondfiletools.ContextBlock`` with read/write ``alias`` property.
This allows for the definition of new context in reference to existing
contexts:

::

    >>> context_block = lilypondfiletools.ContextBlock()
    >>> context_block.context_name = 'Staff'
    >>> context_block.type = 'Engraver_group'
    >>> context_block.name = 'CustomStaff'
    >>> context_block.alias = 'Staff'
    >>> f(context_block)
    \context {
        \Staff
        \name CustomStaff
        \type Engraver_group
        \alias Staff
        \override StaffSymbol #'color = #red
    }

The ``datastructuretools.PayloadTree`` class now implements ``graphviz_format``
and ``graphviz_graph`` properties.  You can use these to visualized any tree
object you create.

The ``Note.sounding_pitch`` property is now read / write.

``Articulation`` marks can now initialize from other ``Articulation`` marks and
``Dynamic`` marks can now initialize from other ``Dynamic`` marks.

The ``MetricGridSpanner`` class has been removed from the ``spannertools``
package.

You may now clear the pitches of a chord with ``chord[:] = []``.
The ``Chord.clear()`` method has been removed.

New ``systemtools.IOManager.profile_expr()`` keywords available. The ``print_callers=True``
and ``print_callees=True`` break profiler output to calling and called
functions, respectively.  Set ``print_to_terminal=False`` to return profiler
output as a string.

A new ``systemtools.IOManager.count_function_calls()`` function is available. Use the
function to return the number of function calls required to interpret any Abjad
expression.

A new ``systemtools.which()`` function is available. The new function is
cross-platform and can be used to check for the presence of commandline tools
before opening pipes.

Automatic line breaking is now available in ``abjad-book`` LaTeX output.
Thanks to Jeffry Treviño for this feature.
