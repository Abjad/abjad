Change log
==========

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



Changes from 2.9 to 2.10
------------------------

Renamed the read-only ``format`` property to ``lilypond_format`` on all system objects.

All iteration functions are now housed in the new ``iterationtools`` package:

- Renamed::

    chordtools.iterate_chords_forward_in_expr()
    chordtools.iterate_chords_backward_in_expr()

  ::

    iterationtools.iterate_chords_in_expr(reverse=[True, False])

- Renamed::

    componenttools.iterate_components_depth_first()
    componenttools.iterate_components_forward_in_expr()
    componenttools.iterate_components_backward_in_expr()
    componenttools.iterate_namesakes_forward_from_component()
    componenttools.iterate_namesakes_backward_from_component()
    componenttools.iterate_thread_forward_from_component()
    componenttools.iterate_thread_backward_from_component()
    componenttools.iterate_thread_forward_in_expr()
    componenttools.iterate_thread_backward_in_expr()
    componenttools.iterate_timeline_forward_from_component()
    componenttools.iterate_timeline_backward_from_component()
    componenttools.iterate_timeline_forward_in_expr()
    componenttools.iterate_timeline_backward_in_expr()

  ::

    iterationtools.iterate_components_depth_first()
    iterationtools.iterate_components_in_expr(reverse=[True, False])
    iterationtools.iterate_namesakes_from_component(reverse=[True, False])
    iterationtools.iterate_thread_from_component(reverse=[True, False])
    iterationtools.iterate_thread_in_expr(reverse=[True, False])
    iterationtools.iterate_timeline_from_component(reverse=[True, False])
    iterationtools.iterate_timeline_in_expr(reverse=[True, False])

- Renamed::

    containertools.iterate_containers_forward_in_expr()
    containertools.iterate_containers_backward_in_expr()

  ::

    iterationtools.iterate_containers_in_expr(reverse=[True, False])

- Renamed::

    contexttools.iterate_contexts_forward_in_expr()
    contexttools.iterate_contexts_backward_in_expr()

  ::

    iterationtools.iterate_contexts_in_expr(reverse=[True, False])

- Renamed::

    gracetools.iterate_components_and_grace_containers_forward_in_expr()

  ::

    iterationtools.iterate_components_and_grace_containers_in_expr()

- Renamed::

    leaftools.iterate_leaf_pairs_forward_in_expr()
    leaftools.iterate_leaves_forward_in_expr()
    leaftools.iterate_leaves_backward_in_expr()
    leaftools.iterate_notes_and_chords_forward_in_expr()
    leaftools.iterate_notes_and_chords_backward_in_expr()

  ::

    iterationtools.iterate_leaf_pairs_in_expr()
    iterationtools.iterate_leaves_in_expr(reverse=[True, False])
    iterationtools.iterate_notes_and_chords_in_expr(reverse=[True, False])

- Renamed::

    measuretools.iterate_measures_forward_in_expr()
    measuretools.iterate_measures_backward_in_expr()

  ::

    iterationtools.iterate_measures_in_expr(reverse=[True, False])

- Renamed::

    notetools.iterate_notes_forward_in_expr()
    notetools.iterate_notes_backward_in_expr()

  ::

    iterationtools.iterate_notes_in_expr(reverse=[True, False])

- Renamed::

    resttools.iterate_rests_forward_in_expr()
    resttools.iterate_rests_backward_in_expr()

  ::

    iterationtools.iterate_rests_in_expr(reverse=[True, False])

- Renamed::

    scoretools.iterate_scores_forward_in_expr()
    scoretools.iterate_scores_backward_in_expr()

  ::

    iterationtools.iterate_scores_in_expr(reverse=[True, False])

- Renamed::

    skiptools.iterate_skips_forward_in_expr()
    skiptools.iterate_skips_backward_in_expr()

  ::

    iterationtools.iterate_skips_in_expr(reverse=[True, False])

