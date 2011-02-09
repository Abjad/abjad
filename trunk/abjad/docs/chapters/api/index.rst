Abjad API
=========

.. toctree::

Abjad score components
----------------------

.. toctree::
   :maxdepth: 1

   components/Chord/Chord
   components/Container/Container
   components/Measure/Measure
   components/Note/Note
   components/Rest/Rest
   components/Score/Score
   components/Staff/Staff
   components/Tuplet/Tuplet
   components/Voice/Voice


Abjad composition packages
--------------------------

.. toctree::
   :maxdepth: 1



beamtools

.. toctree::
   :maxdepth: 1

   tools/beamtools/get_beam_spanner_attached_to_component
   tools/beamtools/is_component_with_beam_spanner_attached


cfgtools

.. toctree::
   :maxdepth: 1

   tools/cfgtools/get_abjad_revision_string
   tools/cfgtools/get_abjad_version_string
   tools/cfgtools/get_lilypond_version_string
   tools/cfgtools/get_python_version_string
   tools/cfgtools/list_abjad_environment_variables
   tools/cfgtools/list_abjad_templates
   tools/cfgtools/set_default_accidental_spelling


chordtools

.. toctree::
   :maxdepth: 1

   tools/chordtools/Cluster/Cluster
   tools/chordtools/arpeggiate_chord
   tools/chordtools/change_defective_chord_to_note_or_rest
   tools/chordtools/color_chord_note_heads_by_pitch_class_color_map
   tools/chordtools/divide_chord_by_chromatic_pitch_number
   tools/chordtools/divide_chord_by_diatonic_pitch_number
   tools/chordtools/get_arithmetic_mean_of_chord
   tools/chordtools/get_note_head_from_chord_by_pitch
   tools/chordtools/yield_all_subchords_of_chord


componenttools

.. toctree::
   :maxdepth: 1

   tools/componenttools/all_are_components
   tools/componenttools/all_are_components_in_same_parent
   tools/componenttools/all_are_components_in_same_score
   tools/componenttools/all_are_components_in_same_thread
   tools/componenttools/all_are_components_scalable_by_multiplier
   tools/componenttools/all_are_contiguous_components
   tools/componenttools/all_are_contiguous_components_in_same_parent
   tools/componenttools/all_are_contiguous_components_in_same_score
   tools/componenttools/all_are_contiguous_components_in_same_thread
   tools/componenttools/all_are_orphan_components
   tools/componenttools/all_are_thread_contiguous_components
   tools/componenttools/clone_and_partition_governed_component_subtree_by_leaf_counts
   tools/componenttools/clone_components_and_covered_spanners
   tools/componenttools/clone_components_and_fracture_crossing_spanners
   tools/componenttools/clone_components_and_immediate_parent_of_first_component
   tools/componenttools/clone_components_and_remove_all_spanners
   tools/componenttools/clone_governed_component_subtree_by_leaf_range
   tools/componenttools/clone_governed_component_subtree_from_prolated_duration_to
   tools/componenttools/component_to_parentage_signature
   tools/componenttools/component_to_pitch_and_rhythm_skeleton
   tools/componenttools/component_to_pitch_and_rhythm_skeleton_with_interface_attributes
   tools/componenttools/component_to_score_depth
   tools/componenttools/component_to_score_index
   tools/componenttools/component_to_score_root
   tools/componenttools/component_to_tuplet_depth
   tools/componenttools/cut_component_at_prolated_duration
   tools/componenttools/extend_in_parent_of_component_and_do_not_grow_spanners
   tools/componenttools/extend_in_parent_of_component_and_grow_spanners
   tools/componenttools/extend_left_in_parent_of_component_and_do_not_grow_spanners
   tools/componenttools/extend_left_in_parent_of_component_and_grow_spanners
   tools/componenttools/get_component_start_offset
   tools/componenttools/get_component_start_offset_in_seconds
   tools/componenttools/get_component_stop_offset
   tools/componenttools/get_component_stop_offset_in_seconds
   tools/componenttools/get_first_component_in_expr_with_name
   tools/componenttools/get_first_component_with_name_in_improper_parentage_of_component
   tools/componenttools/get_first_component_with_name_in_proper_parentage_of_component
   tools/componenttools/get_first_instance_of_klass_in_improper_parentage_of_component
   tools/componenttools/get_first_instance_of_klass_in_proper_parentage_of_component
   tools/componenttools/get_improper_parentage_of_component
   tools/componenttools/get_likely_multiplier_of_components
   tools/componenttools/get_nth_component_in_expr
   tools/componenttools/get_nth_namesake_from_component
   tools/componenttools/get_parent_and_start_stop_indices_of_components
   tools/componenttools/get_proper_parentage_of_component
   tools/componenttools/is_beamable_component
   tools/componenttools/is_orphan_component
   tools/componenttools/is_well_formed_component
   tools/componenttools/iterate_components_backward_in_expr
   tools/componenttools/iterate_components_depth_first
   tools/componenttools/iterate_components_forward_in_expr
   tools/componenttools/iterate_namesakes_backward_from_component
   tools/componenttools/iterate_namesakes_forward_from_component
   tools/componenttools/iterate_timeline_backward_from_component
   tools/componenttools/iterate_timeline_backward_in_expr
   tools/componenttools/iterate_timeline_forward_from_component
   tools/componenttools/iterate_timeline_forward_in_expr
   tools/componenttools/list_badly_formed_components_in_expr
   tools/componenttools/list_improper_contents_of_component_that_cross_prolated_offset
   tools/componenttools/list_leftmost_components_with_prolated_duration_at_most
   tools/componenttools/move_component_subtree_to_right_in_immediate_parent_of_component
   tools/componenttools/move_parentage_and_spanners_from_components_to_components
   tools/componenttools/number_is_between_prolated_start_and_stop_offsets_of_component
   tools/componenttools/number_is_between_start_and_stop_offsets_of_component_in_seconds
   tools/componenttools/partition_components_cyclically_by_durations_in_seconds_exactly_with_overhang
   tools/componenttools/partition_components_cyclically_by_durations_in_seconds_exactly_without_overhang
   tools/componenttools/partition_components_cyclically_by_durations_in_seconds_ge_with_overhang
   tools/componenttools/partition_components_cyclically_by_durations_in_seconds_ge_without_overhang
   tools/componenttools/partition_components_cyclically_by_durations_in_seconds_le_with_overhang
   tools/componenttools/partition_components_cyclically_by_durations_in_seconds_le_without_overhang
   tools/componenttools/partition_components_cyclically_by_prolated_durations_exactly_with_overhang
   tools/componenttools/partition_components_cyclically_by_prolated_durations_exactly_without_overhang
   tools/componenttools/partition_components_cyclically_by_prolated_durations_ge_with_overhang
   tools/componenttools/partition_components_cyclically_by_prolated_durations_ge_without_overhang
   tools/componenttools/partition_components_cyclically_by_prolated_durations_le_with_overhang
   tools/componenttools/partition_components_cyclically_by_prolated_durations_le_without_overhang
   tools/componenttools/partition_components_once_by_durations_in_seconds_exactly_with_overhang
   tools/componenttools/partition_components_once_by_durations_in_seconds_exactly_without_overhang
   tools/componenttools/partition_components_once_by_durations_in_seconds_ge_with_overhang
   tools/componenttools/partition_components_once_by_durations_in_seconds_ge_without_overhang
   tools/componenttools/partition_components_once_by_durations_in_seconds_le_with_overhang
   tools/componenttools/partition_components_once_by_durations_in_seconds_le_without_overhang
   tools/componenttools/partition_components_once_by_prolated_durations_exactly_with_overhang
   tools/componenttools/partition_components_once_by_prolated_durations_exactly_without_overhang
   tools/componenttools/partition_components_once_by_prolated_durations_ge_with_overhang
   tools/componenttools/partition_components_once_by_prolated_durations_ge_without_overhang
   tools/componenttools/partition_components_once_by_prolated_durations_le_with_overhang
   tools/componenttools/partition_components_once_by_prolated_durations_le_without_overhang
   tools/componenttools/remove_component_subtree_from_score_and_spanners
   tools/componenttools/replace_components_with_children_of_components
   tools/componenttools/report_component_format_contributions_as_string
   tools/componenttools/report_component_format_contributions_to_screen
   tools/componenttools/split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners
   tools/componenttools/split_component_at_prolated_duration_and_fracture_crossing_spanners
   tools/componenttools/split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners
   tools/componenttools/split_components_cyclically_by_prolated_durations_and_fracture_crossing_spanners
   tools/componenttools/split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners
   tools/componenttools/split_components_once_by_prolated_durations_and_fracture_crossing_spanners
   tools/componenttools/sum_duration_of_components_in_seconds
   tools/componenttools/sum_preprolated_duration_of_components
   tools/componenttools/sum_prolated_duration_of_components
   tools/componenttools/tabulate_well_formedness_violations_in_expr
   tools/componenttools/yield_components_grouped_by_preprolated_duration
   tools/componenttools/yield_components_grouped_by_prolated_duration
   tools/componenttools/yield_topmost_components_grouped_by_type
   tools/componenttools/yield_topmost_components_of_klass_grouped_by_type


