:orphan:

Changes from 2.9 to 2.10
------------------------

Renamed the read-only ``format`` property to ``lilypond_format`` on all system
objects.

All iteration functions are now housed in the new ``iterationtools`` package:

- Renamed::

    scoretools.iterate_chords_forward_in_expr()
    scoretools.iterate_chords_backward_in_expr()

  ::

    iterationtools.iterate_chords_in_expr(reverse=[True, False])

- Renamed::

    scoretools.iterate_components_depth_first()
    scoretools.iterate_components_forward_in_expr()
    scoretools.iterate_components_backward_in_expr()
    scoretools.iterate_namesakes_forward_from_component()
    scoretools.iterate_namesakes_backward_from_component()
    scoretools.iterate_thread_forward_from_component()
    scoretools.iterate_thread_backward_from_component()
    scoretools.iterate_thread_forward_in_expr()
    scoretools.iterate_thread_backward_in_expr()
    scoretools.iterate_timeline_forward_from_component()
    scoretools.iterate_timeline_backward_from_component()
    scoretools.iterate_timeline_forward_in_expr()
    scoretools.iterate_timeline_backward_in_expr()

  ::

    iterationtools.iterate_components_depth_first()
    iterationtools.iterate_components_in_expr(reverse=[True, False])
    iterationtools.iterate_namesakes_from_component(reverse=[True, False])
    iterationtools.iterate_logical_voice_from_component(reverse=[True, False])
    iterationtools.iterate_logical_voice_in_expr(reverse=[True, False])
    iterationtools.iterate_timeline_from_component(reverse=[True, False])
    iterationtools.iterate_timeline_in_expr(reverse=[True, False])

- Renamed::

    scoretools.iterate_containers_forward_in_expr()
    scoretools.iterate_containers_backward_in_expr()

  ::

    iterationtools.iterate_containers_in_expr(reverse=[True, False])

- Renamed::

    indicatortools.iterate_contexts_forward_in_expr()
    indicatortools.iterate_contexts_backward_in_expr()

  ::

    iterationtools.iterate_contexts_in_expr(reverse=[True, False])

- Renamed::

    gracetools.iterate_components_and_grace_containers_forward_in_expr()

  ::

    iterationtools.iterate_components_and_grace_containers_in_expr()

- Renamed::

    scoretools.iterate_leaf_pairs_forward_in_expr()
    scoretools.iterate_leaves_forward_in_expr()
    scoretools.iterate_leaves_backward_in_expr()
    scoretools.iterate_notes_and_chords_forward_in_expr()
    scoretools.iterate_notes_and_chords_backward_in_expr()

  ::

    iterationtools.iterate_leaf_pairs_in_expr()
    iterationtools.iterate_leaves_in_expr(reverse=[True, False])
    iterationtools.iterate_notes_and_chords_in_expr(reverse=[True, False])

- Renamed::

    scoretools.iterate_measures_forward_in_expr()
    scoretools.iterate_measures_backward_in_expr()

  ::

    iterationtools.iterate_measures_in_expr(reverse=[True, False])

- Renamed::

    scoretools.iterate_notes_forward_in_expr()
    scoretools.iterate_notes_backward_in_expr()

  ::

    iterationtools.iterate_notes_in_expr(reverse=[True, False])

- Renamed::

    scoretools.iterate_rests_forward_in_expr()
    scoretools.iterate_rests_backward_in_expr()

  ::

    iterationtools.iterate_rests_in_expr(reverse=[True, False])

- Renamed::

    scoretools.iterate_scores_forward_in_expr()
    scoretools.iterate_scores_backward_in_expr()

  ::

    iterationtools.iterate_scores_in_expr(reverse=[True, False])

- Renamed::

    scoretools.iterate_skips_forward_in_expr()
    scoretools.iterate_skips_backward_in_expr()

  ::

    iterationtools.iterate_skips_in_expr(reverse=[True, False])