- Renamed::

    stafftools.iterate_staves_forward_in_expr()
    stafftools.iterate_staves_backward_in_expr()

  ::

    iterationtools.iterate_staves_in_expr(reverse=[True, False])

- Renamed::

    tuplettools.iterate_tuplets_forward_in_expr()
    tuplettools.iterate_tuplets_backward_in_expr()

  ::

    iterationtools.iterate_tuplets_in_expr(reverse=[True, False])

- Renamed::

    voicetools.iterate_semantic_voices_forward_in_expr()
    voicetools.iterate_semantic_voices_backward_in_expr()
    voicetools.iterate_voices_forward_in_expr()
    voicetools.iterate_voices_backward_in_expr()

  ::

    voicetools.iterate_semantic_voices_in_expr(reverse=[True, False])
    voicetools.iterate_voices_in_expr(reverse=[True, False])

All labeling functions are now housed in the new ``labeltools`` package:

- Renamed::

    chordtools.color_chord_note_heads_in_expr_by_pitch_class_color_map()

  ::

    labeltools.color_chord_note_heads_in_expr_by_pitch_class_color_map()

- Renamed::

    containertools.color_contents_of_container()

  ::

    labeltools.color_contents_of_container()

- Renamed::

    leaftools.color_leaf()
    leaftools.color_leaves_in_expr()
    leaftools.label_leaves_in_expr_with_inversion_equivalent_chromatic_interval_classes()
    leaftools.label_leaves_in_expr_with_leaf_depth()
    leaftools.label_leaves_in_expr_with_leaf_durations()
    leaftools.label_leaves_in_expr_with_leaf_indices()
    leaftools.label_leaves_in_expr_with_leaf_numbers()
    leaftools.label_leaves_in_expr_with_melodic_chromatic_interval_classes()
    leaftools.label_leaves_in_expr_with_melodic_chromatic_intervals()
    leaftools.label_leaves_in_expr_with_melodic_counterpoint_interval_classes()
    leaftools.label_leaves_in_expr_with_melodic_counterpoint_intervals()
    leaftools.label_leaves_in_expr_with_melodic_diatonic_interval_classes()
    leaftools.label_leaves_in_expr_with_melodic_diatonic_intervals()
    leaftools.label_leaves_in_expr_with_pitch_class_numbers()
    leaftools.label_leaves_in_expr_with_pitch_numbers()
    leaftools.label_leaves_in_expr_with_leaf_duration()
    leaftools.label_leaves_in_expr_with_tuplet_depth()
    leaftools.label_leaves_in_expr_with_written_leaf_duration()

  ::

    labeltools.color_leaf()
    labeltools.color_leaves_in_expr()
    labeltools.label_leaves_in_expr_with_inversion_equivalent_chromatic_interval_classes()
    labeltools.label_leaves_in_expr_with_leaf_depth()
    labeltools.label_leaves_in_expr_with_leaf_durations()
    labeltools.label_leaves_in_expr_with_leaf_indices()
    labeltools.label_leaves_in_expr_with_leaf_numbers()
    labeltools.label_leaves_in_expr_with_melodic_chromatic_interval_classes()
    labeltools.label_leaves_in_expr_with_melodic_chromatic_intervals()
    labeltools.label_leaves_in_expr_with_melodic_counterpoint_interval_classes()
    labeltools.label_leaves_in_expr_with_melodic_counterpoint_intervals()
    labeltools.label_leaves_in_expr_with_melodic_diatonic_interval_classes()
    labeltools.label_leaves_in_expr_with_melodic_diatonic_intervals()
    labeltools.label_leaves_in_expr_with_pitch_class_numbers()
    labeltools.label_leaves_in_expr_with_pitch_numbers()
    labeltools.label_leaves_in_expr_with_leaf_duration()
    labeltools.label_leaves_in_expr_with_tuplet_depth()
    labeltools.label_leaves_in_expr_with_written_leaf_duration()

- Renamed::

    markuptools.remove_markup_from_leaves_in_expr()

  ::

    labeltools.remove_markup_from_leaves_in_expr()

