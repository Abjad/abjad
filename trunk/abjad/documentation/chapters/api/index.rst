Abjad API
=========

.. toctree::

Classes
-------

.. toctree::
   :maxdepth: 1

   components/_Measure/AnonymousMeasure/AnonymousMeasure
   marks/Articulation/Articulation
   components/Chord/Chord
   marks/Clef/Clef
   components/Cluster/Cluster
   components/Container/Container
   components/_Measure/DynamicMeasure/DynamicMeasure
   components/_Tuplet/FixedDurationTuplet/FixedDurationTuplet
   components/_Tuplet/FixedMultiplierTuplet/FixedMultiplierTuplet
   components/Grace/Grace
   components/StaffGroup/GrandStaff
   marks/KeySignature/KeySignature
   marks/Markup/Markup
   marks/Meter/Meter
   components/_Harmonic/NaturalHarmonic
   components/Note/Note
   components/NoteHead/NoteHead
   components/StaffGroup/PianoStaff
   core/Rational/Rational
   components/Rest/Rest
   components/_Measure/RigidMeasure/RigidMeasure
   components/Score/Score
   components/Skip/Skip
   components/Staff/Staff
   components/StaffGroup/StaffGroup
   components/Voice/Voice


Interfaces
----------

.. toctree::
   :maxdepth: 1

   interfaces/AccidentalInterface/AccidentalInterface
   interfaces/ArticulationInterface/ArticulationInterface
   interfaces/BarLineInterface/BarLineInterface
   interfaces/BarNumberInterface/BarNumberInterface
   interfaces/BeamInterface/BeamInterface
   interfaces/BracketsInterface/BracketsInterface
   interfaces/BreaksInterface/BreaksInterface
   interfaces/ClefInterface/ClefInterface
   interfaces/ClusterInterface/ClusterInterface
   interfaces/CommentsInterface/CommentsInterface
   interfaces/DirectivesInterface/DirectivesInterface
   interfaces/DotsInterface/DotsInterface
   interfaces/DynamicLineSpannerInterface/DynamicLineSpannerInterface
   interfaces/DynamicTextInterface/DynamicTextInterface
   interfaces/DynamicTextSpannerInterface/DynamicTextSpannerInterface
   interfaces/DynamicsInterface/DynamicsInterface
   interfaces/GlissandoInterface/GlissandoInterface
   interfaces/GraceInterface/GraceInterface
   interfaces/HairpinInterface/HairpinInterface
   interfaces/HarmonicInterface/HarmonicInterface
   interfaces/HistoryInterface/HistoryInterface
   interfaces/InstrumentInterface/InstrumentInterface
   interfaces/InterfaceAggregator/InterfaceAggregator
   interfaces/KeySignatureInterface/KeySignatureInterface
   interfaces/MarkupInterface/MarkupInterface
   interfaces/MeterInterface/MeterInterface
   interfaces/MultiMeasureRestInterface/MultiMeasureRestInterface
   interfaces/NonMusicalPaperColumnInterface/NonMusicalPaperColumnInterface
   interfaces/NoteColumnInterface/NoteColumnInterface
   interfaces/NoteHeadInterface/NoteHeadInterface
   interfaces/NumberingInterface/NumberingInterface
   interfaces/OffsetInterface/OffsetInterface
   interfaces/OffsetInterface/OffsetProlatedInterface/OffsetProlatedInterface
   interfaces/OttavaBracketInterface/OttavaBracketInterface
   interfaces/ParentageInterface/ParentageInterface
   interfaces/PianoPedalInterface/PianoPedalInterface
   interfaces/RehearsalMarkInterface/RehearsalMarkInterface
   interfaces/RestInterface/RestInterface
   interfaces/ScoreInterface/ScoreInterface
   interfaces/SpacingInterface/ScoreSpacingInterface/ScoreSpacingInterface
   interfaces/ScriptInterface/ScriptInterface
   interfaces/SlurInterface/SlurInterface
   interfaces/SpacingInterface/SpacingInterface
   interfaces/SpanBarInterface/SpanBarInterface
   interfaces/StaffInterface/StaffInterface
   interfaces/StemInterface/StemInterface
   interfaces/StemTremoloInterface/StemTremoloInterface
   interfaces/SystemStartBarInterface/SystemStartBarInterface
   interfaces/TempoInterface/TempoInterface
   interfaces/TextScriptInterface/TextScriptInterface
   interfaces/TextSpannerInterface/TextSpannerInterface
   interfaces/ThreadInterface/ThreadInterface
   interfaces/TieInterface/TieInterface
   interfaces/TremoloInterface/TremoloInterface
   interfaces/TrillInterface/TrillInterface
   interfaces/TrillPitchAccidentalInterface/TrillPitchAccidentalInterface
   interfaces/TupletBracketInterface/TupletBracketInterface
   interfaces/TupletNumberInterface/TupletNumberInterface
   interfaces/VerticalAlignmentInterface/VerticalAlignmentInterface
   interfaces/VerticalAxisGroupInterface/VerticalAxisGroupInterface
   interfaces/VoiceInterface/VoiceInterface