- Renamed::

    scoretools.iterate_staves_forward_in_expr()
    scoretools.iterate_staves_backward_in_expr()

  ::

    iterationtools.iterate_staves_in_expr(reverse=[True, False])

- Renamed::

    scoretools.iterate_tuplets_forward_in_expr()
    scoretools.iterate_tuplets_backward_in_expr()

  ::

    iterationtools.iterate_tuplets_in_expr(reverse=[True, False])

- Renamed::

    scoretools.iterate_semantic_voices_forward_in_expr()
    scoretools.iterate_semantic_voices_backward_in_expr()
    scoretools.iterate_voices_forward_in_expr()
    scoretools.iterate_voices_backward_in_expr()

  ::

    scoretools.iterate_semantic_voices_in_expr(reverse=[True, False])
    scoretools.iterate_voices_in_expr(reverse=[True, False])

All labeling functions are now housed in the new ``labeltools`` package:

- Renamed::

    scoretools.color_chord_note_heads_in_expr_by_pitch_class_color_map()

  ::

    labeltools.color_chord_note_heads_in_expr_by_pitch_class_color_map()

- Renamed::

    scoretools.color_contents_of_container()

  ::

    labeltools.color_contents_of_container()

- Renamed::

    scoretools.color_leaf()
    scoretools.color_leaves_in_expr()
    scoretools.label_leaves_in_expr_with_inversion_equivalent_chromatic_interval_classes()
    scoretools.label_leaves_in_expr_with_leaf_depth()
    scoretools.label_leaves_in_expr_with_leaf_durations()
    scoretools.label_leaves_in_expr_with_leaf_indices()
    scoretools.label_leaves_in_expr_with_leaf_numbers()
    scoretools.label_leaves_in_expr_with_melodic_chromatic_interval_classes()
    scoretools.label_leaves_in_expr_with_melodic_chromatic_intervals()
    scoretools.label_leaves_in_expr_with_melodic_counterpoint_interval_classes()
    scoretools.label_leaves_in_expr_with_melodic_counterpoint_intervals()
    scoretools.label_leaves_in_expr_with_melodic_diatonic_interval_classes()
    scoretools.label_leaves_in_expr_with_melodic_diatonic_intervals()
    scoretools.label_leaves_in_expr_with_pitch_class_numbers()
    scoretools.label_leaves_in_expr_with_pitch_numbers()
    scoretools.label_leaves_in_expr_with_leaf_duration()
    scoretools.label_leaves_in_expr_with_tuplet_depth()
    scoretools.label_leaves_in_expr_with_written_leaf_duration()

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

    scoretools.color_measure()
    scoretools.color_measures_with_non_power_of_two_denominators_in_expr()

  ::

    labeltools.color_measure()
    labeltools.color_measures_with_non_power_of_two_denominators_in_expr()

- Renamed::

    scoretools.color_note_head_by_numbered_pitch_class_color_map()
    scoretools.label_notes_in_expr_with_note_indices()

  ::

    labeltools.color_note_head_by_numbered_pitch_class_color_map()
    labeltools.label_notes_in_expr_with_note_indices()

- Renamed::

    tietools.label_logical_ties_in_expr_with_logical_tie_duration()
    tietools.label_logical_ties_in_expr_with_logical_tie_durations()
    tietools.label_logical_ties_in_expr_with_written_logical_tie_duration()

  ::

    labeltools.label_logical_ties_in_expr_with_logical_tie_duration()
    labeltools.label_logical_ties_in_expr_with_logical_tie_durations()
    labeltools.label_logical_ties_in_expr_with_written_logical_tie_duration()

