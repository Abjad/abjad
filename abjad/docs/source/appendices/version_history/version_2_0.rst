:orphan:

Abjad 2.0
---------

Released 2011-08-17. Built from r4638.

Abjad 2.0 is the first public release of Abjad in more than two years. The new
release of the system more than doubles the number of classes, functions and
packages available in Abjad.

* The API has been cleaned up and completely reorganized. Features have been
  organized into a collection of 39 different libraries::

    cfgtools/          instrumenttools/   mathtools/         scoretools/         tempotools/
    scoretools/        intervaltreetools/ scoretools/      schemetools/       threadtools/
    scoretools/    systemtools/           metertools/        scoretools/        tietools/
    scoretools/    layouttools/       musicxmltools/     seqtools/          tonalanalysistools/
    indicatortools/      scoretools/         scoretools/         sievetools/        scoretools/
    durtools/          lilyfiletools/     pitcharraytools/   scoretools/         verticalitytools/
    gracetools/        indicatortools/         pitchtools/        spannertools/      scoretools/
    systemtools/       markuptools/       quantizationtools/ scoretools/

* The name of almost every function in the public API has been changed to
    better indication what the function does. While this has the effect of making
    Abjad 2.0 largely non-backwards compatible with code written in Abjad 1.x, the
    longer and much more explicit function names in Abjad 2.0 make code used to
    structure complex scores dramatically easier to maintain and understand.

* The ``indicatortools``, ``instrumenttools``, ``intervaltreetools``,
    ``lilyfiletools``, ``indicatortools``, ``pitcharraytools``,
    ``quantizationtools``, ``sievetools``, ``tonalanalysistools`` and
    ``verticalitytools`` packages are completely new.

* The classes implemented in the ``indicatortools`` and ``indicatortools``
    packages provide an object-oriented interfaces to clefs, time signatures, key
    signatures, articulations, tempos and other symbols stuck to the outside of the
    hierarchical score tree. The classes implemented in ``indicatortools`` and
    ``indicatortools`` model information outside the score tree much the way that
    the classes implemented in ``spannertools`` implement object-oriented
    interfaces to beams, brackets, hairpins, glissandi and other line-like symbols.

* The ``instrumenttools`` package provides an object-oriented model of most of
    the conventional instruments of the orchestra.

* The ``intervaltreetools`` package implements a custom way of working with
    chunks of score during composition.

* The ``lilyfiletools`` package implements an object-oriented interface to
    arbitrarily structured LilyPond input files.