Spanners
--------

.. toctree::
   :maxdepth: 1

   spanners/Beam/Beam
   spanners/Bracket/Bracket
   spanners/Beam/ComplexBeam/ComplexBeam
   spanners/Crescendo/Crescendo
   spanners/Decrescendo/Decrescendo
   spanners/Beam/DuratedComplexBeam/DuratedComplexBeam
   spanners/DynamicTextSpanner/DynamicTextSpanner
   spanners/Glissando/Glissando
   spanners/Hairpin/Hairpin
   spanners/InstrumentSpanner/InstrumentSpanner
   spanners/Beam/MeasuredComplexBeam/MeasuredComplexBeam
   spanners/MetricGrid/MetricGrid
   spanners/OctavationSpanner/OctavationSpanner
   spanners/OverrideSpanner/OverrideSpanner
   spanners/PianoPedal/PianoPedal
   spanners/TempoSpanner/ProportionalTempoSpanner/ProportionalTempoSpanner
   spanners/Slur/Slur
   spanners/SpacingSpanner/SpacingSpanner
   spanners/Spanner/Spanner
   spanners/TempoSpanner/TempoSpanner
   spanners/TextScriptSpanner/TextScriptSpanner
   spanners/TextSpanner/TextSpanner
   spanners/Tie/Tie
   spanners/Trill/Trill


Tools
-----

.. toctree::
   :maxdepth: 1



cfgtools

.. toctree::
   :maxdepth: 1

   tools/cfgtools/list_settings


chordtools

.. toctree::
   :maxdepth: 1

   tools/chordtools/arpeggiate_chord
   tools/chordtools/cast_defective_chord
   tools/chordtools/color_chord_note_heads_by_numeric_pitch_class
   tools/chordtools/divide_chord_by_pitch_altitude
   tools/chordtools/divide_chord_by_pitch_number
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
   tools/componenttools/all_are_thread_contiguous_components
   tools/componenttools/clone_and_partition_governed_component_subtree_by_leaf_counts
   tools/componenttools/clone_components_and_covered_spanners
   tools/componenttools/clone_components_and_fracture_crossing_spanners
   tools/componenttools/clone_components_and_immediate_parent_of_first_component
   tools/componenttools/clone_components_and_remove_all_spanners
   tools/componenttools/clone_governed_component_subtree_by_leaf_range
   tools/componenttools/clone_governed_component_subtree_from_prolated_duration_to
   tools/componenttools/cut_component_at_prolated_duration
   tools/componenttools/get_first_component_in_expr_with_name
   tools/componenttools/get_first_instance_of_klass_in_proper_parentage_of_component
   tools/componenttools/get_likely_multiplier_of_components
   tools/componenttools/get_parent_and_start_stop_indices_of_components
   tools/componenttools/group_components_by_like_preprolated_duration
   tools/componenttools/group_components_by_like_prolated_duration
   tools/componenttools/is_well_formed_component
   tools/componenttools/list_badly_formed_components_in_expr
   tools/componenttools/list_improper_contents_of_component_that_cross_prolated_offset
   tools/componenttools/list_leftmost_components_with_prolated_duration_at_most
   tools/componenttools/move_component_subtree_to_right_in_score_and_spanners
   tools/componenttools/move_parentage_and_spanners_from_components_to_components
   tools/componenttools/number_is_between_prolated_start_and_stop_offsets_of_component
   tools/componenttools/number_is_between_start_and_stop_offsets_of_component_in_seconds
   tools/componenttools/partition_components_cyclically_by_counts_and_do_not_fracture_crossing_spanners
   tools/componenttools/partition_components_cyclically_by_counts_and_fracture_crossing_spanners
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
   tools/componenttools/partition_components_once_by_counts_and_do_not_fracture_crossing_spanners
   tools/componenttools/partition_components_once_by_counts_and_fracture_crossing_spanners
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
   tools/componenttools/remove_tie_spanners_from_components
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
   tools/containertools/replace_first_n_elements_in_container_with_big_endian_rests
   tools/containertools/replace_first_n_elements_in_container_with_little_endian_rests
   tools/containertools/replace_first_n_elements_in_container_with_rests
   tools/containertools/replace_larger_left_half_of_elements_in_container_with_big_endian_rests
   tools/containertools/replace_larger_left_half_of_elements_in_container_with_little_endian_rests
   tools/containertools/replace_larger_right_half_of_elements_in_container_with_big_endian_rests
   tools/containertools/replace_larger_right_half_of_elements_in_container_with_little_endian_rests
   tools/containertools/replace_smaller_left_half_of_elements_in_container_with_big_endian_rests
   tools/containertools/replace_smaller_left_half_of_elements_in_container_with_little_endian_rests
   tools/containertools/replace_smaller_right_half_of_elements_in_container_with_big_endian_rests
   tools/containertools/replace_smaller_right_half_of_elements_in_container_with_little_endian_rests
   tools/containertools/report_container_modifications_as_string
   tools/containertools/report_container_modifications_to_screen
   tools/containertools/reverse_contents_of_container
   tools/containertools/scale_contents_of_container
   tools/containertools/set_accidental_style_on_sequential_contexts_in_expr
   tools/containertools/set_container_multiplier
   tools/containertools/split_container_at_index_and_do_not_fracture_crossing_spanners
   tools/containertools/split_container_at_index_and_fracture_crossing_spanners


