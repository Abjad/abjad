Abjad API
=========

.. toctree::

Classes
-------

.. toctree::
   :maxdepth: 1

   accidental/accidental
   accidental/interface
   measure/anonymous/measure
   articulations/articulation
   articulations/interface
   barline/interface
   barnumber/interface
   beam/spanner
   beam/complex/spanner
   beam/complex/durated/spanner
   beam/complex/measured/spanner
   beam/interface
   bracket/spanner
   brackets/interface
   breaks/interface
   chord/chord
   clef/clef
   clef/interface
   cluster/cluster
   cluster/interface
   container/container
   dots/interface
   dynamics/spanner
   measure/dynamic/measure
   dynamics/interface
   tuplet/fd/tuplet
   tuplet/fm/tuplet
   layout/fixed_staff_positioning
   glissando/spanner
   glissando/interface
   grace/grace
   grace/interface
   hairpin/spanner
   harmonic/interface
   history/interface
   instrument/spanner
   instrument/interface
   interfaces/aggregator
   markup/markup
   markup/interface
   meter/meter
   meter/interface
   metricgrid/spanner
   note/note
   notecolumn/interface
   notehead/notehead
   notehead/interface
   numbering/interface
   octavation/spanner
   offset/interface
   offset/prolated/interface
   override/spanner
   parentage/parentage
   pianopedal/spanner
   pianopedal/interface
   pitch/pitch
   rational/rational
   rest/rest
   rest/interface
   measure/rigid/measure
   score/score
   score/interface/interface
   skip/skip
   slur/spanner
   slur/interface
   spacing/indication
   spacing/interface
   spacing/spanner
   spanbar/interface
   spanner/spanner
   staff/staff
   layout/staff_alignment_offsets
   staffgroup/staffgroup
   staff/interface/interface
   stem/interface
   layout/system_y_offsets
   tempo/spanner
   tempo/indication
   tempo/interface
   tempo/proportional/spanner
   text/spanner
   text/interface
   thread/interface
   tie/spanner
   tie/interface
   tremolo/interface
   trill/spanner
   trill/interface
   tuplet/bracket
   tuplet/number
   comments/comments
   directives/interface
   voice/voice
   voice/interface/interface
   debug/debug


Facade classes

.. toctree::
   :maxdepth: 1

   hairpin/crescendo
   hairpin/decrescendo
   staffgroup/grandstaff
   staff/invisiblestaff
   staffgroup/pianostaff
   staff/rhythmicsketchstaff
   staff/rhythmicstaff
   navigator/dfs


Tools
-----

.. toctree::
   :maxdepth: 1



cfgtools

.. toctree::
   :maxdepth: 1

   tools/cfgtools/list_helpers
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
   tools/chordtools/get_notehead
   tools/chordtools/split


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
   tools/construct/rests
   tools/construct/run
   tools/construct/scale


containertools

.. toctree::
   :maxdepth: 1

   tools/containertools/contents_delete
   tools/containertools/contents_multiply
   tools/containertools/contents_reverse
   tools/containertools/contents_scale
   tools/containertools/extend_cyclic
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

   tools/divide/leaf
   tools/divide/pair
   tools/divide/tie_chain


durtools

.. toctree::
   :maxdepth: 1

   tools/durtools/agglomerate_by_prolation
   tools/durtools/denominator_to_multiplier
   tools/durtools/group_prolated
   tools/durtools/group_seconds
   tools/durtools/in_terms_of
   tools/durtools/in_terms_of_binary_multiple
   tools/durtools/is_assignable
   tools/durtools/is_binary_rational
   tools/durtools/is_pair
   tools/durtools/is_token
   tools/durtools/is_tuplet_multiplier
   tools/durtools/naive_prolated_to_written
   tools/durtools/pair_multiply_constant_numerator
   tools/durtools/pair_multiply_naive
   tools/durtools/pair_multiply_reduce_factors
   tools/durtools/prolated_to_written
   tools/durtools/rationalize
   tools/durtools/seconds_to_clock_string
   tools/durtools/sum_preprolated
   tools/durtools/sum_prolated
   tools/durtools/sum_seconds
   tools/durtools/to_fraction
   tools/durtools/token_decompose
   tools/durtools/token_unpack
   tools/durtools/within_prolated
   tools/durtools/within_seconds


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
   tools/io/show
   tools/io/write_and_show
   tools/io/write_ly
   tools/io/write_pdf


iterate

.. toctree::
   :maxdepth: 1

   tools/iterate/backwards
   tools/iterate/chained_contents
   tools/iterate/get_nth
   tools/iterate/grace
   tools/iterate/measure_next
   tools/iterate/measure_prev
   tools/iterate/naive
   tools/iterate/namesakes_from
   tools/iterate/thread
   tools/iterate/thread_from
   tools/iterate/tie_chains


label

.. toctree::
   :maxdepth: 1

   tools/label/clear_leaves
   tools/label/leaf_depth
   tools/label/leaf_durations
   tools/label/leaf_layer
   tools/label/leaf_pcs


layout

.. toctree::
   :maxdepth: 1

   tools/layout/apply_fixed_staff_positioning
   tools/layout/insert_measure_padding
   tools/layout/line_break_every_prolated
   tools/layout/line_break_every_seconds


leaftools

