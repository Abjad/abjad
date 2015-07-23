:orphan:

Abjad 2.8
---------

Released 2012-04-16. Built from r5421.
Implements 306 public classes and 1037 functions totalling 178,000 lines of code.

Many documentation improvements appear in this release.

- A source link now accompanies all classes and functions in the API:

  .. image:: images/arpeggiate-chord-source-listing.png

- All parts of the Abjad codebase are now viewable through
  the HTML version of the API.

- Inheritance diagrams now accompany all classes:

  .. image:: images/multimeasure-rest-inheritance-graph.png

- Inherited attributes now appear in the API entry of each class.

- Added new ``documentationtools`` package::

    documentationtools.APICrawler
    documentationtools.AbjadAPIGenerator
    documentationtools.ClassCrawler
    documentationtools.ClassDocumenter
    documentationtools.Documenter
    documentationtools.FunctionCrawler
    documentationtools.FunctionDocumenter
    documentationtools.InheritanceGraph
    documentationtools.ModuleCrawler
    documentationtools.Pipe

  The package houses custom code to build Abjad documentation.

Added the new ``constrainttools`` API. 

- This release of the ``constrainttools`` package implements the following classes::

    constrainttools.AbsoluteIndexConstraint
    constrainttools.Domain
    constrainttools.FixedLengthStreamSolver
    constrainttools.GlobalConstraint
    constrainttools.GlobalCountsConstraint
    constrainttools.GlobalReferenceConstraint
    constrainttools.RelativeCountsConstraint
    constrainttools.RelativeIndexConstraint
    constrainttools.VariableLengthStreamSolver

- Example::

    >>> from abjad.tools.constraintstools import *

  ::

    >>> domain = Domain([1, 2, 3, 4], 4)

  ::

    >>> all_unique = GlobalCountsConstraint(lambda x: all([y == 1 for y in x.values()]))
    >>> max_interval = RelativeIndexConstraint([0, 1], lambda x, y: abs(x - y) < 3)
    >>> solver = FiniteStreamSolver(domain, [all_unique, max_interval])

  ::

    >>> for solution in solver: print solution
    ... 
    (1, 2, 3, 4)
    (1, 2, 4, 3)
    (1, 3, 2, 4)
    (1, 3, 4, 2)
    (2, 1, 3, 4)
    (2, 4, 3, 1)
    (3, 1, 2, 4)
    (3, 4, 2, 1)
    (4, 2, 1, 3)
    (4, 2, 3, 1)
    (4, 3, 1, 2)
    (4, 3, 2, 1)

- The ``constrainttools`` package is considered unstable and will be subject
  to changes in the next releases of Abjad.

Added octave-transposition mapping model.

- This version of the system contains the following classes::

    pitchtools.Registration
    pitchtools.RegistrationComponent
    pitchtools.RegistrationInventory

- Octave-transposition mappings specify a way to maybe pitches 
  from one registral space to another.

- Use octave-transposition mappings
  as input to ``pitchtools.transpose_chromatic_pitch_number_ty_octave_transposition_mapping()``.

Many Abjad classes are now implemented as abstract base classes.

- Abstract base classes provide functionality to child subclasses.

- Abstract base classes can not be instantiated directly.

- The Abjad API now lists abstract classes and concrete classes separately.

- See http://docs.python.org/library/abc.html for a description of ABCs in Python.

Added the new ``abctools`` package to house abstract classes that are core to the Abjad object model.

- This version of the package contains the following classes::

    abctools.AbjadObject
    abctools.AttributeEqualityAbjadObject
    abctools.ImmutableAbjadObject
    abctools.SortableAttributeEqualityAbjadObject

- All Abjad classes now inherit from ``AbjadObject``.

Added object inventories for several classes.

- This release contains inventories for the following classes::

    indicatortools.ClefInventory
    indicatortools.TempoInventory
    instrumenttools.InstrumentInventory
    markuptools.MarkupInventory
    pitchtools.RegistrationInventory
    pitchtools.PitchRangeInventory
    scoretools.PerformerInventory