containertools

.. toctree::
   :maxdepth: 1

   tools/containertools/color_contents_of_container
   tools/containertools/delete_contents_of_container
   tools/containertools/delete_contents_of_container_starting_at_or_after_prolated_offset
   tools/containertools/delete_contents_of_container_starting_before_or_at_prolated_offset
   tools/containertools/delete_contents_of_container_starting_strictly_after_prolated_offset
   tools/containertools/delete_contents_of_container_starting_strictly_before_prolated_offset
   tools/containertools/fuse_like_named_contiguous_containers_in_expr
   tools/containertools/get_element_starting_at_exactly_prolated_offset
   tools/containertools/get_first_element_starting_at_or_after_prolated_offset
   tools/containertools/get_first_element_starting_before_or_at_prolated_offset
   tools/containertools/get_first_element_starting_strictly_after_prolated_offset
   tools/containertools/get_first_element_starting_strictly_before_prolated_offset
   tools/containertools/insert_component_and_do_not_fracture_crossing_spanners
   tools/containertools/insert_component_and_fracture_crossing_spanners
   tools/containertools/move_parentage_children_and_spanners_from_components_to_empty_container
   tools/containertools/remove_empty_containers_in_expr
   tools/containertools/repeat_contents_of_container
   tools/containertools/repeat_last_n_elements_of_container
   tools/containertools/replace_contents_of_target_container_with_contents_of_source_container
   tools/containertools/replace_larger_left_half_of_elements_in_container_with_big_endian_rests
   tools/containertools/replace_larger_left_half_of_elements_in_container_with_little_endian_rests
   tools/containertools/replace_larger_right_half_of_elements_in_container_with_big_endian_rests
   tools/containertools/replace_larger_right_half_of_elements_in_container_with_little_endian_rests
   tools/containertools/replace_n_edge_elements_in_container_with_big_endian_rests
   tools/containertools/replace_n_edge_elements_in_container_with_little_endian_rests
   tools/containertools/replace_n_edge_elements_in_container_with_rests
   tools/containertools/replace_smaller_left_half_of_elements_in_container_with_big_endian_rests
   tools/containertools/replace_smaller_left_half_of_elements_in_container_with_little_endian_rests
   tools/containertools/replace_smaller_right_half_of_elements_in_container_with_big_endian_rests
   tools/containertools/replace_smaller_right_half_of_elements_in_container_with_little_endian_rests
   tools/containertools/report_container_modifications_as_string
   tools/containertools/report_container_modifications_to_screen
   tools/containertools/reverse_contents_of_container
   tools/containertools/scale_contents_of_container
   tools/containertools/set_container_multiplier
   tools/containertools/split_container_at_index_and_do_not_fracture_crossing_spanners
   tools/containertools/split_container_at_index_and_fracture_crossing_spanners
   tools/containertools/split_container_cyclically_by_counts_and_do_not_fracture_crossing_spanners
   tools/containertools/split_container_cyclically_by_counts_and_fracture_crossing_spanners
   tools/containertools/split_container_once_by_counts_and_do_not_fracture_crossing_spanners
   tools/containertools/split_container_once_by_counts_and_fracture_crossing_spanners


contexttools

.. toctree::
   :maxdepth: 1

   tools/contexttools/ClefMark/ClefMark
   tools/contexttools/ContextMark/ContextMark
   tools/contexttools/DynamicMark/DynamicMark
   tools/contexttools/InstrumentMark/InstrumentMark
   tools/contexttools/KeySignatureMark/KeySignatureMark
   tools/contexttools/StaffChangeMark/StaffChangeMark
   tools/contexttools/TempoMark/TempoMark
   tools/contexttools/TimeSignatureMark/TimeSignatureMark
   tools/contexttools/detach_context_marks_attached_to_start_component
   tools/contexttools/get_all_context_marks_attached_to_any_improper_parent_of_component
   tools/contexttools/get_context_marks_attached_to_start_component
   tools/contexttools/get_dynamic_marks_attached_to_start_component
   tools/contexttools/get_effective_clef
   tools/contexttools/get_effective_dynamic
   tools/contexttools/get_effective_instrument
   tools/contexttools/get_effective_key_signature
   tools/contexttools/get_effective_mark
   tools/contexttools/get_effective_staff
   tools/contexttools/get_effective_tempo
   tools/contexttools/get_effective_time_signature
   tools/contexttools/set_accidental_style_on_sequential_contexts_in_expr


durtools

.. toctree::
   :maxdepth: 1

   tools/durtools/assignable_rational_to_dot_count
   tools/durtools/assignable_rational_to_lilypond_duration_string
   tools/durtools/duration_pair_to_prolation_string
   tools/durtools/duration_token_to_big_endian_list_of_assignable_duration_pairs
   tools/durtools/duration_token_to_reduced_duration_pair
   tools/durtools/group_duration_tokens_by_implied_prolation
   tools/durtools/is_assignable_rational
   tools/durtools/is_binary_rational
   tools/durtools/is_duration_pair
   tools/durtools/is_lilypond_duration_name
   tools/durtools/is_lilypond_duration_string
   tools/durtools/lilypond_duration_string_to_rational
   tools/durtools/lilypond_duration_string_to_rational_list
   tools/durtools/multiply_duration_pair
   tools/durtools/multiply_duration_pair_and_reduce_factors
   tools/durtools/multiply_duration_pair_and_try_to_preserve_numerator
   tools/durtools/numeric_seconds_to_clock_string
   tools/durtools/numeric_seconds_to_escaped_clock_string
   tools/durtools/positive_integer_to_implied_prolation_multipler
   tools/durtools/rational_to_duration_pair_with_multiple_of_specified_integer_denominator
   tools/durtools/rational_to_duration_pair_with_specified_integer_denominator
   tools/durtools/rational_to_equal_or_greater_assignable_rational
   tools/durtools/rational_to_equal_or_greater_binary_rational
   tools/durtools/rational_to_equal_or_lesser_assignable_rational
   tools/durtools/rational_to_equal_or_lesser_binary_rational
   tools/durtools/rational_to_flag_count
   tools/durtools/rational_to_fraction_string
   tools/durtools/rational_to_prolation_string
   tools/durtools/rational_to_proper_fraction
   tools/durtools/rewrite_rational_under_new_tempo
   tools/durtools/yield_all_assignable_rationals_in_cantor_diagonalized_order
   tools/durtools/yield_all_positive_integer_pairs_in_cantor_diagonalized_order
   tools/durtools/yield_all_positive_rationals_in_cantor_diagonalized_order
   tools/durtools/yield_all_positive_rationals_in_cantor_diagonalized_order_uniquely
   tools/durtools/yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order


formattools

.. toctree::
   :maxdepth: 1

   tools/formattools/format_input_lines_as_doc_string
   tools/formattools/format_input_lines_as_regression_test


gracetools

.. toctree::
   :maxdepth: 1

   tools/gracetools/Grace/Grace
   tools/gracetools/iterate_components_and_grace_containers_forward_in_expr


iotools

