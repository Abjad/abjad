:orphan:

Abjad 2.10
----------

Released 2012-10-05. Built from r7615.
Implements 437 public classes and 982 functions totalling 179,000 lines of code.

The following packages now load by default when you start Abjad::

    Abjad 2.10
    >>> [x for x in dir() if x.endswith('tools')]
    ['abjadbooktools', 'beamtools', 'scoretools', 'scoretools', 'scoretools', 'indicatortools', 
    'developerscripttools', 'durationtools', 'formattools', 'gracetools', 'instrumenttools', 
    'introspectiontools', 'systemtools', 'iterationtools', 'labeltools', 'layouttools', 'scoretools', 
    'lilypondfiletools', 'indicatortools', 'markuptools', 'mathtools', 'scoretools', 'scoretools', '
    'systemtools', 'pitcharraytools', 'pitchtools', 'scoretools', 'rhythmtreetools', 'schemetools', 
    'templatetools', 'scoretools', 'sequencetools', 'sievetools', 'scoretools', 'spannertools', 
    'scoretools', 'stringtools', 'tempotools', 'tietools', 'timeintervaltools', 'metertools', 
    'rhythmmakertools', 'tonalanalysistools', 'scoretools', 'verticalitytools', 'scoretools']

Improved formatting engine.  Scores now format approximately 30% faster.

Improved LilyPond parser.

Markup objects now parse input string input on initialization::

    >>> markuptools.Markup(r'\bold \tiny { foo bar baz }')
    Markup((MarkupCommand('bold', MarkupCommand('tiny', ['foo', 'bar', 'baz'])),))
  
::

    >>> print _.indented_lilypond_format
    \markup {
        \bold
            \tiny
                {
                    foo
                    bar
                    baz
                }
        }

You can now use context names to reference named contexts attached to any container:: 

    >>> template = templatetools.StringQuartetScoreTemplate()
    >>> score = template()

::

    >>> score['First Violin Staff']
    Staff-"First Violin Staff"{1}

::

    >>> score['First Violin Voice']
    Voice-"First Violin Voice"{}


Five new constants are available globally. 

- The constants are ``Left``, ``Right``, ``Up``, ``Down`` and ``Center``.

- The constants function like Python's built-in ``True`` and ``False``.

- Use the constants as keyword defaults.

A new configuration tool is available::

    configurationtools.get_abjad_startup_string()

New context tools are available::

    indicatortools.all_are_contexts()

A new ``iterationtools`` package is available::

    iterationtools.iterate_chords_in_expr()
    iterationtools.iterate_components_and_grace_containers_in_expr()
    iterationtools.iterate_components_depth_first()
    iterationtools.iterate_components_in_expr()
    iterationtools.iterate_containers_in_expr()
    iterationtools.iterate_contexts_in_expr()
    iterationtools.iterate_leaf_pairs_in_expr()
    iterationtools.iterate_leaves_in_expr()
    iterationtools.iterate_measures_in_expr()
    iterationtools.iterate_namesakes_from_component()
    iterationtools.iterate_notes_and_chords_in_expr()
    iterationtools.iterate_notes_in_expr()
    iterationtools.iterate_rests_in_expr()
    iterationtools.iterate_scores_in_expr()
    iterationtools.iterate_semantic_voices_in_expr()
    iterationtools.iterate_skips_in_expr()
    iterationtools.iterate_staves_in_expr()
    iterationtools.iterate_logical_voice_from_component()
    iterationtools.iterate_logical_voice_in_expr()
    iterationtools.iterate_timeline_from_component()
    iterationtools.iterate_timeline_in_expr()
    iterationtools.iterate_tuplets_in_expr()
    iterationtools.iterate_voices_in_expr()

New LilyPond file tools are available::

    lilypondfiletools.make_floating_time_signature_lilypond_file()
    
New LilyPond parser tools are available::

    lilypondparsertools.GuileProxy
    lilypondparsertools.LilyPondDuration
    lilypondparsertools.LilyPondEvent
    lilypondparsertools.LilyPondFraction
    lilypondparsertools.LilyPondLexicalDefinition
    lilypondparsertools.LilyPondSyntacticalDefinition
    lilypondparsertools.ReducedLyParser
    lilypondparsertools.SchemeParser
    lilypondparsertools.SyntaxNode
    lilypondparsertools.lilypond_enharmonic_transpose()