.. toctree::
   :maxdepth: 1

   tools/leaftools/duration_change
   tools/leaftools/duration_rewrite
   tools/leaftools/duration_scale
   tools/leaftools/excise
   tools/leaftools/leaves_to_skips
   tools/leaftools/meiose
   tools/leaftools/multiply


listtools

.. toctree::
   :maxdepth: 1

   tools/listtools/cumulative_products
   tools/listtools/cumulative_sums
   tools/listtools/cumulative_sums_zero
   tools/listtools/cumulative_weights_signed
   tools/listtools/difference_series
   tools/listtools/flatten
   tools/listtools/get_cyclic
   tools/listtools/get_unordered_pairs
   tools/listtools/group_by_sign
   tools/listtools/group_by_weights
   tools/listtools/increase_at_indices
   tools/listtools/increase_cyclic
   tools/listtools/insert_slice_cyclic
   tools/listtools/interlace
   tools/listtools/join_sublists_by_sign
   tools/listtools/lengths_to_counts
   tools/listtools/negate_elements_at_indices
   tools/listtools/negate_elements_at_indices_absolutely
   tools/listtools/outer_product
   tools/listtools/overwrite_slices_at
   tools/listtools/pairwise
   tools/listtools/pairwise_cumulative_sums_zero
   tools/listtools/partition_by_lengths
   tools/listtools/partition_by_weights
   tools/listtools/partition_elements_into_canonic_parts
   tools/listtools/permutations
   tools/listtools/phasor
   tools/listtools/remove_weighted_subrun_at
   tools/listtools/repeat_elements_to_count
   tools/listtools/repeat_list_to_length
   tools/listtools/repeat_list_to_weight
   tools/listtools/repeat_subruns_to_count
   tools/listtools/replace_elements_cyclic
   tools/listtools/rotate
   tools/listtools/sign
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
   tools/mathtools/greatest_multiple_less_equal
   tools/mathtools/greatest_power_of_two_less_equal
   tools/mathtools/is_power_of_two
   tools/mathtools/least_common_multiple
   tools/mathtools/least_multiple_greater_equal
   tools/mathtools/least_power_of_two_greater_equal
   tools/mathtools/partition_integer_by_ratio
   tools/mathtools/partition_integer_into_canonic_parts
   tools/mathtools/partition_integer_into_halves
   tools/mathtools/partition_integer_into_thirds
   tools/mathtools/partition_integer_into_units
   tools/mathtools/remove_powers_of_two
   tools/mathtools/sign


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
   tools/measuretools/overdraw
   tools/measuretools/populate
   tools/measuretools/project
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
   tools/metertools/is_token
   tools/metertools/make_best
   tools/metertools/make_binary


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


pickle

.. toctree::
   :maxdepth: 1

   tools/pickle/dump
   tools/pickle/load


pitchtools

.. toctree::
   :maxdepth: 1

   tools/pitchtools/add_staff_spaces
   tools/pitchtools/apply_octavation
   tools/pitchtools/are_in_octave_order
   tools/pitchtools/change_default_accidental_spelling
   tools/pitchtools/chromaticize
   tools/pitchtools/color_by_pc
   tools/pitchtools/diatonic_interval_to_absolute_interval
   tools/pitchtools/diatonic_interval_to_staff_spaces
   tools/pitchtools/diatonic_scale_degree_to_letter
   tools/pitchtools/diatonic_to_chromatic
   tools/pitchtools/diatonic_transpose
   tools/pitchtools/diatonicize
   tools/pitchtools/get_interval_class_vector
   tools/pitchtools/get_interval_vector
   tools/pitchtools/get_pitch
   tools/pitchtools/get_pitches
   tools/pitchtools/get_signed_interval_series
   tools/pitchtools/insert_transposed_pc_subruns
   tools/pitchtools/is_carrier
   tools/pitchtools/is_name
   tools/pitchtools/is_pair
   tools/pitchtools/is_token
   tools/pitchtools/is_token_collection
   tools/pitchtools/letter_pitch_number_to_nearest_accidental_string
   tools/pitchtools/letter_pitch_number_to_octave
   tools/pitchtools/letter_to_diatonic_scale_degree
   tools/pitchtools/letter_to_pc
   tools/pitchtools/make_flat
   tools/pitchtools/make_sharp
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
   tools/pitchtools/pitch_number_adjustment_to_octave
   tools/pitchtools/pitch_number_to_octave
   tools/pitchtools/registrate
   tools/pitchtools/send_pitch_number_to_octave
   tools/pitchtools/staff_space_transpose
   tools/pitchtools/suggest_clef


scoretools

.. toctree::
   :maxdepth: 1

   tools/scoretools/bequeath
   tools/scoretools/donate
   tools/scoretools/find
   tools/scoretools/make_piano_staff


spacing

.. toctree::
   :maxdepth: 1

   tools/spacing/get_global


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
   tools/spannertools/give_attached_to_children
   tools/spannertools/withdraw_from_covered


split

.. toctree::
   :maxdepth: 1

   tools/split/fractured_at_duration
   tools/split/fractured_at_index
   tools/split/unfractured_at_duration
   tools/split/unfractured_at_index


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

   tools/tuplettools/beam_bottommost
   tools/tuplettools/contents_fix
   tools/tuplettools/contents_scale
   tools/tuplettools/slip_trivial
   tools/tuplettools/subsume