- Object inventories model ordered collections of system objects.

Add the new ``datastructuretools`` package.

- This version of the package includes the following classes::

    datastructuretools.Digraph
    datastructuretools.ImmutableDictionary
    datastructuretools.TypedList

- Use ``datastructuretools.Digraph`` to detect cycles in any collection of hashable objects::

    >>> from abjad.tools.datastructuretools import Digraph

  ::

    >>> edges = [('a', 'b'), ('a', 'c'), ('a', 'f'), ('c', 'd'), ('d', 'e'), ('e', 'c')]
    >>> digraph = Digraph(edges)
    >>> digraph
    Digraph(edges=[('a', 'c'), ('a', 'b'), ('a', 'f'), ('c', 'd'), ('d', 'e'), ('e', 'c')])

  ::

    >>> digraph.root_nodes
    ('a',)
    >>> digraph.terminal_nodes
    ('b', 'f')
    >>> digraph.cyclic_nodes
    ('c', 'd', 'e')
    >>> digraph.is_cyclic
    True

- Use ``datastructuretools.TypedList`` as the base class for an ordered collection
  of system objects.

- Object inventories inherit from ``list`` and are mutable.

- Object inventories extend ``append()``, ``extend()`` and ``__contains__()`` to allow
  token input.

Added new ``wellformednesstools`` package.

- This version of the package implements the following classes::

    wellformednesstools.BeamedQuarterNoteCheck
    wellformednesstools.DiscontiguousSpannerCheck
    wellformednesstools.DuplicateIdCheck
    wellformednesstools.EmptyContainerCheck
    wellformednesstools.IntermarkedHairpinCheck
    wellformednesstools.MisduratedMeasureCheck
    wellformednesstools.MisfilledMeasureCheck
    wellformednesstools.MispitchedTieCheck
    wellformednesstools.MisrepresentedFlagCheck
    wellformednesstools.MissingParentCheck
    wellformednesstools.NestedMeasureCheck
    wellformednesstools.OverlappingBeamCheck
    wellformednesstools.OverlappingGlissandoCheck
    wellformednesstools.OverlappingOctavationCheck
    wellformednesstools.ShortHairpinCheck

- The classes check different aspects of score well-formedness.

- To call these classes use ``wellformednesstools.is_well_formed_component()``
  or ``wellformednesstools.tabulate_well_formedness_violations_in_expr()``.

Added new ``decoratortools`` package.

- This version of the package contains only the ``requires`` decorator.

- The ``requires`` decorator will be used in later versions of Abjad
  to specify the input and output types of functions explicitly.

- This will help in the construction of function- and class-population tools.

Added new ``templatetools`` package.

- This version of the package implements the following classes::

    templatetools.StringQuartetScoreTemplate
    templatetools.TwoStaffPianoScoreTemplate

- Example::

    >>> from abjad.tools import templatetools

  ::

    >>> template = templatetools.StringQuartetScoreTemplate()
    >>> score = template()

  ::

    >>> score
    Score-"String Quartet Score"<<1>>

  ::

    >>> f(score)
    \context Score = "String Quartet Score" <<
        \context StaffGroup = "String Quartet Staff Group" <<
            \context Staff = "First Violin Staff" {
                \clef "treble"
                \context Voice = "First Violin Voice" {
                }
            }
            \context Staff = "Second Violin Voice" {
                \clef "treble"
            }
            \context Staff = "Viola Staff" {
                \clef "alto"
            }
            \context Staff = "Cello Staff" {
                \clef "bass"
            }
        >>
    >>

- Class usage follows a two-step initialize-then-call pattern.

Added new ``rhythmtreetools`` package for parsing IRCAM-like RTM syntax.

- This version of the package implements the following function::

    rhythmtreetools.parse_rtm_syntax.parse_rtm_syntax()