- Renamed::

    measuretools.color_measure()
    measuretools.color_measures_with_non_power_of_two_denominators_in_expr()

  ::

    labeltools.color_measure()
    labeltools.color_measures_with_non_power_of_two_denominators_in_expr()

- Renamed::

    notetools.color_note_head_by_numbered_chromatic_pitch_class_color_map()
    notetools.label_notes_in_expr_with_note_indices()

  ::

    labeltools.color_note_head_by_numbered_chromatic_pitch_class_color_map()
    labeltools.label_notes_in_expr_with_note_indices()

- Renamed::

    tietools.label_tie_chains_in_expr_with_tie_chain_duration()
    tietools.label_tie_chains_in_expr_with_tie_chain_durations()
    tietools.label_tie_chains_in_expr_with_written_tie_chain_duration()

  ::

    labeltools.label_tie_chains_in_expr_with_tie_chain_duration()
    labeltools.label_tie_chains_in_expr_with_tie_chain_durations()
    labeltools.label_tie_chains_in_expr_with_written_tie_chain_duration()

- Renamed::

    verticalitytools.label_vertical_moments_in_expr_with_chromatic_interval_classes()
    verticalitytools.label_vertical_moments_in_expr_with_chromatic_intervals()
    verticalitytools.label_vertical_moments_in_expr_with_counterpoint_intervals()
    verticalitytools.label_vertical_moments_in_expr_with_diatonic_intervals()
    verticalitytools.label_vertical_moments_in_expr_with_interval_class_vectors()
    verticalitytools.label_vertical_moments_in_expr_with_numbered_chromatic_pitch_classes()
    verticalitytools.label_vertical_moments_in_expr_with_pitch_numbers()

  ::

    labeltools.label_vertical_moments_in_expr_with_chromatic_interval_classes()
    labeltools.label_vertical_moments_in_expr_with_chromatic_intervals()
    labeltools.label_vertical_moments_in_expr_with_counterpoint_intervals()
    labeltools.label_vertical_moments_in_expr_with_diatonic_intervals()
    labeltools.label_vertical_moments_in_expr_with_interval_class_vectors()
    labeltools.label_vertical_moments_in_expr_with_numbered_chromatic_pitch_classes()
    labeltools.label_vertical_moments_in_expr_with_pitch_numbers()

Renamed all functions that contained ``big_endian``::

    durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs()
    leaftools.fuse_leaves_big_endian()
    leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian()

::

    durationtools.duration_token_to_assignable_duration_pairs()
    leaftools.fuse_leaves()
    leaftools.fuse_leaves_in_tie_chain_by_immediate_parent()

Renamed all functions that contained ``prolated_offset`` to simply ``offset``::

    componenttools.copy_governed_component_subtree_from_prolated_offset_to()
    componenttools.get_improper_descendents_of_component_that_cross_prolated_offset()
    containertools.delete_contents_of_container_starting_at_or_after_prolated_offset()
    containertools.delete_contents_of_container_starting_before_or_at_prolated_offset()
    containertools.delete_contents_of_container_starting_strictly_after_prolated_offset()
    containertools.delete_contents_of_container_starting_strictly_before_prolated_offset()
    containertools.get_element_starting_at_exactly_prolated_offset()
    containertools.get_first_element_starting_at_or_after_prolated_offset()
    containertools.get_first_element_starting_before_or_at_prolated_offset()
    containertools.get_first_element_starting_strictly_after_prolated_offset()
    containertools.get_first_element_starting_strictly_before_prolated_offset()
    prolated_offsettools.update_offset_values_of_component()
    verticalitytools.get_vertical_moment_at_prolated_offset_in_expr()

