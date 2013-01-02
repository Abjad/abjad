Change log
==========

Older Versions
--------------

.. toctree::
   :glob:
   :maxdepth: 1
   
   change_log_*

Changes from 2.10 to 2.11
-------------------------

Changed 'diminution' keyword to 'is_diminution' in three functions:

    * tuplettools.leaf_to_tuplet_with_proportions()
    * tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration()
    * tietools.tie_chain_to_tuplet_with_proportions()


Change ratio objects to reduce terms at initialization.

Old behavior::

    Ratio(2, 4, 2)

New behavior::

    >>> mathtools.Ratio(2, 4, 2)
    Ratio(1, 2, 1)

Renamed the four ratio-related API functions::

    tietools.tie_chain_to_tuplet_with_proportions()
    tuplettools.leaf_to_tuplet_with_proportions()
    tuplettools.make_tuplet_from_duration_and_proportions()
    tuplettools.make_tuplet_from_proportions_and_pair()

::

    tietools.tie_chain_to_tuplet_with_ratio()
    tuplettools.leaf_to_tuplet_with_ratio()
    tuplettools.make_tuplet_from_duration_and_ratio()
    tuplettools.make_tuplet_from_nonreduced_ratio_and_nonreduced_fraction()


Renamed ``timetokentools`` package. The new name is ``rhythmmakertools``.

Renamed all rhythm maker classes.

- Replaced 'TimeTokenMaker' with 'RhythmMaker' everywhere.

- Replaced 'Token' with 'Division' everywhere.


Renamed durationtools.yield_all_assignable_rationals().
The new name is durationtools.yield_all_assignable_durations().

Renamed durationtools.rewrite_rational_under_new_tempo().
The new name is durationtools.rewrite_duration_under_new_tempo().

Renamed durationtools.rewrite_duration_under_new_tempo().
The new name is tempotools.rewrite_duration_under_new_tempo().

Renamed tempotools.integer_tempo_to_tempo_multiplier_pairs().
The new name is tempotools.rewrite_integer_tempo().

Renamed tempotools.integer_tempo_to_tempo_multiplier_pairs_report().
The new name is tempotools.report_integer_tempo_rewrite_pairs().

Removed durationtools.numeric_seconds_to_escaped_clock_string().
Use durationtools.numeric_seconds_to_clock_string(escape_ticks=True) instead.

Removed durationtools.is_assignable_rational().
Use Duration.is_assignable property instead.

Removed durationtools.all_are_duration_tokens().
No need to use anymore. Just coerce durations instead.

Removed durationtools.duration_token_to_duration_pair().
No need to use anymore. Just initialize duration objects instead.

Removed durationtools.is_duration_token().
Just initialize duration objects instead.
Or use Duration.is_token() instead if true look-ahead is required.

Removed durationtools.yield_all_positive_rationals_uniquely().
Use durationtools.yield_all_positive_rationals(unique=True) instead.

Removed durationtools.assignable_rational_to_dot_count property.
Use Duration.dot_count instead.

Removed durationtools.assignable_rational_to_lilypond_duration_string property.
Use Duration.lilypond_duration_string instead.

Removed durationtools.is_duration_pair().
Do not use anymore. Just initialize duration objects instead.

Removed durationtools.is_binary_rational().
Use Duration.is_binary property instead.

Removed durationtools.is_proper_tuplet_multiplier().
Use Multiplier.is_proper_tuplet_multiplier property instead.

Removed durationtools.duration_token_to_rational().
Just initialize duration objects instead.

Removed durationtools.duration_tokens_to_rationals().
Just initialize duration objects instead.

emoved durationtools.lilypond_duration_string_to_rational().
Just initialize duration objects instead.

Removed durationtools.lilypond_duration_string_to_rational_list().
Function is no longer supported.

Removed durationtools.rational_to_flag_count().
Use the Duration.flag_count property instead.

Removed durationtools.rational_to_fraction_string().
Use str(Duration) instead.

Removed durationtools.rational_to_prolation_string().
Use the Duration.prolation_string property instead.

Renamed durationtools.rational_to_proper_fraction().
The new name is mathtools.fraction_to_proper_fraction().

Removed durationtools.rational_to_duration_pair_with_specified_integer_denominator().
Use NonreducedFraction.with_denominator() instead.

Removed durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator().
Use mathtools.NonreducedFraction.with_multiple_of_denominator() instead.

Removed durationtools.duration_pair_to_prolation_string().
Use the Duration.prolation_string property instead.

Renamed durationtools.group_duration_tokens_by_implied_prolation().
The new name is durationtools.group_nonreduced_fractions_by_implied_prolation().

Removed durationtools.multiply_duration_pair().
Use NonreducedFraction.multiply_without_reducing() instead.

Removed durationtools.multiply_duration_pair_and_reduce_factors().
Use NonreducedFraction.multiply_with_cross_cancelation() instead.