- Renamed::

    verticalitytools.label_vertical_moments_in_expr_with_chromatic_interval_classes()
    verticalitytools.label_vertical_moments_in_expr_with_chromatic_intervals()
    verticalitytools.label_vertical_moments_in_expr_with_counterpoint_intervals()
    verticalitytools.label_vertical_moments_in_expr_with_diatonic_intervals()
    verticalitytools.label_vertical_moments_in_expr_with_interval_class_vectors()
    verticalitytools.label_vertical_moments_in_expr_with_numbered_pitch_classes()
    verticalitytools.label_vertical_moments_in_expr_with_pitch_numbers()

  ::

    labeltools.label_vertical_moments_in_expr_with_chromatic_interval_classes()
    labeltools.label_vertical_moments_in_expr_with_chromatic_intervals()
    labeltools.label_vertical_moments_in_expr_with_counterpoint_intervals()
    labeltools.label_vertical_moments_in_expr_with_diatonic_intervals()
    labeltools.label_vertical_moments_in_expr_with_interval_class_vectors()
    labeltools.label_vertical_moments_in_expr_with_numbered_pitch_classes()
    labeltools.label_vertical_moments_in_expr_with_pitch_numbers()

Renamed all functions that contained ``big_endian``::

    durationtools.duration_token_to_big_endian_list_of_assignable_duration_pairs()
    scoretools.fuse_leaves_big_endian()
    scoretools.fuse_leaves_in_logical_tie_by_immediate_parent_big_endian()

::

    durationtools.duration_token_to_assignable_duration_pairs()
    scoretools.fuse_leaves()
    scoretools.fuse_leaves_in_logical_tie_by_immediate_parent()

Renamed all functions that contained ``prolated_offset`` to simply ``offset``::

    scoretools.copy_governed_component_subtree_from_prolated_offset_to()
    scoretools.get_improper_descendents_of_component_that_cross_prolated_offset()
    scoretools.delete_contents_of_container_starting_at_or_after_prolated_offset()
    scoretools.delete_contents_of_container_starting_before_or_at_prolated_offset()
    scoretools.delete_contents_of_container_starting_strictly_after_prolated_offset()
    scoretools.delete_contents_of_container_starting_strictly_before_prolated_offset()
    scoretools.get_element_starting_at_exactly_prolated_offset()
    scoretools.get_first_element_starting_at_or_after_prolated_offset()
    scoretools.get_first_element_starting_before_or_at_prolated_offset()
    scoretools.get_first_element_starting_strictly_after_prolated_offset()
    scoretools.get_first_element_starting_strictly_before_prolated_offset()
    prolated_systemtools.update_offset_values_of_component()
    verticalitytools.get_vertical_moment_at_prolated_offset_in_expr()

::

    scoretools.copy_and_trim()
    scoretools.get_improper_descendants_of_component_that_cross_offset()
    scoretools.delete_contents_of_container_starting_at_or_after_offset()
    scoretools.delete_contents_of_container_starting_before_or_at_offset()
    scoretools.delete_contents_of_container_starting_strictly_after_offset()
    scoretools.delete_contents_of_container_starting_strictly_before_offset()
    scoretools.get_element_starting_at_exactly_offset()
    scoretools.get_first_element_starting_at_or_after_offset()
    scoretools.get_first_element_starting_before_or_at_offset()
    scoretools.get_first_element_starting_strictly_after_offset()
    scoretools.get_first_element_starting_strictly_before_offset()
    systemtools.update_offset_values_of_component()
    verticalitytools.get_vertical_moment_at_offset_in_expr()

Renamed ``prolated_duration`` to ``offset`` in some functions::

    scoretools.split_component_at_prolated_duration()
    scoretools.split_components_by_prolated_durations()
    scoretools.split_leaf_at_prolated_duration()
    scoretools.split_leaf_at_prolated_duration_and_rest_right_half()

::

    scoretools.split_component_by_duration()
    scoretools.split_components_by_offsets()
    scoretools.split_leaf_by_duration()
    scoretools.split_leaf_by_duration_and_rest_right_half()

Renamed all functions that contained ``as_string``::

    scoretools.report_component_format_contributions_as_string()
    scoretools.report_container_modifications_as_string()
    scoretools.report_meter_distribution_as_string()