durtools

.. toctree::
   :maxdepth: 1

   tools/durtools/assignable_rational_to_dot_count
   tools/durtools/assignable_rational_to_lilypond_duration_string
   tools/durtools/duration_pair_to_prolation_string
   tools/durtools/duration_token_to_big_endian_list_of_assignable_duration_pairs
   tools/durtools/duration_token_to_reduced_duration_pair
   tools/durtools/group_duration_tokens_by_like_implied_prolation
   tools/durtools/is_assignable_rational
   tools/durtools/is_binary_rational
   tools/durtools/is_duration_pair
   tools/durtools/is_duration_token
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


iotools

.. toctree::
   :maxdepth: 1

   tools/iotools/f
   tools/iotools/log
   tools/iotools/ly
   tools/iotools/pdf
   tools/iotools/play
   tools/iotools/profile_expr
   tools/iotools/redo
   tools/iotools/show
   tools/iotools/write_expr_to_ly
   tools/iotools/write_expr_to_ly_and_to_pdf_and_show
   tools/iotools/write_expr_to_pdf


iterate

.. toctree::
   :maxdepth: 1

   tools/iterate/components_and_grace_containers_forward_in_expr
   tools/iterate/depth_first
   tools/iterate/get_leaf_at_index_from_measure_number_in_expr
   tools/iterate/get_measure_number_in_expr
   tools/iterate/get_next_measure_from_component
   tools/iterate/get_nth_component_in_expr
   tools/iterate/get_nth_leaf_in_expr
   tools/iterate/get_nth_measure_in_expr
   tools/iterate/get_nth_namesake_from_component
   tools/iterate/get_prev_measure_from_component
   tools/iterate/get_vertical_moment_at_prolated_offset_in_expr
   tools/iterate/get_vertical_moment_starting_with_component
   tools/iterate/group_by_type_and_yield_groups_of_klass
   tools/iterate/group_topmost_components_in_expr_by_type_and_yield_groups
   tools/iterate/group_topmost_components_in_expr_by_type_and_yield_groups_of_klass
   tools/iterate/leaf_pairs_forward_in_expr
   tools/iterate/leaves_backward_in_expr
   tools/iterate/leaves_forward_in_expr
   tools/iterate/measures_backward_in_expr
   tools/iterate/measures_forward_in_expr
   tools/iterate/naive_backward_in_expr
   tools/iterate/naive_forward_in_expr
   tools/iterate/namesakes_backward_from_component
   tools/iterate/namesakes_forward_from_component
   tools/iterate/notes_backward_in_expr
   tools/iterate/notes_forward_in_expr
   tools/iterate/pitch_pairs_forward_in_expr
   tools/iterate/thread_backward_from_component
   tools/iterate/thread_backward_in_expr
   tools/iterate/thread_forward_from_component
   tools/iterate/thread_forward_in_expr
   tools/iterate/tie_chains_backward_in_expr
   tools/iterate/tie_chains_forward_in_expr
   tools/iterate/timeline_backward_from_component
   tools/iterate/timeline_backward_in_expr
   tools/iterate/timeline_forward_from_component
   tools/iterate/timeline_forward_in_expr
   tools/iterate/topmost_tie_chains_and_components_forward_in_expr
   tools/iterate/vertical_moments_backward_in_expr
   tools/iterate/vertical_moments_forward_in_expr


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

   tools/leaftools/add_artificial_harmonic_to_note
   tools/leaftools/change_leaf_preprolated_duration
   tools/leaftools/change_written_duration_and_preserve_preprolated_duration
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
   tools/leaftools/get_prolated_durations_from_leaves_in_expr
   tools/leaftools/get_written_durations_from_leaves_in_expr
   tools/leaftools/is_bar_line_crossing_leaf
   tools/leaftools/label_leaves_in_expr_with_leaf_depth
   tools/leaftools/label_leaves_in_expr_with_leaf_durations
   tools/leaftools/label_leaves_in_expr_with_leaf_indices
   tools/leaftools/label_leaves_in_expr_with_leaf_numbers
   tools/leaftools/label_leaves_in_expr_with_melodic_chromatic_interval_classes
   tools/leaftools/label_leaves_in_expr_with_melodic_chromatic_intervals
   tools/leaftools/label_leaves_in_expr_with_melodic_counterpoint_interval_classes
   tools/leaftools/label_leaves_in_expr_with_melodic_counterpoint_intervals
   tools/leaftools/label_leaves_in_expr_with_melodic_diatonic_intervals
   tools/leaftools/label_leaves_in_expr_with_melodic_diatonic_inteval_classes
   tools/leaftools/label_leaves_in_expr_with_pitch_class_numbers
   tools/leaftools/label_leaves_in_expr_with_pitch_numbers
   tools/leaftools/label_leaves_in_expr_with_prolated_leaf_duration
   tools/leaftools/label_leaves_in_expr_with_tuplet_depth
   tools/leaftools/label_leaves_in_expr_with_written_leaf_duration
   tools/leaftools/leaf_to_augmented_tuplet_with_n_notes_of_equal_written_duration
   tools/leaftools/leaf_to_augmented_tuplet_with_proportions
   tools/leaftools/leaf_to_diminished_tuplet_with_n_notes_of_equal_written_duration
   tools/leaftools/leaf_to_diminished_tuplet_with_proportions
   tools/leaftools/make_accelerating_notes_with_lilypond_multipliers
   tools/leaftools/make_all_notes_in_ascending_and_descending_diatonic_scale
   tools/leaftools/make_first_n_notes_in_ascending_diatonic_scale
   tools/leaftools/make_leaves
   tools/leaftools/make_notes
   tools/leaftools/make_percussion_note
   tools/leaftools/make_quarter_notes_with_lilypond_multipliers
   tools/leaftools/make_repeated_notes
   tools/leaftools/make_repeated_notes_with_shorter_notes_at_end
   tools/leaftools/make_rests
   tools/leaftools/make_skips_with_multiplied_durations
   tools/leaftools/remove_leaf_and_shrink_durated_parent_containers
   tools/leaftools/remove_markup_from_leaves_in_expr
   tools/leaftools/repeat_leaf_and_extend_spanners
   tools/leaftools/repeat_leaves_in_expr_and_extend_spanners
   tools/leaftools/replace_leaves_in_expr_with_skips
   tools/leaftools/scale_preprolated_leaf_duration
   tools/leaftools/show_leaves
   tools/leaftools/split_leaf_at_prolated_duration_and_rest_right_half