::

    componenttools.copy_governed_component_subtree_from_offset_to()
    componenttools.get_improper_descendents_of_component_that_cross_offset()
    containertools.delete_contents_of_container_starting_at_or_after_offset()
    containertools.delete_contents_of_container_starting_before_or_at_offset()
    containertools.delete_contents_of_container_starting_strictly_after_offset()
    containertools.delete_contents_of_container_starting_strictly_before_offset()
    containertools.get_element_starting_at_exactly_offset()
    containertools.get_first_element_starting_at_or_after_offset()
    containertools.get_first_element_starting_before_or_at_offset()
    containertools.get_first_element_starting_strictly_after_offset()
    containertools.get_first_element_starting_strictly_before_offset()
    offsettools.update_offset_values_of_component()
    verticalitytools.get_vertical_moment_at_offset_in_expr()

Renamed ``prolated_duration`` to ``offset`` in some functions::

    componenttools.split_component_at_prolated_duration()
    componenttools.split_components_by_prolated_durations()
    leaftools.split_leaf_at_prolated_duration()
    leaftools.split_leaf_at_prolated_duration_and_rest_right_half()

::

    componenttools.split_component_at_offset()
    componenttools.split_components_by_offsets()
    leaftools.split_leaf_at_offset()
    leaftools.split_leaf_at_offset_and_rest_right_half()

Renamed all functions that contained ``as_string``::

    componenttools.report_component_format_contributions_as_string()
    containertools.report_container_modifications_as_string()
    measuretools.report_meter_distribution_as_string()

::

    formattools.report_component_format_contributions()
    containertools.report_container_modifications()
    measuretools.report_time_signature_distribution()

Changes to the ``componenttools`` package:

- The ``componenttools.split_components_at_offsets()`` function no longer 
  implements a ``tie_after keyword``.
  Use the new ``tie_split_notes`` and ``tie_split_rests`` keywords.
  Note that the new ``tie_split_rests``
  keyword defaults to true where the old ``tie_after`` keyword defaulted to false.
  This changes the default behavior of the function.

- Renamed::

    componenttools.extend_left_in_parent_of_component_and_grow_spanners()
    componenttools.extend_left_in_parent_of_component_and_do_not_grow_spanners()

  ::

    componenttools.extend_left_in_parent_of_component(grow_spanners=[True, False])

- Renamed::

    componenttools.extend_in_parent_of_component_and_grow_spanners()
    componenttools.extend_in_parent_of_component_and_do_not_grow_spanners()

  ::

    componenttools.extend_in_parent_of_component(grow_spanners=[True, False])

- Renamed::

    componenttools.number_is_between_prolated_start_and_stop_offsets_of_component()

  ::

    componenttools.number_is_between_start_and_stop_offsets_of_component()

- Renamed::

    componenttools.partition_components_cyclically_by_durations_in_seconds_exactly_with_overhang()
    componenttools.partition_components_cyclically_by_durations_in_seconds_exactly_without_overhang()
    componenttools.partition_components_cyclically_by_durations_in_seconds_ge_with_overhang()
    componenttools.partition_components_cyclically_by_durations_in_seconds_ge_without_overhang()
    componenttools.partition_components_cyclically_by_durations_in_seconds_le_with_overhang()
    componenttools.partition_components_cyclically_by_durations_in_seconds_le_without_overhang()
    componenttools.partition_components_cyclically_by_prolated_durations_exactly_with_overhang()
    componenttools.partition_components_cyclically_by_prolated_durations_exactly_without_overhang()
    componenttools.partition_components_cyclically_by_prolated_durations_ge_with_overhang()
    componenttools.partition_components_cyclically_by_prolated_durations_ge_without_overhang()
    componenttools.partition_components_cyclically_by_prolated_durations_le_with_overhang()
    componenttools.partition_components_cyclically_by_prolated_durations_le_without_overhang()
    componenttools.partition_components_once_by_durations_in_seconds_exactly_with_overhang()
    componenttools.partition_components_once_by_durations_in_seconds_exactly_without_overhang()
    componenttools.partition_components_once_by_durations_in_seconds_ge_with_overhang()
    componenttools.partition_components_once_by_durations_in_seconds_ge_without_overhang()
    componenttools.partition_components_once_by_durations_in_seconds_le_with_overhang()
    componenttools.partition_components_once_by_durations_in_seconds_le_without_overhang()
    componenttools.partition_components_once_by_prolated_durations_exactly_with_overhang()
    componenttools.partition_components_once_by_prolated_durations_exactly_without_overhang()
    componenttools.partition_components_once_by_prolated_durations_ge_with_overhang()
    componenttools.partition_components_once_by_prolated_durations_ge_without_overhang()
    componenttools.partition_components_once_by_prolated_durations_le_with_overhang()
    componenttools.partition_components_once_by_prolated_durations_le_without_overhang()

  ::

    componenttools.partition_components_by_durations_exactly()
    componenttools.partition_components_by_durations_not_less_than()
    componenttools.partition_components_by_durations_not_greater_than()

