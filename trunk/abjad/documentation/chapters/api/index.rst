Abjad API
=========

.. toctree::

Classes
-------

.. toctree::
   :maxdepth: 1

   tools/pitchtools/Accidental/Accidental
   measure/anonymous/measure
   articulation/articulation
   tools/lilytools/BookBlock
   tools/lilytools/BookpartBlock
   chord/chord
   tools/pitchtools/ChromaticIntervalVector/ChromaticIntervalVector
   clef/clef
   cluster/cluster
   container/container
   measure/dynamic/measure
   tuplet/fd/tuplet
   tuplet/fm/tuplet
   tools/layout/FixedStaffPositioning/FixedStaffPositioning
   grace/grace
   staffgroup/grandstaff
   tools/pitchtools/HarmonicChromaticInterval/HarmonicChromaticInterval
   tools/pitchtools/HarmonicChromaticIntervalClass/HarmonicChromaticIntervalClass
   tools/pitchtools/HarmonicChromaticIntervalSegment/HarmonicChromaticIntervalSegment
   tools/pitchtools/HarmonicChromaticIntervalSet/HarmonicChromaticIntervalSet
   tools/pitchtools/HarmonicCounterpointInterval/HarmonicCounterpointInterval
   tools/pitchtools/HarmonicCounterpointIntervalClass/HarmonicCounterpointIntervalClass
   tools/pitchtools/HarmonicDiatonicInterval/HarmonicDiatonicInterval
   tools/pitchtools/HarmonicDiatonicIntervalClass/HarmonicDiatonicIntervalClass
   tools/pitchtools/HarmonicDiatonicIntervalSegment/HarmonicDiatonicIntervalSegment
   harmonic/natural
   tools/lilytools/HeaderBlock
   tools/pitchtools/IntervalClass/IntervalClass
   tools/pitchtools/IntervalClassSegment/IntervalClassSegment
   tools/pitchtools/IntervalClassSet/IntervalClassSet
   tools/pitchtools/IntervalClassVector/IntervalClassVector
   staff/invisiblestaff
   key_signature/key_signature
   tools/lilytools/LayoutBlock
   tools/layout/LayoutSchema/LayoutSchema
   tools/lilytools/LilyFile
   markup/markup
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
   meter/meter
   tools/lilytools/MidiBlock
   note/note
   notehead/notehead
   tools/lilytools/PaperBlock
   staffgroup/pianostaff
   pitch/pitch
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
   tools/sievetools/rc
   tools/sievetools/rcexpression
   rational/rational
   rest/rest
   staff/rhythmicsketchstaff
   staff/rhythmicstaff
   measure/rigid/measure
   score/score
   tools/lilytools/ScoreBlock
   skip/skip
   tools/spacing/SpacingIndication/SpacingIndication
   staff/staff
   tools/layout/StaffAlignmentDistances/StaffAlignmentDistances
   tools/layout/StaffAlignmentOffsets/StaffAlignmentOffsets
   staffgroup/staffgroup
   tools/layout/SystemYOffsets/SystemYOffsets
   tools/tempotools/TempoIndication/TempoIndication
   tools/pitchtools/TwelveToneRow/TwelveToneRow
   tools/iterate/VerticalMoment/VerticalMoment
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
   interfaces/dynamics/interface
   interfaces/glissando/interface
   interfaces/grace/interface
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
   interfaces/parentage/interface
   interfaces/piano_pedal/interface
   interfaces/rest/interface
   interfaces/score/interface
   interfaces/spacing/score/interface
   interfaces/slur/interface
   interfaces/spacing/interface
   interfaces/span_bar/interface
   interfaces/staff/interface
   interfaces/stem/interface
   interfaces/tempo/interface
   interfaces/text_script/interface
   interfaces/text_spanner/interface
   interfaces/thread/interface
   interfaces/tie/interface
   interfaces/tremolo/interface
   interfaces/trill/interface
   interfaces/tuplet_bracket/interface
   interfaces/tuplet_number/interface
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

   tools/check/are_scalable
   tools/check/assert_components
   tools/check/assert_wf
   tools/check/assess_components
   tools/check/profile
   tools/check/wf