Removed durationtools.multiply_duration_pair_and_try_to_preserve_numerator().
Use NonreducedFraction.multiply_with_numerator_preservation() instead.

Removed durationtools.duration_token_to_assignable_duration_pairs().
Removed durationtools.duration_token_to_assignable_rationals().
Functions are no longer supported. Use leaftools.make_leaves() or notetools.make_notes() instead.

Removed durationtools.duration_tokens_to_duration_pairs().
Function is no longer supported. Just initialize durations intead.

Removed durationtools.duration_tokens_to_least_common_denominator().
Function is no longer supported. Use mathtools.least_common_multiple() instead.

Renamed durationtools.duration_tokens_to_duration_pairs_with_least_common_denominator().
The new name is durationtools.durations_to_nonreduced_fractions_with_common_denominator().

Note that as of 2.11 neither the term 'duration_token' nor 'duration_pair' exist in the public API.

Renamed durationtools.yield_all_assignable_durations().
The new name is durationtools.yield_assignable_durations().

Renamed durationtools.yield_all_positive_integer_pairs().
The new name is durationtools.yield_positive_nonreduced_fractions().

Renamed durationtools.yield_all_positive_rationals().
The new name is durationtools.yield_positive_fractions().

    Note that removing 'all' from the function name is meant to signal
    that the function implements an *infinite* generator.

    Note that 'rational' is now a deprecated term in the public API.
    Use 'fraction' instead to point to the exact class used.

Added four new public properties to Duration::

    * durationtools.Duration.equal_or_greater_assignable
    * durationtools.Duration.equal_or_greater_power_of_two
    * durationtools.Duration.equal_or_lesser_assignable
    * durationtools.Duration.equal_or_lesser_power_of_two

The properties will replace the following four functions::

    * durationtools.rational_to_equal_or_greater_assignable_rational
    * durationtools.rational_to_equal_or_greater_binary_rational
    * durationtools.rational_to_equal_or_lesser_assignable_rational
    * durationtools.rational_to_equal_or_lesser_binary_rational

Note that the terms 'binary' and 'nonbinary' are now deprecated.
Use 'power of two' and 'not power of two' (or 'non-power of two') instead.

Renamed durationtools.yield_positive_fractions().
The new name is durationtools.yield_durations().
The function also now returns durations instead of fractions.

Renamed durationtools.yield_positive_nonreduced_fractions().
The new name is durationtools.yield_nonreduced_fractions().

Removed durationtools.yield_prolation_rewrite_pairs.
The functionality is no longer supported.

Renamed durationtools.yield_nonreduced_fractions.
The new name is mathtools.yield_nonreduced_fractions.

Renamed Duration.is_binary property.
The new name is Duration.has_power_of_two_denominator.

Renamed Measure.is_binary property.
The new name is Measure.has_power_of_two_denominator.

Renamed Tuplet.is_binary property.
The new name is Tuplet.has_power_of_two_denominator.

Renamed Measure.is_nonbinary property.
The new name is Measure.has_non_power_of_two_denominator.

Renamed Tuplet.is_nonbinary property.
The new name is Tuplet.has_non_power_of_two_denominator.

Renamed DynamicMeasure.suppress_meter.
The new name is DynamicMeasure.suppress_time_signature.

Also removed all references to 'meter' in the codebase.
The term is deprecated.
Use 'time signature' instead.

Removed durationtools.integer_to_implied_prolation().
Use the Duration.implied_prolation property instead.

Removed unused resttools.is_lilypond_rest_string() function.
Just instiate rests instead.

Removed durationtools.is_lilypond_duration_string().
Removed durationtools.is_lilypond_duration_name().
Just instiate durations instead.

Removed componenttools.component_to_score_root().
Use component.parentage.root instead.

Removed componenttools.component_to_pitch_and_rhyhtm_skeleton().
Use the parser instead.

Removed componenttools.component_to_score_depth().
Use Component.parentage.depth property instead.

Removed unused componenttools.all_are_orphan_components() function.

Removed unused componenttools.all_are_components_in_same_parent() function.

Removed unused componenttools.all_are_components_in_same_score() function.

Removed unused componenttools.all_are_contiguous_components_in_same_score() function.

Renamed leaftools.make_leaves_from_note_value_signal().
The new name is leaftools.make_leaves_from_talea().

Removed TimeSignatureMark.multiplier property.
Use TimeSignatureMark.implied_prolation instead.

Removed Measure.multiplier property.
Use Measure.implied_prolation instead.

Deprecated timesignaturetools.time_signature_to_time_signature_with_power_of_two_denominator() function.
Use TimeSignatureMark.with_power_of_two_denominator() method instead.

Remvoed timesignaturetools.time_signature_to_time_signature_with_power_of_two_denominator() function.
Use TimeSignatureMark.with_power_of_two_denominator() method instead.