::

    formattools.report_component_format_contributions()
    scoretools.report_container_modifications()
    scoretools.report_time_signature_distribution()

Changes to the ``scoretools`` package:

- The ``scoretools.split()`` function no longer 
  implements a ``tie_after keyword``.
  Use the new ``tie_split_notes`` and ``tie_split_rests`` keywords.
  Note that the new ``tie_split_rests``
  keyword defaults to true where the old ``tie_after`` keyword defaulted to false.
  This changes the default behavior of the function.

- Renamed::

    scoretools.extend_left_in_parent_of_component_and_grow_spanners()
    scoretools.extend_left_in_parent_of_component_and_do_not_grow_spanners()

  ::

    scoretools.extend_left_in_parent_of_component(grow_spanners=[True, False])

- Renamed::

    scoretools.splice_of_component_and_grow_spanners()
    scoretools.splice_of_component_and_do_not_grow_spanners()

  ::

    scoretools.splice_of_component(grow_spanners=[True, False])

- Renamed::

    scoretools.number_is_between_prolated_start_and_stop_offsets_of_component()

  ::

    scoretools.number_is_between_start_and_stop_offsets_of_component()

- Renamed::

    scoretools.partition_components_cyclically_by_durations_in_seconds_exactly_with_overhang()
    scoretools.partition_components_cyclically_by_durations_in_seconds_exactly_without_overhang()
    scoretools.partition_components_cyclically_by_durations_in_seconds_ge_with_overhang()
    scoretools.partition_components_cyclically_by_durations_in_seconds_ge_without_overhang()
    scoretools.partition_components_cyclically_by_durations_in_seconds_le_with_overhang()
    scoretools.partition_components_cyclically_by_durations_in_seconds_le_without_overhang()
    scoretools.partition_components_cyclically_by_prolated_durations_exactly_with_overhang()
    scoretools.partition_components_cyclically_by_prolated_durations_exactly_without_overhang()
    scoretools.partition_components_cyclically_by_prolated_durations_ge_with_overhang()
    scoretools.partition_components_cyclically_by_prolated_durations_ge_without_overhang()
    scoretools.partition_components_cyclically_by_prolated_durations_le_with_overhang()
    scoretools.partition_components_cyclically_by_prolated_durations_le_without_overhang()
    scoretools.partition_components_once_by_durations_in_seconds_exactly_with_overhang()
    scoretools.partition_components_once_by_durations_in_seconds_exactly_without_overhang()
    scoretools.partition_components_once_by_durations_in_seconds_ge_with_overhang()
    scoretools.partition_components_once_by_durations_in_seconds_ge_without_overhang()
    scoretools.partition_components_once_by_durations_in_seconds_le_with_overhang()
    scoretools.partition_components_once_by_durations_in_seconds_le_without_overhang()
    scoretools.partition_components_once_by_prolated_durations_exactly_with_overhang()
    scoretools.partition_components_once_by_prolated_durations_exactly_without_overhang()
    scoretools.partition_components_once_by_prolated_durations_ge_with_overhang()
    scoretools.partition_components_once_by_prolated_durations_ge_without_overhang()
    scoretools.partition_components_once_by_prolated_durations_le_with_overhang()
    scoretools.partition_components_once_by_prolated_durations_le_without_overhang()

  ::

    scoretools.partition_components_by_durations_exactly()
    scoretools.partition_components_by_durations_not_less_than()
    scoretools.partition_components_by_durations_not_greater_than()

- Renamed::

    scoretools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners()
    scoretools.split_component_at_prolated_duration_and_fracture_crossing_spanners()

  ::

    scoretools.split_component_by_duration(fracture_spanners=[True, False])

- Renamed::

    scoretools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners()
    scoretools.split_components_cyclically_by_prolated_durations_and_fracture_crossing_spanners()
    scoretools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners()
    scoretools.split_components_once_by_prolated_durations_and_fracture_crossing_spanners()

  ::

    scoretools.split(fracture_spanners=[True, False], cyclic=[True, False])