.. toctree::
   :maxdepth: 1

   tools/iotools/f
   tools/iotools/get_last_output_file_name
   tools/iotools/get_next_output_file_name
   tools/iotools/log
   tools/iotools/ly
   tools/iotools/parse_lilypond_input_string
   tools/iotools/pdf
   tools/iotools/play
   tools/iotools/profile_expr
   tools/iotools/redo
   tools/iotools/remove_abjad_pyc_files
   tools/iotools/save_last_ly_as
   tools/iotools/save_last_pdf_as
   tools/iotools/show
   tools/iotools/write_expr_to_ly
   tools/iotools/write_expr_to_ly_and_to_pdf_and_show
   tools/iotools/write_expr_to_pdf


layouttools

.. toctree::
   :maxdepth: 1

   tools/layouttools/FixedStaffPositioning/FixedStaffPositioning
   tools/layouttools/LayoutSchema/LayoutSchema
   tools/layouttools/StaffAlignmentDistances/StaffAlignmentDistances
   tools/layouttools/StaffAlignmentOffsets/StaffAlignmentOffsets
   tools/layouttools/SystemYOffsets/SystemYOffsets
   tools/layouttools/apply_fixed_staff_positioning
   tools/layouttools/apply_layout_schema
   tools/layouttools/set_line_breaks_cyclically_by_line_duration_ge
   tools/layouttools/set_line_breaks_cyclically_by_line_duration_in_seconds_ge


leaftools

.. toctree::
   :maxdepth: 1

   tools/leaftools/change_written_leaf_duration_and_preserve_preprolated_leaf_duration
   tools/leaftools/color_leaf
   tools/leaftools/color_leaves_in_expr
   tools/leaftools/copy_written_duration_and_multiplier_from_leaf_to_leaf
   tools/leaftools/divide_leaf_meiotically
   tools/leaftools/divide_leaves_in_expr_meiotically
   tools/leaftools/expr_has_leaf_with_dotted_written_duration
   tools/leaftools/fuse_leaves_big_endian
   tools/leaftools/fuse_leaves_in_container_once_by_counts_into_big_endian_notes
   tools/leaftools/fuse_leaves_in_container_once_by_counts_into_big_endian_rests
   tools/leaftools/fuse_leaves_in_container_once_by_counts_into_little_endian_notes
   tools/leaftools/fuse_leaves_in_container_once_by_counts_into_little_endian_rests
   tools/leaftools/fuse_leaves_in_tie_chain_by_immediate_parent_big_endian
   tools/leaftools/fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang
   tools/leaftools/get_composite_offset_difference_series_from_leaves_in_expr
   tools/leaftools/get_composite_offset_series_from_leaves_in_expr
   tools/leaftools/get_leaf_at_index_in_measure_number_in_expr
   tools/leaftools/get_nth_leaf_in_expr
   tools/leaftools/get_nth_leaf_in_thread_from_leaf
   tools/leaftools/is_bar_line_crossing_leaf
   tools/leaftools/iterate_leaf_pairs_forward_in_expr
   tools/leaftools/iterate_leaves_backward_in_expr
   tools/leaftools/iterate_leaves_forward_in_expr
   tools/leaftools/label_leaves_in_expr_with_leaf_depth
   tools/leaftools/label_leaves_in_expr_with_leaf_durations
   tools/leaftools/label_leaves_in_expr_with_leaf_indices
   tools/leaftools/label_leaves_in_expr_with_leaf_numbers
   tools/leaftools/label_leaves_in_expr_with_melodic_chromatic_interval_classes
   tools/leaftools/label_leaves_in_expr_with_melodic_chromatic_intervals
   tools/leaftools/label_leaves_in_expr_with_melodic_counterpoint_interval_classes
   tools/leaftools/label_leaves_in_expr_with_melodic_counterpoint_intervals
   tools/leaftools/label_leaves_in_expr_with_melodic_diatonic_interval_classes
   tools/leaftools/label_leaves_in_expr_with_melodic_diatonic_intervals
   tools/leaftools/label_leaves_in_expr_with_pitch_class_numbers
   tools/leaftools/label_leaves_in_expr_with_pitch_numbers
   tools/leaftools/label_leaves_in_expr_with_prolated_leaf_duration
   tools/leaftools/label_leaves_in_expr_with_tuplet_depth
   tools/leaftools/label_leaves_in_expr_with_written_leaf_duration
   tools/leaftools/leaf_to_augmented_tuplet_with_n_notes_of_equal_written_duration
   tools/leaftools/leaf_to_augmented_tuplet_with_proportions
   tools/leaftools/leaf_to_diminished_tuplet_with_n_notes_of_equal_written_duration
   tools/leaftools/leaf_to_diminished_tuplet_with_proportions
   tools/leaftools/list_prolated_durations_of_leaves_in_expr
   tools/leaftools/list_written_durations_of_leaves_in_expr
   tools/leaftools/make_leaves
   tools/leaftools/remove_leaf_and_shrink_durated_parent_containers
   tools/leaftools/remove_markup_from_leaves_in_expr
   tools/leaftools/repeat_leaf_and_extend_spanners
   tools/leaftools/repeat_leaves_in_expr_and_extend_spanners
   tools/leaftools/scale_preprolated_leaf_duration
   tools/leaftools/set_preprolated_leaf_duration
   tools/leaftools/show_leaves
   tools/leaftools/split_leaf_at_prolated_duration_and_rest_right_half


lilyfiletools

.. toctree::
   :maxdepth: 1

   tools/lilyfiletools/AbjadRevisionToken/AbjadRevisionToken
   tools/lilyfiletools/BookBlock/BookBlock
   tools/lilyfiletools/BookpartBlock/BookpartBlock
   tools/lilyfiletools/DateTimeToken/DateTimeToken
   tools/lilyfiletools/HeaderBlock/HeaderBlock
   tools/lilyfiletools/LayoutBlock/LayoutBlock
   tools/lilyfiletools/LilyFile/LilyFile
   tools/lilyfiletools/LilyPondLanguageToken/LilyPondLanguageToken
   tools/lilyfiletools/LilyPondVersionToken/LilyPondVersionToken
   tools/lilyfiletools/MidiBlock/MidiBlock
   tools/lilyfiletools/PaperBlock/PaperBlock
   tools/lilyfiletools/ScoreBlock/ScoreBlock
   tools/lilyfiletools/make_basic_lily_file


marktools

.. toctree::
   :maxdepth: 1

   tools/marktools/Annotation/Annotation
   tools/marktools/Articulation/Articulation
   tools/marktools/Comment/Comment
   tools/marktools/LilyPondCommandMark/LilyPondCommandMark
   tools/marktools/Mark/Mark
   tools/marktools/detach_annotations_attached_to_component
   tools/marktools/detach_comments_attached_to_component
   tools/marktools/detach_lilypond_command_marks_attached_to_component
   tools/marktools/get_all_marks_attached_to_component
   tools/marktools/get_annotation_attached_to_component
   tools/marktools/get_annotations_attached_to_component
   tools/marktools/get_articulations_attached_to_component
   tools/marktools/get_comments_attached_to_component
   tools/marktools/get_lilypond_command_marks_attached_to_component
   tools/marktools/is_component_with_lilypond_command_mark_attached


markuptools

.. toctree::
   :maxdepth: 1

   tools/markuptools/Markup/Markup
   tools/markuptools/get_markup_attached_to_component
   tools/markuptools/make_big_centered_page_number_markup
   tools/markuptools/remove_markup_attached_to_component


mathtools