- Renamed::

    componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners()
    componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners()

  ::

    componenttools.split_component_at_offset(fracture_spanners=[True, False])

- Renamed::

    componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners()
    componenttools.split_components_cyclically_by_prolated_durations_and_fracture_crossing_spanners()
    componenttools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners()
    componenttools.split_components_once_by_prolated_durations_and_fracture_crossing_spanners()

  ::

    componenttools.split_components_at_offsets(fracture_spanners=[True, False], cyclic=[True, False])

Changeds to the ``continertools`` package:

- Renamed::

    containertools.remove_empty_containers_in_expr()

  ::

    containertools.remove_leafless_containers_in_expr()

- Renamed::

    containertools.replace_larger_left_half_of_elements_in_container_with_big_endian_rests()
    containertools.replace_larger_left_half_of_elements_in_container_with_little_endian_rests()
    containertools.replace_larger_right_half_of_elements_in_container_with_big_endian_rests()
    containertools.replace_larger_right_half_of_elements_in_container_with_little_endian_rests()
    containertools.replace_n_edge_elements_in_container_with_big_endian_rests()
    containertools.replace_n_edge_elements_in_container_with_little_endian_rests()
    containertools.replace_n_edge_elements_in_container_with_rests()
    containertools.replace_smaller_left_half_of_elements_in_container_with_big_endian_rests()
    containertools.replace_smaller_left_half_of_elements_in_container_with_little_endian_rests()
    containertools.replace_smaller_right_half_of_elements_in_container_with_big_endian_rests()
    containertools.replace_smaller_right_half_of_elements_in_container_with_little_endian_rests()

  ::

    containertools.replace_container_slice_with_rests()

- Renamed::

    containertools.split_container_at_index_and_do_not_fracture_crossing_spanners()
    containertools.split_container_at_index_and_fracture_crossing_spanners()

  ::

    containertools.split_container_at_index(fracture_spanners=[True, False])

- Renamed::

    containertools.split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners()
    containertools.split_container_cyclically_by_counts_and_fracture_crossing_spanners()
    containertools.split_container_once_by_counts_and_do_not_fracture_crossing_spanners()
    containertools.split_container_once_by_counts_and_fracture_crossing_spanners()

  ::

    containertools.split_container_by_counts(fracture_spanners=[True, False], cyclic=[True, False])

Changes to the ``durationtools`` package:

- Renamed::

    durationtools.yield_all_assignable_rationals_in_cantor_diagonalized_order()
    durationtools.yield_all_positive_integer_pairs_in_cantor_diagonalized_order()
    durationtools.yield_all_positive_rationals_in_cantor_diagonalized_order()
    durationtools.yield_all_positive_rationals_in_cantor_diagonalized_order_uniquely()
    durationtools.yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order()

  ::

    durationtools.yield_assignable_durations()
    mathtools.yield_nonreduced_fractions()
    durationtools.yield_durations()
    durationtools.yield_all_positive_rationals_uniquely()
    metricmodulationtools.yield_prolation_rewrite_pairs()

Changes to the ``instrumenttools`` package:

- Renamed::

    instrumenttools.transpose_notes_and_chords_in_expr_from_sounding_pitch_to_fingered_pitch()

  ::

    instrumenttools.transpose_from_sounding_pitch_to_fingered_pitch()

