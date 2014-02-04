:orphan:

Abjad 2.9
---------

Released 2012-06-05. Built from r5795.
Implements 405 public classes and 1066 functions totalling 182,000 lines of code.

Extended markup handling is now available.

- The LilyPond parser accepts complex markup as input::

    >>> f(p(r'''{ c'4 _ \markup { \put-adjacent #1 #-1 \bold \fontsize #2 \upright foo bar } }'''))
    {
        c'4
            _ \markup {
                \put-adjacent
                    #1
                    #-1
                    \bold
                        \fontsize
                            #2
                            \upright
                                foo
                    bar
                }
    }


- Format routines allow for markup indentation::

    >>> circle = markuptools.MarkupCommand('draw-circle', 2.5, 0.1, False)
    >>> square = markuptools.MarkupCommand('rounded-box', 'hello?')
    >>> line = markuptools.MarkupCommand('line', [square, 'wow!'])
    >>> markup = markuptools.Markup(('X', square, 'Y', line, 'Z'), direction='up')

  ::

    >>> print '\n'.join(markup._get_format_pieces(is_indented=True))
    ^ \markup {
        X
        \rounded-box
            hello?
        Y
        \line
            {
                \rounded-box
                    hello?
                wow!
            }
        Z
        }

- Nontrivial markup format with indentation automatically::

    >>> staff = Staff("c")
    >>> m1 = markuptools.Markup('foo')(staff[0])
    >>> m2 = markuptools.Markup('bar')(staff[0])
    >>> m3 = markuptools.Markup('baz', 'up')(staff[0])
    >>> m4 = markuptools.Markup('quux', 'down')(staff[0])
    >>> accent = indicatortools.Articulation('accent')(staff[0])

  ::

    >>> f(staff)
    \new Staff {
        c4 -\accent
            ^ \markup { baz }
            _ \markup { quux }
            - \markup {
                \column
                    {
                        foo
                        bar
                    }
                }
    }

- ``Markup.contents`` is now a tuple of strings or ``MarkupCommand`` instances. 

- Removed the markup ``style_string`` property.
  Use ``schemetools`` classes for constructing Scheme-style formatting.

- Changed ``Markup.contents_string`` to ``Markup.contents``.


An entirely new tuplet microlanguage is now available.

- This "reduced ly" syntax uses braces to show tuplet nesting and represents rhythm without pitch::

    >>> from abjad.tools import rhythmtreetools

  ::

    >>> container = rhythmtreetools.parse_reduced_ly_syntax('4 -4 8 5/3 { 2/3 { 8 8 8 } { 8 8 } -8 } 4')

  ::

    >>> f(container)
    {
        c'4
        r4
        c'8
        \fraction \times 5/3 {
            \times 2/3 {
                c'8
                c'8
                c'8
            }
            {
                c'8
                c'8
            }
            r8
        }
        c'4
    }

- Measures and dotted values are also available::

    >>> container = rhythmtreetools.parse_reduced_ly_syntax('|2/4 8. 16 8. 16| |4/4 2/3 { 2 2 2 }|')

  ::

    f(container)

  ::

    {
        {
            \time 2/4
            c'8.
            c'16
            c'8.
            c'16
        }
        {
            \time 4/4
            \times 2/3 {
                c'2
                c'2
                c'2
            }
        }
    }


Extended container input syntax.

- You can now pass strings directly to the ``append()`` and ``extend()`` methods of any container::

    >>> container = Container()
    >>> container
    {}

  ::

    >>> container.extend('a b c')
    >>> container
    {a4, b4, c4}

  ::

    >>> container.append('d')
    >>> container
    {a4, b4, c4, d4}


