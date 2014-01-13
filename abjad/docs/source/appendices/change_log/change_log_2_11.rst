:orphan:

Changes from 2.10 to 2.11
-------------------------

Renamed ``timetokentools`` package. The new name is ``rhythmmakertools``.

Renamed all rhythm maker classes.
Replaced ``TimeTokenMaker`` with ``RhythmMaker`` everywhere.
Replaced ``Token`` with ``Division`` everywhere.

Renamed ``durationtools.yield_all_assignable_rationals()``.
The new name is ``durationtools.yield_all_assignable_durations()``.

Renamed ``durationtools.rewrite_rational_under_new_tempo()``.
The new name is ``durationtools.rewrite_duration_under_new_tempo()``.

Renamed ``durationtools.rewrite_duration_under_new_tempo()``.
The new name is ``tempotools.rewrite_duration_under_new_tempo()``.

Renamed ``tempotools.integer_tempo_to_tempo_multiplier_pairs()``.
The new name is ``tempotools.rewrite_integer_tempo()``.

Renamed ``tempotools.integer_tempo_to_tempo_multiplier_pairs_report()``.
The new name is ``tempotools.report_integer_tempo_rewrite_pairs()``.

Removed ``durationtools.numeric_seconds_to_escaped_clock_string()``.
Use ``durationtools.numeric_seconds_to_clock_string(escape_ticks=True)`` instead.

Removed ``durationtools.is_assignable_rational()``.
Use ``Duration.is_assignable`` property instead.

Removed ``durationtools.all_are_duration_tokens()``.
Just coerce durations instead.

Removed ``durationtools.duration_token_to_duration_pair()``.
Just initialize duration objects instead.

Removed ``durationtools.is_duration_token()``.
Just initialize duration objects instead.
Or use ``Duration.is_token()`` instead if true look-ahead is required.

Removed ``durationtools.yield_all_positive_rationals_uniquely()``.
Use ``durationtools.yield_all_positive_rationals(unique=True)`` instead.

Removed ``durationtools.assignable_rational_to_dot_count`` property.
Use ``Duration.dot_count`` instead.

Removed ``durationtools.assignable_rational_to_lilypond_duration_string`` property.
Use ``Duration.lilypond_duration_string`` instead.

Removed ``durationtools.is_duration_pair()``.
Just initialize duration objects instead.

Removed ``durationtools.is_binary_rational()``.
Use ``Duration.is_binary`` property instead.

Removed ``durationtools.is_proper_tuplet_multiplier()``.
Use ``Multiplier.is_proper_tuplet_multiplier`` property instead.

Removed ``durationtools.duration_token_to_rational()``.
Just initialize duration objects instead.

Removed ``durationtools.duration_tokens_to_rationals()``.
Just initialize duration objects instead.

emoved ``durationtools.lilypond_duration_string_to_rational()``.
Just initialize duration objects instead.

Removed ``durationtools.lilypond_duration_string_to_rational_list()``.
Function is no longer supported.

Removed ``durationtools.rational_to_flag_count()``.
Use the ``Duration.flag_count`` property instead.

Removed ``durationtools.rational_to_fraction_string()``.
Use ``str(Duration)`` instead.

Removed ``durationtools.rational_to_prolation_string()``.
Use the ``Duration.prolation_string`` property instead.

Renamed ``durationtools.rational_to_proper_fraction()``.
The new name is ``mathtools.fraction_to_proper_fraction()``.

Removed ``durationtools.rational_to_duration_pair_with_specified_integer_denominator()``.
Use ``NonreducedFraction.with_denominator()`` instead.

Removed ``durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator()``.
Use ``mathtools.NonreducedFraction.with_multiple_of_denominator()`` instead.

Removed ``durationtools.duration_pair_to_prolation_string()``.
Use the ``Duration.prolation_string`` property instead.

Renamed ``durationtools.group_duration_tokens_by_implied_prolation()``.
The new name is ``durationtools.group_nonreduced_fractions_by_implied_prolation()``.

Removed ``durationtools.multiply_duration_pair()``.
Use ``NonreducedFraction.multiply_without_reducing()`` instead.

Removed ``durationtools.multiply_duration_pair_and_reduce_factors()``.
Use ``NonreducedFraction.multiply_with_cross_cancelation()`` instead.

Removed ``durationtools.multiply_duration_pair_and_try_to_preserve_numerator()``.
Use ``NonreducedFraction.multiply_with_numerator_preservation()`` instead.

Removed ``durationtools.duration_token_to_assignable_duration_pairs()``.
Removed ``durationtools.duration_token_to_assignable_rationals()``.
Functions are no longer supported. Use ``scoretools.make_leaves()`` 
or ``scoretools.make_notes()`` instead.

Removed ``durationtools.duration_tokens_to_duration_pairs()``.
Function is no longer supported. Just initialize durations intead.

Removed ``durationtools.duration_tokens_to_least_common_denominator()``.
Function is no longer supported. Use ``mathtools.least_common_multiple()`` instead.

Renamed ``durationtools.duration_tokens_to_duration_pairs_with_least_common_denominator()``.
The new name is ``durationtools.durations_to_nonreduced_fractions()``.