Changeds to the ``continertools`` package:

- Renamed::

    scoretools.remove_empty_containers_in_expr()

  ::

    scoretools.remove_leafless_containers_in_expr()

- Renamed::

    scoretools.replace_larger_left_half_of_elements_in_container_with_big_endian_rests()
    scoretools.replace_larger_left_half_of_elements_in_container_with_little_endian_rests()
    scoretools.replace_larger_right_half_of_elements_in_container_with_big_endian_rests()
    scoretools.replace_larger_right_half_of_elements_in_container_with_little_endian_rests()
    scoretools.replace_n_edge_elements_in_container_with_big_endian_rests()
    scoretools.replace_n_edge_elements_in_container_with_little_endian_rests()
    scoretools.replace_n_edge_elements_in_container_with_rests()
    scoretools.replace_smaller_left_half_of_elements_in_container_with_big_endian_rests()
    scoretools.replace_smaller_left_half_of_elements_in_container_with_little_endian_rests()
    scoretools.replace_smaller_right_half_of_elements_in_container_with_big_endian_rests()
    scoretools.replace_smaller_right_half_of_elements_in_container_with_little_endian_rests()

  ::

    scoretools.replace_container_slice_with_rests()

- Renamed::

    scoretools.split_container_at_index_and_do_not_fracture_crossing_spanners()
    scoretools.split_container_at_index_and_fracture_crossing_spanners()

  ::

    scoretools.split_container_at_index(fracture_spanners=[True, False])

- Renamed::

    scoretools.split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners()
    scoretools.split_container_cyclically_by_counts_and_fracture_crossing_spanners()
    scoretools.split_container_once_by_counts_and_do_not_fracture_crossing_spanners()
    scoretools.split_container_once_by_counts_and_fracture_crossing_spanners()

  ::

    scoretools.split_container_at_indices(fracture_spanners=[True, False], cyclic=[True, False])

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

    instrumenttools.transpose_notes_and_chords_in_expr_from_sounding_pitch_to_written_pitch()

  ::

    instrumenttools.transpose_from_sounding_pitch_to_written_pitch()

- Renamed::

    instrumenttools.transpose_notes_and_chords_in_expr_from_written_pitch_to_sounding_pitch()

  ::

    instrumenttools.transpose_from_written_pitch_to_sounding_pitch()

Chnages to the ``scoretools`` package:

- Renamed::

    scoretools.fuse_leaves_in_container_once_by_counts_into_big_endian_notes()
    scoretools.fuse_leaves_in_container_once_by_counts_into_big_endian_rests()
    scoretools.fuse_leaves_in_container_once_by_counts_into_little_endian_notes()
    scoretools.fuse_leaves_in_container_once_by_counts_into_little_endian_rests()

  ::

    scoretools.fuse_leaves_in_container_once_by_counts(big_endian=[True, False], klass=None)

- Renamed::

    scoretools.leaf_to_augmented_tuplet_with_n_notes_of_equal_written_duration()
    scoretools.leaf_to_augmented_tuplet_with_proportions()
    scoretools.leaf_to_diminished_tuplet_with_n_notes_of_equal_written_duration()
    scoretools.leaf_to_diminished_tuplet_with_proportions()

  ::

    scoretools.leaf_to_tuplet_with_n_notes_of_equal_written_duration()
    scoretools.leaf_to_tuplet_with_ratio()

- Renamed::

    scoretools.split_leaf_by_duration_and_rest_right_half()

  ::

    scoretools.rest_leaf_at_offset()

- Renamed::

    scoretools.repeat_leaf_and_extend_spanners()
    scoretools.repeat_leaves_in_expr_and_extend_spanners()

  ::

    scoretools.repeat_leaf()
    scoretools.repeat_leaves_in_expr()

Changes to the ``mathtools`` package.

- Removed ``mathtools.partition_integer_into_thirds()``.