.. toctree::
   :maxdepth: 1

   tools/mathtools/arithmetic_mean
   tools/mathtools/binomial_coefficient
   tools/mathtools/cumulative_products
   tools/mathtools/cumulative_signed_weights
   tools/mathtools/cumulative_sums
   tools/mathtools/cumulative_sums_zero
   tools/mathtools/difference_series
   tools/mathtools/divide_number_by_ratio
   tools/mathtools/divisors
   tools/mathtools/factors
   tools/mathtools/get_shared_numeric_sign
   tools/mathtools/greatest_common_divisor
   tools/mathtools/greatest_multiple_less_equal
   tools/mathtools/greatest_power_of_two_less_equal
   tools/mathtools/integer_equivalent_number_to_integer
   tools/mathtools/integer_to_base_k_tuple
   tools/mathtools/integer_to_binary_string
   tools/mathtools/interpolate_cosine
   tools/mathtools/interpolate_divide
   tools/mathtools/interpolate_divide_multiple
   tools/mathtools/interpolate_exponential
   tools/mathtools/interpolate_linear
   tools/mathtools/is_assignable_integer
   tools/mathtools/is_dotted_integer
   tools/mathtools/is_integer_equivalent_number
   tools/mathtools/is_negative_integer
   tools/mathtools/is_nonnegative_integer
   tools/mathtools/is_nonnegative_integer_power_of_two
   tools/mathtools/is_positive_integer
   tools/mathtools/least_common_multiple
   tools/mathtools/least_multiple_greater_equal
   tools/mathtools/least_power_of_two_greater_equal
   tools/mathtools/next_integer_partition
   tools/mathtools/partition_integer_by_ratio
   tools/mathtools/partition_integer_into_canonic_parts
   tools/mathtools/partition_integer_into_halves
   tools/mathtools/partition_integer_into_thirds
   tools/mathtools/partition_integer_into_units
   tools/mathtools/remove_powers_of_two
   tools/mathtools/sign
   tools/mathtools/trivial_float_to_int
   tools/mathtools/weight
   tools/mathtools/yield_all_compositions_of_integer
   tools/mathtools/yield_all_partitions_of_integer


measuretools

.. toctree::
   :maxdepth: 1

   tools/measuretools/AnonymousMeasure/AnonymousMeasure
   tools/measuretools/DynamicMeasure/DynamicMeasure
   tools/measuretools/append_spacer_skip_to_underfull_measure
   tools/measuretools/append_spacer_skips_to_underfull_measures_in_expr
   tools/measuretools/apply_beam_spanner_to_measure
   tools/measuretools/apply_beam_spanners_to_measures_in_expr
   tools/measuretools/apply_complex_beam_spanner_to_measure
   tools/measuretools/apply_complex_beam_spanners_to_measures_in_expr
   tools/measuretools/apply_durated_complex_beam_spanner_to_measures
   tools/measuretools/apply_full_measure_tuplets_to_contents_of_measures_in_expr
   tools/measuretools/color_measure
   tools/measuretools/color_nonbinary_measures_in_expr
   tools/measuretools/comment_measures_in_container_with_measure_numbers
   tools/measuretools/extend_measures_in_expr_and_apply_full_measure_tuplets_to_measure_contents
   tools/measuretools/fill_measures_in_expr_with_big_endian_notes
   tools/measuretools/fill_measures_in_expr_with_full_measure_spacer_skips
   tools/measuretools/fill_measures_in_expr_with_little_endian_notes
   tools/measuretools/fill_measures_in_expr_with_meter_denominator_notes
   tools/measuretools/fill_measures_in_expr_with_repeated_notes
   tools/measuretools/fuse_contiguous_measures_in_container_cyclically_by_counts
   tools/measuretools/fuse_measures
   tools/measuretools/get_next_measure_from_component
   tools/measuretools/get_nth_measure_in_expr
   tools/measuretools/get_one_indexed_measure_number_in_expr
   tools/measuretools/get_prev_measure_from_component
   tools/measuretools/iterate_measures_backward_in_expr
   tools/measuretools/iterate_measures_forward_in_expr
   tools/measuretools/make_rigid_measures_with_full_measure_spacer_skips
   tools/measuretools/move_measure_prolation_to_full_measure_tuplet
   tools/measuretools/move_prolation_of_full_measure_tuplet_to_meter_of_measure
   tools/measuretools/multiply_contents_of_measures_in_expr
   tools/measuretools/multiply_contents_of_measures_in_expr_and_scale_meter_denominators
   tools/measuretools/pad_measures_in_expr_with_rests
   tools/measuretools/pad_measures_in_expr_with_skips
   tools/measuretools/pitch_array_row_to_measure
   tools/measuretools/pitch_array_to_measures
   tools/measuretools/replace_contents_of_measures_in_expr
   tools/measuretools/report_meter_distribution_as_string
   tools/measuretools/report_meter_distribution_to_screen
   tools/measuretools/scale_contents_of_measures_in_expr
   tools/measuretools/scale_measure_by_multiplier_and_adjust_meter
   tools/measuretools/scale_measure_denominator_and_adjust_measure_contents
   tools/measuretools/set_measure_denominator_and_adjust_numerator


metertools

.. toctree::
   :maxdepth: 1

   tools/metertools/Meter/Meter
   tools/metertools/duration_and_possible_denominators_to_meter
   tools/metertools/get_nonbinary_factor_from_meter_denominator
   tools/metertools/is_meter_token
   tools/metertools/is_meter_with_equivalent_binary_representation
   tools/metertools/list_meters_of_measures_in_expr
   tools/metertools/meter_to_binary_meter


notetools

.. toctree::
   :maxdepth: 1

   tools/notetools/NaturalHarmonic/NaturalHarmonic
   tools/notetools/NoteHead/NoteHead
   tools/notetools/add_artificial_harmonic_to_note
   tools/notetools/color_note_head_by_numeric_chromatic_pitch_class_color_map
   tools/notetools/iterate_notes_backward_in_expr
   tools/notetools/iterate_notes_forward_in_expr
   tools/notetools/make_accelerating_notes_with_lilypond_multipliers
   tools/notetools/make_notes
   tools/notetools/make_percussion_note
   tools/notetools/make_quarter_notes_with_lilypond_multipliers
   tools/notetools/make_repeated_notes
   tools/notetools/make_repeated_notes_from_time_signature
   tools/notetools/make_repeated_notes_from_time_signatures
   tools/notetools/make_repeated_notes_with_shorter_notes_at_end


pitchtools