lilyfiletools

.. toctree::
   :maxdepth: 1

   tools/lilyfiletools/BookBlock/BookBlock
   tools/lilyfiletools/BookpartBlock/BookpartBlock
   tools/lilyfiletools/HeaderBlock/HeaderBlock
   tools/lilyfiletools/LayoutBlock/LayoutBlock
   tools/lilyfiletools/LilyFile/LilyFile
   tools/lilyfiletools/MidiBlock/MidiBlock
   tools/lilyfiletools/PaperBlock/PaperBlock
   tools/lilyfiletools/ScoreBlock/ScoreBlock
   tools/lilyfiletools/make_basic_lily_file
   tools/lilyfiletools/parse_note_entry_string
   tools/lilyfiletools/save_last_ly_as
   tools/lilyfiletools/save_last_pdf_as


listtools

.. toctree::
   :maxdepth: 1

   tools/listtools/all_ordered_sublists
   tools/listtools/all_restricted_growth_functions_of_length
   tools/listtools/all_rotations
   tools/listtools/all_set_partitions
   tools/listtools/are_assignable_integers
   tools/listtools/arithmetic_mean
   tools/listtools/contiguous_sublists
   tools/listtools/count_repetitions
   tools/listtools/cumulative_products
   tools/listtools/cumulative_sums
   tools/listtools/cumulative_sums_zero
   tools/listtools/cumulative_weights_signed
   tools/listtools/difference_series
   tools/listtools/flatten
   tools/listtools/flatten_at_indices
   tools/listtools/forward_and_backward_nonoverlapping
   tools/listtools/forward_and_backward_overlapping
   tools/listtools/get_cyclic
   tools/listtools/get_elements_at_indices
   tools/listtools/get_period
   tools/listtools/get_shared_numeric_sign
   tools/listtools/get_unordered_pairs
   tools/listtools/group_by_equality
   tools/listtools/group_by_sign
   tools/listtools/group_by_weights
   tools/listtools/increase_at_indices
   tools/listtools/increase_cyclic
   tools/listtools/insert_slice_cyclic
   tools/listtools/interlace
   tools/listtools/is_decreasing_monotonically
   tools/listtools/is_decreasing_strictly
   tools/listtools/is_increasing_monotonically
   tools/listtools/is_increasing_strictly
   tools/listtools/is_numeric
   tools/listtools/is_repetition_free
   tools/listtools/is_restricted_growth_function
   tools/listtools/is_uniform
   tools/listtools/is_unique
   tools/listtools/join_sublists_by_sign
   tools/listtools/lengths_to_counts
   tools/listtools/negate_elements_at_indices
   tools/listtools/negate_elements_at_indices_absolutely
   tools/listtools/nwise_cyclic
   tools/listtools/nwise_strict
   tools/listtools/nwise_wrapped
   tools/listtools/outer_product
   tools/listtools/overwrite_slices_at
   tools/listtools/pairs_from_to
   tools/listtools/pairwise
   tools/listtools/pairwise_cumulative_sums_zero
   tools/listtools/partition_by_lengths
   tools/listtools/partition_by_restricted_growth_function
   tools/listtools/partition_by_weights
   tools/listtools/partition_by_weights_not_less_than
   tools/listtools/partition_by_weights_ratio
   tools/listtools/partition_elements_into_canonic_parts
   tools/listtools/permutations
   tools/listtools/permute
   tools/listtools/phasor
   tools/listtools/remove_elements_at_indices
   tools/listtools/remove_elements_at_indices_cyclic
   tools/listtools/remove_repetitions
   tools/listtools/remove_weighted_subrun_at
   tools/listtools/repeat_elements_at_indices
   tools/listtools/repeat_elements_at_indices_cyclic
   tools/listtools/repeat_elements_to_count
   tools/listtools/repeat_list_to_length
   tools/listtools/repeat_list_to_weight
   tools/listtools/repeat_n_cycles
   tools/listtools/repeat_subruns_to_count
   tools/listtools/replace_elements_cyclic
   tools/listtools/retain_elements_at_indices
   tools/listtools/retain_elements_at_indices_cyclic
   tools/listtools/rotate
   tools/listtools/sublists
   tools/listtools/sum_by_sign
   tools/listtools/sum_slices_at
   tools/listtools/true_indices
   tools/listtools/truncate_subruns
   tools/listtools/truncate_to_sum
   tools/listtools/truncate_to_weight
   tools/listtools/unique
   tools/listtools/weight
   tools/listtools/zip_cyclic
   tools/listtools/zip_nontruncating


