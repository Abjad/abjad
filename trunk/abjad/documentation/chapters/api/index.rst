Abjad API
=========

.. toctree::

Classes
-------

.. toctree::
   :maxdepth: 1

   measure/anonymous/measure
   articulation/articulation
   chord/chord
   clef/clef
   cluster/cluster
   container/container
   measure/dynamic/measure
   tuplet/fd/tuplet
   tuplet/fm/tuplet
   grace/grace
   staffgroup/grandstaff
   harmonic/natural
   staff/invisiblestaff
   key_signature/key_signature
   markup/markup
   meter/meter
   note/note
   notehead/notehead
   staffgroup/pianostaff
   pitch/pitch
   rational/rational
   rest/rest
   staff/rhythmicsketchstaff
   staff/rhythmicstaff
   measure/rigid/measure
   score/score
   skip/skip
   staff/staff
   staffgroup/staffgroup
   voice/voice


Interfaces
----------

.. toctree::
   :maxdepth: 1

   interfaces/accidental/interface
   interfaces/articulation/interface
   interfaces/bar_line/interface
   interfaces/bar_number/interface
   interfaces/beam/interface
   interfaces/brackets/interface
   interfaces/breaks/interface
   interfaces/clef/interface
   interfaces/cluster/interface
   interfaces/comments/interface
   interfaces/directives/interface
   interfaces/dots/interface
   interfaces/dynamic_line_spanner/interface
   interfaces/dynamic_text/interface
   interfaces/dynamic_text_spanner/interface
   interfaces/dynamics/interface
   interfaces/glissando/interface
   interfaces/grace/interface
   interfaces/hairpin/interface
   interfaces/harmonic/interface
   interfaces/history/interface
   interfaces/instrument/interface
   interfaces/interface_aggregator/aggregator
   interfaces/key_signature/interface
   interfaces/markup/interface
   interfaces/meter/interface
   interfaces/non_musical_paper_column/interface
   interfaces/note_column/interface
   interfaces/note_head/interface
   interfaces/numbering/interface
   interfaces/offset/interface
   interfaces/offset/prolated/interface
   interfaces/ottava_bracket/interface
   interfaces/parentage/interface
   interfaces/piano_pedal/interface
   interfaces/rehearsal_mark/interface
   interfaces/rest/interface
   interfaces/score/interface
   interfaces/spacing/score/interface
   interfaces/script/interface
   interfaces/slur/interface
   interfaces/spacing/interface
   interfaces/span_bar/interface
   interfaces/staff/interface
   interfaces/stem/interface
   interfaces/stem_tremolo/interface
   interfaces/system_start_bar/interface
   interfaces/tempo/interface
   interfaces/text_script/interface
   interfaces/text_spanner/interface
   interfaces/thread/interface
   interfaces/tie/interface
   interfaces/tremolo/interface
   interfaces/trill/interface
   interfaces/trill_pitch_accidental/interface
   interfaces/tuplet_bracket/interface
   interfaces/tuplet_number/interface
   interfaces/vertical_alignment/interface
   interfaces/vertical_axis_group/interface
   interfaces/voice/interface


Spanners
--------

.. toctree::
   :maxdepth: 1

   spanners/beam/spanner
   spanners/beam/complex/spanner
   spanners/beam/complex/durated/spanner
   spanners/beam/complex/measured/spanner
   spanners/bracket/spanner
   spanners/crescendo/spanner
   spanners/decrescendo/spanner
   spanners/dynamics/spanner
   spanners/glissando/spanner
   spanners/hairpin/spanner
   spanners/instrument/spanner
   spanners/metric_grid/spanner
   spanners/octavation/spanner
   spanners/override/spanner
   spanners/piano_pedal/spanner
   spanners/slur/spanner
   spanners/spacing/spanner
   spanners/spanner/spanner
   spanners/tempo/spanner
   spanners/tempo/proportional/spanner
   spanners/text_script/spanner
   spanners/text/spanner
   spanners/tie/spanner
   spanners/trill/spanner