.. toctree::
   :maxdepth: 1

   tools/pitchtools/Accidental/Accidental
   tools/pitchtools/HarmonicChromaticInterval/HarmonicChromaticInterval
   tools/pitchtools/HarmonicChromaticIntervalClass/HarmonicChromaticIntervalClass
   tools/pitchtools/HarmonicChromaticIntervalClassVector/HarmonicChromaticIntervalClassVector
   tools/pitchtools/HarmonicChromaticIntervalSegment/HarmonicChromaticIntervalSegment
   tools/pitchtools/HarmonicChromaticIntervalSet/HarmonicChromaticIntervalSet
   tools/pitchtools/HarmonicCounterpointInterval/HarmonicCounterpointInterval
   tools/pitchtools/HarmonicCounterpointIntervalClass/HarmonicCounterpointIntervalClass
   tools/pitchtools/HarmonicDiatonicInterval/HarmonicDiatonicInterval
   tools/pitchtools/HarmonicDiatonicIntervalClass/HarmonicDiatonicIntervalClass
   tools/pitchtools/HarmonicDiatonicIntervalClassSet/HarmonicDiatonicIntervalClassSet
   tools/pitchtools/HarmonicDiatonicIntervalSegment/HarmonicDiatonicIntervalSegment
   tools/pitchtools/HarmonicDiatonicIntervalSet/HarmonicDiatonicIntervalSet
   tools/pitchtools/InversionEquivalentChromaticIntervalClass/InversionEquivalentChromaticIntervalClass
   tools/pitchtools/InversionEquivalentChromaticIntervalClassSegment/InversionEquivalentChromaticIntervalClassSegment
   tools/pitchtools/InversionEquivalentChromaticIntervalClassSet/InversionEquivalentChromaticIntervalClassSet
   tools/pitchtools/InversionEquivalentChromaticIntervalClassVector/InversionEquivalentChromaticIntervalClassVector
   tools/pitchtools/InversionEquivalentDiatonicIntervalClass/InversionEquivalentDiatonicIntervalClass
   tools/pitchtools/InversionEquivalentDiatonicIntervalClassSegment/InversionEquivalentDiatonicIntervalClassSegment
   tools/pitchtools/InversionEquivalentDiatonicIntervalClassVector/InversionEquivalentDiatonicIntervalClassVector
   tools/pitchtools/MelodicChromaticInterval/MelodicChromaticInterval
   tools/pitchtools/MelodicChromaticIntervalClass/MelodicChromaticIntervalClass
   tools/pitchtools/MelodicChromaticIntervalClassSegment/MelodicChromaticIntervalClassSegment
   tools/pitchtools/MelodicChromaticIntervalClassVector/MelodicChromaticIntervalClassVector
   tools/pitchtools/MelodicChromaticIntervalSegment/MelodicChromaticIntervalSegment
   tools/pitchtools/MelodicChromaticIntervalSet/MelodicChromaticIntervalSet
   tools/pitchtools/MelodicCounterpointInterval/MelodicCounterpointInterval
   tools/pitchtools/MelodicCounterpointIntervalClass/MelodicCounterpointIntervalClass
   tools/pitchtools/MelodicDiatonicInterval/MelodicDiatonicInterval
   tools/pitchtools/MelodicDiatonicIntervalClass/MelodicDiatonicIntervalClass
   tools/pitchtools/MelodicDiatonicIntervalSegment/MelodicDiatonicIntervalSegment
   tools/pitchtools/MelodicDiatonicIntervalSet/MelodicDiatonicIntervalSet
   tools/pitchtools/NamedChromaticPitch/NamedChromaticPitch
   tools/pitchtools/NamedChromaticPitchClass/NamedChromaticPitchClass
   tools/pitchtools/NamedChromaticPitchClassSegment/NamedChromaticPitchClassSegment
   tools/pitchtools/NamedChromaticPitchClassSet/NamedChromaticPitchClassSet
   tools/pitchtools/NamedChromaticPitchSegment/NamedChromaticPitchSegment
   tools/pitchtools/NamedChromaticPitchSet/NamedChromaticPitchSet
   tools/pitchtools/NamedChromaticPitchVector/NamedChromaticPitchVector
   tools/pitchtools/NamedDiatonicPitch/NamedDiatonicPitch
   tools/pitchtools/NamedDiatonicPitchClass/NamedDiatonicPitchClass
   tools/pitchtools/NumberedChromaticPitch/NumberedChromaticPitch
   tools/pitchtools/NumberedChromaticPitchClass/NumberedChromaticPitchClass
   tools/pitchtools/NumberedChromaticPitchClassColorMap/NumberedChromaticPitchClassColorMap
   tools/pitchtools/NumberedChromaticPitchClassSegment/NumberedChromaticPitchClassSegment
   tools/pitchtools/NumberedChromaticPitchClassSet/NumberedChromaticPitchClassSet
   tools/pitchtools/NumberedChromaticPitchClassVector/NumberedChromaticPitchClassVector
   tools/pitchtools/NumberedDiatonicPitch/NumberedDiatonicPitch
   tools/pitchtools/NumberedDiatonicPitchClass/NumberedDiatonicPitchClass
   tools/pitchtools/PitchRange/PitchRange
   tools/pitchtools/TwelveToneRow/TwelveToneRow
   tools/pitchtools/all_are_chromatic_pitch_class_name_octave_number_pairs
   tools/pitchtools/apply_accidental_to_named_chromatic_pitch
   tools/pitchtools/apply_octavation_spanner_to_pitched_components
   tools/pitchtools/calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier
   tools/pitchtools/calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier
   tools/pitchtools/calculate_harmonic_counterpoint_interval_class_from_named_pchromatic_pitch_to_named_chromatic_pitch
   tools/pitchtools/calculate_harmonic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch
   tools/pitchtools/calculate_harmonic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch
   tools/pitchtools/calculate_harmonic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch
   tools/pitchtools/calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier
   tools/pitchtools/calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier
   tools/pitchtools/calculate_melodic_counterpoint_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch
   tools/pitchtools/calculate_melodic_counterpoint_interval_from_named_chromatic_pitch_to_named_chromatic_pitch
   tools/pitchtools/calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch
   tools/pitchtools/calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch
   tools/pitchtools/chromatic_pitch_class_name_to_chromatic_pitch_class_number
   tools/pitchtools/chromatic_pitch_class_name_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_pair
   tools/pitchtools/chromatic_pitch_class_number_to_chromatic_pitch_class_name
   tools/pitchtools/chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats
   tools/pitchtools/chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps
   tools/pitchtools/chromatic_pitch_name_to_chromatic_pitch_class_name
   tools/pitchtools/chromatic_pitch_name_to_chromatic_pitch_class_number
   tools/pitchtools/chromatic_pitch_name_to_chromatic_pitch_number
   tools/pitchtools/chromatic_pitch_name_to_diatonic_pitch_class_name
   tools/pitchtools/chromatic_pitch_name_to_diatonic_pitch_class_number
   tools/pitchtools/chromatic_pitch_name_to_diatonic_pitch_name
   tools/pitchtools/chromatic_pitch_name_to_diatonic_pitch_number
   tools/pitchtools/chromatic_pitch_name_to_octave_number
   tools/pitchtools/chromatic_pitch_names_string_to_named_chromatic_pitch_list
   tools/pitchtools/chromatic_pitch_number_and_accidental_semitones_to_octave_number
   tools/pitchtools/chromatic_pitch_number_diatonic_pitch_class_name_to_alphabetic_accidental_abbreviation_octave_number_pair
   tools/pitchtools/chromatic_pitch_number_to_chromatic_pitch_class_number
   tools/pitchtools/chromatic_pitch_number_to_chromatic_pitch_name
   tools/pitchtools/chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple
   tools/pitchtools/chromatic_pitch_number_to_octave_number
   tools/pitchtools/clef_and_staff_position_number_to_named_chromatic_pitch
   tools/pitchtools/diatonic_interval_number_and_chromatic_interval_number_to_melodic_diatonic_interval
   tools/pitchtools/diatonic_pitch_class_name_to_chromatic_pitch_class_number
   tools/pitchtools/diatonic_pitch_class_name_to_diatonic_pitch_class_number
   tools/pitchtools/diatonic_pitch_class_name_to_one_indexed_diatonic_scale_degree_number
   tools/pitchtools/diatonic_pitch_class_number_to_chromatic_pitch_class_number
   tools/pitchtools/diatonic_pitch_class_number_to_diatonic_pitch_class_name
   tools/pitchtools/diatonic_pitch_name_to_diatonic_pitch_class_name
   tools/pitchtools/diatonic_pitch_name_to_diatonic_pitch_number
   tools/pitchtools/diatonic_pitch_number_to_diatonic_pitch_class_name
   tools/pitchtools/diatonic_pitch_number_to_diatonic_pitch_class_number
   tools/pitchtools/diatonic_pitch_number_to_diatonic_pitch_name
   tools/pitchtools/expr_has_duplicate_named_chromatic_pitch
   tools/pitchtools/expr_has_duplicate_numeric_chromatic_pitch_class
   tools/pitchtools/expr_to_melodic_chromatic_interval_segment
   tools/pitchtools/get_named_chromatic_pitch_from_pitch_carrier
   tools/pitchtools/get_numeric_chromatic_pitch_class_from_pitch_carrier
   tools/pitchtools/insert_and_transpose_nested_subruns_in_chromatic_pitch_class_number_list
   tools/pitchtools/inventory_aggregate_subsets
   tools/pitchtools/inventory_inversion_equivalent_diatonic_interval_classes
   tools/pitchtools/is_alphabetic_accidental_abbreviation
   tools/pitchtools/is_chromatic_pitch_class_name
   tools/pitchtools/is_chromatic_pitch_class_name_octave_number_pair
   tools/pitchtools/is_chromatic_pitch_class_number
   tools/pitchtools/is_chromatic_pitch_name
   tools/pitchtools/is_chromatic_pitch_number
   tools/pitchtools/is_diatonic_pitch_class_name
   tools/pitchtools/is_diatonic_pitch_class_number
   tools/pitchtools/is_diatonic_pitch_name
   tools/pitchtools/is_diatonic_pitch_number
   tools/pitchtools/is_named_chromatic_pitch_token
   tools/pitchtools/is_octave_tick_string
   tools/pitchtools/is_pitch_carrier
   tools/pitchtools/iterate_named_chromatic_pitch_pairs_forward_in_expr
   tools/pitchtools/list_chromatic_pitch_numbers_in_expr
   tools/pitchtools/list_harmonic_chromatic_intervals_in_expr
   tools/pitchtools/list_harmonic_diatonic_intervals_in_expr
   tools/pitchtools/list_melodic_chromatic_interval_numbers_pairwise_between_pitch_carriers
   tools/pitchtools/list_named_chromatic_pitch_carriers_in_expr_sorted_by_numeric_chromatic_pitch_class
   tools/pitchtools/list_named_chromatic_pitches_in_expr
   tools/pitchtools/list_numeric_chromatic_pitch_classes_in_expr
   tools/pitchtools/list_octave_transpositions_of_pitch_carrier_within_pitch_range
   tools/pitchtools/list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2
   tools/pitchtools/list_unordered_named_chromatic_pitch_pairs_in_expr
   tools/pitchtools/named_chromatic_pitch_and_clef_to_staff_position_number
   tools/pitchtools/named_chromatic_pitch_tokens_to_named_chromatic_pitches
   tools/pitchtools/named_chromatic_pitches_to_harmonic_chromatic_interval_class_number_dictionary
   tools/pitchtools/named_chromatic_pitches_to_inversion_equivalent_chromatic_interval_class_number_dictionary
   tools/pitchtools/octave_number_to_octave_tick_string
   tools/pitchtools/octave_tick_string_to_octave_number
   tools/pitchtools/one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name
   tools/pitchtools/ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers
   tools/pitchtools/pentatonic_pitch_number_to_chromatic_pitch_number
   tools/pitchtools/permute_named_chromatic_pitch_carrier_list_by_twelve_tone_row
   tools/pitchtools/register_chromatic_pitch_class_numbers_by_chromatic_pitch_number_aggregate
   tools/pitchtools/respell_named_chromatic_pitches_in_expr_with_flats
   tools/pitchtools/respell_named_chromatic_pitches_in_expr_with_sharps
   tools/pitchtools/set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr
   tools/pitchtools/set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr
   tools/pitchtools/suggest_clef_for_named_chromatic_pitches
   tools/pitchtools/transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number
   tools/pitchtools/transpose_chromatic_pitch_number_by_octave_transposition_mapping
   tools/pitchtools/transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell
   tools/pitchtools/transpose_pitch_carrier_by_melodic_chromatic_interval
   tools/pitchtools/transpose_pitch_carrier_by_melodic_diatonic_interval
   tools/pitchtools/transpose_pitch_carrier_by_melodic_interval