Renamed ``durationtools.yield_all_assignable_durations()``.
The new name is ``durationtools.yield_assignable_durations()``.

Renamed ``durationtools.yield_all_positive_integer_pairs()``.
The new name is ``durationtools.yield_positive_nonreduced_fractions()``.

Renamed ``durationtools.yield_all_positive_rationals()``.
The new name is ``durationtools.yield_positive_fractions()``.

Renamed ``durationtools.yield_positive_fractions()``.
The new name is ``durationtools.yield_durations()``.
The function also now returns durations instead of fractions.

Renamed ``durationtools.yield_positive_nonreduced_fractions()``.
The new name is ``durationtools.yield_nonreduced_fractions()``.

Removed ``durationtools.yield_prolation_rewrite_pairs()``.
The functionality is no longer supported.

Renamed ``durationtools.yield_nonreduced_fractions()``.
The new name is ``mathtools.yield_nonreduced_fractions()``.

Renamed ``Duration.is_binary`` property.
The new name is ``Duration.has_power_of_two_denominator``.

Renamed ``Measure.is_binary`` property.
The new name is ``Measure.has_power_of_two_denominator``.

Renamed ``Tuplet.is_binary`` property.
The new name is ``Tuplet.has_power_of_two_denominator``.

Renamed ``Measure.is_nonbinary`` property.
The new name is ``Measure.has_non_power_of_two_denominator``.

Renamed ``Tuplet.is_nonbinary`` property.
The new name is ``Tuplet.has_non_power_of_two_denominator``.

Renamed ``DynamicMeasure.suppress_meter``.
The new name is ``DynamicMeasure.suppress_time_signature``.

Removed ``durationtools.integer_to_implied_prolation()``.
Use the ``Duration.implied_prolation`` property instead.

Removed unused scoretools.is_lilypond_rest_string()`` function.
Just instantiate rests instead.

Removed ``durationtools.is_lilypond_duration_string()``.
Removed ``durationtools.is_lilypond_duration_name()``.
Just instantiate durations instead.

Removed ``scoretools.component_to_score_root()``.
Use ``Component.parentage.root`` instead.

Removed ``scoretools.component_to_pitch_and_rhyhtm_skeleton()``.
Use the parser instead.

Removed ``scoretools.component_to_score_depth()``.
Use ``Component.parentage.depth`` property instead.

Removed unused ``scoretools.all_are_orphan_components()`` function.

Removed unused ``scoretools.all_are_components_in_same_parent()`` function.

Removed unused ``scoretools.all_are_components_in_same_score()`` function.

Removed unused ``scoretools.all_are_contiguous_components_in_same_score()`` function.

Renamed ``scoretools.make_leaves_from_note_value_signal()``.
The new name is ``scoretools.make_leaves_from_talea()``.

Removed ``TimeSignature.multiplier`` property.
Use ``TimeSignature.implied_prolation`` instead.

Removed ``Measure.multiplier`` property.
Use ``Measure.implied_prolation`` instead.

Deprecated ``metertools.time_signature_to_time_signature_with_power_of_two_denominator()`` function.
Use ``TimeSignature.with_power_of_two_denominator()`` method instead.

Remvoed ``metertools.time_signature_to_time_signature_with_power_of_two_denominator()`` function.
Use ``TimeSignature.with_power_of_two_denominator()`` method instead.

Moved one function from ``scoretools`` to ``scoretools``.
The function is ``get_likely_multiplier_components()``.

Moved one function from ``scoretools`` to ``formattools``.
The function is ``report_component_format_contributions()``.

Globally replaced rhythm maker ``pattern`` names to ``talea``.
The name change harmonizes with the new names fo the rhythm maker classes.

Removed ``big endian`` and ``little endian`` from codebase.
Use ``decrease_durations_monotonically=True`` keyword instead.

Removed the word ``duration_token`` from mainline.
The term is deprecated.
Use ``duration`` instead.

Deprecated the term ``pitch_token``.
Use ``pitch`` instead.

Removed ``pitchtools.named_pitch_tokens_to_named_pitches()``.
Just instantiate pitches instead.

Removed the term ``signal`` from the ``rhythmmakertools`` package.
Use ``talea`` instead. The plural of ``talea`` is ``taleas``.

Moved ``scoretools.component_to_tuplet_depth()``.
The function is now bound to parentage as the ``Component.parentage.tuplet_depth`` property.

Moved ``scoretools.component_to_score_index()``.
The function is now bound to parentage as the ``Component.parentage.score_index`` property.

Moved ``scoretools.component_to_logical_voice()``.
The function is now bound to parentage as the ``Component.parentage.logical_voice`` property.

Moved ``scoretools.component_to_parentage_signature()``.
The function is now bound to parentage as the ``Component.parentage.parentage_signature`` property.

Renamed ``scoretools.cut_component_by_at_prolated_duration()``.
The new name is ``scoretools.shorten_component_by_prolated_duration()``.

Renamed ``scoretools.get_leftmost_components_with_prolated_duration_at_most()``.
The new name is ``scoretools.get_leftmost_components_with_total_duration_at_most()``.