Tools
-----

.. toctree::
   :maxdepth: 1



cfgtools

.. toctree::
   :maxdepth: 1

   tools/cfgtools/list_settings


check

.. toctree::
   :maxdepth: 1

   tools/check/assert_components
   tools/check/assert_wf
   tools/check/assess_components
   tools/check/profile
   tools/check/wf


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

   tools/componenttools/clone_and_partition_governed_component_subtree_by_leaf_counts
   tools/componenttools/clone_components_and_covered_spanners
   tools/componenttools/clone_components_and_fracture_crossing_spanners
   tools/componenttools/clone_components_and_immediate_parent_of_first_component
   tools/componenttools/clone_components_and_remove_all_spanners
   tools/componenttools/clone_governed_component_subtree_by_leaf_range
   tools/componenttools/clone_governed_component_subtree_from_prolated_duration_to
   tools/componenttools/cut_component_at_prolated_duration
   tools/componenttools/get_likely_multiplier_of_components
   tools/componenttools/get_preprolated_duration_of_components
   tools/componenttools/list_improper_contents_of_component_that_cross_prolated_offset
   tools/componenttools/list_leftmost_components_with_prolated_duration_at_most
   tools/componenttools/move_component_subtree_to_right_in_score_and_spanners
   tools/componenttools/remove_component_subtree_from_score_and_spanners
   tools/componenttools/remove_tie_spanners_from_components
   tools/componenttools/replace_components_with_children_of_components


containertools

.. toctree::
   :maxdepth: 1

   tools/containertools/color_contents_of_container
   tools/containertools/delete_contents_of_container
   tools/containertools/delete_contents_of_container_starting_at_or_after_prolated_offset
   tools/containertools/delete_contents_of_container_starting_before_or_at_prolated_offset
   tools/containertools/delete_contents_of_container_starting_strictly_after_prolated_offset
   tools/containertools/delete_contents_of_container_starting_strictly_before_prolated_offset
   tools/containertools/get_element_starting_at_exactly_prolated_offset
   tools/containertools/get_first_element_starting_at_or_after_prolated_offset
   tools/containertools/get_first_element_starting_before_or_at_prolated_offset
   tools/containertools/get_first_element_starting_strictly_after_prolated_offset
   tools/containertools/get_first_element_starting_strictly_before_prolated_offset
   tools/containertools/insert_component_and_do_not_fracture_crossing_spanners
   tools/containertools/insert_component_and_fracture_crossing_spanners
   tools/containertools/remove_empty_containers_in_expr
   tools/containertools/repeat_contents_of_container
   tools/containertools/repeat_last_n_elements_of_container
   tools/containertools/rest_by_count
   tools/containertools/rest_half
   tools/containertools/reverse_contents_of_container
   tools/containertools/scale_contents_of_container
   tools/containertools/set_container_multiplier


divide

.. toctree::
   :maxdepth: 1

   tools/divide/duration_into_arbitrary_augmentation_dotted
   tools/divide/duration_into_arbitrary_augmentation_undotted
   tools/divide/duration_into_arbitrary_diminution_dotted
   tools/divide/duration_into_arbitrary_diminution_undotted
   tools/divide/leaf_into_arbitrary_augmentation
   tools/divide/leaf_into_arbitrary_diminution
   tools/divide/leaf_into_even_augmentation
   tools/divide/leaf_into_even_diminution
   tools/divide/pair
   tools/divide/tie_chain_into_arbitrary_augmentation_dotted
   tools/divide/tie_chain_into_arbitrary_augmentation_undotted
   tools/divide/tie_chain_into_arbitrary_diminution_dotted
   tools/divide/tie_chain_into_arbitrary_diminution_undotted


durtools