resttools

.. toctree::
   :maxdepth: 1

   tools/resttools/MultiMeasureRest/MultiMeasureRest
   tools/resttools/is_lilypond_rest_string
   tools/resttools/make_repeated_rests_from_time_signature
   tools/resttools/make_repeated_rests_from_time_signatures
   tools/resttools/make_rests
   tools/resttools/set_vertical_positioning_pitch_on_rest


schemetools

.. toctree::
   :maxdepth: 1

   tools/schemetools/SchemeAssociativeList/SchemeAssociativeList
   tools/schemetools/SchemeColor/SchemeColor
   tools/schemetools/SchemeFunction/SchemeFunction
   tools/schemetools/SchemeMoment/SchemeMoment
   tools/schemetools/SchemePair/SchemePair
   tools/schemetools/SchemeString/SchemeString
   tools/schemetools/SchemeVector/SchemeVector
   tools/schemetools/SchemeVectorConstant/SchemeVectorConstant


scoretools

.. toctree::
   :maxdepth: 1

   tools/scoretools/GrandStaff/GrandStaff
   tools/scoretools/PianoStaff/PianoStaff
   tools/scoretools/StaffGroup/StaffGroup
   tools/scoretools/make_empty_piano_score
   tools/scoretools/make_piano_score_from_leaves
   tools/scoretools/make_piano_sketch_score_from_leaves
   tools/scoretools/make_pitch_array_score_from_pitch_arrays


seqtools

.. toctree::
   :maxdepth: 1

   tools/seqtools/all_are_assignable_integers
   tools/seqtools/all_are_equal
   tools/seqtools/all_are_nonnegative_integer_powers_of_two
   tools/seqtools/all_are_nonnegative_integers
   tools/seqtools/all_are_numbers
   tools/seqtools/all_are_positive_integers
   tools/seqtools/all_are_unequal
   tools/seqtools/count_length_two_runs
   tools/seqtools/flatten_sequence
   tools/seqtools/flatten_sequence_at_indices
   tools/seqtools/generate_all_k_ary_sequences_of_length
   tools/seqtools/generate_all_restricted_growth_functions_of_length
   tools/seqtools/get_degree_of_rotational_symmetry_of_sequence
   tools/seqtools/get_indices_of_sequence_elements_equal_to_true
   tools/seqtools/get_period_of_rotation_of_sequence
   tools/seqtools/get_sequence_element_at_cyclic_index
   tools/seqtools/get_sequence_elements_at_indices
   tools/seqtools/group_sequence_elements_by_counts
   tools/seqtools/group_sequence_elements_by_equality
   tools/seqtools/group_sequence_elements_by_sign
   tools/seqtools/group_sequence_elements_cyclically_by_weights_at_least_with_overhang
   tools/seqtools/group_sequence_elements_cyclically_by_weights_at_least_without_overhang
   tools/seqtools/group_sequence_elements_cyclically_by_weights_at_most_with_overhang
   tools/seqtools/group_sequence_elements_cyclically_by_weights_at_most_without_overhang
   tools/seqtools/group_sequence_elements_cyclically_by_weights_exactly_with_overhang
   tools/seqtools/group_sequence_elements_cyclically_by_weights_exactly_without_overhang
   tools/seqtools/group_sequence_elements_once_by_weights_at_least_with_overhang
   tools/seqtools/group_sequence_elements_once_by_weights_at_least_without_overhang
   tools/seqtools/group_sequence_elements_once_by_weights_at_most_with_overhang
   tools/seqtools/group_sequence_elements_once_by_weights_at_most_without_overhang
   tools/seqtools/group_sequence_elements_once_by_weights_exactly_with_overhang
   tools/seqtools/group_sequence_elements_once_by_weights_exactly_without_overhang
   tools/seqtools/increase_sequence_elements_at_indices_by_addenda
   tools/seqtools/increase_sequence_elements_cyclically_by_addenda
   tools/seqtools/interlace_sequences
   tools/seqtools/is_monotonically_decreasing_sequence
   tools/seqtools/is_monotonically_increasing_sequence
   tools/seqtools/is_permutation
   tools/seqtools/is_repetition_free_sequence
   tools/seqtools/is_restricted_growth_function
   tools/seqtools/is_strictly_decreasing_sequence
   tools/seqtools/is_strictly_increasing_sequence
   tools/seqtools/iterate_sequence_cyclically
   tools/seqtools/iterate_sequence_cyclically_from_start_to_stop
   tools/seqtools/iterate_sequence_forward_and_backward_nonoverlapping
   tools/seqtools/iterate_sequence_forward_and_backward_overlapping
   tools/seqtools/iterate_sequence_nwise_cyclic
   tools/seqtools/iterate_sequence_nwise_strict
   tools/seqtools/iterate_sequence_nwise_wrapped
   tools/seqtools/iterate_sequence_pairwise_cyclic
   tools/seqtools/iterate_sequence_pairwise_strict
   tools/seqtools/iterate_sequence_pairwise_wrapped
   tools/seqtools/join_subsequences_by_sign
   tools/seqtools/list_pairwise_cumulative_sums_from_zero
   tools/seqtools/map_sequence_elements_to_numbered_sublists
   tools/seqtools/negate_sequence_elements_at_indices
   tools/seqtools/negate_sequence_elements_at_indices_absolutely
   tools/seqtools/overwrite_sequence_elements_at_indices
   tools/seqtools/partition_sequence_by_restricted_growth_function
   tools/seqtools/partition_sequence_by_weights
   tools/seqtools/partition_sequence_by_weights_not_less_than
   tools/seqtools/partition_sequence_by_weights_ratio
   tools/seqtools/partition_sequence_cyclically_by_counts_with_overhang
   tools/seqtools/partition_sequence_cyclically_by_counts_without_overhang
   tools/seqtools/partition_sequence_elements_into_canonic_parts
   tools/seqtools/partition_sequence_once_by_counts_with_overhang
   tools/seqtools/partition_sequence_once_by_counts_without_overhang
   tools/seqtools/permute_sequence
   tools/seqtools/remove_sequence_elements_at_indices
   tools/seqtools/remove_sequence_elements_at_indices_cyclically
   tools/seqtools/remove_subsequence_of_weight_at_index
   tools/seqtools/repeat_sequence_elements_at_indices
   tools/seqtools/repeat_sequence_elements_at_indices_cyclically
   tools/seqtools/repeat_sequence_elements_n_times_each
   tools/seqtools/repeat_sequence_n_times
   tools/seqtools/repeat_sequence_to_length
   tools/seqtools/repeat_sequence_to_weight_at_least
   tools/seqtools/repeat_sequence_to_weight_at_most
   tools/seqtools/repeat_sequence_to_weight_exactly
   tools/seqtools/repeat_subruns_to_count
   tools/seqtools/replace_sequence_elements_cyclically_with_new_material
   tools/seqtools/retain_sequence_elements_at_indices
   tools/seqtools/retain_sequence_elements_at_indices_cyclically
   tools/seqtools/rotate_sequence
   tools/seqtools/splice_new_elements_between_sequence_elements
   tools/seqtools/split_sequence_cyclically_by_weights_with_overhang
   tools/seqtools/split_sequence_cyclically_by_weights_without_overhang
   tools/seqtools/split_sequence_once_by_weights_with_overhang
   tools/seqtools/split_sequence_once_by_weights_without_overhang
   tools/seqtools/sum_consecutive_sequence_elements_by_sign
   tools/seqtools/sum_sequence_elements_at_indices
   tools/seqtools/truncate_sequence_to_sum
   tools/seqtools/truncate_sequence_to_weight
   tools/seqtools/truncate_subruns
   tools/seqtools/yield_all_combinations_of_elements
   tools/seqtools/yield_all_pairs_between_sequences
   tools/seqtools/yield_all_partitions_of_sequence
   tools/seqtools/yield_all_permutations_of_sequence
   tools/seqtools/yield_all_permutations_of_sequence_in_orbit
   tools/seqtools/yield_all_rotations_of_sequence
   tools/seqtools/yield_all_set_partitions_of_sequence
   tools/seqtools/yield_all_subsequences_of_sequence
   tools/seqtools/yield_all_unordered_pairs_of_sequence
   tools/seqtools/yield_outer_product_of_sequences
   tools/seqtools/zip_sequences_cyclically
   tools/seqtools/zip_sequences_without_truncation


