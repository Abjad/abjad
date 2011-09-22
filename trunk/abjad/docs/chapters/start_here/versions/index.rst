Version history
===============


Abjad 2.5
---------

Released 2011-09-22. Built from r4803.

* Added ``get_leaf_in_expr_with_minimum_prolated_duration()`` function to ``leaftools``.
* Added ``get_leaf_in_expr_with_maximum_prolated_duration()`` function to ``leaftools``.
* Added ``are_relatively_prime()`` function to ``mathtools``.
* Added ``CyclicTree`` class to ``sequencetools``.
* Added ``get_next_n_nodes_at_leve(n, level)`` method to ``sequencetools.Tree``.
* Extended spanners to sort by repr.
* Renamed ``lilyfiletools`` to ``lilypondfiletools``.
* Renamed ``lilyfiletools.LilyFile`` to ``lilypondfiletools.LilyPondFile``.
* Renamed ``lilyfiletools.make_basic_lily_file()`` to ``lilypondfiletools.make_basic_lilypond_file()``.

Note that the three renames change user syntax.
Composers working with the ``lilypondfiletools`` module should update their score code.


Abjad 2.4
---------

Released 2011-09-12. Built from r4769.

* Added Mozart Musikalisches Wuerfelspiel.

.. image:: ../../examples/mozart/images/mozart-lily.png

* Added new ``Tree`` class to ``sequencetools`` to work with sequences whose elements have been grouped into arbitrarily many levels of containment.

* Added new ``BarLine`` class to ``marktools`` package.
* Added new ``HorizontalBracketSpanner`` to ``spannertools`` package.
* Improved ``schemetools.SchemePair`` handling.
* Extended ``LilyPondFile`` blocks with double underscore-delimited attributes.


Abjad 2.3
---------

Released 2011-09-04. Built from r4747.

Filled out the API for working with marks::

    marktools.attach_articulations_to_components_in_expr()
    marktools.detach_articulations_attached_to_component()
    marktools.get_articulations_attached_to_component()
    marktools.get_articulation_attached_to_component()
    marktools.is_component_with_articulation_attached()

These five type of functions are now implemented for the following marks::

    marktools.Annotation
    marktools.Articulation
    marktools.LilyPondCommandMark
    marktools.LilyPondComment
    marktools.StemTremolo

The same type of functions are likewise implemented for the following context marks::

    contexttools.ClefMark
    contexttools.DynamicMark
    contexttools.InstrumentMark
    contexttools.KeySignatureMark
    contexttools.StaffChangeMark
    contexttools.TempoMark
    contexttools.TimeSignatureMark

* Extended ``Container.extend()`` to allow for LilyPond input strings. You can now say ``container.extend("c'4 d'4 e'4 f'4")``.

* Added public ``parent`` attribute to all components. You can now say ``note.parent``. The attribute is read-only.
* Added ``cfgtools.list_package_dependency_version()``.
* Added ``py.test`` and ``Sphinx`` dependencies to the Abjad package.
* Added LilyPond command mark chapter to reference manual

* Renamed ``cfgtools`` to ``configurationtools``.
* Renamed ``durtools`` to ``durationtools``.
* Renamed ``metertools`` to ``timesignaturetools``.
* Renamed ``seqtools`` to ``sequencetools``.
* Renamed ``Mark.attach_mark()`` to ``Mark.attach()``.
* Renamed ``Mark.detach_mark()`` to ``Mark.detach()``.
* Renamed ``marktools.Comment`` to ``marktools.LilyPondComment``. This matches ``marktools.LilyPondCommandMark``.
* Removed ``contexttools.TimeSignatureMark(3, 8)`` initialization. You must now say ``contexttools.TimeSignatureMark((3, 8))`` instead. This parallels the initialization syntax for rests, skips and measures.


Abjad 2.2
---------

Released 2011-08-30. Built from r4677. 

* Added articulations chapter to reference manual.
* Reordered the way in which Abjad determines the value of the ``HOME`` environment variable.
* Updated ``scr/devel/replace-in-files`` to avoid image files.
* Updated ``iotools.log()`` to call operating-specific text editor.


Abjad 2.1
---------

Released 2011-08-21. Built from r4655. 

* Updated instrument mark ``repr`` to display target context when instrument mark is attached.
* Extended ``scr/abj`` and ``scr/abjad`` to display Abjad version and revision numbers on startup.


Abjad 2.0
---------

Released 2011-08-17. Built from r4638.

Abjad 2.0 is the first public release of Abjad in more than two years. The new release of the system more than doubles the number of classes, functions and packages available in Abjad.

* The API has been cleaned up and completely reorganized. Features have been organized into a collection of 39 different libraries::

    cfgtools/          instrumenttools/   mathtools/         resttools/         tempotools/
    chordtools/        intervaltreetools/ measuretools/      schemetools/       threadtools/
    componenttools/    iotools/           metertools/        scoretools/        tietools/
    containertools/    layouttools/       musicxmltools/     seqtools/          tonalitytools/
    contexttools/      leaftools/         notetools/         sievetools/        tuplettools/
    durtools/          lilyfiletools/     pitcharraytools/   skiptools/         verticalitytools/
    gracetools/        marktools/         pitchtools/        spannertools/      voicetools/
    importtools/       markuptools/       quantizationtools/ stafftools/