- Example::

    >>> from abjad.tools.rhythmtreetools import parse_rtm_syntax

  ::

    >>> rtm = '(1 (1 (1 (1 1)) 1))'
    >>> result = parse_rtm_syntax(rtm)
    >>> result
    FixedDurationTuplet(1/4, [c'8, c'16, c'16, c'8])

- Use the ``rhythmtreetools`` package to turn nested lists of numbers into Abjad tuplets.

Added new ``rhythmmakertools`` package.

- This version of the package contains the following concrete classes::

    rhythmmakertools.NoteRhythmMaker
    rhythmmakertools.OutputBurnishedTaleaRhythmMaker
    rhythmmakertools.OutputIncisedNoteRhythmMaker
    rhythmmakertools.OutputIncisedRestRhythmMaker
    rhythmmakertools.RestRhythmMaker
    rhythmmakertools.TaleaRhythmMaker
    rhythmmakertools.DivisionBurnishedTaleaRhythmMaker
    rhythmmakertools.DivisionIncisedNoteRhythmMaker
    rhythmmakertools.DivisionIncisedRestRhythmMaker

- The ``rhythmmakertools`` package implements a family of related rhythm-making classes.

- Class usage follows a two-step initialize-then-call pattern.

Added new classes to ``instrumenttools``.

- Added human voice classes::

    instrumenttools.BaritoneVoice
    instrumenttools.BassVoice
    instrumenttools.AltoVoice
    instrumenttools.MezzoSopranoVoice
    instrumenttools.SopranoVoice
    instrumenttools.TenorVoice

Added new time-interval tree functionality:

- Extended ``TimeIntervalTree`` with the following public methods::

    scale_by_rational()
    scale_to_rational()
    shift_by_rational()
    shift_to_rational()
    split_at_rationals()

- These methods allow time-interval trees to behave
  more similary to time-intervals.

All score components are now public.

- The following classes are now publically available for the first time::

    scoretools.Component
    scoretools.Context
    scoretools.Leaf

Further new functionality:

- Added the ``indicatortools.BendAfter`` class to model LilyPond's ``\bendAfter command``::

    >>> n = Note(0, 1)
    >>> indicatortools.BendAfter(8)(n)
    BendAfter(8.0)(c'1)
    >>> f(n)
    c'1 - \bendAfter #'8.0

- Added public ``pair`` property to ``indicatortools.TimeSignature``::

    >>> time_signature = indicatortools.TimeSignature((3, 16))
    >>> time_signature.pair
    (3, 16)

- Added ``_is_hairpin_token()`` to ``spannertools.Hairpin`` class.

  Hairpin tokens are triples of the form ``(x, y, z)`` with dynamic tokens ``x``, ``y``
  and hairpin shape string ``z``. For example ``('p', '<', 'f')``.

- Added ``scoretools.replace_leaves_in_expr_with_rests()``.

- Added ``scoretools.replace_leaves_in_expr_with_parallel_voices()``.

- Added ``scoretools.replace_leaves_in_expr_with_named_parallel_voices()``.

  Use the functions listed above to replace leaves in an expression with parallel
  voices containing copies of those leaves in both voices. This is useful for
  generating stemmed-glissandi structures.

- Added ``indicatortools.list_clef_names()``::

    >>> indicatortools.list_clef_names()
    ['alto', 'baritone', 'bass', 'mezzosoprano', 'percussion', 'soprano', 'treble']

- Added ``find-slots-implementation-inconsistencies`` development script.

Changes to end-user functionality:

- Changed ``intervaltreetools`` to ``timeintervaltools``.

- Changed ``scoretools.Context.context`` to ``scoretools.Context.context_name``.

- Calling ``bool(Container())`` on empty containers now returns false.
  The previous behavior of the system was to return true.
  The new behavior better conforms to the Python iterable interface.

- Moved ``abjad/docs/scr/make-abjad-api`` to ``abjad/scr/make-abjad-api``.