chordtools

.. toctree::
   :maxdepth: 1

   tools/chordtools/arpeggiate
   tools/chordtools/cast_defective
   tools/chordtools/color_note_heads_by_pc
   tools/chordtools/get_note_head
   tools/chordtools/split_by_altitude
   tools/chordtools/split_by_pitch_number
   tools/chordtools/subchords


clone

.. toctree::
   :maxdepth: 1

   tools/clone/covered
   tools/clone/fracture
   tools/clone/unspan


clonewp

.. toctree::
   :maxdepth: 1

   tools/clonewp/by_duration_with_parentage
   tools/clonewp/by_leaf_counts_with_parentage
   tools/clonewp/by_leaf_range_with_parentage
   tools/clonewp/with_parent


componenttools

.. toctree::
   :maxdepth: 1

   tools/componenttools/detach
   tools/componenttools/flip
   tools/componenttools/get_duration_crossers
   tools/componenttools/get_duration_preprolated
   tools/componenttools/get_le_duration_prolated
   tools/componenttools/get_likely_multiplier
   tools/componenttools/slip
   tools/componenttools/untie_shallow


construct

.. toctree::
   :maxdepth: 1

   tools/construct/engender
   tools/construct/leaves
   tools/construct/note_train
   tools/construct/notes
   tools/construct/notes_curve
   tools/construct/percussion_note
   tools/construct/pitches
   tools/construct/quarter_notes_with_multipliers
   tools/construct/rests
   tools/construct/run
   tools/construct/scale
   tools/construct/skips_with_multipliers


containertools

.. toctree::
   :maxdepth: 1

   tools/containertools/contents_color
   tools/containertools/contents_delete
   tools/containertools/contents_delete_starting_not_before_prolated_offset
   tools/containertools/contents_multiply
   tools/containertools/contents_reverse
   tools/containertools/contents_scale
   tools/containertools/extend_cyclic
   tools/containertools/get_element_starting_at_prolated_offset
   tools/containertools/get_first_element_starting_not_before_prolated_offset
   tools/containertools/get_first_index_starting_not_before_prolated_offset
   tools/containertools/get_index_starting_at_prolated_offset
   tools/containertools/insert_and_fracture
   tools/containertools/multiplier_set
   tools/containertools/remove_empty
   tools/containertools/rest_by_count
   tools/containertools/rest_half


cut

.. toctree::
   :maxdepth: 1

   tools/cut/by_duration


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
   tools/durtools/denominator_to_multiplier
   tools/durtools/diagonalize_all_assignable_durations
   tools/durtools/diagonalize_all_positive_integer_pairs
   tools/durtools/diagonalize_all_rationals
   tools/durtools/diagonalize_all_rationals_unique
   tools/durtools/group_prolated
   tools/durtools/group_seconds
   tools/durtools/in_terms_of
   tools/durtools/in_terms_of_binary_multiple
   tools/durtools/is_assignable
   tools/durtools/is_binary_rational
   tools/durtools/is_duration_token
   tools/durtools/is_pair
   tools/durtools/is_tuplet_multiplier
   tools/durtools/naive_prolated_to_written_not_greater_than
   tools/durtools/naive_prolated_to_written_not_less_than
   tools/durtools/pair_multiply_constant_numerator
   tools/durtools/pair_multiply_naive
   tools/durtools/pair_multiply_reduce_factors
   tools/durtools/pair_to_prolation_string
   tools/durtools/prolated_to_prolated
   tools/durtools/prolated_to_prolation_written_pairs
   tools/durtools/prolated_to_written_not_greater_than
   tools/durtools/prolated_to_written_not_less_than
   tools/durtools/rational_to_fraction_string
   tools/durtools/rational_to_prolation_string
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

   tools/formattools/report
   tools/formattools/wrapper