skiptools

.. toctree::
   :maxdepth: 1

   tools/skiptools/Skip/Skip
   tools/skiptools/make_repeated_skips_from_time_signature
   tools/skiptools/make_repeated_skips_from_time_signatures
   tools/skiptools/make_skips_with_multiplied_durations
   tools/skiptools/replace_leaves_in_expr_with_skips


spacingtools

.. toctree::
   :maxdepth: 1

   tools/spacingtools/SpacingIndication/SpacingIndication


spannertools

.. toctree::
   :maxdepth: 1

   tools/spannertools/BeamSpanner/BeamSpanner
   tools/spannertools/BracketSpanner/BracketSpanner
   tools/spannertools/ComplexBeamSpanner/ComplexBeamSpanner
   tools/spannertools/CrescendoSpanner/CrescendoSpanner
   tools/spannertools/DecrescendoSpanner/DecrescendoSpanner
   tools/spannertools/DuratedComplexBeamSpanner/DuratedComplexBeamSpanner
   tools/spannertools/DynamicTextSpanner/DynamicTextSpanner
   tools/spannertools/GlissandoSpanner/GlissandoSpanner
   tools/spannertools/HairpinSpanner/HairpinSpanner
   tools/spannertools/HiddenStaffSpanner/HiddenStaffSpanner
   tools/spannertools/MeasuredComplexBeamSpanner/MeasuredComplexBeamSpanner
   tools/spannertools/MetricGridSpanner/MetricGridSpanner
   tools/spannertools/MultipartBeamSpanner/MultipartBeamSpanner
   tools/spannertools/OctavationSpanner/OctavationSpanner
   tools/spannertools/PhrasingSlurSpanner/PhrasingSlurSpanner
   tools/spannertools/PianoPedalSpanner/PianoPedalSpanner
   tools/spannertools/SlurSpanner/SlurSpanner
   tools/spannertools/Spanner/Spanner
   tools/spannertools/StaffLinesSpanner/StaffLinesSpanner
   tools/spannertools/TextScriptSpanner/TextScriptSpanner
   tools/spannertools/TextSpanner/TextSpanner
   tools/spannertools/TieSpanner/TieSpanner
   tools/spannertools/TrillSpanner/TrillSpanner
   tools/spannertools/destroy_all_spanners_attached_to_component
   tools/spannertools/find_index_of_spanner_component_at_score_offset
   tools/spannertools/find_spanner_component_starting_at_exactly_score_offset
   tools/spannertools/fracture_all_spanners_attached_to_component
   tools/spannertools/fracture_spanners_that_cross_components
   tools/spannertools/get_all_spanners_attached_to_any_improper_child_of_component
   tools/spannertools/get_all_spanners_attached_to_any_improper_parent_of_component
   tools/spannertools/get_all_spanners_attached_to_any_proper_child_of_component
   tools/spannertools/get_all_spanners_attached_to_any_proper_parent_of_component
   tools/spannertools/get_all_spanners_attached_to_component
   tools/spannertools/get_nth_leaf_in_spanner
   tools/spannertools/get_spanners_contained_by_components
   tools/spannertools/get_spanners_covered_by_components
   tools/spannertools/get_spanners_on_components_or_component_children
   tools/spannertools/get_spanners_that_cross_components
   tools/spannertools/get_spanners_that_dominate_component_pair
   tools/spannertools/get_spanners_that_dominate_components
   tools/spannertools/get_spanners_that_dominate_container_components_from_to
   tools/spannertools/get_the_only_spanner_attached_to_any_improper_parent_of_component
   tools/spannertools/get_the_only_spanner_attached_to_component
   tools/spannertools/is_component_with_spanner_attached
   tools/spannertools/iterate_components_backward_in_spanner
   tools/spannertools/iterate_components_forward_in_spanner
   tools/spannertools/make_dynamic_spanner_below_with_nib_at_right
   tools/spannertools/make_solid_text_spanner_above_with_nib_at_right
   tools/spannertools/make_solid_text_spanner_below_with_nib_at_right
   tools/spannertools/move_spanners_from_component_to_children_of_component
   tools/spannertools/report_as_string_format_contributions_of_all_spanners_attached_to_component
   tools/spannertools/report_as_string_format_contributions_of_all_spanners_attached_to_improper_parentage_of_component
   tools/spannertools/report_to_screen_format_contributions_of_all_spanners_attached_to_component
   tools/spannertools/report_to_screen_format_contributions_of_all_spanners_attached_to_improper_parentage_of_component
   tools/spannertools/withdraw_components_from_spanners_covered_by_components


stafftools

.. toctree::
   :maxdepth: 1

   tools/stafftools/RhythmicStaff/RhythmicStaff
   tools/stafftools/make_invisible_staff
   tools/stafftools/make_rhythmic_sketch_staff


stringtools

.. toctree::
   :maxdepth: 1

   tools/stringtools/underscore_delimited_lowercase_to_lowercamelcase
   tools/stringtools/underscore_delimited_lowercase_to_uppercamelcase


tempotools

.. toctree::
   :maxdepth: 1

   tools/tempotools/integer_tempo_to_multiplier_tempo_pairs
   tools/tempotools/integer_tempo_to_multiplier_tempo_pairs_report


threadtools

.. toctree::
   :maxdepth: 1

   tools/threadtools/component_to_thread_signature
   tools/threadtools/iterate_thread_backward_from_component
   tools/threadtools/iterate_thread_backward_in_expr
   tools/threadtools/iterate_thread_forward_from_component
   tools/threadtools/iterate_thread_forward_in_expr


tietools