markuptools

.. toctree::
   :maxdepth: 1

   tools/markuptools/make_big_centered_page_number_markup


mathtools

.. toctree::
   :maxdepth: 1

   tools/mathtools/binary_string
   tools/mathtools/divide_scalar_by_ratio
   tools/mathtools/divisors
   tools/mathtools/factors
   tools/mathtools/fragment
   tools/mathtools/greatest_common_divisor
   tools/mathtools/greatest_multiple_less_equal
   tools/mathtools/greatest_power_of_two_less_equal
   tools/mathtools/integer_compositions
   tools/mathtools/integer_partitions
   tools/mathtools/interpolate_cosine
   tools/mathtools/interpolate_divide
   tools/mathtools/interpolate_divide_multiple
   tools/mathtools/interpolate_exponential
   tools/mathtools/interpolate_linear
   tools/mathtools/is_assignable_integer
   tools/mathtools/is_dotted_integer
   tools/mathtools/is_power_of_two
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


measuretools

.. toctree::
   :maxdepth: 1

   tools/measuretools/append_spacer_skip_to_underfull_measure
   tools/measuretools/append_spacer_skips_to_underfull_measures_in
   tools/measuretools/apply_beam_spanner_to_measure
   tools/measuretools/apply_beam_spanners_to_measures_in
   tools/measuretools/apply_complex_beam_spanner_to_measure
   tools/measuretools/apply_complex_beam_spanners_to_measures_in
   tools/measuretools/apply_durated_complex_beam_spanner_to_measures
   tools/measuretools/color_measure
   tools/measuretools/color_nonbinary_measures_in
   tools/measuretools/comment_measures_in_container_with_measure_numbers
   tools/measuretools/fuse_contiguous_measures_in_container_cyclically_by_counts
   tools/measuretools/fuse_measures
   tools/measuretools/make_rigid_measures_with_full_measure_spacer_skips
   tools/measuretools/move_measure_prolation_to_full_measure_tuplet
   tools/measuretools/move_prolation_of_full_measure_tuplet_to_meter_of_measure
   tools/measuretools/multiply_measure_contents_and_scale_meter_denominator_in
   tools/measuretools/multiply_measure_contents_in
   tools/measuretools/pad_measures_in_expr_with_rests
   tools/measuretools/pad_measures_in_expr_with_skips
   tools/measuretools/pitch_array_row_to_measure
   tools/measuretools/pitch_array_to_measures
   tools/measuretools/populate
   tools/measuretools/replace_measure_contents_in
   tools/measuretools/report_meter_distribution
   tools/measuretools/scale_measure_by_multiplier_and_adjust_meter
   tools/measuretools/scale_measure_contents_in
   tools/measuretools/scale_measure_denominator_and_adjust_measure_contents
   tools/measuretools/set_measure_denominator_and_adjust_numerator
   tools/measuretools/tupletize