fuse

.. toctree::
   :maxdepth: 1

   tools/fuse/containers_by_reference
   tools/fuse/contents_by_count
   tools/fuse/leaves_by_reference
   tools/fuse/leaves_in_tie_chain
   tools/fuse/measures_by_count_cyclic
   tools/fuse/measures_by_reference
   tools/fuse/tie_chains_by_durations
   tools/fuse/tuplets_by_reference


harmonictools

.. toctree::
   :maxdepth: 1

   tools/harmonictools/add_artificial


interpolate

.. toctree::
   :maxdepth: 1

   tools/interpolate/cosine
   tools/interpolate/divide
   tools/interpolate/divide_multiple
   tools/interpolate/exponential
   tools/interpolate/linear


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
   tools/io/write_and_show
   tools/io/write_ly
   tools/io/write_pdf


iterate

.. toctree::
   :maxdepth: 1

   tools/iterate/chained_contents
   tools/iterate/depth_first
   tools/iterate/get_nth_component
   tools/iterate/get_nth_leaf
   tools/iterate/get_nth_measure
   tools/iterate/get_vertical_moment_at_prolated_offset_in
   tools/iterate/get_vertical_moment_starting_with
   tools/iterate/grace
   tools/iterate/leaf_pairs_forward_in
   tools/iterate/leaves_backward_in
   tools/iterate/leaves_forward_in
   tools/iterate/measure_next
   tools/iterate/measure_prev
   tools/iterate/measures_backward_in
   tools/iterate/measures_forward_in
   tools/iterate/naive_backward_in
   tools/iterate/naive_backward_in
   tools/iterate/naive_forward_in
   tools/iterate/naive_forward_in
   tools/iterate/namesakes_backward_from
   tools/iterate/namesakes_forward_from
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

   tools/layout/apply_fixed_staff_positioning
   tools/layout/apply_layout_schema
   tools/layout/insert_measure_padding_rest
   tools/layout/insert_measure_padding_skip
   tools/layout/line_break_every_prolated
   tools/layout/line_break_every_seconds


leaftools

.. toctree::
   :maxdepth: 1

   tools/leaftools/composite_offset_difference_series
   tools/leaftools/composite_offset_series
   tools/leaftools/copy_duration_from_to
   tools/leaftools/duration_change
   tools/leaftools/duration_rewrite
   tools/leaftools/duration_scale
   tools/leaftools/excise
   tools/leaftools/get_durations_prolated
   tools/leaftools/get_durations_written
   tools/leaftools/has_dotted_written_duration
   tools/leaftools/leaves_to_skips
   tools/leaftools/meiose
   tools/leaftools/multiply
   tools/leaftools/show_leaves


lilytools

.. toctree::
   :maxdepth: 1

   tools/lilytools/make_basic_lily_file
   tools/lilytools/save_ly_as
   tools/lilytools/save_pdf_as


listtools

.. toctree::
   :maxdepth: 1

   tools/listtools/all_ordered_sublists
   tools/listtools/all_restricted_growth_functions_of_length
   tools/listtools/all_set_partitions
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
   tools/listtools/get_period
   tools/listtools/get_unordered_pairs
   tools/listtools/group_by_equality
   tools/listtools/group_by_sign
   tools/listtools/group_by_weights
   tools/listtools/increase_at_indices
   tools/listtools/increase_cyclic
   tools/listtools/insert_slice_cyclic
   tools/listtools/interlace
   tools/listtools/is_assignable
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
   tools/listtools/sign
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
   tools/mathtools/is_assignable
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

   tools/measuretools/beam
   tools/measuretools/beam_together
   tools/measuretools/binary_to_nonbinary
   tools/measuretools/color_nonbinary
   tools/measuretools/concentrate
   tools/measuretools/denominator_set
   tools/measuretools/make
   tools/measuretools/make_underfull_spacer_skip
   tools/measuretools/overdraw
   tools/measuretools/overwrite_contents
   tools/measuretools/pitch_array_row_to_measure
   tools/measuretools/pitch_array_to_measures
   tools/measuretools/populate
   tools/measuretools/project
   tools/measuretools/remedy_underfull_measures
   tools/measuretools/report_meter_distribution
   tools/measuretools/scale
   tools/measuretools/scale_and_remeter
   tools/measuretools/spin
   tools/measuretools/subsume
   tools/measuretools/tupletize