.. toctree::
   :maxdepth: 1

   tools/durtools/agglomerate_by_prolation
   tools/durtools/are_scalable
   tools/durtools/denominator_to_multiplier
   tools/durtools/diagonalize_all_assignable_durations
   tools/durtools/diagonalize_all_positive_integer_pairs
   tools/durtools/diagonalize_all_rationals
   tools/durtools/diagonalize_all_rationals_unique
   tools/durtools/duration_string_to_rational
   tools/durtools/duration_string_to_rationals
   tools/durtools/group_by_duration_preprolated
   tools/durtools/group_by_duration_prolated
   tools/durtools/group_prolated
   tools/durtools/group_seconds
   tools/durtools/in_terms_of
   tools/durtools/in_terms_of_binary_multiple
   tools/durtools/is_assignable_duration
   tools/durtools/is_binary_rational
   tools/durtools/is_duration_pair
   tools/durtools/is_duration_token
   tools/durtools/is_tuplet_multiplier
   tools/durtools/naive_prolated_to_written_not_greater_than
   tools/durtools/naive_prolated_to_written_not_less_than
   tools/durtools/pair_multiply_constant_numerator
   tools/durtools/pair_multiply_naive
   tools/durtools/pair_multiply_reduce_factors
   tools/durtools/pair_to_prolation_string
   tools/durtools/partition_noncyclic_with_overhang_by_durations_prolated
   tools/durtools/partition_noncyclic_with_overhang_by_durations_prolated_not_less_than
   tools/durtools/partition_noncyclic_without_overhang_by_durations_prolated
   tools/durtools/partition_noncyclic_without_overhang_by_durations_prolated_not_less_than
   tools/durtools/prolated_to_prolated
   tools/durtools/prolated_to_prolation_written_pairs
   tools/durtools/prolated_to_written_not_greater_than
   tools/durtools/prolated_to_written_not_less_than
   tools/durtools/rational_to_dot_count
   tools/durtools/rational_to_duration_string
   tools/durtools/rational_to_flag_count
   tools/durtools/rational_to_fraction_string
   tools/durtools/rational_to_prolation_string
   tools/durtools/rational_to_undotted_duration
   tools/durtools/rational_to_undotted_duration_string
   tools/durtools/rationalize
   tools/durtools/seconds_to_clock_string
   tools/durtools/seconds_to_clock_string_escaped
   tools/durtools/sum_preprolated
   tools/durtools/sum_prolated
   tools/durtools/sum_seconds
   tools/durtools/token_decompose
   tools/durtools/token_unpack
   tools/durtools/within_prolated
   tools/durtools/within_seconds


formattools

.. toctree::
   :maxdepth: 1

   tools/formattools/docstring
   tools/formattools/regression
   tools/formattools/report
   tools/formattools/wrapper


fuse

.. toctree::
   :maxdepth: 1

   tools/fuse/containers_by_reference
   tools/fuse/contents_by_counts
   tools/fuse/leaves_by_reference
   tools/fuse/leaves_in_tie_chain
   tools/fuse/measures_by_counts_cyclic
   tools/fuse/measures_by_reference
   tools/fuse/tied_leaves_by_prolated_durations
   tools/fuse/tuplets_by_reference


io

.. toctree::
   :maxdepth: 1

   tools/io/f
   tools/io/log
   tools/io/ly
   tools/io/pdf
   tools/io/play
   tools/io/redo
   tools/io/show
   tools/io/write_expr_to_ly
   tools/io/write_expr_to_ly_and_to_pdf_and_show
   tools/io/write_expr_to_pdf


iterate