metertools

.. toctree::
   :maxdepth: 1

   tools/metertools/duration_and_possible_denominators_to_meter
   tools/metertools/extract_meters_from_measures_in_expr
   tools/metertools/get_nonbinary_factor_from_meter_denominator
   tools/metertools/is_meter_token
   tools/metertools/is_meter_with_equivalent_binary_representation
   tools/metertools/meter_to_binary_meter


overridetools

.. toctree::
   :maxdepth: 1

   tools/overridetools/clear_all_overrides_on_grob_handler
   tools/overridetools/promote_attribute_to_context_on_grob_handler


persistencetools

.. toctree::
   :maxdepth: 1

   tools/persistencetools/component_to_pitch_and_rhythm_skeleton
   tools/persistencetools/dump_pickle
   tools/persistencetools/load_pickle


pitchtools

.. toctree::
   :maxdepth: 1

   tools/pitchtools/Accidental/Accidental
   tools/pitchtools/ChromaticIntervalVector/ChromaticIntervalVector
   tools/pitchtools/DiatonicIntervalClass/DiatonicIntervalClass
   tools/pitchtools/DiatonicIntervalClassSegment/DiatonicIntervalClassSegment
   tools/pitchtools/DiatonicIntervalClassVector/DiatonicIntervalClassVector
   tools/pitchtools/HarmonicChromaticInterval/HarmonicChromaticInterval
   tools/pitchtools/HarmonicChromaticIntervalClass/HarmonicChromaticIntervalClass
   tools/pitchtools/HarmonicChromaticIntervalSegment/HarmonicChromaticIntervalSegment
   tools/pitchtools/HarmonicChromaticIntervalSet/HarmonicChromaticIntervalSet
   tools/pitchtools/HarmonicCounterpointInterval/HarmonicCounterpointInterval
   tools/pitchtools/HarmonicCounterpointIntervalClass/HarmonicCounterpointIntervalClass
   tools/pitchtools/HarmonicDiatonicInterval/HarmonicDiatonicInterval
   tools/pitchtools/HarmonicDiatonicIntervalClass/HarmonicDiatonicIntervalClass
   tools/pitchtools/HarmonicDiatonicIntervalClassSet/HarmonicDiatonicIntervalClassSet
   tools/pitchtools/HarmonicDiatonicIntervalSegment/HarmonicDiatonicIntervalSegment
   tools/pitchtools/HarmonicDiatonicIntervalSet/HarmonicDiatonicIntervalSet
   tools/pitchtools/IntervalClass/IntervalClass
   tools/pitchtools/IntervalClassSegment/IntervalClassSegment
   tools/pitchtools/IntervalClassSet/IntervalClassSet
   tools/pitchtools/IntervalClassVector/IntervalClassVector
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
   tools/pitchtools/NamedPitch/NamedPitch
   tools/pitchtools/NamedPitchClass/NamedPitchClass
   tools/pitchtools/NamedPitchClassSegment/NamedPitchClassSegment
   tools/pitchtools/NamedPitchClassSet/NamedPitchClassSet
   tools/pitchtools/NumericPitch/NumericPitch
   tools/pitchtools/PitchArray/PitchArray
   tools/pitchtools/PitchArray/PitchArrayCell/PitchArrayCell
   tools/pitchtools/PitchArray/PitchArrayColumn/PitchArrayColumn
   tools/pitchtools/PitchArray/PitchArrayRow/PitchArrayRow
   tools/pitchtools/PitchClass/PitchClass
   tools/pitchtools/PitchClassColorMap/PitchClassColorMap
   tools/pitchtools/PitchClassSegment/PitchClassSegment
   tools/pitchtools/PitchClassSet/PitchClassSet
   tools/pitchtools/PitchClassVector/PitchClassVector
   tools/pitchtools/PitchRange/PitchRange
   tools/pitchtools/PitchSegment/PitchSegment
   tools/pitchtools/PitchSet/PitchSet
   tools/pitchtools/PitchVector/PitchVector
   tools/pitchtools/TwelveToneRow/TwelveToneRow
   tools/pitchtools/apply_octavation
   tools/pitchtools/are_in_octave_order
   tools/pitchtools/array_to_nonspanning_subarrays
   tools/pitchtools/change_default_accidental_spelling
   tools/pitchtools/chromaticize
   tools/pitchtools/clef_and_staff_position_number_to_pitch
   tools/pitchtools/color_by_pc
   tools/pitchtools/diatonic_and_chromatic_interval_numbers_to_diatonic_interval
   tools/pitchtools/diatonic_scale_degree_to_letter
   tools/pitchtools/diatonic_to_chromatic
   tools/pitchtools/diatonicize
   tools/pitchtools/expr_to_melodic_chromatic_interval_segment
   tools/pitchtools/get_harmonic_chromatic_intervals_in
   tools/pitchtools/get_harmonic_diatonic_intervals_in
   tools/pitchtools/get_interval_class_vector
   tools/pitchtools/get_interval_vector
   tools/pitchtools/get_pitch
   tools/pitchtools/get_pitch_class
   tools/pitchtools/get_pitch_classes
   tools/pitchtools/get_pitch_numbers
   tools/pitchtools/get_pitches
   tools/pitchtools/get_signed_interval_series
   tools/pitchtools/harmonic_chromatic_interval_class_from_to
   tools/pitchtools/harmonic_chromatic_interval_from_to
   tools/pitchtools/harmonic_counterpoint_interval_class_from_to
   tools/pitchtools/harmonic_counterpoint_interval_from_to
   tools/pitchtools/harmonic_diatonic_interval_class_from_to
   tools/pitchtools/harmonic_diatonic_interval_from_to
   tools/pitchtools/has_duplicate_pitch
   tools/pitchtools/has_duplicate_pitch_class
   tools/pitchtools/insert_transposed_pc_subruns
   tools/pitchtools/is_carrier
   tools/pitchtools/is_name
   tools/pitchtools/is_pitch_pair
   tools/pitchtools/is_pitch_token
   tools/pitchtools/is_pitch_token_collection
   tools/pitchtools/leaf_iterables_to_pitch_array_empty
   tools/pitchtools/leaf_iterables_to_pitch_array_populated
   tools/pitchtools/letter_to_diatonic_scale_degree
   tools/pitchtools/letter_to_pc
   tools/pitchtools/list_all_diatonic_interval_classes
   tools/pitchtools/make_all_aggregate_subsets
   tools/pitchtools/make_flat
   tools/pitchtools/make_pitches
   tools/pitchtools/make_sharp
   tools/pitchtools/melodic_chromatic_interval_class_from_to
   tools/pitchtools/melodic_chromatic_interval_from_to
   tools/pitchtools/melodic_counterpoint_interval_class_from_to
   tools/pitchtools/melodic_counterpoint_interval_from_to
   tools/pitchtools/melodic_diatonic_interval_class_from_to
   tools/pitchtools/melodic_diatonic_interval_from_to
   tools/pitchtools/merge_pitch_arrays
   tools/pitchtools/name_to_letter_accidental
   tools/pitchtools/nearest_neighbor
   tools/pitchtools/number_letter_to_accidental_octave
   tools/pitchtools/number_to_letter_accidental_octave
   tools/pitchtools/octave_transpositions
   tools/pitchtools/pc_to_pitch_name
   tools/pitchtools/pc_to_pitch_name_flats
   tools/pitchtools/pc_to_pitch_name_sharps
   tools/pitchtools/pentatonic_to_chromatic
   tools/pitchtools/permute_by_row
   tools/pitchtools/pitch_and_clef_to_staff_position_number
   tools/pitchtools/pitch_number_and_accidental_semitones_to_octave
   tools/pitchtools/pitch_number_to_octave
   tools/pitchtools/pitch_pairs_from_to
   tools/pitchtools/pitch_pairs_within
   tools/pitchtools/pitch_string_to_name
   tools/pitchtools/pitch_string_to_octave_number
   tools/pitchtools/pitch_string_to_pitch
   tools/pitchtools/pitch_string_to_pitches
   tools/pitchtools/pitches_to_diatonic_interval
   tools/pitchtools/registrate
   tools/pitchtools/send_pitch_number_to_octave
   tools/pitchtools/sort_by_pc
   tools/pitchtools/staff_space_transpose
   tools/pitchtools/suggest_clef
   tools/pitchtools/tick_string_to_octave_number
   tools/pitchtools/transpose_by_melodic_chromatic_interval
   tools/pitchtools/transpose_by_melodic_diatonic_interval
   tools/pitchtools/transpose_by_melodic_interval