* The name of almost every function in the public API has been changed to better indication what the function does. While this has the effect of making Abjad 2.0 largely non-backwards compatible with code written in Abjad 1.x, the longer and much more explicit function names in Abjad 2.0 make code used to structure complex scores dramatically easier to maintain and understand.

* The ``contexttools``, ``instrumenttools``, ``intervaltreetools``, ``lilyfiletools``, ``marktools``, ``pitcharraytools``, ``quantizationtools``, ``sievetools``, ``tonalitytools`` and ``verticalitytools`` packages are completely new.

* The classes implemented in the ``contexttools`` and ``marktools`` packages provide an object-oriented interfaces to clefs, time signatures, key signatures, articulations, tempo marks and other symbols stuck to the outside of the hierarchical score tree. The classes implemented in ``contexttools`` and ``marktools`` model information outside the score tree much the way that the classes implemented in ``spannertools`` implement object-oriented interfaces to beams, brackets, hairpins, glissandi and other line-like symbols.

* The ``instrumenttools`` package provides an object-oriented model of most of the conventional instruments of the orchestra.

* The ``intervaltreetools`` package implements a custom way of working with chunks of score during composition.

* The ``lilyfiletools`` package implements an object-oriented interface to arbitrarily structured LilyPond input files.

* The ``pitcharraytools`` package implements an object-oriented way of composing with pitches, pitch-classes and other pitch-related objects independent of rhythmic context.

* The experimental ``quantizationtools`` package implements classes and functions for quantizing rhythmic events.

* The ``sievetools`` package implements an object-oriented interface to the basics of Xenakis's system of sieves.

* The ``tonalitytools`` package implements classes and methods to model the basics of functional harmonic analysis.

* The ``verticalitytools`` package provides vertical-moment-based iteration and analysis of any score. 

* The ``pitchtools`` package has grown considerably in size and functionality. Classes now exist to model named and numbered chromatic pitches (and pitch-classes), named and numbered diatonic pitches (and pitch-classes), melodic and harmonic diatonic intervals (and interval-classes), melodic and harmonic chromatic intervals (and interval-classes), as well as ordered segments and unordered sets of these and related objects. The package contains dozens of functions to create, inspect, iterate, analyze and transpose these classes and their collections.

* The old ``listtools`` package has been renamed seqtools.

* Dozens of new functions for cutting, pasting, partitioning, breaking, arranging and reordering score components have been added to the system. See the new functions in ``componenttools``, ``containertools``, ``leaftools``, ``measuretools`` and ``scoretools`` for details.

* The core component classes modeling notes, rests, chords, tuplets, measures, voices, staves and scores have been reimplemented to consume dramatically less memory, making it much easier to work with arrays of hundreds and thousands of components.

* Abjad core formatting logic has been optimized to make the formatting of scores with hundreds or thousands of events take much less time than before. 

* The component duration interfaces have been replaced by more straightforward read-only component attributes.

* Added Ferneyhough Unsichbare Farben example.

.. image:: ../../examples/ferneyhough/images/ferneyhough-1.png



Abjad 1.1.1
-----------


*   More complete documentation.

*   The configuration file ``config`` changed to pure Python ``config.py``. 
    The file now supports more settings previously read as environment 
    variables. All user setings are now found in this file. 
    Users no longer need to set environment variables. 

*   Some new classes

    *   ``_HistoryInterface``. Use the _HistoryInterface to apply attributes to 
        any component in score that will be completely ignored by Abjad. 
        Think of the _HistoryInterface as a private user namespace.
    *   ``_NoteColumnInterface`` to handle the LilyPond NoteColumn grob. 
    *   ``_SpanBarInterface``. See API for details.
    *   ``InvisibleStaff()`` staff.
    *   ``Moment`` utility class to model the Abjad representation of the LilyPond moment.

*   New Spanners

    *   ``TempoProportional`` spanner.

*   More than a dozen new tools added. 


Abjad 1.1.0
-----------

*   Many structure transform tools added. See the `abjad.tools.*`
    in the :doc:`Abjad API </chapters/api/index>` package.

*   Construction, transformation, manipulation and all other tools
    now grouped cleanly into packages.

*   New ``abjad-book`` application available. 
    Use ``abjad-book`` to interpret Abjad code blocks embedded in 
    HTML, LaTex and reST documents. 



Abjad 1.0.1055
----------------

Changes to the public interface:

*   Abjad now models ties exclusively with the Tie spanner. 
    The old ``_TieInterface._set`` attribute is now deprecated.

*   You can no longer say ``t.tie = True`` or ``t.tie = False``, 
    for leaf ``t``. You must structurally span ``t`` as ``Tie(t)`` 
    instead.

*   New public properties in ``_SpannerReceptor``: ``chain, parented, count``.

*   New public helpers: 

    *  ``construct.notes_curve()``
    *  ``durationtools.rationalize()``
    *  ``iterate.tie_chains()``
    *  ``list_helpers()``
    *  ``mathtools.interpolate_divide()``
    *  ``measuretools.concentrate()``
    *  ``measuretools.scale_and_remeter()``
    *  ``measuretools.spin()`` 
    *  ``play()``

*   Grace note ``append()`` and ``extend()`` no longer throw errors.


Abjad 1.0.1022
----------------

*   First public release of Abjad.