Renamed ``scoretools.shorten_component_by_prolated_duration()``.
The new name is ``scoretools.shorten_component_by_duration()``.

Renamed ``scoretools.sum_prolated_duration_of_components()``.
The new name is ``scoretools.sum_duration_of_components()``.

Renamed ``scoretools.yield_components_grouped_by_prolated_duration()``.
The new name is ``scoretools.yield_components_grouped_by_duration()``.

Renamed ``labeltools.label_leaves_in_expr_with_prolated_leaf_duration()``.
The new name is ``labeltools.label_leaves_in_expr_with_leaf_duration()``.

Renamed ``labeltools.label_logical_ties_in_expr_with_prolated_logical_tie_duration()``.
The new name is ``labeltools.label_logical_ties_in_expr_with_logical_tie_duration()``.

Renamed ``scoretools.fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang()``.
The new name is ``scoretools.fuse_tied_leaves_in_components_once_by_durations_without_overhang()``.

Renamed ``scoretools.get_leaf_in_expr_with_maximum_prolated_duration()``.
The new name is ``scoretools.get_leaf_in_expr_with_maximum_duration()``.

Renamed ``scoretools.get_leaf_in_expr_with_minimum_prolated_duration()``.
The new name is ``scoretools.get_leaf_in_expr_with_minimum_duration()``.

Rename ``scoretools.list_prolated_durations_of_leaves_in_expr()``.
The new name is ``scoretools.list_durations_of_leaves_in_expr()``.

Renamed ``VerticalMoment.prolated_offset`` to ``VerticalMoment.offset``.

Merged ``scoretools.extend_left_in_parent_of_component()`` into 
``scoretools.splice_of_component()``.
Use the ``left=True`` keyword.

Removed ``scoretools.extend_left_in_parent_of_component()``
Use ``scoretools.splice_of_component(left=True)`` instead.

Removed ``scoretools.get_component_start_offset()``.
Removed ``scoretools.get_component_stop_offset()``.
Use the ``Component.start_offset`` and ``Component.stop_offset`` properties instead.

Removed ``scoretools.get_component_start_offset_in_seconds()``.
Removed ``scoretools.get_component_stop_offset_in_seconds()``.
Use the ``Component.start_offset_in_seconds`` and ``Component.stop_offset_in_seconds`` properties instead.

Removed ``scoretools.is_orphan_component()``.
Use the new ``Component.parentage.is_orphan`` property instead.

Renamed ``scoretools.partition_components_by_durations_ge()``
The new name is ``scoretools.partition_components_by_durations_not_less_than()``

Renamed ``scoretools.partition_components_by_durations_le()``
The new name is ``scoretools.partition_components_by_durations_not_greater_than()``

emoved ``scoretools.sum_preprolated_duration_of_components()``
Use ``scoretools.sum_duration_of_components(preprolated=True)`` instead.

Removed ``scoretools.sum_duration_of_components_in_seconds()``.
Use ``scoretools.sum_duration_of_components(in_seconds=True)`` instead.

Changed ratio objects to reduce terms at initialization.

Changed ``diminution`` keyword to ``is_diminution`` in three functions::

    scoretools.leaf_to_tuplet_with_proportions()
    scoretools.leaf_to_tuplet_with_n_notes_of_equal_written_duration()
    tietools.logical_tie_to_tuplet_with_proportions()

Moved three functions from ``scoretools`` to ``wellformednesstools``.
The functions are these::

    is_well_formed_component()
    list_badly_formed_components_in_expr()
    tabulate_well_formedness_violations_in_expr()

Removed two ``scoretools`` functions.
Use ``timespantools`` instead.
The functions are these::

    scoretools.number_is_between_start_and_stop_offsets_of_component()
    scoretools.number_is_between_start_and_stop_offsets_of_component_in_seconds()

Renamed ``tied=True`` keyword in four functions::

    scoretools.make_leaves()
    scoretools.make_tied_leaf()
    scoretools.make_tied_rest()
    scoretools.make_rests()

Renamed the four ratio-related API functions::

    tietools.logical_tie_to_tuplet_with_proportions()
    scoretools.leaf_to_tuplet_with_proportions()
    scoretools.make_tuplet_from_duration_and_proportions()
    scoretools.make_tuplet_from_proportions_and_pair()

::

    tietools.logical_tie_to_tuplet_with_ratio()
    scoretools.leaf_to_tuplet_with_ratio()
    Tuplet.from_duration_and_ratio()
    scoretools.from_ratio_and_nonreduced_fraction()

Added four new public properties to ``Duration`` that replace functions::

    Duration.equal_or_greater_assignable
    Duration.equal_or_greater_power_of_two
    Duration.equal_or_lesser_assignable
    Duration.equal_or_lesser_power_of_two

::

    durationtools.rational_to_equal_or_greater_assignable_rational()
    durationtools.rational_to_equal_or_greater_binary_rational()
    durationtools.rational_to_equal_or_lesser_assignable_rational()
    durationtools.rational_to_equal_or_lesser_binary_rational()