.. toctree::
   :maxdepth: 1

   tools/iterate/VerticalMoment/VerticalMoment
   tools/iterate/chained_contents
   tools/iterate/depth_first
   tools/iterate/get_measure_leaf
   tools/iterate/get_measure_number
   tools/iterate/get_nth_component
   tools/iterate/get_nth_leaf_in
   tools/iterate/get_nth_measure
   tools/iterate/get_nth_namesake_from
   tools/iterate/get_vertical_moment_at_prolated_offset_in
   tools/iterate/get_vertical_moment_starting_with
   tools/iterate/grace
   tools/iterate/group_by_type_and_yield_groups
   tools/iterate/group_by_type_and_yield_groups_of_klass
   tools/iterate/leaf_pairs_forward_in
   tools/iterate/leaves_backward_in
   tools/iterate/leaves_forward_in
   tools/iterate/measure_next
   tools/iterate/measure_prev
   tools/iterate/measures_backward_in
   tools/iterate/measures_forward_in
   tools/iterate/naive_backward_in
   tools/iterate/naive_forward_in
   tools/iterate/namesakes_backward_from
   tools/iterate/namesakes_forward_from
   tools/iterate/notes_backward_in
   tools/iterate/notes_forward_in
   tools/iterate/pitch_pairs_forward_in
   tools/iterate/thread_backward_from
   tools/iterate/thread_backward_in
   tools/iterate/thread_forward_from
   tools/iterate/thread_forward_in
   tools/iterate/tie_chains_backward_in
   tools/iterate/tie_chains_forward_in
   tools/iterate/timeline_backward_from
   tools/iterate/timeline_backward_in
   tools/iterate/timeline_forward_from
   tools/iterate/timeline_forward_in
   tools/iterate/vertical_moments_backward_in
   tools/iterate/vertical_moments_forward_in


label

.. toctree::
   :maxdepth: 1

   tools/label/clear_leaves
   tools/label/leaf_depth
   tools/label/leaf_depth_tuplet
   tools/label/leaf_durations
   tools/label/leaf_indices
   tools/label/leaf_numbers
   tools/label/leaf_pcs
   tools/label/leaf_pitch_numbers
   tools/label/measure_numbers
   tools/label/melodic_chromatic_interval_classes
   tools/label/melodic_chromatic_intervals
   tools/label/melodic_counterpoint_interval_classes
   tools/label/melodic_counterpoint_intervals
   tools/label/melodic_diatonic_interval_classes
   tools/label/melodic_diatonic_intervals
   tools/label/vertical_moment_chromatic_interval_classes
   tools/label/vertical_moment_chromatic_intervals
   tools/label/vertical_moment_counterpoint_intervals
   tools/label/vertical_moment_diatonic_intervals
   tools/label/vertical_moment_interval_class_vectors
   tools/label/vertical_moment_pitch_classes
   tools/label/vertical_moment_pitch_numbers


layout

.. toctree::
   :maxdepth: 1

   tools/layout/FixedStaffPositioning/FixedStaffPositioning
   tools/layout/LayoutSchema/LayoutSchema
   tools/layout/StaffAlignmentDistances/StaffAlignmentDistances
   tools/layout/StaffAlignmentOffsets/StaffAlignmentOffsets
   tools/layout/SystemYOffsets/SystemYOffsets
   tools/layout/apply_fixed_staff_positioning
   tools/layout/apply_layout_schema
   tools/layout/insert_measure_padding_rest
   tools/layout/insert_measure_padding_skip
   tools/layout/line_break_every_prolated
   tools/layout/line_break_every_seconds


leaftools

.. toctree::
   :maxdepth: 1

   tools/leaftools/add_artificial_harmonic_to_note
   tools/leaftools/change_leaf_preprolated_duration
   tools/leaftools/change_written_duration_and_preserve_preprolated_duration
   tools/leaftools/clone_and_splice_leaf
   tools/leaftools/clone_and_splice_leaves_in
   tools/leaftools/color_leaf
   tools/leaftools/color_leaves_in
   tools/leaftools/copy_written_duration_and_multiplier_from_to
   tools/leaftools/divide_leaf_meiotically
   tools/leaftools/divide_leaves_meiotically_in
   tools/leaftools/get_composite_offset_difference_series
   tools/leaftools/get_composite_offset_series
   tools/leaftools/get_durations_prolated
   tools/leaftools/get_durations_written
   tools/leaftools/has_leaf_with_dotted_written_duration_in
   tools/leaftools/is_bar_line_crossing_leaf
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
   tools/leaftools/replace_leaves_with_skips_in
   tools/leaftools/scale_leaf_preprolated_duration
   tools/leaftools/split_leaf_at_prolated_duration_and_rest_right_half


lilytools