A new ``Ratio`` class is available in the ``mathtools`` package::

    >>> mathtools.Ratio(1, 2, -1)
    Ratio(1, 2, -1)

New rhythm-tree tools are available.

- Implemented RTM expression parser::

    rhythmtreetools.RhythmTreeParser

- Implemented new classes for explicitly constructing rhythm-trees::

    RhythmTreeNode
    RhythmTreeLeaf
    RhythmTreeContainer

  ::

    >>> from abjad import *
    >>> rtm = '(1 (1 (2 (1 -1 1)) -2))'
    >>> result = rhythmtreetools.RhythmTreeParser()(rtm)

  ::

    >>> result[0]
    RhythmTreeContainer(
        children=(
            RhythmTreeLeaf(
                duration=1,
                pitched=True,
                ),
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=1,
                        pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=1,
                        pitched=False,
                        ),
                    RhythmTreeLeaf(
                        duration=1,
                        pitched=True,
                        ),
                ),
                duration=2
                ),
            RhythmTreeLeaf(
                duration=2,
                pitched=False,
                ),
        ),
        duration=1
        )

  ::

    >>> _.rtm_format
    '(1 (1 (2 (1 -1 1)) -2))'

  ::

    >>> result[0]((1, 4))
    FixedDurationTuplet(1/4, [c'16, {@ 3:2 c'16, r16, c'16 @}, r8])

  ::

    >>> f(_)
    \times 4/5 {
        c'16
        \times 2/3 {
            c'16
            r16
            c'16
        }
        r8
    }

New Scheme tools are available.

- Added ``force_quotes`` boolean keyword to ``schemetools.Scheme`` 
  and ``schemetools.format_scheme_value()``::

    >>> schemetools.format_scheme_value('foo')
    'foo'

  ::

    >>> schemetools.format_scheme_value('foo', force_quotes=True)
    '"foo"'

  This allows you to force double quotes around strings which contain no spaces.
  This is necessary for some LilyPond grob overrides.

- A new Scheme formatting function is available::

    schemetools.format_scheme_value()

New score-template tools are available::

    templatetools.GroupedStavesScoreTemplate

New sequence tools are available:

- Added ``sequencetools.merge_duration_sequences()``::

    >>> sequencetools.merge_duration_sequences([10, 10, 10], [7])
    [7, 3, 10, 10]

- Added ``sequencetools.pair_duration_sequence_elements_with_input_pair_values()``::

    >>> duration_sequence = [10, 10, 10, 10]
    >>> input_pairs = [('red', 1), ('orange', 18), ('yellow', 200)]
    >>> sequencetools.pair_duration_sequence_elements_with_input_pair_values(
    ... duration_sequence, input_pairs)
    [(10, 'red'), (10, 'orange'), (10, 'yellow'), (10, 'yellow')]

New tie tools are available::

    tietools.get_tie_spanner_attached_to_component()

New time-interval tools are available::

    timeintervaltools.make_voice_from_nonoverlapping_intervals()

New time-token tools are available:

- Added ``SkipRhythmMaker`` to ``rhythmmakertools`` package::

    >>> maker = rhythmmakertools.SkipRhythmMaker()

  ::

    >>> duration_tokens = [(1, 5), (1, 4), (1, 6), (7, 9)]
    >>> leaf_lists = maker(duration_tokens)
    >>> leaves = sequencetools.flatten_sequence(leaf_lists)

  ::

    >>> staff = Staff(leaves)

  ::

    >>> f(staff)
    \new Staff {
        s1 * 1/5
        s1 * 1/4
        s1 * 1/6
        s1 * 7/9
    }

- Added ``TupletMonadRhythmMaker`` to ``rhythmmakertools`` package::

    >>> maker = rhythmmakertools.TupletMonadRhythmMaker()

  ::

    >>> duration_tokens = [(1, 5), (1, 4), (1, 6), (7, 9)]
    >>> tuplets = maker(duration_tokens)
    >>> staff = Staff(tuplets)

  ::

    >>> f(staff)
    \new Staff {
        \times 4/5 {
            c'4
        }
        {
            c'4
        }
        \times 2/3 {
            c'4
        }
        \times 8/9 {
            c'2..
        }
    }