Changes to the ``scoretools`` package:

- Renamed::

    scoretools.fill_measures_in_expr_with_meter_denominator_notes()
    scoretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure()
    scoretools.multiply_contents_of_measures_in_expr_and_scale_meter_denominators()
    scoretools.scale_measure_by_multiplier_and_adjust_meter()

  ::

    scoretools.fill_measures_in_expr_with_time_signature_denominator_notes()
    scoretools.move_full_measure_tuplet_prolation_to_measure_time_signature()
    scoretools.multiply_contents_of_measures_in_expr_and_scale_time_signature_denominators()
    scoretools.scale_measure_and_adjust_time_signature()

- Renamed::

    scoretools.fill_measures_in_expr_with_big_endian_notes()
    scoretools.fill_measures_in_expr_with_litte_endian_notes()

  ::

    scoretools.scoretools.fill_measures_in_expr_with_minimal_number_of_notes(big_endian=[True, False])

- Renamed::

    scoretools.extend_measures_in_expr_and_apply_full_measure_tuplets_to_measure_contents()

  ::

    measuretoools.extend_measures_in_expr_and_apply_full_measure_tuplets()

- Renamed::

    scoretools.get_previous_measure_from_component()

  ::

    scoretools.get_previous_measure_from_component()

- Renamed::

    scoretools.multiply_contents_of_measures_in_expr_and_scale_time_signature_denominators()

  ::

    scoretools.multiply_and_scale_contents_of_measures_in_expr()

- Renamed::

    scoretools.pitch_array_row_to_measure()
    scoretools.pitch_array_to_measures()

  ::

    pitchtools.pitch_array_row_to_measure()
    pitchtools.pitch_array_to_measures()

Changes to the ``pitchtools`` package:

- Renamed::

    pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier()
    pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier()
    pitchtools.calculate_harmonic_counterpoint_interval_class_from_named_pitch_to_named_pitch()
    pitchtools.calculate_harmonic_counterpoint_interval_from_named_pitch_to_named_pitch()
    pitchtools.calculate_harmonic_diatonic_interval_class_from_named_pitch_to_named_pitch()
    pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch()

  ::

    pitchtools.NumberedHarmonicIntervalClass.from_pitch_carriers()
    pitchtools.NumberedHarmonicInterval.from_pitch_carriers()
    pitchtools.HarmonicCounterpointIntervalClass.from_pitch_carriers()
    pitchtools.HarmonicCounterpointInterval.from_pitch_carriers()
    pitchtools.NamedHarmonicIntervalClass.from_pitch_carriers()
    pitchtools.NamedHarmonicInterval.from_pitch_carriers()

- Renamed::

    pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier()
    pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier()
    pitchtools.calculate_melodic_counterpoint_interval_class_from_named_pitch_to_named_pitch()
    pitchtools.calculate_melodic_counterpoint_interval_from_named_pitch_to_named_pitch()
    pitchtools.NamedMelodicInterval.from_pitch_carriers_class_from_named_pitch_to_named_pitch()
    pitchtools.NamedMelodicInterval.from_pitch_carriers_from_named_pitch_to_named_pitch()

  ::

    pitchtools.NumberedIntervalClass.from_pitch_carriers()
    pitchtools.NumberedInterval.from_pitch_carriers()
    pitchtools.MelodicCounterpointIntervalClass.from_pitch_carriers()
    pitchtools.MelodicCounterpointInterval.from_pitch_carriers()
    pitchtools.NamedMelodicInterval.from_pitch_carriers_class()
    pitchtools.NamedMelodicInterval.from_pitch_carriers()

- Renamed::

    pitchtools.pitch_class_name_to_diatonic_pitch_class_name_abbreviation_pair()

  ::

    pitchtools.split_pitch_class_name()


- Renamed::

    pitchtools.diatonic_interval_number_and_chromatic_interval_number_to_melodic_diatonic_interval()
 
  ::

    pitchtools.spell_chromatic_interval_number()