schemetools

.. toctree::
   :maxdepth: 1

   tools/schemetools/SchemeColor/SchemeColor
   tools/schemetools/SchemeFunction/SchemeFunction
   tools/schemetools/SchemeMoment/SchemeMoment
   tools/schemetools/SchemeString/SchemeString
   tools/schemetools/SchemeVector/SchemeVector


scoretools

.. toctree::
   :maxdepth: 1

   tools/scoretools/make_empty_piano_score
   tools/scoretools/make_piano_score_from_leaves
   tools/scoretools/make_piano_sketch_score_from_leaves
   tools/scoretools/make_pitch_array_score_from_pitch_arrays


sievetools

.. toctree::
   :maxdepth: 1

   tools/sievetools/ResidueClass/ResidueClass
   tools/sievetools/ResidueClassExpression/ResidueClassExpression
   tools/sievetools/cycle_tokens_to_sieve


spacingtools

.. toctree::
   :maxdepth: 1

   tools/spacingtools/SpacingIndication/SpacingIndication
   tools/spacingtools/get_scorewide_spacing


spannertools

.. toctree::
   :maxdepth: 1

   tools/spannertools/find_component_at_score_offset
   tools/spannertools/find_index_at_score_offset
   tools/spannertools/fracture_crossing
   tools/spannertools/get_contained
   tools/spannertools/get_nth_leaf_in_spanner
   tools/spannertools/get_spanners_covered_by_components
   tools/spannertools/get_spanners_on_components_or_component_children
   tools/spannertools/get_spanners_that_cross_components
   tools/spannertools/get_spanners_that_dominate_component_pair
   tools/spannertools/get_spanners_that_dominate_components
   tools/spannertools/get_spanners_that_dominate_container_components_from_to
   tools/spannertools/iterate_components_backward_in_spanner
   tools/spannertools/iterate_components_forward_in_spanner
   tools/spannertools/make_dynamic_spanner_below_with_nib_at_right
   tools/spannertools/make_solid_text_spanner_above_with_nib_at_right
   tools/spannertools/make_solid_text_spanner_below_with_nib_at_right
   tools/spannertools/move_spanners_from_component_to_children_of_component
   tools/spannertools/withdraw_components_from_spanners_covered_by_components