.. toctree::
   :maxdepth: 1

   tools/lilytools/BookBlock/BookBlock
   tools/lilytools/BookpartBlock/BookpartBlock
   tools/lilytools/HeaderBlock/HeaderBlock
   tools/lilytools/LayoutBlock/LayoutBlock
   tools/lilytools/LilyFile/LilyFile
   tools/lilytools/MidiBlock/MidiBlock
   tools/lilytools/PaperBlock/PaperBlock
   tools/lilytools/ScoreBlock/ScoreBlock
   tools/lilytools/make_basic_lily_file
   tools/lilytools/parse_note_entry_string
   tools/lilytools/save_ly_as
   tools/lilytools/save_pdf_as


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


markup

.. toctree::
   :maxdepth: 1

   tools/markup/big_centered_page_number


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
   tools/measuretools/change_binary_measure_to_nonbinary
   tools/measuretools/color_measure
   tools/measuretools/color_nonbinary_measures_in
   tools/measuretools/make
   tools/measuretools/multiply_measure_contents_and_scale_meter_denominator_in
   tools/measuretools/multiply_measure_contents_in
   tools/measuretools/pitch_array_row_to_measure
   tools/measuretools/pitch_array_to_measures
   tools/measuretools/populate
   tools/measuretools/project
   tools/measuretools/replace_measure_contents_in
   tools/measuretools/report_meter_distribution
   tools/measuretools/scale_and_remeter
   tools/measuretools/scale_measure_contents_in
   tools/measuretools/set_measure_denominator_and_multiply_numerator
   tools/measuretools/subsume
   tools/measuretools/tupletize


metertools

.. toctree::
   :maxdepth: 1

   tools/metertools/extract_meter_list
   tools/metertools/get_nonbinary_factor
   tools/metertools/is_meter_token
   tools/metertools/is_meter_with_equivalent_binary_representation
   tools/metertools/make_best
   tools/metertools/meter_to_binary_meter


overridetools

.. toctree::
   :maxdepth: 1

   tools/overridetools/clear_all_overrides_on_grob_handler
   tools/overridetools/promote_attribute_to_context_on_grob_handler


parenttools

.. toctree::
   :maxdepth: 1

   tools/parenttools/get_first
   tools/parenttools/get_with_indices


partition

.. toctree::
   :maxdepth: 1

   tools/partition/cyclic_fractured_by_counts
   tools/partition/cyclic_fractured_by_durations
   tools/partition/cyclic_unfractured_by_counts
   tools/partition/cyclic_unfractured_by_durations
   tools/partition/fractured_by_counts
   tools/partition/fractured_by_durations
   tools/partition/unfractured_by_counts
   tools/partition/unfractured_by_durations


persistencetools

.. toctree::
   :maxdepth: 1

   tools/persistencetools/component_to_pitch_and_rhythm_skeleton
   tools/persistencetools/pickle_dump
   tools/persistencetools/pickle_load


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

   tools/scoretools/bequeath
   tools/scoretools/donate
   tools/scoretools/find
   tools/scoretools/make_piano_score
   tools/scoretools/make_piano_sketch_score
   tools/scoretools/make_piano_staff
   tools/scoretools/pitch_arrays_to_score
   tools/scoretools/set_accidental_style
   tools/scoretools/show_leaves


sievetools

.. toctree::
   :maxdepth: 1

   tools/sievetools/RC/RC
   tools/sievetools/RCExpression/RCExpression
   tools/sievetools/cycle_tokens_to_sieve


spacing

.. toctree::
   :maxdepth: 1

   tools/spacing/SpacingIndication/SpacingIndication
   tools/spacing/get_scorewide_spacing


spanners

.. toctree::
   :maxdepth: 1

   tools/spanners/dynamic_spanner_below_with_nib_at_right
   tools/spanners/solid_text_spanner_above_with_nib_at_right
   tools/spanners/solid_text_spanner_below_with_nib_at_right


spannertools