- Renamed::

    pitchtools.named_pitches_to_harmonic_chromatic_interval_class_number_dictionary()

  ::

    pitchtools.harmonic_chromatic_interval_class_number_dictionary()

- Renamed::

    pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_abbreviation_octave_number_pair()

  ::

    pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair()

- Renamed::

    pitchtools.list_named_pitch_carriers_in_expr_sorted_by_numbered_pitch_class()

  ::

    pitchtools.sort_named_pitch_carriers_in_expr()

- Renamed::

    pitchtools.named_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary()

  ::

    pitchtools.inversion_equivalent_chromatic_interval_class_number_dictionary()

- Renamed::

    pitchtools.transpose_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number()

  ::

    pitchtools.transpose_pitch_class_number_to_neighbor_of_chromatic_pitch_number()

- Renamed::

    pitchtools.ordered_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers()

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

    pitchtools.set_ascending_named_pitches_on_nontied_pitched_components_in_expr()

  ::

    pitchtools.set_ascending_named_pitches_on_logical_ties_in_expr()

- Renamed::

    pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr()

  ::

    pitchtools.set_ascending_diatonic_pitches_on_logical_ties_in_expr()

- Renamed::

    pitchtools.transpose_pitch_class_number_to_neighbor_of_chromatic_pitch_number()

  ::

    pitchtools.transpose_pitch_class_number_chromatic_pitch_number_neighbor()

Changes to the ``rhythmtreetools`` package:

- Renamed::

    rhythmtreetools.parse_reduced_ly_syntax()

  ::

    lilypondparsertools.parse_reduced_ly_syntax()

Chnages to the ``templatetools`` package:

- Renamed::

    templatetools.GroupedRhythmcStavesScoreTemplate.n

  ::

    templatetools.GroupedRhythmcStavesScoreTemplate.staff_count

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

    sequencetools.split_sequence()

- Renamed::

    sequencetools.split_sequence_extended_to_weights_with_overhang()
    sequencetools.split_sequence_extended_to_weights_without_overhang()

  ::

    sequencetools.split_sequence_extended_to_weights()

Changes to the ``tietools`` package:

- Renamed::

    tietools.logical_tie_to_augmented_tuplet_with_proportions_and_avoid_dots()
    tietools.logical_tie_to_augmented_tuplet_with_proportions_and_encourage_dots()
    tietools.logical_tie_to_diminished_tuplet_with_proportions_and_avoid_dots()
    tietools.logical_tie_to_diminished_tuplet_with_proportions_and_encourage_dots()

  ::

    tietools.logical_tie_to_tuplet_with_ratio()

- Renamed::

    tietools.iterate_nontrivial_logical_ties_forward_in_expr()
    tietools.iterate_nontrivial_logical_ties_backward_in_expr()
    tietools.iterate_pitched_logical_ties_forward_in_expr()
    tietools.iterate_pitched_logical_ties_backward_in_expr()
    tietools.iterate_logical_ties_forward_in_expr()
    tietools.iterate_logical_ties_backward_in_expr()

  ::

    iterationtools.iterate_nontrivial_logical_ties_in_expr(reverse=[True, False])
    iterationtools.iterate_pitched_logical_ties_in_expr(reverse=[True, False])
    iterationtools.iterate_logical_ties_in_expr(reverse=[True, False])

Changes to the ``scoretools`` package:

- Renamed::

    scoretools.is_proper_tuplet_multiplier()

  ::

    durationtools.is_proper_tuplet_multiplier()

- Renamed::

    scoretools.make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots()
    scoretools.make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots()
    scoretools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots()
    scoretools.make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots()

  ::

    scoretools.make_tuplet_from_durations_and_proportions(big_endian=[True, False])

Removed three packages.

- Removed ``constrainttools`` package.

- Removed ``lyricstools`` package.

- Removed ``quantizationtools`` package.