- You can assign a string to any container item:: 

    >>> container = Container("c' d' e'")
    >>> container
    {c'4, d'4, e'4}

  ::

    >>> container[1] = 'r'
    >>> container
    {c'4, r4, e'4}

- You can assign a string to any container slice::

    >>> container = Container("c' d' e'")
    >>> container
    {c'4, d'4, e'4}

  ::

    >>> container[:2] = 'r8 r r'
    >>> container
    {r8, r8, r8, e'4}

- You can initialize containers from strings using alternate parsers.

  Use the ``'abj'`` prefix to initialize a container with the new reduced ly syntax::

    >>> staff = Staff('abj: | 2/4 2/3 { 8 4 } 8 8 || 3/4 4 4 4 |')

  ::

    >>> f(staff)
    \new Staff {
        {
            \time 2/4
            \times 2/3 {
                c'8
                c'4
            }
            c'8
            c'8
        }
        {
            \time 3/4
            c'4
            c'4
            c'4
        }
    }

- Use the ``'rtm'`` prefix to initialize a container with IRCAM RTM-style syntax::

    >>> staff = Staff('rtm: (1 (1 (2 (1 1 1)) 1)) (1 (1 1))')

  ::

    >>> f(staff)
    \new Staff {
        c'16
        \times 2/3 {
            c'16
            c'16
            c'16
        }
        c'16
        c'8
        c'8
    }

- Parallel contexts, such as Score, can be instantiated from strings which parse
  to a sequence of contexts::

    Score(r'''\new Staff { c' } \new Staff = { c, }''')

- Added a new ``FixedDurationContainer`` class to the ``scoretools`` package.

  Fixed-duration containers extend container behavior with format-time
  checking against a user-specified target duration::

    >>> container = scoretools.FixedDurationContainer((3, 8), "c'8 d'8 e'8")

  ::

    >>> container
    FixedDurationContainer(Duration(3, 8), [Note("c'8"), Note("d'8"), Note("e'8")])

  ::

    >>> f(container)
    {
        c'8
        d'8
        e'8
    }

  ::

    >>> container.is_misfilled
    False

  ::

    >>> container.pop()
    Note("e'8")

  ::

    >>> container
    FixedDurationContainer(Duration(3, 8), [Note("c'8"), Note("d'8")])

  ::

    >>> container.is_misfilled
    True

  Misfilled fixed-duration containers will raise an exception at format-time.
  Fixed-duration containers share this behavior with measures.


Regularized measure modification behavior.

- By default measures do not automatically adjust time signature after contents modification:: 

    >>> measure = Measure((3, 4), "c' d' e'")
    >>> measure
    Measure(3/4, [c'4, d'4, e'4])

  ::

    >>> measure.append('r')
    >>> measure
    Measure(3/4, [c'4, d'4, e'4, r4])

  ::

    >>> measure.is_overfull
    True

- But it is now possible to cause measures to automatically adjust time signature after
  contents modification::

    >>> measure = Measure((3, 4), "c' d' e'")
    >>> measure.automatically_adjust_time_signature = True
    >>> measure
    Measure(3/4, [c'4, d'4, e'4])

  ::

    >>> measure.append('r')
    >>> measure
    Measure(4/4, [c'4, d'4, e'4, r4])

  ::

    >>> measure.is_misfilled
    False

  Previous implementations of measure ``append()``, ``extend()`` and set-item
  never adjusted measure time signatures.

  Now the behavior of such operations is controllable on a measure-by-measure basis by the end user.


New functionality is available for working with ties.

- Added a ``LogicalTie`` class to the ``tietools`` package.
  Tie chains now return as a custom ``LogicalTie`` object instead of tuple:: 

    >>> staff = Staff("c' d' e' ~ e'")

  ::

    >>> tietools.get_logical_tie(staff[2])
    LogicalTie((Note("e'4"), Note("e'4")))


  Reimplemented logical tie duration attributes as explicit class attributes.
  The following four functions have been removed::

    tietools.get_preprolated_logical_tie_duration()
    tietools.get_prolated_logical_tie_duration()
    tietools.get_logical_tie_duration_in_seconds()
    tietools.get_written_logical_tie_duration()

  Use these read-only properties instead::

    LogicalTie.preprolated_duration
    LogicalTie.prolated_duration
    LogicalTie.get_duration(in_seconds=True)
    LogicalTie.written_duration

  The ``LogicalTie`` class inherits from the new ``SliceSelection`` abstract base class.

  Added new ``tietools`` functions:: 

    tietools.iterate_pitched_logical_ties_forward_in_expr()
    tietools.iterate_pitched_logical_ties_backward_in_expr()
    tietools.iterate_nontrivial_logical_ties_forward_in_expr()
    tietools.iterate_nontrivial_logical_ties_backward_in_expr()

  Removed ``tietools.is_logical_tie(expr)``.  Use ``isinstance(expr, selectiontools.LogicalTie)`` instead.

  Removed ``tietools.get_leaves_in_logical_tie()``. Use ``LogicalTie.leaves`` instead.

  Removed ``tietools.group_leaves_in_logical_tie_by_immediate_parents()``.
  Use ``LogicalTie.leaves_grouped_by_immediate_parents instead``.

  Removed ``tietools.is_logical_tie_with_all_leaves_in_same_parent()``.
  Use ``LogicalTie.all_leaves_are_in_same_parent`` instead.


Added a new ``stringtools`` package.

- The following functions all migrated from the ``systemtools`` package::

    stringtools.capitalize_string_start()
    stringtools.format_input_lines_as_doc_string()
    stringtools.format_input_lines_as_regression_test()
    stringtools.is_lower_camel_case_string()
    stringtools.is_space_delimited_lowercase_string()
    stringtools.is_snake_case_file_name()
    stringtools.is_snake_case_file_name_with_extension()
    stringtools.is_snake_case_package_name()
    stringtools.is_snake_case_string()
    stringtools.is_upper_camel_case_string()
    stringtools.space_delimited_lowercase_to_upper_camel_case()
    stringtools.string_to_accent_free_snake_case()
    stringtools.strip_diacritics_from_binary_string()
    stringtools.snake_case_to_lower_camel_case()
    stringtools.snake_case_to_upper_camel_case()
    stringtools.upper_camel_case_to_space_delimited_lowercase()
    stringtools.upper_camel_case_to_snake_case()

  The package also contains these new functions::

    stringtools.arg_to_bidirectional_direction_string()
    stringtools.arg_to_bidirectional_lilypond_symbol()
    stringtools.arg_to_tridirectional_direction_string()
    stringtools.arg_to_tridirectional_lilypond_symbol()

  ::

    >>> stringtools.arg_to_bidirectional_lilypond_symbol(1)
    '^'
    >>> stringtools.arg_to_tridirectional_direction_string('-')
    'neutral'


Added a new ``beamtools`` package.

- This release of the ``beamtools`` package contains the following classes and functions::

    spannertools.Beam
    spannertools.ComplexBeam
    spannertools.DuratedComplexBeam
    spannertools.MultipartBeam

  ::

    beamtools._is_beamable_component
    beamtools.apply_beam_spanner_to_measure
    beamtools.attach_beam_spanners_to_measures_in_expr
    beamtools.apply_complex_beam_spanner_to_measure
    beamtools.attach_complex_beam_spanners_to_measures_in_expr
    beamtools.attach_durated_complex_beam_spanner_to_measures
    beamtools.beam_bottommost_tuplets_in_expr
    beamtools.get_beam_spanner_attached_to_component
    beamtools._is_beamable_component
    beamtools.is_component_with_beam_spanner_attached

  Note that the following two functions have been removed::

    beamtools.apply_beam_spanner_to_measure()
    beamtools.apply_complex_beam_spanner_to_measure()

  Use these two functions instead::
    
    beamtools.attach_beam_spanners_to_measures_in_expr()
    beamtools.attach_complex_beam_spanners_to_measures_in_expr()


New ``constrainttools`` functionality is now available.

- Extended the ``VariableLengthStreamSolver`` class.

  The class now produces more randomly
  ordered solution sets than before, when in randomized mode.  Note that the
  solution sets tend to increase in size.
  Also note that there is an increased performance hit for such PMC-style
  randomized constraint solving::

    >>> from abjad.tools.constrainttools import *

  ::

    >>> domain = Domain([1, 2, 3, 4], 1)
    >>> boundary_sum = GlobalConstraint(lambda x: sum(x) < 6)
    >>> target_sum = GlobalConstraint(lambda x: sum(x) == 5)
    >>> random_solver = VariableLengthStreamSolver(domain,
    ... [boundary_sum], [target_sum], randomized=True)
    >>> for x in random_solver: x
    ... 
    [1, 3, 1]
    [4, 1]
    [3, 2]
    [2, 3]
    [1, 4]
    [3, 1, 1]
    [2, 1, 2]
    [1, 2, 1, 1]
    [2, 1, 1, 1]
    [2, 2, 1]
    [1, 1, 1, 2]
    [1, 2, 2]
    [1, 1, 1, 1, 1]
    [1, 1, 3]
    [1, 1, 2, 1]

- Randomized the ``FixedLengthStreamSolvers`` class.

  The class now produces truly randomly ordered solution sets.


New sequence tools are available.

- Added new type- and form-checking predicates to the ``sequencetools`` package:: 

    mathtools.all_are_integer_equivalent_exprs
    mathtools.is_null_tuple(expr)
    mathtools.is_singleton(expr)
    mathtools.is_pair(expr)
    mathtools.is_n_tuple(expr, n)
    mathtools.is_integer_singleton(expr)
    mathtools.is_integer_pair(expr)
    mathtools.is_integer_n_tuple(expr, n)
    mathtools.is_integer_equivalent_n_tuple
    mathtools.is_integer_equivalent_pair
    mathtools.is_integer_equivalent_singleton
    mathtools.is_fraction_equivalent_pair
 
  Each function returns a boolean::

    >>> mathtools.is_integer_singleton((19,))
    True

- Added a new ``NonreducedFraction`` class to the ``sequencetools`` package::

    >>> sequencetools.NonreducedFraction(3, 6)
    NonreducedFraction(3, 6)

  Like built-in fraction but numerator and denominator do NOT simplify.

  All six comparators are implemented on nonreduced fractions.

  Addition and subtraction are implemented on nonreduced fractions::

    >>> sequencetools.NonreducedFraction(3, 6) + sequencetools.NonreducedFraction(3, 6)
    NonreducedFraction(6, 6)

  Use nonreduced fractions to model arithmetic operations on time signature-like objects
  absent any of the special time signature features like partial-measure pick-ups.


New spanners and spanner handlers are now available.

- Added a ``ComplexGlissandoSpanner`` to the ``spannertools`` package.

  This spanner generates a glissando which skips over rests.  It can be used
  in combination with spannertools.Beam and an override of the Stem grob
  to generate the appearance of durated glissandi::

    >>> staff = Staff("c'16 [ d' r e' r r r g' ]")

  ::

    >>> f(staff)
    \new Staff {
        c'16 [
        d'16
        r16
        e'16
        r16
        r16
        r16
        g'16 ]
    }

    >>> spannertools.ComplexGlissandoSpanner(staff[:])
    ComplexGlissandoSpanner(c'16, d'16, r16, e'16, r16, r16, r16, g'16)

  ::

    >>> staff.override.stem.stemlet_length = 2
    >>> f(staff)
    \new Staff \with {
        \override Stem #'stemlet-length = #2
    } {
        c'16 [ \glissando
        d'16 \glissando
        \once \override NoteColumn #'glissando-skip = ##t
        \once \override Rest #'transparent = ##t
        r16
        e'16 \glissando
        \once \override NoteColumn #'glissando-skip = ##t
        \once \override Rest #'transparent = ##t
        r16
        \once \override NoteColumn #'glissando-skip = ##t
        \once \override Rest #'transparent = ##t
        r16
        \once \override NoteColumn #'glissando-skip = ##t
        \once \override Rest #'transparent = ##t
        r16
        g'16 ]
    }

- Added new ``spannertools`` function::

    spannertools.destory_spanners_attached_to_components_in_expr(expr, klass=None)

  The function can be useful for removing all spanners when debugging a complex expression.

- Spanners are now callable::

    >>> staff = Staff("c'8 d'8 e'8 f'8")

  ::

    >>> beam = spannertools.Beam()
    >>> beam(staff[:])
    Staff{4}

  ::

    >>> f(staff)
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }

  This works the same way as marks::

    >>> indicatortools.Articulation('.')(staff[1])
    Articulation('.')(d'8)

  ::

    >>> f(staff)
    \new Staff {
        c'8 [
        d'8 -\staccato
        e'8
        f'8 ]
    }

  Callable spanners are provided as an experimental way of unifying
  the attachment syntax of spanners and marks.


Many new functions are available in the ``scoretools`` package.

- New getters::

    scoretools.get_proper_contents_of_component()
    scoretools.get_improper_contents_of_component()
    scoretools.get_improper_contents_of_component_that_start_with_component()
    scoretools.get_improper_contents_of_component_that_stop_with_component()
    scoretools.get_proper_descendants_of_component()
    scoretools.get_improper_descendants_of_component()
    scoretools.get_improper_descendents_of_component_that_cross_prolated_offset
    scoretools.get_improper_descendants_of_component_that_start_with_component
    scoretools.get_improper_descendants_of_component_that_stop_with_component
    scoretools.get_lineage_of_component()
    scoretools.get_lineage_of_component_that_start_with_component()
    scoretools.get_lineage_of_component_that_stop_with_component()
    scoretools.get_nth_sibling_from_component(component, n)
    scoretools.get_nth_component_from_component_in_time_order(component, n)
    scoretools.get_nth_namesake_from_component
    scoretools.get_most_distant_sequential_container_in_improper_parentage_of_component()

  Use these functions to interrogate the structural relations of components resident
  inside arbitrarily complex pieces of score.

  The functions are useful as primitive methods when implementing more complex
  operations designed to mutate the score tree.

- Note the difference between the 'contents' of a component and the 'descendents' of a component::

    >>> scoretools.get_proper_contents_of_component(staff)
    [Note("c'4"), Tuplet(2/3, [d'8, e'8, f'8])]

  Versus::

    >>> scoretools.get_proper_descendants_of_component(staff)
    [Note("c'4"), Tuplet(2/3, [d'8, e'8, f'8]), Note("d'8"), Note("e'8"), Note("f'8")]

- Also add the following ``scoretools`` predicate::

    scoretools.is_immediate_temporal_successor_of_component()


Further new functionality:

- Added new ``gracetools`` function::

    gracetools.detach_grace_containers_attached_to_leaves_in_expr()

  Use the function to strip all grace containers from an arbitrary piece of score.

- Added new ``indicatortools`` functions::

    indicatortools.get_marks_attached_to_components_in_expr()
    indicatortools.detach_marks_attached_to_components_in_expr()
    indicatortools.move_marks(donor, recipient).

- Added new ``pitchtools`` function::

    pitchtools.set_written_pitch_of_pitched_components_in_expr(expr, written_pitch=0)

  Use the function to neutralize pitch information in an arbitrary piece of score.

- Added new ``scoretools`` functions::

   scoretools.change_fixed_duration_tuplets_in_expr_to_tuplets()
   scoretools.change_tuplets_in_expr_to_fixed_duration_tuplets()

- Extended ``lilypondfiletools.ContextBlock`` with the following attributes::

    ContextBlock.consists_commands
    ContextBlock.remove_commands
    ContextBlock.context_name
    ContextBlock.name
    ContextBlock.type

  The attributes correspond to backslash-initiated LilyPond commands available in LilyPond context blocks.

- Updated ``LilyPondLanguageToken`` to format LilyPond ``\language`` command 
  instead of LilyPond ``\include`` command.

- Extended ``Duration`` to initialize from LilyPond duration strings::

    >>> Duration('8.')
    Duration(3, 16)

  Note that this means that ``Duration('2')`` now gives ``Duration(1, 2)``.
  Previously ``Duration('2')`` gave ``Duration(2, 1)`` just like ``Fraction('2')``.


Changes to end-user functionality:

- Changed::

    scoretools.copy_components_and_remove_all_spanners()

  ::

    scoretools.copy_components_and_detach_spanners()

- Changed::

    scoretools.get_improper_contents_of_component_that_cross_prolated_offset()

  ::

    scoretools.get_leftmost_components_with_total_duration_at_most()

- Changed::

    scoretools.list_improper_contents_of_component_that_cross_prolated_offset()

  ::

    scoretools.list_leftmost_components_with_prolated_duration_at_most()

- Changed::

    configurationtool.set_default_accidental_spelling()

  ::

    pitchtools.set_default_accidental_spelling()

- Changed::

    gracetools.Grace

  ::

    scoretools.GraceContainer

- Changed::

    spannertools.destory_all_spanners_attached_to_component()

  ::

    spannertools.destory_spanners_attached_to_component()

- Changed::

    spannertools.fracture_all_spanners_attached_to_component()

  ::

    spannertools.fracture_spanners_attached_to_component()

- Changed::

    spannertools.report_as_string_format_contributions_of_all_spanners_attached_to_component()

  ::

    spannertools.report_as_string_format_contributions_of_spanners_attached_to_component()

- Changed::

    spannertools.report_as_string_format_contributions_of_all_spanners_attached_to_improper_parentage_of_component()

  ::

    spannertools.report_as_string_format_contributions_of_spanners_attached_to_improper_parentage_of_component()

- Changed::

    tietools.get_logical_ties_in_expr()

  ::

    tietools.get_nontrivial_logical_ties_masked_by_components()

- Changed::

    tietools.remove_all_leaves_in_logical_tie_except_first()

  ::

    tietools.remove_nonfirst_leaves_in_logical_tie()

- Changed::

    scr/devel/rename-public-helper

  ::

    scr/devel/rename-public-function

- Removed the ``threadtools`` package and moved all functions to ``scoretools``.

  Instead of these::

    threadtools.iterate_thread_backward_from_component()
    threadtools.iterate_thread_backward_in_expr()
    threadtools.iterate_thread_forward_from_component()
    threadtools.iterate_thread_forward_in_expr()
    threadtools.component_to_thread_signature()

  Use these::

    scoretools.iterate_thread_backward_from_component()
    scoretools.iterate_thread_backward_in_expr()
    scoretools.iterate_thread_forward_from_component()
    scoretools.iterate_thread_forward_in_expr()
    scoretools.component_to_logical_voice()

- Removed the read-only ``Component.marks`` property entirely.

- Removed the top-level ``abjad/exceptions`` directory.
  Use the new ``exceptiontools`` package instead.

- Removed the top-level ``abjad/templates`` directory.

  Make sure to read the changes carefully.

  If you have been working with grace notes, for example, 
  you will need to change all occurrences of ``gracetools.Grace``
  to ``scoretools.GraceContainer``.