Moved three functions from componenttools to wellformednesstools.
The functions are these::

    is_well_formed_component()
    list_badly_formed_components_in_expr()
    tabulate_well_formedness_violations_in_expr()

Removed two componenttools functions.
Use timerelationtools instead.
The functions are these::

    componenttools.number_is_between_start_and_stop_offsets_of_component
    componenttools.number_is_between_start_and_stop_offsets_of_component_in_seconds

Moved one function from componenttools to measuretools.
The function is get_likely_multiplier_components().

Moved one function from componenttools to formattools.
The function is report_component_format_contributions().

Globally replaced rhythm maker 'pattern' names to 'talea'.
The name change harmonizes with the new names fo the rhythm maker classes.

Removed 'big endian' and 'little endian' from codebase.
Use 'decrease_durations_monotonically=True' keyword instead.

Removed the word 'duration_token' from mainline.
The term is deprecated.
Use 'duration' instead.
Coerce as necessary.

Deprecated the term 'pitch_token'.
Use 'pitch' instead.
Coerce as necessary.

Removed pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches().
Just instantiate pitches instead.

Removed the term 'signal' from the rhythmmakertools package.
Use 'talea' instead. The plural of 'talea' is 'talee'.
The term 'signal' no longer appears anywhere in the mainline.

Renamed 'tied=True' keyword in four functions:

    * leaftools.make_leaves()
    * leaftools.make_tied_leaf()
    * resttools.make_tied_rest()
    * resttools.make_rests()

Moved componenttools.component_to_tuplet_depth().
The function is now bound to parentage as the Component.parentage.tuplet_depth property.

Moved componenttools.component_to_score_index().
The function is now bound to parentage as the Component.parentage.score_index property.

Moved componenttools.component_to_containment_signature().
The function is now bound to parentage as the Component.parentage.containment_signature property.

Moved componenttools.component_to_parentage_signature().
The function is now bound to parentage as the Component.parentage.parentage_signature property.

Renamed componenttools.cut_component_by_at_prolated_duration().
The new name is componenttools.shorten_component_by_prolated_duration().

Renamed input parameter 'prolated_duration' to 'duration' in last remaining spots in codebase.
The use of 'prolated_duration' as an input parameter name is deprecated. Just use 'duration' instead.

    componenttools.get_leftmost_components_with_prolated_duration_at_most() ==>
    componenttools.get_leftmost_components_with_total_duration_at_most()

    componenttools.shorten_component_by_prolated_duration() ==>
    componenttools.shorten_component_by_duration()

    componenttools.sum_prolated_duration_of_components() ==>
    componenttools.sum_duration_of_components()

    componenttools.yield_components_grouped_by_prolated_duration() ==>
    componenttools.yield_components_grouped_by_duration()

    labeltools.label_leaves_in_expr_with_prolated_leaf_duration() ==>
    labeltools.label_leaves_in_expr_with_leaf_duration()

    labeltools.label_tie_chains_in_expr_with_prolated_tie_chain_duration() ==>
    labeltools.label_tie_chains_in_expr_with_tie_chain_duration()

    leaftools.fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang() ==>
    leaftools.fuse_tied_leaves_in_components_once_by_durations_without_overhang()

    leaftools.get_leaf_in_expr_with_maximum_prolated_duration() ==>
    leaftools.get_leaf_in_expr_with_maximum_duration()

    leaftools.get_leaf_in_expr_with_minimum_prolated_duration() ==>
    leaftools.get_leaf_in_expr_with_minimum_duration()

    leaftools.list_prolated_durations_of_leaves_in_expr() ==>
    leaftools.list_durations_of_leaves_in_expr()

Renamed VerticalMoment.prolated_offset to VerticalMoment.offset.
The concept of a 'prolated' offset is not well defined.

Merged componenttools.extend_left_in_parent_of_component() into componenttools.extend_in_parent_of_component().
Use the left=True keyword.

Removed componenttools.extend_left_in_parent_of_component()
Use componenttools.extend_in_parent_of_component(left=True) instead.

Removed componenttools.get_component_start_offset().
Removed componenttools.get_component_stop_offset().
Use the component.start_offset and component.stop_offset properties instead.

Removed componenttools.get_component_start_offset_in_seconds().
Removed componenttools.get_component_stop_offset_in_seconds().
Use the component.start_offset_in_seconds and component.stop_offset_in_seconds properties instead.

Removed componenttools.is_orphan_component().
Use the new component.parentage.is_orphan property instead.

Renamed componenttools.partition_components_by_durations_ge()
The new name is componenttools.partition_components_by_durations_not_less_than()

Renamed componenttools.partition_components_by_durations_le()
The new name is componenttools.partition_components_by_durations_not_greater_than()

emoved componenttools.sum_preprolated_duration_of_components()
Use componenttools.sum_duration_of_components(preprolated=True) instead.

Removed componenttools.sum_duration_of_components_in_seconds().
Use componenttools.sum_duration_of_components(in_seconds=True) instead.