.. toctree::
   :maxdepth: 1

   tools/tietools/add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration
   tools/tietools/add_or_remove_tie_chain_notes_to_achieve_written_duration
   tools/tietools/apply_tie_spanner_to_leaf_pair
   tools/tietools/are_components_in_same_tie_spanner
   tools/tietools/get_leaves_in_tie_chain
   tools/tietools/get_preprolated_tie_chain_duration
   tools/tietools/get_prolated_tie_chain_duration
   tools/tietools/get_tie_chain
   tools/tietools/get_tie_chain_duration_in_seconds
   tools/tietools/get_tie_chains_in_expr
   tools/tietools/get_written_tie_chain_duration
   tools/tietools/group_leaves_in_tie_chain_by_immediate_parents
   tools/tietools/is_component_with_tie_spanner_attached
   tools/tietools/is_tie_chain
   tools/tietools/is_tie_chain_with_all_leaves_in_same_parent
   tools/tietools/iterate_tie_chains_backward_in_expr
   tools/tietools/iterate_tie_chains_forward_in_expr
   tools/tietools/iterate_topmost_tie_chains_and_components_forward_in_expr
   tools/tietools/label_tie_chains_in_expr_with_prolated_tie_chain_duration
   tools/tietools/label_tie_chains_in_expr_with_tie_chain_durations
   tools/tietools/label_tie_chains_in_expr_with_written_tie_chain_duration
   tools/tietools/remove_all_leaves_in_tie_chain_except_first
   tools/tietools/remove_tie_spanners_from_components
   tools/tietools/tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots
   tools/tietools/tie_chain_to_augmented_tuplet_with_proportions_and_encourage_dots
   tools/tietools/tie_chain_to_diminished_tuplet_with_proportions_and_avoid_dots
   tools/tietools/tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots


tuplettools

.. toctree::
   :maxdepth: 1

   tools/tuplettools/FixedDurationTuplet/FixedDurationTuplet
   tools/tuplettools/beam_bottommost_tuplets_in_expr
   tools/tuplettools/change_augmented_tuplets_in_expr_to_diminished
   tools/tuplettools/change_diminished_tuplets_in_expr_to_augmented
   tools/tuplettools/fix_contents_of_tuplets_in_expr
   tools/tuplettools/fuse_tuplets
   tools/tuplettools/is_proper_tuplet_multiplier
   tools/tuplettools/make_augmented_tuplet_from_duration_and_proportions_and_avoid_dots
   tools/tuplettools/make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots
   tools/tuplettools/make_diminished_tuplet_from_duration_and_proportions_and_avoid_dots
   tools/tuplettools/make_diminished_tuplet_from_duration_and_proportions_and_encourage_dots
   tools/tuplettools/make_tuplet_from_proportions_and_pair
   tools/tuplettools/move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet
   tools/tuplettools/remove_trivial_tuplets_in_expr
   tools/tuplettools/scale_contents_of_tuplets_in_expr_by_multiplier


verticalitytools

.. toctree::
   :maxdepth: 1

   tools/verticalitytools/VerticalMoment/VerticalMoment
   tools/verticalitytools/get_vertical_moment_at_prolated_offset_in_expr
   tools/verticalitytools/get_vertical_moment_starting_with_component
   tools/verticalitytools/iterate_vertical_moments_backward_in_expr
   tools/verticalitytools/iterate_vertical_moments_forward_in_expr
   tools/verticalitytools/label_vertical_moments_in_expr_with_chromatic_interval_classes
   tools/verticalitytools/label_vertical_moments_in_expr_with_chromatic_intervals
   tools/verticalitytools/label_vertical_moments_in_expr_with_counterpoint_intervals
   tools/verticalitytools/label_vertical_moments_in_expr_with_diatonic_intervals
   tools/verticalitytools/label_vertical_moments_in_expr_with_interval_class_vectors
   tools/verticalitytools/label_vertical_moments_in_expr_with_numbered_chromatic_pitch_classes
   tools/verticalitytools/label_vertical_moments_in_expr_with_pitch_numbers


Additional Abjad composition packages (load manually)
-----------------------------------------------------

.. toctree::
   :maxdepth: 1



pitcharraytools

.. toctree::
   :maxdepth: 1

   tools/pitcharraytools/PitchArray/PitchArray
   tools/pitcharraytools/PitchArrayCell/PitchArrayCell
   tools/pitcharraytools/PitchArrayColumn/PitchArrayColumn
   tools/pitcharraytools/PitchArrayRow/PitchArrayRow
   tools/pitcharraytools/concatenate_pitch_arrays
   tools/pitcharraytools/list_nonspanning_subarrays_of_pitch_array
   tools/pitcharraytools/make_empty_pitch_array_from_list_of_pitch_lists
   tools/pitcharraytools/make_populated_pitch_array_from_list_of_pitch_lists


sievetools

.. toctree::
   :maxdepth: 1

   tools/sievetools/ResidueClass/ResidueClass
   tools/sievetools/ResidueClassExpression/ResidueClassExpression
   tools/sievetools/cycle_tokens_to_sieve


tonalitytools

.. toctree::
   :maxdepth: 1

   tools/tonalitytools/ChordClass/ChordClass
   tools/tonalitytools/ChordQualityIndicator/ChordQualityIndicator
   tools/tonalitytools/DoublingIndicator/DoublingIndicator
   tools/tonalitytools/ExtentIndicator/ExtentIndicator
   tools/tonalitytools/InversionIndicator/InversionIndicator
   tools/tonalitytools/Mode/Mode
   tools/tonalitytools/OmissionIndicator/OmissionIndicator
   tools/tonalitytools/QualityIndicator/QualityIndicator
   tools/tonalitytools/Scale/Scale
   tools/tonalitytools/ScaleDegree/ScaleDegree
   tools/tonalitytools/SuspensionIndicator/SuspensionIndicator
   tools/tonalitytools/TonalFunction/TonalFunction
   tools/tonalitytools/analyze_chord
   tools/tonalitytools/analyze_incomplete_chord
   tools/tonalitytools/analyze_incomplete_tonal_function
   tools/tonalitytools/analyze_tonal_function
   tools/tonalitytools/are_scalar_notes
   tools/tonalitytools/are_stepwise_ascending_notes
   tools/tonalitytools/are_stepwise_descending_notes
   tools/tonalitytools/are_stepwise_notes
   tools/tonalitytools/chord_class_cardinality_to_extent
   tools/tonalitytools/chord_class_extent_to_cardinality
   tools/tonalitytools/chord_class_extent_to_extent_name
   tools/tonalitytools/diatonic_interval_class_segment_to_chord_quality_string
   tools/tonalitytools/is_neighbor_note
   tools/tonalitytools/is_passing_tone
   tools/tonalitytools/is_unlikely_melodic_diatonic_interval_in_chorale
   tools/tonalitytools/make_all_notes_in_ascending_and_descending_diatonic_scale
   tools/tonalitytools/make_first_n_notes_in_ascending_diatonic_scale


treetools

.. toctree::
   :maxdepth: 1

   tools/treetools/Block/Block
   tools/treetools/BoundedInterval/BoundedInterval
   tools/treetools/IntervalTree/IntervalTree
   tools/treetools/all_interval_payloads_contain_key_of_klass
   tools/treetools/all_intervals_in_tree_are_contiguous
   tools/treetools/all_intervals_in_tree_are_nonoverlapping
   tools/treetools/compute_depth_of_tree
   tools/treetools/compute_logical_and_of_intervals
   tools/treetools/compute_logical_not_of_intervals
   tools/treetools/compute_logical_or_of_intervals
   tools/treetools/compute_logical_xor_of_intervals
   tools/treetools/concatenate_trees
   tools/treetools/explode_overlapping_tree_into_nonoverlapping_trees_compactly
   tools/treetools/explode_overlapping_tree_into_nonoverlapping_trees_uncompactly
   tools/treetools/fuse_overlapping_intervals
   tools/treetools/fuse_tangent_or_overlapping_intervals
   tools/treetools/get_all_unique_bounds_in_tree
   tools/treetools/group_all_contiguous_or_overlapping_intervals_in_tree_and_yield_groups
   tools/treetools/group_all_overlapping_intervals_in_tree_and_yield_groups
   tools/treetools/make_percussion_score_of_depth_tree
   tools/treetools/make_percussion_score_of_tree
   tools/treetools/mask_intervals_with_intervals_while_preserving_payloads
   tools/treetools/scale_tree_by_value
   tools/treetools/scale_tree_to_value
   tools/treetools/shift_tree_by_value
   tools/treetools/shift_tree_to_value
   tools/treetools/split_intervals_in_tree_at_values