- Renamed::

    instrumenttools.transpose_notes_and_chords_in_expr_from_fingered_pitch_to_sounding_pitch()

  ::

    instrumenttools.transpose_from_fingered_pitch_to_sounding_pitch()

Chnages to the ``leaftools`` package:

- Renamed::

    leaftools.fuse_leaves_in_container_once_by_counts_into_big_endian_notes()
    leaftools.fuse_leaves_in_container_once_by_counts_into_big_endian_rests()
    leaftools.fuse_leaves_in_container_once_by_counts_into_little_endian_notes()
    leaftools.fuse_leaves_in_container_once_by_counts_into_little_endian_rests()

  ::

    leaftools.fuse_leaves_in_container_once_by_counts(big_endian=[True, False], klass=None)

- Renamed::

    leaftools.leaf_to_augmented_tuplet_with_n_notes_of_equal_written_duration()
    leaftools.leaf_to_augmented_tuplet_with_proportions()
    leaftools.leaf_to_diminished_tuplet_with_n_notes_of_equal_written_duration()
    leaftools.leaf_to_diminished_tuplet_with_proportions()

  ::

    tuplettools.leaf_to_tuplet_with_n_notes_of_equal_written_duration()
    tuplettools.leaf_to_tuplet_with_ratio()

- Renamed::

    leaftools.split_leaf_at_offset_and_rest_right_half()

  ::

    leaftools.rest_leaf_at_offset()

- Renamed::

    leaftools.repeat_leaf_and_extend_spanners()
    leaftools.repeat_leaves_in_expr_and_extend_spanners()

  ::

    leaftools.repeat_leaf()
    leaftools.repeat_leaves_in_expr()

Changes to the ``mathtools`` package.

- Removed ``mathtools.partition_integer_into_thirds()``.

Changes to the ``measuretools`` package:

- Renamed::

    measuretools.fill_measures_in_expr_with_meter_denominator_notes()
    measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure()
    measuretools.multiply_contents_of_measures_in_expr_and_scale_meter_denominators()
    measuretools.scale_measure_by_multiplier_and_adjust_meter()

  ::

    measuretools.fill_measures_in_expr_with_time_signature_denominator_notes()
    measuretools.move_full_measure_tuplet_prolation_to_measure_time_signature()
    measuretools.multiply_contents_of_measures_in_expr_and_scale_time_signature_denominators()
    measuretools.scale_measure_and_adjust_time_signature()

- Renamed::

    measuretools.fill_measures_in_expr_with_big_endian_notes()
    measuretools.fill_measures_in_expr_with_litte_endian_notes()

  ::

    measuretools.measuretools.fill_measures_in_expr_with_minimal_number_of_notes(big_endian=[True, False])

- Renamed::

    measuretools.extend_measures_in_expr_and_apply_full_measure_tuplets_to_measure_contents()

  ::

    measuretoools.extend_measures_in_expr_and_apply_full_measure_tuplets()

- Renamed::

    measuretools.get_previous_measure_from_component()

  ::

    measuretools.get_previous_measure_from_component()

- Renamed::

    measuretools.multiply_contents_of_measures_in_expr_and_scale_time_signature_denominators()

  ::

    measuretools.multiply_and_scale_contents_of_measures_in_expr()

- Renamed::

    measuretools.pitch_array_row_to_measure()
    measuretools.pitch_array_to_measures()

  ::

    pitchtools.pitch_array_row_to_measure()
    pitchtools.pitch_array_to_measures()

Changes to the ``pitchtools`` package:

- Renamed::

    pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier()
    pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier()
    pitchtools.calculate_harmonic_counterpoint_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch()
    pitchtools.calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch()
    pitchtools.calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch()
    pitchtools.calculate_harmonic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch()

  ::

    pitchtools.calculate_harmonic_chromatic_interval_class()
    pitchtools.calculate_harmonic_chromatic_interval()
    pitchtools.calculate_harmonic_counterpoint_interval_class()
    pitchtools.calculate_harmonic_counterpoint_interval()
    pitchtools.calculate_harmonic_diatonic_interval_class()
    pitchtools.calculate_harmonic_diatonic_interval()