metertools

.. toctree::
   :maxdepth: 1

   tools/metertools/extract_meter_list
   tools/metertools/get_nonbinary_factor
   tools/metertools/is_binary_equivalent
   tools/metertools/is_meter_token
   tools/metertools/make_best
   tools/metertools/make_binary


overridetools

.. toctree::
   :maxdepth: 1

   tools/overridetools/clear_all
   tools/overridetools/promote


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

   tools/persistencetools/pickle_dump
   tools/persistencetools/pickle_load
   tools/persistencetools/pitch_and_rhythm_skeleton


pitchtools

.. toctree::
   :maxdepth: 1

   tools/pitchtools/apply_octavation
   tools/pitchtools/are_in_octave_order
   tools/pitchtools/array_to_nonspanning_subarrays
   tools/pitchtools/change_default_accidental_spelling
   tools/pitchtools/chromaticize
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
   tools/pitchtools/is_pair
   tools/pitchtools/is_pitch_token
   tools/pitchtools/is_pitch_token_collection
   tools/pitchtools/leaf_iterables_to_pitch_array_empty
   tools/pitchtools/leaf_iterables_to_pitch_array_populated
   tools/pitchtools/letter_to_diatonic_scale_degree
   tools/pitchtools/letter_to_pc
   tools/pitchtools/make_all_aggregate_subsets
   tools/pitchtools/make_flat
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
   tools/pitchtools/pitch_number_and_accidental_semitones_to_octave
   tools/pitchtools/pitch_number_to_octave
   tools/pitchtools/pitch_pairs_from_to
   tools/pitchtools/pitch_pairs_within
   tools/pitchtools/pitches_to_diatonic_interval
   tools/pitchtools/registrate
   tools/pitchtools/send_pitch_number_to_octave
   tools/pitchtools/sort_by_pc
   tools/pitchtools/staff_space_transpose
   tools/pitchtools/suggest_clef
   tools/pitchtools/transpose_by_melodic_chromatic_interval
   tools/pitchtools/transpose_by_melodic_diatonic_interval
   tools/pitchtools/transpose_by_melodic_interval


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


sievetools

.. toctree::
   :maxdepth: 1

   tools/sievetools/cycle_tokens_to_sieve


spacing

.. toctree::
   :maxdepth: 1

   tools/spacing/get_scorewide


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

   tools/tempotools/integer_tempo_to_multiplier_tempo_pairs
   tools/tempotools/integer_tempo_to_multiplier_tempo_pairs_report


tietools

.. toctree::
   :maxdepth: 1

   tools/tietools/are_in_same_spanner
   tools/tietools/duration_change
   tools/tietools/duration_scale
   tools/tietools/get_duration_preprolated
   tools/tietools/get_duration_prolated
   tools/tietools/get_duration_seconds
   tools/tietools/get_duration_written
   tools/tietools/get_leaves
   tools/tietools/get_tie_chains
   tools/tietools/group_by_parent
   tools/tietools/is_chain
   tools/tietools/is_in_same_parent
   tools/tietools/span_leaf_pair
   tools/tietools/truncate


tuplettools

.. toctree::
   :maxdepth: 1

   tools/tuplettools/augmentation_to_diminution
   tools/tuplettools/beam_bottommost
   tools/tuplettools/contents_fix
   tools/tuplettools/contents_scale
   tools/tuplettools/diminution_to_augmentation
   tools/tuplettools/slip_trivial
   tools/tuplettools/subsume