.. toctree::
   :maxdepth: 1

   tools/spannertools/find_component_at_score_offset
   tools/spannertools/find_index_at_score_offset
   tools/spannertools/fracture_crossing
   tools/spannertools/get_attached
   tools/spannertools/get_contained
   tools/spannertools/get_covered
   tools/spannertools/get_crossing
   tools/spannertools/get_dominant
   tools/spannertools/get_dominant_between
   tools/spannertools/get_dominant_slice
   tools/spannertools/get_nth_leaf
   tools/spannertools/give_attached_to_children
   tools/spannertools/iterate_components_backward
   tools/spannertools/iterate_components_forward
   tools/spannertools/withdraw_from_covered


split

.. toctree::
   :maxdepth: 1

   tools/split/fractured_at_duration
   tools/split/fractured_at_index
   tools/split/unfractured_at_duration
   tools/split/unfractured_at_index


tempotools

.. toctree::
   :maxdepth: 1

   tools/tempotools/TempoIndication/TempoIndication
   tools/tempotools/integer_tempo_to_multiplier_tempo_pairs
   tools/tempotools/integer_tempo_to_multiplier_tempo_pairs_report


tietools

.. toctree::
   :maxdepth: 1

   tools/tietools/are_in_same_spanner
   tools/tietools/duration_change
   tools/tietools/duration_scale
   tools/tietools/get_duration_prolated
   tools/tietools/get_duration_seconds
   tools/tietools/get_duration_written
   tools/tietools/get_leaves
   tools/tietools/get_tie_chain_duration_preprolated
   tools/tietools/get_tie_chains
   tools/tietools/group_by_parent
   tools/tietools/is_chain
   tools/tietools/is_in_same_parent
   tools/tietools/span_leaf_pair
   tools/tietools/truncate


tonalharmony

.. toctree::
   :maxdepth: 1

   tools/tonalharmony/ChordClass/ChordClass
   tools/tonalharmony/ChordQualityIndicator/ChordQualityIndicator
   tools/tonalharmony/DoublingIndicator/DoublingIndicator
   tools/tonalharmony/ExtentIndicator/ExtentIndicator
   tools/tonalharmony/InversionIndicator/InversionIndicator
   tools/tonalharmony/Mode/Mode
   tools/tonalharmony/OmissionIndicator/OmissionIndicator
   tools/tonalharmony/QualityIndicator/QualityIndicator
   tools/tonalharmony/Scale/Scale
   tools/tonalharmony/ScaleDegree/ScaleDegree
   tools/tonalharmony/SuspensionIndicator/SuspensionIndicator
   tools/tonalharmony/TonalFunction/TonalFunction
   tools/tonalharmony/analyze_chord
   tools/tonalharmony/analyze_incomplete_chord
   tools/tonalharmony/analyze_incomplete_tonal_function
   tools/tonalharmony/analyze_tonal_function
   tools/tonalharmony/are_scalar
   tools/tonalharmony/are_stepwise
   tools/tonalharmony/are_stepwise_ascending
   tools/tonalharmony/are_stepwise_descending
   tools/tonalharmony/chord_class_cardinality_to_extent
   tools/tonalharmony/chord_class_extent_to_cardinality
   tools/tonalharmony/chord_class_extent_to_extent_name
   tools/tonalharmony/diatonic_interval_class_segment_to_chord_quality_string
   tools/tonalharmony/is_neighbor_note
   tools/tonalharmony/is_passing_tone
   tools/tonalharmony/is_unlikely_melodic_diatonic_interval_in_chorale


tuplettools

.. toctree::
   :maxdepth: 1

   tools/tuplettools/beam_bottommost_tuplets_in_expr
   tools/tuplettools/change_augmented_tuplets_in_expr_to_diminished
   tools/tuplettools/change_diminished_tuplets_in_expr_to_augmented
   tools/tuplettools/fix_contents_of_tuplets_in_expr
   tools/tuplettools/move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet
   tools/tuplettools/remove_trivial_tuplets_in_expr
   tools/tuplettools/scale_contents_of_tuplets_in_expr_by_multiplier