stafftools

.. toctree::
   :maxdepth: 1

   tools/stafftools/make_invisible_staff
   tools/stafftools/make_rhythmic_sketch_staff
   tools/stafftools/make_rhythmic_staff


tempotools

.. toctree::
   :maxdepth: 1

   tools/tempotools/TempoIndication/TempoIndication
   tools/tempotools/integer_tempo_to_multiplier_tempo_pairs
   tools/tempotools/integer_tempo_to_multiplier_tempo_pairs_report


tietools

.. toctree::
   :maxdepth: 1

   tools/tietools/add_or_remove_tie_chain_notes_to_achieve_scaled_written_duration
   tools/tietools/add_or_remove_tie_chain_notes_to_achieve_written_duration
   tools/tietools/apply_tie_spanner_to_leaf_pair
   tools/tietools/are_components_in_same_tie_spanner
   tools/tietools/get_leaves_in_tie_chain
   tools/tietools/get_tie_chain_duration_in_seconds
   tools/tietools/get_tie_chain_preprolated_duration
   tools/tietools/get_tie_chain_prolated_duration
   tools/tietools/get_tie_chain_written_duration
   tools/tietools/get_tie_chains_in_expr
   tools/tietools/group_leaves_in_tie_chain_by_immediate_parents
   tools/tietools/is_tie_chain
   tools/tietools/is_tie_chain_with_all_leaves_in_same_parent
   tools/tietools/label_tie_chains_in_expr_with_prolated_tie_chain_duration
   tools/tietools/label_tie_chains_in_expr_with_tie_chain_durations
   tools/tietools/label_tie_chains_in_expr_with_written_tie_chain_duration
   tools/tietools/remove_all_leaves_in_tie_chain_except_first
   tools/tietools/tie_chain_to_augmented_tuplet_with_proportions_and_avoid_dots
   tools/tietools/tie_chain_to_augmented_tuplet_with_proportions_and_encourage_dots
   tools/tietools/tie_chain_to_diminished_tuplet_with_proportions_and_avoid_dots
   tools/tietools/tie_chain_to_diminished_tuplet_with_proportions_and_encourage_dots


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
   tools/tonalitytools/are_scalar
   tools/tonalitytools/are_stepwise
   tools/tonalitytools/are_stepwise_ascending
   tools/tonalitytools/are_stepwise_descending
   tools/tonalitytools/chord_class_cardinality_to_extent
   tools/tonalitytools/chord_class_extent_to_cardinality
   tools/tonalitytools/chord_class_extent_to_extent_name
   tools/tonalitytools/diatonic_interval_class_segment_to_chord_quality_string
   tools/tonalitytools/is_neighbor_note
   tools/tonalitytools/is_passing_tone
   tools/tonalitytools/is_unlikely_melodic_diatonic_interval_in_chorale


tuplettools

.. toctree::
   :maxdepth: 1

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
   tools/verticalitytools/label_vertical_moments_in_expr_with_chromatic_interval_classes
   tools/verticalitytools/label_vertical_moments_in_expr_with_chromatic_intervals
   tools/verticalitytools/label_vertical_moments_in_expr_with_counterpoint_intervals
   tools/verticalitytools/label_vertical_moments_in_expr_with_diatonic_intervals
   tools/verticalitytools/label_vertical_moments_in_expr_with_interval_class_vectors
   tools/verticalitytools/label_vertical_moments_in_expr_with_numeric_pitch_classes
   tools/verticalitytools/label_vertical_moments_in_expr_with_pitch_numbers