- Renamed::

    pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier()
    pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier()
    pitchtools.calculate_melodic_counterpoint_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch()
    pitchtools.calculate_melodic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch()
    pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch()
    pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch()

  ::

    pitchtools.calculate_melodic_chromatic_interval_class()
    pitchtools.calculate_melodic_chromatic_interval()
    pitchtools.calculate_melodic_counterpoint_interval_class()
    pitchtools.calculate_melodic_counterpoint_interval()
    pitchtools.calculate_melodic_diatonic_interval_class()
    pitchtools.calculate_melodic_diatonic_interval()

- Renamed::

    pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair()

  ::

    pitchtools.split_chromatic_pitch_class_name()


- Renamed::

    pitchtools.diatonic_interval_number_and_chromatic_interval_number_to_melodic_diatonic_interval()
 
  ::

    pitchtools.spell_chromatic_interval_number()

- Renamed::

    pitchtools.named_chromatic_pitches_to_harmonic_chromatic_interval_class_number_dictionary()

  ::

    pitchtools.harmonic_chromatic_interval_class_number_dictionary()

- Renamed::

    pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_alphabetic_accidental_abbreviation_octave_number_pair()

  ::

    pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair()

- Renamed::

    pitchtools.list_named_chromatic_pitch_carriers_in_expr_sorted_by_numbered_chromatic_pitch_class()

  ::

    pitchtools.sort_named_chromatic_pitch_carriers_in_expr()

- Renamed::

    pitchtools.named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary()

  ::

    pitchtools.inversion_equivalent_chromatic_interval_class_number_dictionary()

- Renamed::

    pitchtools.transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number()

  ::

    pitchtools.transpose_chromatic_pitch_class_number_to_neighbor_of_chromatic_pitch_number()

- Renamed::

    pitchtools.ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers()

  ::

    pitchtools.contains_subsegment()

- Renamed::

    pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise_between_pitch_carriers()

  ::

    pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise()

- Renamed::

    pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_pitch_carriers()

  ::

    pitchtools.list_melodic_chromatic_interval_numbers_pairwise()

- Renamed::

    pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple()

  ::

    pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple()

- Renamed::

    pitchtools.apply_octavation_spanner_to_pitched_components()

  ::

    spannertools.apply_octavation_spanner_to_pitched_components()

- Renamed::

    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr()

  ::

    pitchtools.set_ascending_named_chromatic_pitches_on_tie_chains_in_expr()

- Renamed::

    pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr()

  ::

    pitchtools.set_ascending_diatonic_pitches_on_tie_chains_in_expr()

- Renamed::

    pitchtools.transpose_chromatic_pitch_class_number_to_neighbor_of_chromatic_pitch_number()

  ::

    pitchtools.transpose_chromatic_pitch_class_number_chromatic_pitch_number_neighbor()

Changes to the ``rhythmtreetools`` package:

- Renamed::

    rhythmtreetools.parse_reduced_ly_syntax()

  ::

    lilypondparsertools.parse_reduced_ly_syntax()

Chnages to the ``scoretemplatetools`` package:

- Renamed::

    scoretemplatetools.GroupedRhythmcStavesScoreTemplate.n

  ::

    scoretemplatetools.GroupedRhythmcStavesScoreTemplate.staff_count

Changes to the ``scoretools`` package:

- Renamed::

    scoretools.make_pitch_array_score_from_pitch_arrays()

  ::

    pitchtools.make_pitch_array_score_from_pitch_arrays()

Changes to the ``sequencetools`` package:

- Renamed::

    sequencetools.partition_sequence_cyclically_by_counts_with_overhang()
    sequencetools.partition_sequence_cyclically_by_counts_without_overhang()
    sequencetools.partition_sequence_once_by_counts_with_overhang()
    sequencetools.partition_sequence_once_by_counts_without_overhang()

  ::

    sequencetools.partition_sequence_by_counts(cyclic=[True, False], overhang=[True, False]) 

- Renamed::

    sequencetools.partition_sequence_extended_to_counts_with_overhang()
    sequencetools.partition_sequence_extended_to_counts_without_overhang()

  ::

    sequencetools.partition_sequence_extended_to_counts(overhang=[True, False])

- Renamed::

    sequencetools.partition_sequence_cyclically_by_weights_at_least_with_overhang()
    sequencetools.partition_sequence_cyclically_by_weights_at_least_without_overhang()
    sequencetools.partition_sequence_once_by_weights_at_least_with_overhang()
    sequencetools.partition_sequence_once_by_weights_at_least_without_overhang()

  ::

    sequencetools.partition_sequence_by_weights_at_least()

- Renamed::

    sequencetools.partition_sequence_cyclically_by_weights_at_most_with_overhang()
    sequencetools.partition_sequence_cyclically_by_weights_at_most_without_overhang()
    sequencetools.partition_sequence_once_by_weights_at_most_with_overhang()
    sequencetools.partition_sequence_once_by_weights_at_most_without_overhang()

  ::

    sequencetools.partition_sequence_by_weights_at_most()

- Renamed::

    sequencetools.partition_sequence_cyclically_by_weights_at_exactly_with_overhang()
    sequencetools.partition_sequence_cyclically_by_weights_at_exactly_without_overhang()
    sequencetools.partition_sequence_once_by_weights_at_exactly_with_overhang()
    sequencetools.partition_sequence_once_by_weights_at_exactly_without_overhang()

  ::

    sequencetools.partition_sequence_by_weights_at_exactly()

- Renamed::

    sequencetools.split_sequence_cyclically_by_weights_with_overhang()
    sequencetools.split_sequence_cyclically_by_weights_without_overhang()
    sequencetools.split_sequence_once_by_weights_with_overhang()
    sequencetools.split_sequence_once_by_weights_without_overhang()

  ::

    sequencetools.split_sequence_by_weights()

- Renamed::

    sequencetools.split_sequence_extended_to_weights_with_overhang()
    sequencetools.split_sequence_extended_to_weights_without_overhang()

  ::

    sequencetools.split_sequence_extended_to_weights()

Changes to the ``tietools`` package:

- Renamed::

    tietools.tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots()
    tietools.tie_chain_to_augmented_tuplet_with_proportions_and_encourage_dots()
    tietools.tie_chain_to_diminished_tuplet_with_proportions_and_avoid_dots()
    tietools.tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots()

  ::

    tietools.tie_chain_to_tuplet_with_ratio()

- Renamed::

    tietools.iterate_nontrivial_tie_chains_forward_in_expr()
    tietools.iterate_nontrivial_tie_chains_backward_in_expr()
    tietools.iterate_pitched_tie_chains_forward_in_expr()
    tietools.iterate_pitched_tie_chains_backward_in_expr()
    tietools.iterate_tie_chains_forward_in_expr()
    tietools.iterate_tie_chains_backward_in_expr()

  ::

    tietools.iterate_nontrivial_tie_chains_in_expr(reverse=[True, False])
    tietools.iterate_pitched_tie_chains_in_expr(reverse=[True, False])
    tietools.iterate_tie_chains_in_expr(reverse=[True, False])

Changes to the ``tuplettools`` package:

- Renamed::

    tuplettools.is_proper_tuplet_multiplier()

  ::

    durationtools.is_proper_tuplet_multiplier()

- Renamed::

    tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots()
    tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots()
    tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots()
    tuplettools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots()

  ::

    tuplettools.make_tuplet_from_durations_and_proportions(big_endian=[True, False])

Removed three packages.

- Removed ``constrainttools`` package.

- Removed ``lyricstools`` package.

- Removed ``quantizationtools`` package.
