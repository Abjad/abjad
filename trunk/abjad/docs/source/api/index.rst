#########
Abjad API
#########

*************************
Core composition packages
*************************

.. toctree::
   :maxdepth: 1


:py:mod:`chordtools <abjad.tools.chordtools>`
=============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/chordtools/Chord/Chord

   --------

   .. toctree::
      :maxdepth: 1

      tools/chordtools/make_tied_chord

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/chordtools/Chord/Chord

   Functions
   ---------

   .. toctree::

      tools/chordtools/make_tied_chord

:py:mod:`componenttools <abjad.tools.componenttools>`
=====================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/componenttools/Component/Component

   --------

   .. toctree::
      :maxdepth: 1

      tools/componenttools/ContainmentSignature/ContainmentSignature
      tools/componenttools/Descendants/Descendants
      tools/componenttools/Lineage/Lineage
      tools/componenttools/Parentage/Parentage
      tools/componenttools/VerticalMoment/VerticalMoment

   --------

   .. toctree::
      :maxdepth: 1

      tools/componenttools/all_are_components
      tools/componenttools/all_are_components_in_same_thread
      tools/componenttools/all_are_components_scalable_by_multiplier
      tools/componenttools/all_are_contiguous_components
      tools/componenttools/all_are_contiguous_components_in_same_parent
      tools/componenttools/all_are_contiguous_components_in_same_thread
      tools/componenttools/all_are_thread_contiguous_components
      tools/componenttools/copy_and_partition_governed_component_subtree_by_leaf_counts
      tools/componenttools/copy_components_and_covered_spanners
      tools/componenttools/copy_components_and_detach_spanners
      tools/componenttools/copy_components_and_fracture_crossing_spanners
      tools/componenttools/copy_components_and_immediate_parent_of_first_component
      tools/componenttools/copy_governed_component_subtree_by_leaf_range
      tools/componenttools/copy_governed_component_subtree_from_offset_to
      tools/componenttools/extend_in_parent_of_component
      tools/componenttools/get_first_component_with_name_in_improper_parentage_of_component
      tools/componenttools/get_first_component_with_name_in_proper_parentage_of_component
      tools/componenttools/get_improper_descendants_of_component_that_cross_offset
      tools/componenttools/get_improper_descendants_of_component_that_start_with_component
      tools/componenttools/get_improper_descendants_of_component_that_stop_with_component
      tools/componenttools/get_improper_parentage_of_component_that_start_with_component
      tools/componenttools/get_improper_parentage_of_component_that_stop_with_component
      tools/componenttools/get_leftmost_components_with_total_duration_at_most
      tools/componenttools/get_lineage_of_component_that_start_with_component
      tools/componenttools/get_lineage_of_component_that_stop_with_component
      tools/componenttools/get_most_distant_sequential_container_in_improper_parentage_of_component
      tools/componenttools/get_nth_component_in_expr
      tools/componenttools/get_nth_component_in_time_order_from_component
      tools/componenttools/get_nth_namesake_from_component
      tools/componenttools/get_nth_sibling_from_component
      tools/componenttools/get_parent_and_start_stop_indices_of_components
      tools/componenttools/is_immediate_temporal_successor_of_component
      tools/componenttools/move_component_subtree_to_right_in_immediate_parent_of_component
      tools/componenttools/move_parentage_and_spanners_from_components_to_components
      tools/componenttools/partition_components_by_durations
      tools/componenttools/partition_components_by_durations_exactly
      tools/componenttools/partition_components_by_durations_not_greater_than
      tools/componenttools/partition_components_by_durations_not_less_than
      tools/componenttools/remove_component_subtree_from_score_and_spanners
      tools/componenttools/replace_components_with_children_of_components
      tools/componenttools/shorten_component_by_duration
      tools/componenttools/split_component_at_offset
      tools/componenttools/split_components_at_offsets
      tools/componenttools/yield_components_grouped_by_duration
      tools/componenttools/yield_components_grouped_by_preprolated_duration
      tools/componenttools/yield_groups_of_mixed_classes_in_sequence
      tools/componenttools/yield_topmost_components_grouped_by_type
      tools/componenttools/yield_topmost_components_of_class_grouped_by_type

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/componenttools/Component/Component

   Concrete Classes
   ----------------

   .. toctree::

      tools/componenttools/ContainmentSignature/ContainmentSignature
      tools/componenttools/Descendants/Descendants
      tools/componenttools/Lineage/Lineage
      tools/componenttools/Parentage/Parentage
      tools/componenttools/VerticalMoment/VerticalMoment

   Functions
   ---------

   .. toctree::

      tools/componenttools/all_are_components
      tools/componenttools/all_are_components_in_same_thread
      tools/componenttools/all_are_components_scalable_by_multiplier
      tools/componenttools/all_are_contiguous_components
      tools/componenttools/all_are_contiguous_components_in_same_parent
      tools/componenttools/all_are_contiguous_components_in_same_thread
      tools/componenttools/all_are_thread_contiguous_components
      tools/componenttools/copy_and_partition_governed_component_subtree_by_leaf_counts
      tools/componenttools/copy_components_and_covered_spanners
      tools/componenttools/copy_components_and_detach_spanners
      tools/componenttools/copy_components_and_fracture_crossing_spanners
      tools/componenttools/copy_components_and_immediate_parent_of_first_component
      tools/componenttools/copy_governed_component_subtree_by_leaf_range
      tools/componenttools/copy_governed_component_subtree_from_offset_to
      tools/componenttools/extend_in_parent_of_component
      tools/componenttools/get_first_component_with_name_in_improper_parentage_of_component
      tools/componenttools/get_first_component_with_name_in_proper_parentage_of_component
      tools/componenttools/get_improper_descendants_of_component_that_cross_offset
      tools/componenttools/get_improper_descendants_of_component_that_start_with_component
      tools/componenttools/get_improper_descendants_of_component_that_stop_with_component
      tools/componenttools/get_improper_parentage_of_component_that_start_with_component
      tools/componenttools/get_improper_parentage_of_component_that_stop_with_component
      tools/componenttools/get_leftmost_components_with_total_duration_at_most
      tools/componenttools/get_lineage_of_component_that_start_with_component
      tools/componenttools/get_lineage_of_component_that_stop_with_component
      tools/componenttools/get_most_distant_sequential_container_in_improper_parentage_of_component
      tools/componenttools/get_nth_component_in_expr
      tools/componenttools/get_nth_component_in_time_order_from_component
      tools/componenttools/get_nth_namesake_from_component
      tools/componenttools/get_nth_sibling_from_component
      tools/componenttools/get_parent_and_start_stop_indices_of_components
      tools/componenttools/is_immediate_temporal_successor_of_component
      tools/componenttools/move_component_subtree_to_right_in_immediate_parent_of_component
      tools/componenttools/move_parentage_and_spanners_from_components_to_components
      tools/componenttools/partition_components_by_durations
      tools/componenttools/partition_components_by_durations_exactly
      tools/componenttools/partition_components_by_durations_not_greater_than
      tools/componenttools/partition_components_by_durations_not_less_than
      tools/componenttools/remove_component_subtree_from_score_and_spanners
      tools/componenttools/replace_components_with_children_of_components
      tools/componenttools/shorten_component_by_duration
      tools/componenttools/split_component_at_offset
      tools/componenttools/split_components_at_offsets
      tools/componenttools/yield_components_grouped_by_duration
      tools/componenttools/yield_components_grouped_by_preprolated_duration
      tools/componenttools/yield_groups_of_mixed_classes_in_sequence
      tools/componenttools/yield_topmost_components_grouped_by_type
      tools/componenttools/yield_topmost_components_of_class_grouped_by_type

:py:mod:`containertools <abjad.tools.containertools>`
=====================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/containertools/Cluster/Cluster
      tools/containertools/Container/Container
      tools/containertools/FixedDurationContainer/FixedDurationContainer

   --------

   .. toctree::
      :maxdepth: 1

      tools/containertools/delete_contents_of_container
      tools/containertools/delete_contents_of_container_starting_at_or_after_offset
      tools/containertools/delete_contents_of_container_starting_before_or_at_offset
      tools/containertools/delete_contents_of_container_starting_strictly_after_offset
      tools/containertools/delete_contents_of_container_starting_strictly_before_offset
      tools/containertools/eject_contents_of_container
      tools/containertools/fuse_like_named_contiguous_containers_in_expr
      tools/containertools/get_element_starting_at_exactly_offset
      tools/containertools/get_first_element_starting_at_or_after_offset
      tools/containertools/get_first_element_starting_before_or_at_offset
      tools/containertools/get_first_element_starting_strictly_after_offset
      tools/containertools/get_first_element_starting_strictly_before_offset
      tools/containertools/insert_component
      tools/containertools/move_parentage_children_and_spanners_from_components_to_empty_container
      tools/containertools/remove_leafless_containers_in_expr
      tools/containertools/repeat_contents_of_container
      tools/containertools/repeat_last_n_elements_of_container
      tools/containertools/replace_container_slice_with_rests
      tools/containertools/replace_contents_of_target_container_with_contents_of_source_container
      tools/containertools/report_container_modifications
      tools/containertools/reverse_contents_of_container
      tools/containertools/scale_contents_of_container
      tools/containertools/set_container_multiplier
      tools/containertools/split_container_at_index
      tools/containertools/split_container_by_counts

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/containertools/Cluster/Cluster
      tools/containertools/Container/Container
      tools/containertools/FixedDurationContainer/FixedDurationContainer

   Functions
   ---------

   .. toctree::

      tools/containertools/delete_contents_of_container
      tools/containertools/delete_contents_of_container_starting_at_or_after_offset
      tools/containertools/delete_contents_of_container_starting_before_or_at_offset
      tools/containertools/delete_contents_of_container_starting_strictly_after_offset
      tools/containertools/delete_contents_of_container_starting_strictly_before_offset
      tools/containertools/eject_contents_of_container
      tools/containertools/fuse_like_named_contiguous_containers_in_expr
      tools/containertools/get_element_starting_at_exactly_offset
      tools/containertools/get_first_element_starting_at_or_after_offset
      tools/containertools/get_first_element_starting_before_or_at_offset
      tools/containertools/get_first_element_starting_strictly_after_offset
      tools/containertools/get_first_element_starting_strictly_before_offset
      tools/containertools/insert_component
      tools/containertools/move_parentage_children_and_spanners_from_components_to_empty_container
      tools/containertools/remove_leafless_containers_in_expr
      tools/containertools/repeat_contents_of_container
      tools/containertools/repeat_last_n_elements_of_container
      tools/containertools/replace_container_slice_with_rests
      tools/containertools/replace_contents_of_target_container_with_contents_of_source_container
      tools/containertools/report_container_modifications
      tools/containertools/reverse_contents_of_container
      tools/containertools/scale_contents_of_container
      tools/containertools/set_container_multiplier
      tools/containertools/split_container_at_index
      tools/containertools/split_container_by_counts

:py:mod:`contexttools <abjad.tools.contexttools>`
=================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/contexttools/ClefMark/ClefMark
      tools/contexttools/ClefMarkInventory/ClefMarkInventory
      tools/contexttools/Context/Context
      tools/contexttools/ContextMark/ContextMark
      tools/contexttools/DynamicMark/DynamicMark
      tools/contexttools/InstrumentMark/InstrumentMark
      tools/contexttools/KeySignatureMark/KeySignatureMark
      tools/contexttools/StaffChangeMark/StaffChangeMark
      tools/contexttools/TempoMark/TempoMark
      tools/contexttools/TempoMarkInventory/TempoMarkInventory
      tools/contexttools/TimeSignatureMark/TimeSignatureMark

   --------

   .. toctree::
      :maxdepth: 1

      tools/contexttools/detach_clef_marks_attached_to_component
      tools/contexttools/detach_context_marks_attached_to_component
      tools/contexttools/detach_dynamic_marks_attached_to_component
      tools/contexttools/detach_instrument_marks_attached_to_component
      tools/contexttools/detach_key_signature_marks_attached_to_component
      tools/contexttools/detach_staff_change_marks_attached_to_component
      tools/contexttools/detach_tempo_marks_attached_to_component
      tools/contexttools/detach_time_signature_marks_attached_to_component
      tools/contexttools/get_clef_mark_attached_to_component
      tools/contexttools/get_clef_marks_attached_to_component
      tools/contexttools/get_context_mark_attached_to_component
      tools/contexttools/get_context_marks_attached_to_any_improper_parent_of_component
      tools/contexttools/get_context_marks_attached_to_component
      tools/contexttools/get_dynamic_mark_attached_to_component
      tools/contexttools/get_dynamic_marks_attached_to_component
      tools/contexttools/get_effective_clef
      tools/contexttools/get_effective_context_mark
      tools/contexttools/get_effective_dynamic
      tools/contexttools/get_effective_instrument
      tools/contexttools/get_effective_key_signature
      tools/contexttools/get_effective_staff
      tools/contexttools/get_effective_tempo
      tools/contexttools/get_effective_time_signature
      tools/contexttools/get_instrument_mark_attached_to_component
      tools/contexttools/get_instrument_marks_attached_to_component
      tools/contexttools/get_key_signature_mark_attached_to_component
      tools/contexttools/get_key_signature_marks_attached_to_component
      tools/contexttools/get_staff_change_mark_attached_to_component
      tools/contexttools/get_staff_change_marks_attached_to_component
      tools/contexttools/get_tempo_mark_attached_to_component
      tools/contexttools/get_tempo_marks_attached_to_component
      tools/contexttools/get_time_signature_mark_attached_to_component
      tools/contexttools/get_time_signature_marks_attached_to_component
      tools/contexttools/is_component_with_clef_mark_attached
      tools/contexttools/is_component_with_context_mark_attached
      tools/contexttools/is_component_with_dynamic_mark_attached
      tools/contexttools/is_component_with_instrument_mark_attached
      tools/contexttools/is_component_with_key_signature_mark_attached
      tools/contexttools/is_component_with_staff_change_mark_attached
      tools/contexttools/is_component_with_tempo_mark_attached
      tools/contexttools/is_component_with_time_signature_mark_attached
      tools/contexttools/list_clef_names
      tools/contexttools/set_accidental_style_on_sequential_contexts_in_expr

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/contexttools/ClefMark/ClefMark
      tools/contexttools/ClefMarkInventory/ClefMarkInventory
      tools/contexttools/Context/Context
      tools/contexttools/ContextMark/ContextMark
      tools/contexttools/DynamicMark/DynamicMark
      tools/contexttools/InstrumentMark/InstrumentMark
      tools/contexttools/KeySignatureMark/KeySignatureMark
      tools/contexttools/StaffChangeMark/StaffChangeMark
      tools/contexttools/TempoMark/TempoMark
      tools/contexttools/TempoMarkInventory/TempoMarkInventory
      tools/contexttools/TimeSignatureMark/TimeSignatureMark

   Functions
   ---------

   .. toctree::

      tools/contexttools/detach_clef_marks_attached_to_component
      tools/contexttools/detach_context_marks_attached_to_component
      tools/contexttools/detach_dynamic_marks_attached_to_component
      tools/contexttools/detach_instrument_marks_attached_to_component
      tools/contexttools/detach_key_signature_marks_attached_to_component
      tools/contexttools/detach_staff_change_marks_attached_to_component
      tools/contexttools/detach_tempo_marks_attached_to_component
      tools/contexttools/detach_time_signature_marks_attached_to_component
      tools/contexttools/get_clef_mark_attached_to_component
      tools/contexttools/get_clef_marks_attached_to_component
      tools/contexttools/get_context_mark_attached_to_component
      tools/contexttools/get_context_marks_attached_to_any_improper_parent_of_component
      tools/contexttools/get_context_marks_attached_to_component
      tools/contexttools/get_dynamic_mark_attached_to_component
      tools/contexttools/get_dynamic_marks_attached_to_component
      tools/contexttools/get_effective_clef
      tools/contexttools/get_effective_context_mark
      tools/contexttools/get_effective_dynamic
      tools/contexttools/get_effective_instrument
      tools/contexttools/get_effective_key_signature
      tools/contexttools/get_effective_staff
      tools/contexttools/get_effective_tempo
      tools/contexttools/get_effective_time_signature
      tools/contexttools/get_instrument_mark_attached_to_component
      tools/contexttools/get_instrument_marks_attached_to_component
      tools/contexttools/get_key_signature_mark_attached_to_component
      tools/contexttools/get_key_signature_marks_attached_to_component
      tools/contexttools/get_staff_change_mark_attached_to_component
      tools/contexttools/get_staff_change_marks_attached_to_component
      tools/contexttools/get_tempo_mark_attached_to_component
      tools/contexttools/get_tempo_marks_attached_to_component
      tools/contexttools/get_time_signature_mark_attached_to_component
      tools/contexttools/get_time_signature_marks_attached_to_component
      tools/contexttools/is_component_with_clef_mark_attached
      tools/contexttools/is_component_with_context_mark_attached
      tools/contexttools/is_component_with_dynamic_mark_attached
      tools/contexttools/is_component_with_instrument_mark_attached
      tools/contexttools/is_component_with_key_signature_mark_attached
      tools/contexttools/is_component_with_staff_change_mark_attached
      tools/contexttools/is_component_with_tempo_mark_attached
      tools/contexttools/is_component_with_time_signature_mark_attached
      tools/contexttools/list_clef_names
      tools/contexttools/set_accidental_style_on_sequential_contexts_in_expr

:py:mod:`durationtools <abjad.tools.durationtools>`
===================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/durationtools/Duration/Duration
      tools/durationtools/Multiplier/Multiplier
      tools/durationtools/Offset/Offset

   --------

   .. toctree::
      :maxdepth: 1

      tools/durationtools/count_offsets_in_expr
      tools/durationtools/durations_to_integers
      tools/durationtools/durations_to_nonreduced_fractions_with_common_denominator
      tools/durationtools/group_nonreduced_fractions_by_implied_prolation
      tools/durationtools/numeric_seconds_to_clock_string
      tools/durationtools/yield_durations

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/durationtools/Duration/Duration
      tools/durationtools/Multiplier/Multiplier
      tools/durationtools/Offset/Offset

   Functions
   ---------

   .. toctree::

      tools/durationtools/count_offsets_in_expr
      tools/durationtools/durations_to_integers
      tools/durationtools/durations_to_nonreduced_fractions_with_common_denominator
      tools/durationtools/group_nonreduced_fractions_by_implied_prolation
      tools/durationtools/numeric_seconds_to_clock_string
      tools/durationtools/yield_durations

:py:mod:`gracetools <abjad.tools.gracetools>`
=============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/gracetools/GraceContainer/GraceContainer

   --------

   .. toctree::
      :maxdepth: 1

      tools/gracetools/detach_grace_containers_attached_to_leaf
      tools/gracetools/detach_grace_containers_attached_to_leaves_in_expr
      tools/gracetools/get_grace_containers_attached_to_leaf

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/gracetools/GraceContainer/GraceContainer

   Functions
   ---------

   .. toctree::

      tools/gracetools/detach_grace_containers_attached_to_leaf
      tools/gracetools/detach_grace_containers_attached_to_leaves_in_expr
      tools/gracetools/get_grace_containers_attached_to_leaf

:py:mod:`instrumenttools <abjad.tools.instrumenttools>`
=======================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/instrumenttools/BrassInstrument/BrassInstrument
      tools/instrumenttools/Clarinet/Clarinet
      tools/instrumenttools/DoubleReedInstrument/DoubleReedInstrument
      tools/instrumenttools/Instrument/Instrument
      tools/instrumenttools/KeyboardInstrument/KeyboardInstrument
      tools/instrumenttools/PercussionInstrument/PercussionInstrument
      tools/instrumenttools/ReedInstrument/ReedInstrument
      tools/instrumenttools/Saxophone/Saxophone
      tools/instrumenttools/SingleReedInstrument/SingleReedInstrument
      tools/instrumenttools/StringInstrument/StringInstrument
      tools/instrumenttools/Trombone/Trombone
      tools/instrumenttools/Voice/Voice
      tools/instrumenttools/WindInstrument/WindInstrument

   --------

   .. toctree::
      :maxdepth: 1

      tools/instrumenttools/Accordion/Accordion
      tools/instrumenttools/AltoFlute/AltoFlute
      tools/instrumenttools/AltoSaxophone/AltoSaxophone
      tools/instrumenttools/AltoTrombone/AltoTrombone
      tools/instrumenttools/BFlatClarinet/BFlatClarinet
      tools/instrumenttools/BaritoneSaxophone/BaritoneSaxophone
      tools/instrumenttools/BaritoneVoice/BaritoneVoice
      tools/instrumenttools/BassClarinet/BassClarinet
      tools/instrumenttools/BassFlute/BassFlute
      tools/instrumenttools/BassSaxophone/BassSaxophone
      tools/instrumenttools/BassTrombone/BassTrombone
      tools/instrumenttools/BassVoice/BassVoice
      tools/instrumenttools/Bassoon/Bassoon
      tools/instrumenttools/Cello/Cello
      tools/instrumenttools/ClarinetInA/ClarinetInA
      tools/instrumenttools/Contrabass/Contrabass
      tools/instrumenttools/ContrabassClarinet/ContrabassClarinet
      tools/instrumenttools/ContrabassFlute/ContrabassFlute
      tools/instrumenttools/ContrabassSaxophone/ContrabassSaxophone
      tools/instrumenttools/Contrabassoon/Contrabassoon
      tools/instrumenttools/ContraltoVoice/ContraltoVoice
      tools/instrumenttools/EFlatClarinet/EFlatClarinet
      tools/instrumenttools/EnglishHorn/EnglishHorn
      tools/instrumenttools/Flute/Flute
      tools/instrumenttools/FrenchHorn/FrenchHorn
      tools/instrumenttools/Glockenspiel/Glockenspiel
      tools/instrumenttools/Guitar/Guitar
      tools/instrumenttools/Harp/Harp
      tools/instrumenttools/Harpsichord/Harpsichord
      tools/instrumenttools/InstrumentInventory/InstrumentInventory
      tools/instrumenttools/Marimba/Marimba
      tools/instrumenttools/MezzoSopranoVoice/MezzoSopranoVoice
      tools/instrumenttools/Oboe/Oboe
      tools/instrumenttools/Piano/Piano
      tools/instrumenttools/Piccolo/Piccolo
      tools/instrumenttools/SopraninoSaxophone/SopraninoSaxophone
      tools/instrumenttools/SopranoSaxophone/SopranoSaxophone
      tools/instrumenttools/SopranoVoice/SopranoVoice
      tools/instrumenttools/TenorSaxophone/TenorSaxophone
      tools/instrumenttools/TenorTrombone/TenorTrombone
      tools/instrumenttools/TenorVoice/TenorVoice
      tools/instrumenttools/Trumpet/Trumpet
      tools/instrumenttools/Tuba/Tuba
      tools/instrumenttools/UntunedPercussion/UntunedPercussion
      tools/instrumenttools/Vibraphone/Vibraphone
      tools/instrumenttools/Viola/Viola
      tools/instrumenttools/Violin/Violin
      tools/instrumenttools/WoodwindFingering/WoodwindFingering
      tools/instrumenttools/Xylophone/Xylophone

   --------

   .. toctree::
      :maxdepth: 1

      tools/instrumenttools/default_instrument_name_to_instrument_class
      tools/instrumenttools/iterate_notes_and_chords_in_expr_outside_traditional_instrument_ranges
      tools/instrumenttools/list_instrument_names
      tools/instrumenttools/list_instruments
      tools/instrumenttools/list_primary_instruments
      tools/instrumenttools/list_secondary_instruments
      tools/instrumenttools/notes_and_chords_in_expr_are_on_expected_clefs
      tools/instrumenttools/notes_and_chords_in_expr_are_within_traditional_instrument_ranges
      tools/instrumenttools/transpose_from_fingered_pitch_to_sounding_pitch
      tools/instrumenttools/transpose_from_sounding_pitch_to_fingered_pitch

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/instrumenttools/BrassInstrument/BrassInstrument
      tools/instrumenttools/Clarinet/Clarinet
      tools/instrumenttools/DoubleReedInstrument/DoubleReedInstrument
      tools/instrumenttools/Instrument/Instrument
      tools/instrumenttools/KeyboardInstrument/KeyboardInstrument
      tools/instrumenttools/PercussionInstrument/PercussionInstrument
      tools/instrumenttools/ReedInstrument/ReedInstrument
      tools/instrumenttools/Saxophone/Saxophone
      tools/instrumenttools/SingleReedInstrument/SingleReedInstrument
      tools/instrumenttools/StringInstrument/StringInstrument
      tools/instrumenttools/Trombone/Trombone
      tools/instrumenttools/Voice/Voice
      tools/instrumenttools/WindInstrument/WindInstrument

   Concrete Classes
   ----------------

   .. toctree::

      tools/instrumenttools/Accordion/Accordion
      tools/instrumenttools/AltoFlute/AltoFlute
      tools/instrumenttools/AltoSaxophone/AltoSaxophone
      tools/instrumenttools/AltoTrombone/AltoTrombone
      tools/instrumenttools/BFlatClarinet/BFlatClarinet
      tools/instrumenttools/BaritoneSaxophone/BaritoneSaxophone
      tools/instrumenttools/BaritoneVoice/BaritoneVoice
      tools/instrumenttools/BassClarinet/BassClarinet
      tools/instrumenttools/BassFlute/BassFlute
      tools/instrumenttools/BassSaxophone/BassSaxophone
      tools/instrumenttools/BassTrombone/BassTrombone
      tools/instrumenttools/BassVoice/BassVoice
      tools/instrumenttools/Bassoon/Bassoon
      tools/instrumenttools/Cello/Cello
      tools/instrumenttools/ClarinetInA/ClarinetInA
      tools/instrumenttools/Contrabass/Contrabass
      tools/instrumenttools/ContrabassClarinet/ContrabassClarinet
      tools/instrumenttools/ContrabassFlute/ContrabassFlute
      tools/instrumenttools/ContrabassSaxophone/ContrabassSaxophone
      tools/instrumenttools/Contrabassoon/Contrabassoon
      tools/instrumenttools/ContraltoVoice/ContraltoVoice
      tools/instrumenttools/EFlatClarinet/EFlatClarinet
      tools/instrumenttools/EnglishHorn/EnglishHorn
      tools/instrumenttools/Flute/Flute
      tools/instrumenttools/FrenchHorn/FrenchHorn
      tools/instrumenttools/Glockenspiel/Glockenspiel
      tools/instrumenttools/Guitar/Guitar
      tools/instrumenttools/Harp/Harp
      tools/instrumenttools/Harpsichord/Harpsichord
      tools/instrumenttools/InstrumentInventory/InstrumentInventory
      tools/instrumenttools/Marimba/Marimba
      tools/instrumenttools/MezzoSopranoVoice/MezzoSopranoVoice
      tools/instrumenttools/Oboe/Oboe
      tools/instrumenttools/Piano/Piano
      tools/instrumenttools/Piccolo/Piccolo
      tools/instrumenttools/SopraninoSaxophone/SopraninoSaxophone
      tools/instrumenttools/SopranoSaxophone/SopranoSaxophone
      tools/instrumenttools/SopranoVoice/SopranoVoice
      tools/instrumenttools/TenorSaxophone/TenorSaxophone
      tools/instrumenttools/TenorTrombone/TenorTrombone
      tools/instrumenttools/TenorVoice/TenorVoice
      tools/instrumenttools/Trumpet/Trumpet
      tools/instrumenttools/Tuba/Tuba
      tools/instrumenttools/UntunedPercussion/UntunedPercussion
      tools/instrumenttools/Vibraphone/Vibraphone
      tools/instrumenttools/Viola/Viola
      tools/instrumenttools/Violin/Violin
      tools/instrumenttools/WoodwindFingering/WoodwindFingering
      tools/instrumenttools/Xylophone/Xylophone

   Functions
   ---------

   .. toctree::

      tools/instrumenttools/default_instrument_name_to_instrument_class
      tools/instrumenttools/iterate_notes_and_chords_in_expr_outside_traditional_instrument_ranges
      tools/instrumenttools/list_instrument_names
      tools/instrumenttools/list_instruments
      tools/instrumenttools/list_primary_instruments
      tools/instrumenttools/list_secondary_instruments
      tools/instrumenttools/notes_and_chords_in_expr_are_on_expected_clefs
      tools/instrumenttools/notes_and_chords_in_expr_are_within_traditional_instrument_ranges
      tools/instrumenttools/transpose_from_fingered_pitch_to_sounding_pitch
      tools/instrumenttools/transpose_from_sounding_pitch_to_fingered_pitch

:py:mod:`iotools <abjad.tools.iotools>`
=======================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/iotools/RedirectedStreams/RedirectedStreams

   --------

   .. toctree::
      :maxdepth: 1

      tools/iotools/clear_terminal
      tools/iotools/count_function_calls
      tools/iotools/f
      tools/iotools/get_last_output_file_name
      tools/iotools/get_next_output_file_name
      tools/iotools/graph
      tools/iotools/log
      tools/iotools/ly
      tools/iotools/p
      tools/iotools/pdf
      tools/iotools/play
      tools/iotools/plot
      tools/iotools/profile_expr
      tools/iotools/redo
      tools/iotools/save_last_ly_as
      tools/iotools/save_last_pdf_as
      tools/iotools/show
      tools/iotools/spawn_subprocess
      tools/iotools/which
      tools/iotools/write_expr_to_ly
      tools/iotools/write_expr_to_pdf
      tools/iotools/z

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/iotools/RedirectedStreams/RedirectedStreams

   Functions
   ---------

   .. toctree::

      tools/iotools/clear_terminal
      tools/iotools/count_function_calls
      tools/iotools/f
      tools/iotools/get_last_output_file_name
      tools/iotools/get_next_output_file_name
      tools/iotools/graph
      tools/iotools/log
      tools/iotools/ly
      tools/iotools/p
      tools/iotools/pdf
      tools/iotools/play
      tools/iotools/plot
      tools/iotools/profile_expr
      tools/iotools/redo
      tools/iotools/save_last_ly_as
      tools/iotools/save_last_pdf_as
      tools/iotools/show
      tools/iotools/spawn_subprocess
      tools/iotools/which
      tools/iotools/write_expr_to_ly
      tools/iotools/write_expr_to_pdf
      tools/iotools/z

:py:mod:`iterationtools <abjad.tools.iterationtools>`
=====================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/iterationtools/iterate_chords_in_expr
      tools/iterationtools/iterate_components_and_grace_containers_in_expr
      tools/iterationtools/iterate_components_depth_first
      tools/iterationtools/iterate_components_in_expr
      tools/iterationtools/iterate_containers_in_expr
      tools/iterationtools/iterate_contexts_in_expr
      tools/iterationtools/iterate_leaf_pairs_in_expr
      tools/iterationtools/iterate_leaves_in_expr
      tools/iterationtools/iterate_measures_in_expr
      tools/iterationtools/iterate_namesakes_from_component
      tools/iterationtools/iterate_nontrivial_tie_chains_in_expr
      tools/iterationtools/iterate_notes_and_chords_in_expr
      tools/iterationtools/iterate_notes_in_expr
      tools/iterationtools/iterate_pitched_tie_chains_in_expr
      tools/iterationtools/iterate_rests_in_expr
      tools/iterationtools/iterate_scores_in_expr
      tools/iterationtools/iterate_semantic_voices_in_expr
      tools/iterationtools/iterate_skips_in_expr
      tools/iterationtools/iterate_staves_in_expr
      tools/iterationtools/iterate_thread_from_component
      tools/iterationtools/iterate_thread_in_expr
      tools/iterationtools/iterate_tie_chains_in_expr
      tools/iterationtools/iterate_timeline_from_component
      tools/iterationtools/iterate_timeline_in_expr
      tools/iterationtools/iterate_topmost_tie_chains_and_components_in_expr
      tools/iterationtools/iterate_tuplets_in_expr
      tools/iterationtools/iterate_vertical_moments_in_expr
      tools/iterationtools/iterate_voices_in_expr

.. only:: latex

   Functions
   ---------

   .. toctree::

      tools/iterationtools/iterate_chords_in_expr
      tools/iterationtools/iterate_components_and_grace_containers_in_expr
      tools/iterationtools/iterate_components_depth_first
      tools/iterationtools/iterate_components_in_expr
      tools/iterationtools/iterate_containers_in_expr
      tools/iterationtools/iterate_contexts_in_expr
      tools/iterationtools/iterate_leaf_pairs_in_expr
      tools/iterationtools/iterate_leaves_in_expr
      tools/iterationtools/iterate_measures_in_expr
      tools/iterationtools/iterate_namesakes_from_component
      tools/iterationtools/iterate_nontrivial_tie_chains_in_expr
      tools/iterationtools/iterate_notes_and_chords_in_expr
      tools/iterationtools/iterate_notes_in_expr
      tools/iterationtools/iterate_pitched_tie_chains_in_expr
      tools/iterationtools/iterate_rests_in_expr
      tools/iterationtools/iterate_scores_in_expr
      tools/iterationtools/iterate_semantic_voices_in_expr
      tools/iterationtools/iterate_skips_in_expr
      tools/iterationtools/iterate_staves_in_expr
      tools/iterationtools/iterate_thread_from_component
      tools/iterationtools/iterate_thread_in_expr
      tools/iterationtools/iterate_tie_chains_in_expr
      tools/iterationtools/iterate_timeline_from_component
      tools/iterationtools/iterate_timeline_in_expr
      tools/iterationtools/iterate_topmost_tie_chains_and_components_in_expr
      tools/iterationtools/iterate_tuplets_in_expr
      tools/iterationtools/iterate_vertical_moments_in_expr
      tools/iterationtools/iterate_voices_in_expr

:py:mod:`labeltools <abjad.tools.labeltools>`
=============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/labeltools/color_chord_note_heads_in_expr_by_pitch_class_color_map
      tools/labeltools/color_contents_of_container
      tools/labeltools/color_leaf
      tools/labeltools/color_leaves_in_expr
      tools/labeltools/color_measure
      tools/labeltools/color_measures_with_non_power_of_two_denominators_in_expr
      tools/labeltools/color_note_head_by_numbered_chromatic_pitch_class_color_map
      tools/labeltools/label_leaves_in_expr_with_inversion_equivalent_chromatic_interval_classes
      tools/labeltools/label_leaves_in_expr_with_leaf_depth
      tools/labeltools/label_leaves_in_expr_with_leaf_duration
      tools/labeltools/label_leaves_in_expr_with_leaf_durations
      tools/labeltools/label_leaves_in_expr_with_leaf_indices
      tools/labeltools/label_leaves_in_expr_with_leaf_numbers
      tools/labeltools/label_leaves_in_expr_with_melodic_chromatic_interval_classes
      tools/labeltools/label_leaves_in_expr_with_melodic_chromatic_intervals
      tools/labeltools/label_leaves_in_expr_with_melodic_counterpoint_interval_classes
      tools/labeltools/label_leaves_in_expr_with_melodic_counterpoint_intervals
      tools/labeltools/label_leaves_in_expr_with_melodic_diatonic_interval_classes
      tools/labeltools/label_leaves_in_expr_with_melodic_diatonic_intervals
      tools/labeltools/label_leaves_in_expr_with_pitch_class_numbers
      tools/labeltools/label_leaves_in_expr_with_pitch_numbers
      tools/labeltools/label_leaves_in_expr_with_tuplet_depth
      tools/labeltools/label_leaves_in_expr_with_written_leaf_duration
      tools/labeltools/label_notes_in_expr_with_note_indices
      tools/labeltools/label_tie_chains_in_expr_with_tie_chain_duration
      tools/labeltools/label_tie_chains_in_expr_with_tie_chain_durations
      tools/labeltools/label_tie_chains_in_expr_with_written_tie_chain_duration
      tools/labeltools/label_vertical_moments_in_expr_with_chromatic_interval_classes
      tools/labeltools/label_vertical_moments_in_expr_with_chromatic_intervals
      tools/labeltools/label_vertical_moments_in_expr_with_counterpoint_intervals
      tools/labeltools/label_vertical_moments_in_expr_with_diatonic_intervals
      tools/labeltools/label_vertical_moments_in_expr_with_interval_class_vectors
      tools/labeltools/label_vertical_moments_in_expr_with_numbered_chromatic_pitch_classes
      tools/labeltools/label_vertical_moments_in_expr_with_pitch_numbers
      tools/labeltools/remove_markup_from_leaves_in_expr

.. only:: latex

   Functions
   ---------

   .. toctree::

      tools/labeltools/color_chord_note_heads_in_expr_by_pitch_class_color_map
      tools/labeltools/color_contents_of_container
      tools/labeltools/color_leaf
      tools/labeltools/color_leaves_in_expr
      tools/labeltools/color_measure
      tools/labeltools/color_measures_with_non_power_of_two_denominators_in_expr
      tools/labeltools/color_note_head_by_numbered_chromatic_pitch_class_color_map
      tools/labeltools/label_leaves_in_expr_with_inversion_equivalent_chromatic_interval_classes
      tools/labeltools/label_leaves_in_expr_with_leaf_depth
      tools/labeltools/label_leaves_in_expr_with_leaf_duration
      tools/labeltools/label_leaves_in_expr_with_leaf_durations
      tools/labeltools/label_leaves_in_expr_with_leaf_indices
      tools/labeltools/label_leaves_in_expr_with_leaf_numbers
      tools/labeltools/label_leaves_in_expr_with_melodic_chromatic_interval_classes
      tools/labeltools/label_leaves_in_expr_with_melodic_chromatic_intervals
      tools/labeltools/label_leaves_in_expr_with_melodic_counterpoint_interval_classes
      tools/labeltools/label_leaves_in_expr_with_melodic_counterpoint_intervals
      tools/labeltools/label_leaves_in_expr_with_melodic_diatonic_interval_classes
      tools/labeltools/label_leaves_in_expr_with_melodic_diatonic_intervals
      tools/labeltools/label_leaves_in_expr_with_pitch_class_numbers
      tools/labeltools/label_leaves_in_expr_with_pitch_numbers
      tools/labeltools/label_leaves_in_expr_with_tuplet_depth
      tools/labeltools/label_leaves_in_expr_with_written_leaf_duration
      tools/labeltools/label_notes_in_expr_with_note_indices
      tools/labeltools/label_tie_chains_in_expr_with_tie_chain_duration
      tools/labeltools/label_tie_chains_in_expr_with_tie_chain_durations
      tools/labeltools/label_tie_chains_in_expr_with_written_tie_chain_duration
      tools/labeltools/label_vertical_moments_in_expr_with_chromatic_interval_classes
      tools/labeltools/label_vertical_moments_in_expr_with_chromatic_intervals
      tools/labeltools/label_vertical_moments_in_expr_with_counterpoint_intervals
      tools/labeltools/label_vertical_moments_in_expr_with_diatonic_intervals
      tools/labeltools/label_vertical_moments_in_expr_with_interval_class_vectors
      tools/labeltools/label_vertical_moments_in_expr_with_numbered_chromatic_pitch_classes
      tools/labeltools/label_vertical_moments_in_expr_with_pitch_numbers
      tools/labeltools/remove_markup_from_leaves_in_expr

:py:mod:`layouttools <abjad.tools.layouttools>`
===============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/layouttools/SpacingIndication/SpacingIndication

   --------

   .. toctree::
      :maxdepth: 1

      tools/layouttools/make_spacing_vector
      tools/layouttools/set_line_breaks_by_line_duration
      tools/layouttools/set_line_breaks_cyclically_by_line_duration_ge
      tools/layouttools/set_line_breaks_cyclically_by_line_duration_in_seconds_ge

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/layouttools/SpacingIndication/SpacingIndication

   Functions
   ---------

   .. toctree::

      tools/layouttools/make_spacing_vector
      tools/layouttools/set_line_breaks_by_line_duration
      tools/layouttools/set_line_breaks_cyclically_by_line_duration_ge
      tools/layouttools/set_line_breaks_cyclically_by_line_duration_in_seconds_ge

:py:mod:`leaftools <abjad.tools.leaftools>`
===========================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/leaftools/Leaf/Leaf
      tools/leaftools/TieChain/TieChain

   --------

   .. toctree::
      :maxdepth: 1

      tools/leaftools/change_written_leaf_duration_and_preserve_preprolated_leaf_duration
      tools/leaftools/copy_written_duration_and_multiplier_from_leaf_to_leaf
      tools/leaftools/divide_leaf_meiotically
      tools/leaftools/divide_leaves_in_expr_meiotically
      tools/leaftools/expr_has_leaf_with_dotted_written_duration
      tools/leaftools/fuse_leaves
      tools/leaftools/fuse_leaves_in_container_once_by_counts
      tools/leaftools/fuse_leaves_in_tie_chain_by_immediate_parent
      tools/leaftools/get_composite_offset_difference_series_from_leaves_in_expr
      tools/leaftools/get_composite_offset_series_from_leaves_in_expr
      tools/leaftools/get_leaf_at_index_in_measure_number_in_expr
      tools/leaftools/get_leaf_in_expr_with_maximum_duration
      tools/leaftools/get_leaf_in_expr_with_minimum_duration
      tools/leaftools/get_nth_leaf_in_expr
      tools/leaftools/get_nth_leaf_in_thread_from_leaf
      tools/leaftools/is_bar_line_crossing_leaf
      tools/leaftools/list_durations_of_leaves_in_expr
      tools/leaftools/list_written_durations_of_leaves_in_expr
      tools/leaftools/make_leaves
      tools/leaftools/make_leaves_from_talea
      tools/leaftools/make_tied_leaf
      tools/leaftools/remove_initial_rests_from_sequence
      tools/leaftools/remove_leaf_and_shrink_durated_parent_containers
      tools/leaftools/remove_outer_rests_from_sequence
      tools/leaftools/remove_terminal_rests_from_sequence
      tools/leaftools/repeat_leaf
      tools/leaftools/repeat_leaves_in_expr
      tools/leaftools/replace_leaves_in_expr_with_named_parallel_voices
      tools/leaftools/replace_leaves_in_expr_with_parallel_voices
      tools/leaftools/rest_leaf_at_offset
      tools/leaftools/scale_preprolated_leaf_duration
      tools/leaftools/set_preprolated_leaf_duration
      tools/leaftools/show_leaves
      tools/leaftools/split_leaf_at_offset
      tools/leaftools/split_leaf_at_offsets
      tools/leaftools/yield_groups_of_mixed_notes_and_chords_in_sequence

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/leaftools/Leaf/Leaf
      tools/leaftools/TieChain/TieChain

   Functions
   ---------

   .. toctree::

      tools/leaftools/change_written_leaf_duration_and_preserve_preprolated_leaf_duration
      tools/leaftools/copy_written_duration_and_multiplier_from_leaf_to_leaf
      tools/leaftools/divide_leaf_meiotically
      tools/leaftools/divide_leaves_in_expr_meiotically
      tools/leaftools/expr_has_leaf_with_dotted_written_duration
      tools/leaftools/fuse_leaves
      tools/leaftools/fuse_leaves_in_container_once_by_counts
      tools/leaftools/fuse_leaves_in_tie_chain_by_immediate_parent
      tools/leaftools/get_composite_offset_difference_series_from_leaves_in_expr
      tools/leaftools/get_composite_offset_series_from_leaves_in_expr
      tools/leaftools/get_leaf_at_index_in_measure_number_in_expr
      tools/leaftools/get_leaf_in_expr_with_maximum_duration
      tools/leaftools/get_leaf_in_expr_with_minimum_duration
      tools/leaftools/get_nth_leaf_in_expr
      tools/leaftools/get_nth_leaf_in_thread_from_leaf
      tools/leaftools/is_bar_line_crossing_leaf
      tools/leaftools/list_durations_of_leaves_in_expr
      tools/leaftools/list_written_durations_of_leaves_in_expr
      tools/leaftools/make_leaves
      tools/leaftools/make_leaves_from_talea
      tools/leaftools/make_tied_leaf
      tools/leaftools/remove_initial_rests_from_sequence
      tools/leaftools/remove_leaf_and_shrink_durated_parent_containers
      tools/leaftools/remove_outer_rests_from_sequence
      tools/leaftools/remove_terminal_rests_from_sequence
      tools/leaftools/repeat_leaf
      tools/leaftools/repeat_leaves_in_expr
      tools/leaftools/replace_leaves_in_expr_with_named_parallel_voices
      tools/leaftools/replace_leaves_in_expr_with_parallel_voices
      tools/leaftools/rest_leaf_at_offset
      tools/leaftools/scale_preprolated_leaf_duration
      tools/leaftools/set_preprolated_leaf_duration
      tools/leaftools/show_leaves
      tools/leaftools/split_leaf_at_offset
      tools/leaftools/split_leaf_at_offsets
      tools/leaftools/yield_groups_of_mixed_notes_and_chords_in_sequence

:py:mod:`lilypondfiletools <abjad.tools.lilypondfiletools>`
===========================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/lilypondfiletools/AttributedBlock/AttributedBlock
      tools/lilypondfiletools/NonattributedBlock/NonattributedBlock

   --------

   .. toctree::
      :maxdepth: 1

      tools/lilypondfiletools/AbjadRevisionToken/AbjadRevisionToken
      tools/lilypondfiletools/BookBlock/BookBlock
      tools/lilypondfiletools/BookpartBlock/BookpartBlock
      tools/lilypondfiletools/ContextBlock/ContextBlock
      tools/lilypondfiletools/DateTimeToken/DateTimeToken
      tools/lilypondfiletools/HeaderBlock/HeaderBlock
      tools/lilypondfiletools/LayoutBlock/LayoutBlock
      tools/lilypondfiletools/LilyPondDimension/LilyPondDimension
      tools/lilypondfiletools/LilyPondFile/LilyPondFile
      tools/lilypondfiletools/LilyPondLanguageToken/LilyPondLanguageToken
      tools/lilypondfiletools/LilyPondVersionToken/LilyPondVersionToken
      tools/lilypondfiletools/MIDIBlock/MIDIBlock
      tools/lilypondfiletools/PaperBlock/PaperBlock
      tools/lilypondfiletools/ScoreBlock/ScoreBlock

   --------

   .. toctree::
      :maxdepth: 1

      tools/lilypondfiletools/make_basic_lilypond_file
      tools/lilypondfiletools/make_floating_time_signature_lilypond_file
      tools/lilypondfiletools/make_time_signature_context_block

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/lilypondfiletools/AttributedBlock/AttributedBlock
      tools/lilypondfiletools/NonattributedBlock/NonattributedBlock

   Concrete Classes
   ----------------

   .. toctree::

      tools/lilypondfiletools/AbjadRevisionToken/AbjadRevisionToken
      tools/lilypondfiletools/BookBlock/BookBlock
      tools/lilypondfiletools/BookpartBlock/BookpartBlock
      tools/lilypondfiletools/ContextBlock/ContextBlock
      tools/lilypondfiletools/DateTimeToken/DateTimeToken
      tools/lilypondfiletools/HeaderBlock/HeaderBlock
      tools/lilypondfiletools/LayoutBlock/LayoutBlock
      tools/lilypondfiletools/LilyPondDimension/LilyPondDimension
      tools/lilypondfiletools/LilyPondFile/LilyPondFile
      tools/lilypondfiletools/LilyPondLanguageToken/LilyPondLanguageToken
      tools/lilypondfiletools/LilyPondVersionToken/LilyPondVersionToken
      tools/lilypondfiletools/MIDIBlock/MIDIBlock
      tools/lilypondfiletools/PaperBlock/PaperBlock
      tools/lilypondfiletools/ScoreBlock/ScoreBlock

   Functions
   ---------

   .. toctree::

      tools/lilypondfiletools/make_basic_lilypond_file
      tools/lilypondfiletools/make_floating_time_signature_lilypond_file
      tools/lilypondfiletools/make_time_signature_context_block

:py:mod:`marktools <abjad.tools.marktools>`
===========================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/marktools/DirectedMark/DirectedMark

   --------

   .. toctree::
      :maxdepth: 1

      tools/marktools/Annotation/Annotation
      tools/marktools/Articulation/Articulation
      tools/marktools/BarLine/BarLine
      tools/marktools/BendAfter/BendAfter
      tools/marktools/LilyPondCommandMark/LilyPondCommandMark
      tools/marktools/LilyPondComment/LilyPondComment
      tools/marktools/Mark/Mark
      tools/marktools/StemTremolo/StemTremolo

   --------

   .. toctree::
      :maxdepth: 1

      tools/marktools/attach_annotations_to_components_in_expr
      tools/marktools/attach_articulations_to_notes_and_chords_in_expr
      tools/marktools/attach_lilypond_command_marks_to_components_in_expr
      tools/marktools/attach_lilypond_comments_to_components_in_expr
      tools/marktools/attach_stem_tremolos_to_notes_and_chords_in_expr
      tools/marktools/detach_annotations_attached_to_component
      tools/marktools/detach_articulations_attached_to_component
      tools/marktools/detach_lilypond_command_marks_attached_to_component
      tools/marktools/detach_lilypond_comments_attached_to_component
      tools/marktools/detach_marks_attached_to_component
      tools/marktools/detach_marks_attached_to_components_in_expr
      tools/marktools/detach_noncontext_marks_attached_to_component
      tools/marktools/detach_stem_tremolos_attached_to_component
      tools/marktools/get_annotation_attached_to_component
      tools/marktools/get_annotations_attached_to_component
      tools/marktools/get_articulation_attached_to_component
      tools/marktools/get_articulations_attached_to_component
      tools/marktools/get_lilypond_command_mark_attached_to_component
      tools/marktools/get_lilypond_command_marks_attached_to_component
      tools/marktools/get_lilypond_comment_attached_to_component
      tools/marktools/get_lilypond_comments_attached_to_component
      tools/marktools/get_mark_attached_to_component
      tools/marktools/get_marks_attached_to_component
      tools/marktools/get_marks_attached_to_components_in_expr
      tools/marktools/get_noncontext_mark_attached_to_component
      tools/marktools/get_noncontext_marks_attached_to_component
      tools/marktools/get_stem_tremolo_attached_to_component
      tools/marktools/get_stem_tremolos_attached_to_component
      tools/marktools/get_value_of_annotation_attached_to_component
      tools/marktools/is_component_with_annotation_attached
      tools/marktools/is_component_with_articulation_attached
      tools/marktools/is_component_with_lilypond_command_mark_attached
      tools/marktools/is_component_with_lilypond_comment_attached
      tools/marktools/is_component_with_mark_attached
      tools/marktools/is_component_with_noncontext_mark_attached
      tools/marktools/is_component_with_stem_tremolo_attached
      tools/marktools/move_marks

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/marktools/DirectedMark/DirectedMark

   Concrete Classes
   ----------------

   .. toctree::

      tools/marktools/Annotation/Annotation
      tools/marktools/Articulation/Articulation
      tools/marktools/BarLine/BarLine
      tools/marktools/BendAfter/BendAfter
      tools/marktools/LilyPondCommandMark/LilyPondCommandMark
      tools/marktools/LilyPondComment/LilyPondComment
      tools/marktools/Mark/Mark
      tools/marktools/StemTremolo/StemTremolo

   Functions
   ---------

   .. toctree::

      tools/marktools/attach_annotations_to_components_in_expr
      tools/marktools/attach_articulations_to_notes_and_chords_in_expr
      tools/marktools/attach_lilypond_command_marks_to_components_in_expr
      tools/marktools/attach_lilypond_comments_to_components_in_expr
      tools/marktools/attach_stem_tremolos_to_notes_and_chords_in_expr
      tools/marktools/detach_annotations_attached_to_component
      tools/marktools/detach_articulations_attached_to_component
      tools/marktools/detach_lilypond_command_marks_attached_to_component
      tools/marktools/detach_lilypond_comments_attached_to_component
      tools/marktools/detach_marks_attached_to_component
      tools/marktools/detach_marks_attached_to_components_in_expr
      tools/marktools/detach_noncontext_marks_attached_to_component
      tools/marktools/detach_stem_tremolos_attached_to_component
      tools/marktools/get_annotation_attached_to_component
      tools/marktools/get_annotations_attached_to_component
      tools/marktools/get_articulation_attached_to_component
      tools/marktools/get_articulations_attached_to_component
      tools/marktools/get_lilypond_command_mark_attached_to_component
      tools/marktools/get_lilypond_command_marks_attached_to_component
      tools/marktools/get_lilypond_comment_attached_to_component
      tools/marktools/get_lilypond_comments_attached_to_component
      tools/marktools/get_mark_attached_to_component
      tools/marktools/get_marks_attached_to_component
      tools/marktools/get_marks_attached_to_components_in_expr
      tools/marktools/get_noncontext_mark_attached_to_component
      tools/marktools/get_noncontext_marks_attached_to_component
      tools/marktools/get_stem_tremolo_attached_to_component
      tools/marktools/get_stem_tremolos_attached_to_component
      tools/marktools/get_value_of_annotation_attached_to_component
      tools/marktools/is_component_with_annotation_attached
      tools/marktools/is_component_with_articulation_attached
      tools/marktools/is_component_with_lilypond_command_mark_attached
      tools/marktools/is_component_with_lilypond_comment_attached
      tools/marktools/is_component_with_mark_attached
      tools/marktools/is_component_with_noncontext_mark_attached
      tools/marktools/is_component_with_stem_tremolo_attached
      tools/marktools/move_marks

:py:mod:`markuptools <abjad.tools.markuptools>`
===============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/markuptools/Markup/Markup
      tools/markuptools/MarkupCommand/MarkupCommand
      tools/markuptools/MarkupInventory/MarkupInventory
      tools/markuptools/MusicGlyph/MusicGlyph

   --------

   .. toctree::
      :maxdepth: 1

      tools/markuptools/combine_markup_commands
      tools/markuptools/get_down_markup_attached_to_component
      tools/markuptools/get_markup_attached_to_component
      tools/markuptools/get_up_markup_attached_to_component
      tools/markuptools/make_big_centered_page_number_markup
      tools/markuptools/make_blank_line_markup
      tools/markuptools/make_centered_title_markup
      tools/markuptools/make_vertically_adjusted_composer_markup
      tools/markuptools/remove_markup_attached_to_component

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/markuptools/Markup/Markup
      tools/markuptools/MarkupCommand/MarkupCommand
      tools/markuptools/MarkupInventory/MarkupInventory
      tools/markuptools/MusicGlyph/MusicGlyph

   Functions
   ---------

   .. toctree::

      tools/markuptools/combine_markup_commands
      tools/markuptools/get_down_markup_attached_to_component
      tools/markuptools/get_markup_attached_to_component
      tools/markuptools/get_up_markup_attached_to_component
      tools/markuptools/make_big_centered_page_number_markup
      tools/markuptools/make_blank_line_markup
      tools/markuptools/make_centered_title_markup
      tools/markuptools/make_vertically_adjusted_composer_markup
      tools/markuptools/remove_markup_attached_to_component

:py:mod:`mathtools <abjad.tools.mathtools>`
===========================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/mathtools/BoundedObject/BoundedObject

   --------

   .. toctree::
      :maxdepth: 1

      tools/mathtools/Infinity/Infinity
      tools/mathtools/NegativeInfinity/NegativeInfinity
      tools/mathtools/NonreducedFraction/NonreducedFraction
      tools/mathtools/NonreducedRatio/NonreducedRatio
      tools/mathtools/Ratio/Ratio

   --------

   .. toctree::
      :maxdepth: 1

      tools/mathtools/are_relatively_prime
      tools/mathtools/arithmetic_mean
      tools/mathtools/binomial_coefficient
      tools/mathtools/cumulative_products
      tools/mathtools/cumulative_signed_weights
      tools/mathtools/cumulative_sums
      tools/mathtools/cumulative_sums_zero
      tools/mathtools/cumulative_sums_zero_pairwise
      tools/mathtools/difference_series
      tools/mathtools/divide_number_by_ratio
      tools/mathtools/divisors
      tools/mathtools/factors
      tools/mathtools/fraction_to_proper_fraction
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
      tools/mathtools/interval_string_to_pair_and_indicators
      tools/mathtools/is_assignable_integer
      tools/mathtools/is_dotted_integer
      tools/mathtools/is_integer_equivalent_expr
      tools/mathtools/is_integer_equivalent_number
      tools/mathtools/is_negative_integer
      tools/mathtools/is_nonnegative_integer
      tools/mathtools/is_nonnegative_integer_equivalent_number
      tools/mathtools/is_nonnegative_integer_power_of_two
      tools/mathtools/is_positive_integer
      tools/mathtools/is_positive_integer_equivalent_number
      tools/mathtools/is_positive_integer_power_of_two
      tools/mathtools/least_common_multiple
      tools/mathtools/least_multiple_greater_equal
      tools/mathtools/least_power_of_two_greater_equal
      tools/mathtools/next_integer_partition
      tools/mathtools/partition_integer_by_ratio
      tools/mathtools/partition_integer_into_canonic_parts
      tools/mathtools/partition_integer_into_halves
      tools/mathtools/partition_integer_into_parts_less_than_double
      tools/mathtools/partition_integer_into_units
      tools/mathtools/remove_powers_of_two
      tools/mathtools/sign
      tools/mathtools/weight
      tools/mathtools/yield_all_compositions_of_integer
      tools/mathtools/yield_all_partitions_of_integer
      tools/mathtools/yield_nonreduced_fractions

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/mathtools/BoundedObject/BoundedObject

   Concrete Classes
   ----------------

   .. toctree::

      tools/mathtools/Infinity/Infinity
      tools/mathtools/NegativeInfinity/NegativeInfinity
      tools/mathtools/NonreducedFraction/NonreducedFraction
      tools/mathtools/NonreducedRatio/NonreducedRatio
      tools/mathtools/Ratio/Ratio

   Functions
   ---------

   .. toctree::

      tools/mathtools/are_relatively_prime
      tools/mathtools/arithmetic_mean
      tools/mathtools/binomial_coefficient
      tools/mathtools/cumulative_products
      tools/mathtools/cumulative_signed_weights
      tools/mathtools/cumulative_sums
      tools/mathtools/cumulative_sums_zero
      tools/mathtools/cumulative_sums_zero_pairwise
      tools/mathtools/difference_series
      tools/mathtools/divide_number_by_ratio
      tools/mathtools/divisors
      tools/mathtools/factors
      tools/mathtools/fraction_to_proper_fraction
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
      tools/mathtools/interval_string_to_pair_and_indicators
      tools/mathtools/is_assignable_integer
      tools/mathtools/is_dotted_integer
      tools/mathtools/is_integer_equivalent_expr
      tools/mathtools/is_integer_equivalent_number
      tools/mathtools/is_negative_integer
      tools/mathtools/is_nonnegative_integer
      tools/mathtools/is_nonnegative_integer_equivalent_number
      tools/mathtools/is_nonnegative_integer_power_of_two
      tools/mathtools/is_positive_integer
      tools/mathtools/is_positive_integer_equivalent_number
      tools/mathtools/is_positive_integer_power_of_two
      tools/mathtools/least_common_multiple
      tools/mathtools/least_multiple_greater_equal
      tools/mathtools/least_power_of_two_greater_equal
      tools/mathtools/next_integer_partition
      tools/mathtools/partition_integer_by_ratio
      tools/mathtools/partition_integer_into_canonic_parts
      tools/mathtools/partition_integer_into_halves
      tools/mathtools/partition_integer_into_parts_less_than_double
      tools/mathtools/partition_integer_into_units
      tools/mathtools/remove_powers_of_two
      tools/mathtools/sign
      tools/mathtools/weight
      tools/mathtools/yield_all_compositions_of_integer
      tools/mathtools/yield_all_partitions_of_integer
      tools/mathtools/yield_nonreduced_fractions

:py:mod:`measuretools <abjad.tools.measuretools>`
=================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/measuretools/Measure/Measure

   --------

   .. toctree::
      :maxdepth: 1

      tools/measuretools/append_spacer_skip_to_underfull_measure
      tools/measuretools/append_spacer_skips_to_underfull_measures_in_expr
      tools/measuretools/apply_full_measure_tuplets_to_contents_of_measures_in_expr
      tools/measuretools/comment_measures_in_container_with_measure_numbers
      tools/measuretools/extend_measures_in_expr_and_apply_full_measure_tuplets
      tools/measuretools/fill_measures_in_expr_with_full_measure_spacer_skips
      tools/measuretools/fill_measures_in_expr_with_minimal_number_of_notes
      tools/measuretools/fill_measures_in_expr_with_repeated_notes
      tools/measuretools/fill_measures_in_expr_with_time_signature_denominator_notes
      tools/measuretools/fuse_contiguous_measures_in_container_cyclically_by_counts
      tools/measuretools/fuse_measures
      tools/measuretools/get_likely_multiplier_of_components
      tools/measuretools/get_measure_that_starts_with_container
      tools/measuretools/get_measure_that_stops_with_container
      tools/measuretools/get_next_measure_from_component
      tools/measuretools/get_nth_measure_in_expr
      tools/measuretools/get_one_indexed_measure_number_in_expr
      tools/measuretools/get_previous_measure_from_component
      tools/measuretools/list_time_signatures_of_measures_in_expr
      tools/measuretools/make_measures_with_full_measure_spacer_skips
      tools/measuretools/measure_to_one_line_input_string
      tools/measuretools/move_full_measure_tuplet_prolation_to_measure_time_signature
      tools/measuretools/move_measure_prolation_to_full_measure_tuplet
      tools/measuretools/multiply_and_scale_contents_of_measures_in_expr
      tools/measuretools/multiply_contents_of_measures_in_expr
      tools/measuretools/pad_measures_in_expr
      tools/measuretools/pad_measures_in_expr_with_rests
      tools/measuretools/pad_measures_in_expr_with_skips
      tools/measuretools/replace_contents_of_measures_in_expr
      tools/measuretools/report_time_signature_distribution
      tools/measuretools/scale_contents_of_measures_in_expr
      tools/measuretools/scale_measure_and_adjust_time_signature
      tools/measuretools/scale_measure_denominator_and_adjust_measure_contents
      tools/measuretools/set_always_format_time_signature_of_measures_in_expr
      tools/measuretools/set_measure_denominator_and_adjust_numerator

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/measuretools/Measure/Measure

   Functions
   ---------

   .. toctree::

      tools/measuretools/append_spacer_skip_to_underfull_measure
      tools/measuretools/append_spacer_skips_to_underfull_measures_in_expr
      tools/measuretools/apply_full_measure_tuplets_to_contents_of_measures_in_expr
      tools/measuretools/comment_measures_in_container_with_measure_numbers
      tools/measuretools/extend_measures_in_expr_and_apply_full_measure_tuplets
      tools/measuretools/fill_measures_in_expr_with_full_measure_spacer_skips
      tools/measuretools/fill_measures_in_expr_with_minimal_number_of_notes
      tools/measuretools/fill_measures_in_expr_with_repeated_notes
      tools/measuretools/fill_measures_in_expr_with_time_signature_denominator_notes
      tools/measuretools/fuse_contiguous_measures_in_container_cyclically_by_counts
      tools/measuretools/fuse_measures
      tools/measuretools/get_likely_multiplier_of_components
      tools/measuretools/get_measure_that_starts_with_container
      tools/measuretools/get_measure_that_stops_with_container
      tools/measuretools/get_next_measure_from_component
      tools/measuretools/get_nth_measure_in_expr
      tools/measuretools/get_one_indexed_measure_number_in_expr
      tools/measuretools/get_previous_measure_from_component
      tools/measuretools/list_time_signatures_of_measures_in_expr
      tools/measuretools/make_measures_with_full_measure_spacer_skips
      tools/measuretools/measure_to_one_line_input_string
      tools/measuretools/move_full_measure_tuplet_prolation_to_measure_time_signature
      tools/measuretools/move_measure_prolation_to_full_measure_tuplet
      tools/measuretools/multiply_and_scale_contents_of_measures_in_expr
      tools/measuretools/multiply_contents_of_measures_in_expr
      tools/measuretools/pad_measures_in_expr
      tools/measuretools/pad_measures_in_expr_with_rests
      tools/measuretools/pad_measures_in_expr_with_skips
      tools/measuretools/replace_contents_of_measures_in_expr
      tools/measuretools/report_time_signature_distribution
      tools/measuretools/scale_contents_of_measures_in_expr
      tools/measuretools/scale_measure_and_adjust_time_signature
      tools/measuretools/scale_measure_denominator_and_adjust_measure_contents
      tools/measuretools/set_always_format_time_signature_of_measures_in_expr
      tools/measuretools/set_measure_denominator_and_adjust_numerator

:py:mod:`notetools <abjad.tools.notetools>`
===========================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/notetools/NaturalHarmonic/NaturalHarmonic
      tools/notetools/Note/Note
      tools/notetools/NoteHead/NoteHead

   --------

   .. toctree::
      :maxdepth: 1

      tools/notetools/add_artificial_harmonic_to_note
      tools/notetools/make_accelerating_notes_with_lilypond_multipliers
      tools/notetools/make_notes
      tools/notetools/make_notes_with_multiplied_durations
      tools/notetools/make_percussion_note
      tools/notetools/make_quarter_notes_with_lilypond_multipliers
      tools/notetools/make_repeated_notes
      tools/notetools/make_repeated_notes_from_time_signature
      tools/notetools/make_repeated_notes_from_time_signatures
      tools/notetools/make_repeated_notes_with_shorter_notes_at_end
      tools/notetools/make_tied_note

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/notetools/NaturalHarmonic/NaturalHarmonic
      tools/notetools/Note/Note
      tools/notetools/NoteHead/NoteHead

   Functions
   ---------

   .. toctree::

      tools/notetools/add_artificial_harmonic_to_note
      tools/notetools/make_accelerating_notes_with_lilypond_multipliers
      tools/notetools/make_notes
      tools/notetools/make_notes_with_multiplied_durations
      tools/notetools/make_percussion_note
      tools/notetools/make_quarter_notes_with_lilypond_multipliers
      tools/notetools/make_repeated_notes
      tools/notetools/make_repeated_notes_from_time_signature
      tools/notetools/make_repeated_notes_from_time_signatures
      tools/notetools/make_repeated_notes_with_shorter_notes_at_end
      tools/notetools/make_tied_note

:py:mod:`pitcharraytools <abjad.tools.pitcharraytools>`
=======================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/pitcharraytools/PitchArray/PitchArray
      tools/pitcharraytools/PitchArrayCell/PitchArrayCell
      tools/pitcharraytools/PitchArrayColumn/PitchArrayColumn
      tools/pitcharraytools/PitchArrayRow/PitchArrayRow

   --------

   .. toctree::
      :maxdepth: 1

      tools/pitcharraytools/concatenate_pitch_arrays
      tools/pitcharraytools/list_nonspanning_subarrays_of_pitch_array
      tools/pitcharraytools/make_pitch_array_from_leaf_iterables
      tools/pitcharraytools/make_pitch_array_score_from_pitch_arrays
      tools/pitcharraytools/pitch_array_row_to_measure
      tools/pitcharraytools/pitch_array_to_measures

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/pitcharraytools/PitchArray/PitchArray
      tools/pitcharraytools/PitchArrayCell/PitchArrayCell
      tools/pitcharraytools/PitchArrayColumn/PitchArrayColumn
      tools/pitcharraytools/PitchArrayRow/PitchArrayRow

   Functions
   ---------

   .. toctree::

      tools/pitcharraytools/concatenate_pitch_arrays
      tools/pitcharraytools/list_nonspanning_subarrays_of_pitch_array
      tools/pitcharraytools/make_pitch_array_from_leaf_iterables
      tools/pitcharraytools/make_pitch_array_score_from_pitch_arrays
      tools/pitcharraytools/pitch_array_row_to_measure
      tools/pitcharraytools/pitch_array_to_measures

:py:mod:`pitchtools <abjad.tools.pitchtools>`
=============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/pitchtools/ChromaticInterval/ChromaticInterval
      tools/pitchtools/ChromaticIntervalClass/ChromaticIntervalClass
      tools/pitchtools/ChromaticObject/ChromaticObject
      tools/pitchtools/ChromaticPitch/ChromaticPitch
      tools/pitchtools/CounterpointInterval/CounterpointInterval
      tools/pitchtools/CounterpointIntervalClass/CounterpointIntervalClass
      tools/pitchtools/CounterpointObject/CounterpointObject
      tools/pitchtools/DiatonicInterval/DiatonicInterval
      tools/pitchtools/DiatonicIntervalClass/DiatonicIntervalClass
      tools/pitchtools/DiatonicObject/DiatonicObject
      tools/pitchtools/DiatonicPitch/DiatonicPitch
      tools/pitchtools/DiatonicPitchClass/DiatonicPitchClass
      tools/pitchtools/HarmonicInterval/HarmonicInterval
      tools/pitchtools/HarmonicIntervalClass/HarmonicIntervalClass
      tools/pitchtools/HarmonicObject/HarmonicObject
      tools/pitchtools/Interval/Interval
      tools/pitchtools/IntervalClass/IntervalClass
      tools/pitchtools/IntervalClassSegment/IntervalClassSegment
      tools/pitchtools/IntervalClassSet/IntervalClassSet
      tools/pitchtools/IntervalSegment/IntervalSegment
      tools/pitchtools/IntervalSet/IntervalSet
      tools/pitchtools/MelodicInterval/MelodicInterval
      tools/pitchtools/MelodicIntervalClass/MelodicIntervalClass
      tools/pitchtools/MelodicObject/MelodicObject
      tools/pitchtools/NumberedObject/NumberedObject
      tools/pitchtools/NumberedPitch/NumberedPitch
      tools/pitchtools/NumberedPitchClass/NumberedPitchClass
      tools/pitchtools/Pitch/Pitch
      tools/pitchtools/PitchClass/PitchClass
      tools/pitchtools/PitchClassSegment/PitchClassSegment
      tools/pitchtools/PitchClassSet/PitchClassSet
      tools/pitchtools/PitchSegment/PitchSegment
      tools/pitchtools/PitchSet/PitchSet
      tools/pitchtools/Segment/Segment
      tools/pitchtools/Set/Set
      tools/pitchtools/Vector/Vector

   --------

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
      tools/pitchtools/OctaveTranspositionMapping/OctaveTranspositionMapping
      tools/pitchtools/OctaveTranspositionMappingComponent/OctaveTranspositionMappingComponent
      tools/pitchtools/OctaveTranspositionMappingInventory/OctaveTranspositionMappingInventory
      tools/pitchtools/PitchRange/PitchRange
      tools/pitchtools/PitchRangeInventory/PitchRangeInventory
      tools/pitchtools/TwelveToneRow/TwelveToneRow

   --------

   .. toctree::
      :maxdepth: 1

      tools/pitchtools/all_are_chromatic_pitch_class_name_octave_number_pairs
      tools/pitchtools/all_are_named_chromatic_pitch_tokens
      tools/pitchtools/alphabetic_accidental_abbreviation_to_symbolic_accidental_string
      tools/pitchtools/apply_accidental_to_named_chromatic_pitch
      tools/pitchtools/calculate_harmonic_chromatic_interval
      tools/pitchtools/calculate_harmonic_chromatic_interval_class
      tools/pitchtools/calculate_harmonic_counterpoint_interval
      tools/pitchtools/calculate_harmonic_counterpoint_interval_class
      tools/pitchtools/calculate_harmonic_diatonic_interval
      tools/pitchtools/calculate_harmonic_diatonic_interval_class
      tools/pitchtools/calculate_melodic_chromatic_interval
      tools/pitchtools/calculate_melodic_chromatic_interval_class
      tools/pitchtools/calculate_melodic_counterpoint_interval
      tools/pitchtools/calculate_melodic_counterpoint_interval_class
      tools/pitchtools/calculate_melodic_diatonic_interval
      tools/pitchtools/calculate_melodic_diatonic_interval_class
      tools/pitchtools/chromatic_pitch_class_name_to_chromatic_pitch_class_number
      tools/pitchtools/chromatic_pitch_class_name_to_diatonic_pitch_class_name
      tools/pitchtools/chromatic_pitch_class_number_to_chromatic_pitch_class_name
      tools/pitchtools/chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats
      tools/pitchtools/chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps
      tools/pitchtools/chromatic_pitch_class_number_to_diatonic_pitch_class_number
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
      tools/pitchtools/chromatic_pitch_number_to_chromatic_pitch_class_number
      tools/pitchtools/chromatic_pitch_number_to_chromatic_pitch_name
      tools/pitchtools/chromatic_pitch_number_to_chromatic_pitch_triple
      tools/pitchtools/chromatic_pitch_number_to_diatonic_pitch_class_number
      tools/pitchtools/chromatic_pitch_number_to_diatonic_pitch_number
      tools/pitchtools/chromatic_pitch_number_to_octave_number
      tools/pitchtools/clef_and_staff_position_number_to_named_chromatic_pitch
      tools/pitchtools/contains_subsegment
      tools/pitchtools/diatonic_pitch_class_name_to_chromatic_pitch_class_number
      tools/pitchtools/diatonic_pitch_class_name_to_diatonic_pitch_class_number
      tools/pitchtools/diatonic_pitch_class_number_to_chromatic_pitch_class_number
      tools/pitchtools/diatonic_pitch_class_number_to_diatonic_pitch_class_name
      tools/pitchtools/diatonic_pitch_name_to_chromatic_pitch_class_name
      tools/pitchtools/diatonic_pitch_name_to_chromatic_pitch_class_number
      tools/pitchtools/diatonic_pitch_name_to_chromatic_pitch_name
      tools/pitchtools/diatonic_pitch_name_to_chromatic_pitch_number
      tools/pitchtools/diatonic_pitch_name_to_diatonic_pitch_class_name
      tools/pitchtools/diatonic_pitch_name_to_diatonic_pitch_class_number
      tools/pitchtools/diatonic_pitch_name_to_diatonic_pitch_number
      tools/pitchtools/diatonic_pitch_number_to_chromatic_pitch_number
      tools/pitchtools/diatonic_pitch_number_to_diatonic_pitch_class_name
      tools/pitchtools/diatonic_pitch_number_to_diatonic_pitch_class_number
      tools/pitchtools/diatonic_pitch_number_to_diatonic_pitch_name
      tools/pitchtools/expr_has_duplicate_named_chromatic_pitch
      tools/pitchtools/expr_has_duplicate_numbered_chromatic_pitch_class
      tools/pitchtools/expr_to_melodic_chromatic_interval_segment
      tools/pitchtools/get_named_chromatic_pitch_from_pitch_carrier
      tools/pitchtools/get_numbered_chromatic_pitch_class_from_pitch_carrier
      tools/pitchtools/harmonic_chromatic_interval_class_number_dictionary
      tools/pitchtools/insert_and_transpose_nested_subruns_in_chromatic_pitch_class_number_list
      tools/pitchtools/instantiate_pitch_and_interval_test_collection
      tools/pitchtools/inventory_aggregate_subsets
      tools/pitchtools/inventory_inversion_equivalent_diatonic_interval_classes
      tools/pitchtools/inversion_equivalent_chromatic_interval_class_number_dictionary
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
      tools/pitchtools/is_diatonic_quality_abbreviation
      tools/pitchtools/is_harmonic_diatonic_interval_abbreviation
      tools/pitchtools/is_melodic_diatonic_interval_abbreviation
      tools/pitchtools/is_named_chromatic_pitch_token
      tools/pitchtools/is_octave_tick_string
      tools/pitchtools/is_pitch_carrier
      tools/pitchtools/is_pitch_class_octave_number_string
      tools/pitchtools/is_symbolic_accidental_string
      tools/pitchtools/is_symbolic_pitch_range_string
      tools/pitchtools/iterate_named_chromatic_pitch_pairs_in_expr
      tools/pitchtools/list_chromatic_pitch_numbers_in_expr
      tools/pitchtools/list_harmonic_chromatic_intervals_in_expr
      tools/pitchtools/list_harmonic_diatonic_intervals_in_expr
      tools/pitchtools/list_inversion_equivalent_chromatic_interval_classes_pairwise
      tools/pitchtools/list_melodic_chromatic_interval_numbers_pairwise
      tools/pitchtools/list_named_chromatic_pitches_in_expr
      tools/pitchtools/list_numbered_chromatic_pitch_classes_in_expr
      tools/pitchtools/list_octave_transpositions_of_pitch_carrier_within_pitch_range
      tools/pitchtools/list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2
      tools/pitchtools/list_unordered_named_chromatic_pitch_pairs_in_expr
      tools/pitchtools/make_n_middle_c_centered_pitches
      tools/pitchtools/named_chromatic_pitch_and_clef_to_staff_position_number
      tools/pitchtools/octave_number_to_octave_tick_string
      tools/pitchtools/octave_tick_string_to_octave_number
      tools/pitchtools/pentatonic_pitch_number_to_chromatic_pitch_number
      tools/pitchtools/permute_named_chromatic_pitch_carrier_list_by_twelve_tone_row
      tools/pitchtools/pitch_class_octave_number_string_to_chromatic_pitch_name
      tools/pitchtools/register_chromatic_pitch_class_numbers_by_chromatic_pitch_number_aggregate
      tools/pitchtools/respell_named_chromatic_pitches_in_expr_with_flats
      tools/pitchtools/respell_named_chromatic_pitches_in_expr_with_sharps
      tools/pitchtools/set_ascending_named_chromatic_pitches_on_tie_chains_in_expr
      tools/pitchtools/set_ascending_named_diatonic_pitches_on_tie_chains_in_expr
      tools/pitchtools/set_default_accidental_spelling
      tools/pitchtools/set_written_pitch_of_pitched_components_in_expr
      tools/pitchtools/sort_named_chromatic_pitch_carriers_in_expr
      tools/pitchtools/spell_chromatic_interval_number
      tools/pitchtools/spell_chromatic_pitch_number
      tools/pitchtools/split_chromatic_pitch_class_name
      tools/pitchtools/suggest_clef_for_named_chromatic_pitches
      tools/pitchtools/symbolic_accidental_string_to_alphabetic_accidental_abbreviation
      tools/pitchtools/transpose_chromatic_pitch_by_melodic_chromatic_interval_segment
      tools/pitchtools/transpose_chromatic_pitch_class_number_to_chromatic_pitch_number_neighbor
      tools/pitchtools/transpose_chromatic_pitch_number_by_octave_transposition_mapping
      tools/pitchtools/transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell
      tools/pitchtools/transpose_pitch_carrier_by_melodic_interval
      tools/pitchtools/transpose_pitch_expr_into_pitch_range

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/pitchtools/ChromaticInterval/ChromaticInterval
      tools/pitchtools/ChromaticIntervalClass/ChromaticIntervalClass
      tools/pitchtools/ChromaticObject/ChromaticObject
      tools/pitchtools/ChromaticPitch/ChromaticPitch
      tools/pitchtools/CounterpointInterval/CounterpointInterval
      tools/pitchtools/CounterpointIntervalClass/CounterpointIntervalClass
      tools/pitchtools/CounterpointObject/CounterpointObject
      tools/pitchtools/DiatonicInterval/DiatonicInterval
      tools/pitchtools/DiatonicIntervalClass/DiatonicIntervalClass
      tools/pitchtools/DiatonicObject/DiatonicObject
      tools/pitchtools/DiatonicPitch/DiatonicPitch
      tools/pitchtools/DiatonicPitchClass/DiatonicPitchClass
      tools/pitchtools/HarmonicInterval/HarmonicInterval
      tools/pitchtools/HarmonicIntervalClass/HarmonicIntervalClass
      tools/pitchtools/HarmonicObject/HarmonicObject
      tools/pitchtools/Interval/Interval
      tools/pitchtools/IntervalClass/IntervalClass
      tools/pitchtools/IntervalClassSegment/IntervalClassSegment
      tools/pitchtools/IntervalClassSet/IntervalClassSet
      tools/pitchtools/IntervalSegment/IntervalSegment
      tools/pitchtools/IntervalSet/IntervalSet
      tools/pitchtools/MelodicInterval/MelodicInterval
      tools/pitchtools/MelodicIntervalClass/MelodicIntervalClass
      tools/pitchtools/MelodicObject/MelodicObject
      tools/pitchtools/NumberedObject/NumberedObject
      tools/pitchtools/NumberedPitch/NumberedPitch
      tools/pitchtools/NumberedPitchClass/NumberedPitchClass
      tools/pitchtools/Pitch/Pitch
      tools/pitchtools/PitchClass/PitchClass
      tools/pitchtools/PitchClassSegment/PitchClassSegment
      tools/pitchtools/PitchClassSet/PitchClassSet
      tools/pitchtools/PitchSegment/PitchSegment
      tools/pitchtools/PitchSet/PitchSet
      tools/pitchtools/Segment/Segment
      tools/pitchtools/Set/Set
      tools/pitchtools/Vector/Vector

   Concrete Classes
   ----------------

   .. toctree::

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
      tools/pitchtools/OctaveTranspositionMapping/OctaveTranspositionMapping
      tools/pitchtools/OctaveTranspositionMappingComponent/OctaveTranspositionMappingComponent
      tools/pitchtools/OctaveTranspositionMappingInventory/OctaveTranspositionMappingInventory
      tools/pitchtools/PitchRange/PitchRange
      tools/pitchtools/PitchRangeInventory/PitchRangeInventory
      tools/pitchtools/TwelveToneRow/TwelveToneRow

   Functions
   ---------

   .. toctree::

      tools/pitchtools/all_are_chromatic_pitch_class_name_octave_number_pairs
      tools/pitchtools/all_are_named_chromatic_pitch_tokens
      tools/pitchtools/alphabetic_accidental_abbreviation_to_symbolic_accidental_string
      tools/pitchtools/apply_accidental_to_named_chromatic_pitch
      tools/pitchtools/calculate_harmonic_chromatic_interval
      tools/pitchtools/calculate_harmonic_chromatic_interval_class
      tools/pitchtools/calculate_harmonic_counterpoint_interval
      tools/pitchtools/calculate_harmonic_counterpoint_interval_class
      tools/pitchtools/calculate_harmonic_diatonic_interval
      tools/pitchtools/calculate_harmonic_diatonic_interval_class
      tools/pitchtools/calculate_melodic_chromatic_interval
      tools/pitchtools/calculate_melodic_chromatic_interval_class
      tools/pitchtools/calculate_melodic_counterpoint_interval
      tools/pitchtools/calculate_melodic_counterpoint_interval_class
      tools/pitchtools/calculate_melodic_diatonic_interval
      tools/pitchtools/calculate_melodic_diatonic_interval_class
      tools/pitchtools/chromatic_pitch_class_name_to_chromatic_pitch_class_number
      tools/pitchtools/chromatic_pitch_class_name_to_diatonic_pitch_class_name
      tools/pitchtools/chromatic_pitch_class_number_to_chromatic_pitch_class_name
      tools/pitchtools/chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats
      tools/pitchtools/chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps
      tools/pitchtools/chromatic_pitch_class_number_to_diatonic_pitch_class_number
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
      tools/pitchtools/chromatic_pitch_number_to_chromatic_pitch_class_number
      tools/pitchtools/chromatic_pitch_number_to_chromatic_pitch_name
      tools/pitchtools/chromatic_pitch_number_to_chromatic_pitch_triple
      tools/pitchtools/chromatic_pitch_number_to_diatonic_pitch_class_number
      tools/pitchtools/chromatic_pitch_number_to_diatonic_pitch_number
      tools/pitchtools/chromatic_pitch_number_to_octave_number
      tools/pitchtools/clef_and_staff_position_number_to_named_chromatic_pitch
      tools/pitchtools/contains_subsegment
      tools/pitchtools/diatonic_pitch_class_name_to_chromatic_pitch_class_number
      tools/pitchtools/diatonic_pitch_class_name_to_diatonic_pitch_class_number
      tools/pitchtools/diatonic_pitch_class_number_to_chromatic_pitch_class_number
      tools/pitchtools/diatonic_pitch_class_number_to_diatonic_pitch_class_name
      tools/pitchtools/diatonic_pitch_name_to_chromatic_pitch_class_name
      tools/pitchtools/diatonic_pitch_name_to_chromatic_pitch_class_number
      tools/pitchtools/diatonic_pitch_name_to_chromatic_pitch_name
      tools/pitchtools/diatonic_pitch_name_to_chromatic_pitch_number
      tools/pitchtools/diatonic_pitch_name_to_diatonic_pitch_class_name
      tools/pitchtools/diatonic_pitch_name_to_diatonic_pitch_class_number
      tools/pitchtools/diatonic_pitch_name_to_diatonic_pitch_number
      tools/pitchtools/diatonic_pitch_number_to_chromatic_pitch_number
      tools/pitchtools/diatonic_pitch_number_to_diatonic_pitch_class_name
      tools/pitchtools/diatonic_pitch_number_to_diatonic_pitch_class_number
      tools/pitchtools/diatonic_pitch_number_to_diatonic_pitch_name
      tools/pitchtools/expr_has_duplicate_named_chromatic_pitch
      tools/pitchtools/expr_has_duplicate_numbered_chromatic_pitch_class
      tools/pitchtools/expr_to_melodic_chromatic_interval_segment
      tools/pitchtools/get_named_chromatic_pitch_from_pitch_carrier
      tools/pitchtools/get_numbered_chromatic_pitch_class_from_pitch_carrier
      tools/pitchtools/harmonic_chromatic_interval_class_number_dictionary
      tools/pitchtools/insert_and_transpose_nested_subruns_in_chromatic_pitch_class_number_list
      tools/pitchtools/instantiate_pitch_and_interval_test_collection
      tools/pitchtools/inventory_aggregate_subsets
      tools/pitchtools/inventory_inversion_equivalent_diatonic_interval_classes
      tools/pitchtools/inversion_equivalent_chromatic_interval_class_number_dictionary
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
      tools/pitchtools/is_diatonic_quality_abbreviation
      tools/pitchtools/is_harmonic_diatonic_interval_abbreviation
      tools/pitchtools/is_melodic_diatonic_interval_abbreviation
      tools/pitchtools/is_named_chromatic_pitch_token
      tools/pitchtools/is_octave_tick_string
      tools/pitchtools/is_pitch_carrier
      tools/pitchtools/is_pitch_class_octave_number_string
      tools/pitchtools/is_symbolic_accidental_string
      tools/pitchtools/is_symbolic_pitch_range_string
      tools/pitchtools/iterate_named_chromatic_pitch_pairs_in_expr
      tools/pitchtools/list_chromatic_pitch_numbers_in_expr
      tools/pitchtools/list_harmonic_chromatic_intervals_in_expr
      tools/pitchtools/list_harmonic_diatonic_intervals_in_expr
      tools/pitchtools/list_inversion_equivalent_chromatic_interval_classes_pairwise
      tools/pitchtools/list_melodic_chromatic_interval_numbers_pairwise
      tools/pitchtools/list_named_chromatic_pitches_in_expr
      tools/pitchtools/list_numbered_chromatic_pitch_classes_in_expr
      tools/pitchtools/list_octave_transpositions_of_pitch_carrier_within_pitch_range
      tools/pitchtools/list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2
      tools/pitchtools/list_unordered_named_chromatic_pitch_pairs_in_expr
      tools/pitchtools/make_n_middle_c_centered_pitches
      tools/pitchtools/named_chromatic_pitch_and_clef_to_staff_position_number
      tools/pitchtools/octave_number_to_octave_tick_string
      tools/pitchtools/octave_tick_string_to_octave_number
      tools/pitchtools/pentatonic_pitch_number_to_chromatic_pitch_number
      tools/pitchtools/permute_named_chromatic_pitch_carrier_list_by_twelve_tone_row
      tools/pitchtools/pitch_class_octave_number_string_to_chromatic_pitch_name
      tools/pitchtools/register_chromatic_pitch_class_numbers_by_chromatic_pitch_number_aggregate
      tools/pitchtools/respell_named_chromatic_pitches_in_expr_with_flats
      tools/pitchtools/respell_named_chromatic_pitches_in_expr_with_sharps
      tools/pitchtools/set_ascending_named_chromatic_pitches_on_tie_chains_in_expr
      tools/pitchtools/set_ascending_named_diatonic_pitches_on_tie_chains_in_expr
      tools/pitchtools/set_default_accidental_spelling
      tools/pitchtools/set_written_pitch_of_pitched_components_in_expr
      tools/pitchtools/sort_named_chromatic_pitch_carriers_in_expr
      tools/pitchtools/spell_chromatic_interval_number
      tools/pitchtools/spell_chromatic_pitch_number
      tools/pitchtools/split_chromatic_pitch_class_name
      tools/pitchtools/suggest_clef_for_named_chromatic_pitches
      tools/pitchtools/symbolic_accidental_string_to_alphabetic_accidental_abbreviation
      tools/pitchtools/transpose_chromatic_pitch_by_melodic_chromatic_interval_segment
      tools/pitchtools/transpose_chromatic_pitch_class_number_to_chromatic_pitch_number_neighbor
      tools/pitchtools/transpose_chromatic_pitch_number_by_octave_transposition_mapping
      tools/pitchtools/transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell
      tools/pitchtools/transpose_pitch_carrier_by_melodic_interval
      tools/pitchtools/transpose_pitch_expr_into_pitch_range

:py:mod:`quantizationtools <abjad.tools.quantizationtools>`
===========================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/quantizationtools/AttackPointOptimizer/AttackPointOptimizer
      tools/quantizationtools/GraceHandler/GraceHandler
      tools/quantizationtools/Heuristic/Heuristic
      tools/quantizationtools/JobHandler/JobHandler
      tools/quantizationtools/QEvent/QEvent
      tools/quantizationtools/QSchema/QSchema
      tools/quantizationtools/QSchemaItem/QSchemaItem
      tools/quantizationtools/QTarget/QTarget
      tools/quantizationtools/SearchTree/SearchTree

   --------

   .. toctree::
      :maxdepth: 1

      tools/quantizationtools/BeatwiseQSchema/BeatwiseQSchema
      tools/quantizationtools/BeatwiseQSchemaItem/BeatwiseQSchemaItem
      tools/quantizationtools/BeatwiseQTarget/BeatwiseQTarget
      tools/quantizationtools/CollapsingGraceHandler/CollapsingGraceHandler
      tools/quantizationtools/ConcatenatingGraceHandler/ConcatenatingGraceHandler
      tools/quantizationtools/DiscardingGraceHandler/DiscardingGraceHandler
      tools/quantizationtools/DistanceHeuristic/DistanceHeuristic
      tools/quantizationtools/MeasurewiseAttackPointOptimizer/MeasurewiseAttackPointOptimizer
      tools/quantizationtools/MeasurewiseQSchema/MeasurewiseQSchema
      tools/quantizationtools/MeasurewiseQSchemaItem/MeasurewiseQSchemaItem
      tools/quantizationtools/MeasurewiseQTarget/MeasurewiseQTarget
      tools/quantizationtools/NaiveAttackPointOptimizer/NaiveAttackPointOptimizer
      tools/quantizationtools/NullAttackPointOptimizer/NullAttackPointOptimizer
      tools/quantizationtools/ParallelJobHandler/ParallelJobHandler
      tools/quantizationtools/ParallelJobHandlerWorker/ParallelJobHandlerWorker
      tools/quantizationtools/PitchedQEvent/PitchedQEvent
      tools/quantizationtools/QEventProxy/QEventProxy
      tools/quantizationtools/QEventSequence/QEventSequence
      tools/quantizationtools/QGrid/QGrid
      tools/quantizationtools/QGridContainer/QGridContainer
      tools/quantizationtools/QGridLeaf/QGridLeaf
      tools/quantizationtools/QTargetBeat/QTargetBeat
      tools/quantizationtools/QTargetMeasure/QTargetMeasure
      tools/quantizationtools/QuantizationJob/QuantizationJob
      tools/quantizationtools/Quantizer/Quantizer
      tools/quantizationtools/SerialJobHandler/SerialJobHandler
      tools/quantizationtools/SilentQEvent/SilentQEvent
      tools/quantizationtools/TerminalQEvent/TerminalQEvent
      tools/quantizationtools/UnweightedSearchTree/UnweightedSearchTree
      tools/quantizationtools/WeightedSearchTree/WeightedSearchTree

   --------

   .. toctree::
      :maxdepth: 1

      tools/quantizationtools/make_test_time_segments
      tools/quantizationtools/millisecond_pitch_pairs_to_q_events
      tools/quantizationtools/milliseconds_to_q_events
      tools/quantizationtools/tempo_scaled_duration_to_milliseconds
      tools/quantizationtools/tempo_scaled_durations_to_q_events
      tools/quantizationtools/tempo_scaled_leaves_to_q_events

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/quantizationtools/AttackPointOptimizer/AttackPointOptimizer
      tools/quantizationtools/GraceHandler/GraceHandler
      tools/quantizationtools/Heuristic/Heuristic
      tools/quantizationtools/JobHandler/JobHandler
      tools/quantizationtools/QEvent/QEvent
      tools/quantizationtools/QSchema/QSchema
      tools/quantizationtools/QSchemaItem/QSchemaItem
      tools/quantizationtools/QTarget/QTarget
      tools/quantizationtools/SearchTree/SearchTree

   Concrete Classes
   ----------------

   .. toctree::

      tools/quantizationtools/BeatwiseQSchema/BeatwiseQSchema
      tools/quantizationtools/BeatwiseQSchemaItem/BeatwiseQSchemaItem
      tools/quantizationtools/BeatwiseQTarget/BeatwiseQTarget
      tools/quantizationtools/CollapsingGraceHandler/CollapsingGraceHandler
      tools/quantizationtools/ConcatenatingGraceHandler/ConcatenatingGraceHandler
      tools/quantizationtools/DiscardingGraceHandler/DiscardingGraceHandler
      tools/quantizationtools/DistanceHeuristic/DistanceHeuristic
      tools/quantizationtools/MeasurewiseAttackPointOptimizer/MeasurewiseAttackPointOptimizer
      tools/quantizationtools/MeasurewiseQSchema/MeasurewiseQSchema
      tools/quantizationtools/MeasurewiseQSchemaItem/MeasurewiseQSchemaItem
      tools/quantizationtools/MeasurewiseQTarget/MeasurewiseQTarget
      tools/quantizationtools/NaiveAttackPointOptimizer/NaiveAttackPointOptimizer
      tools/quantizationtools/NullAttackPointOptimizer/NullAttackPointOptimizer
      tools/quantizationtools/ParallelJobHandler/ParallelJobHandler
      tools/quantizationtools/ParallelJobHandlerWorker/ParallelJobHandlerWorker
      tools/quantizationtools/PitchedQEvent/PitchedQEvent
      tools/quantizationtools/QEventProxy/QEventProxy
      tools/quantizationtools/QEventSequence/QEventSequence
      tools/quantizationtools/QGrid/QGrid
      tools/quantizationtools/QGridContainer/QGridContainer
      tools/quantizationtools/QGridLeaf/QGridLeaf
      tools/quantizationtools/QTargetBeat/QTargetBeat
      tools/quantizationtools/QTargetMeasure/QTargetMeasure
      tools/quantizationtools/QuantizationJob/QuantizationJob
      tools/quantizationtools/Quantizer/Quantizer
      tools/quantizationtools/SerialJobHandler/SerialJobHandler
      tools/quantizationtools/SilentQEvent/SilentQEvent
      tools/quantizationtools/TerminalQEvent/TerminalQEvent
      tools/quantizationtools/UnweightedSearchTree/UnweightedSearchTree
      tools/quantizationtools/WeightedSearchTree/WeightedSearchTree

   Functions
   ---------

   .. toctree::

      tools/quantizationtools/make_test_time_segments
      tools/quantizationtools/millisecond_pitch_pairs_to_q_events
      tools/quantizationtools/milliseconds_to_q_events
      tools/quantizationtools/tempo_scaled_duration_to_milliseconds
      tools/quantizationtools/tempo_scaled_durations_to_q_events
      tools/quantizationtools/tempo_scaled_leaves_to_q_events

:py:mod:`resttools <abjad.tools.resttools>`
===========================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/resttools/MultiMeasureRest/MultiMeasureRest
      tools/resttools/Rest/Rest

   --------

   .. toctree::
      :maxdepth: 1

      tools/resttools/make_multi_measure_rests
      tools/resttools/make_repeated_rests_from_time_signature
      tools/resttools/make_repeated_rests_from_time_signatures
      tools/resttools/make_rests
      tools/resttools/make_tied_rest
      tools/resttools/replace_leaves_in_expr_with_rests
      tools/resttools/set_vertical_positioning_pitch_on_rest

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/resttools/MultiMeasureRest/MultiMeasureRest
      tools/resttools/Rest/Rest

   Functions
   ---------

   .. toctree::

      tools/resttools/make_multi_measure_rests
      tools/resttools/make_repeated_rests_from_time_signature
      tools/resttools/make_repeated_rests_from_time_signatures
      tools/resttools/make_rests
      tools/resttools/make_tied_rest
      tools/resttools/replace_leaves_in_expr_with_rests
      tools/resttools/set_vertical_positioning_pitch_on_rest

:py:mod:`rhythmmakertools <abjad.tools.rhythmmakertools>`
=========================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/rhythmmakertools/BurnishedRhythmMaker/BurnishedRhythmMaker
      tools/rhythmmakertools/DivisionIncisedRhythmMaker/DivisionIncisedRhythmMaker
      tools/rhythmmakertools/IncisedRhythmMaker/IncisedRhythmMaker
      tools/rhythmmakertools/OutputIncisedRhythmMaker/OutputIncisedRhythmMaker
      tools/rhythmmakertools/RhythmMaker/RhythmMaker

   --------

   .. toctree::
      :maxdepth: 1

      tools/rhythmmakertools/DivisionBurnishedTaleaRhythmMaker/DivisionBurnishedTaleaRhythmMaker
      tools/rhythmmakertools/DivisionIncisedNoteRhythmMaker/DivisionIncisedNoteRhythmMaker
      tools/rhythmmakertools/DivisionIncisedRestRhythmMaker/DivisionIncisedRestRhythmMaker
      tools/rhythmmakertools/EqualDivisionRhythmMaker/EqualDivisionRhythmMaker
      tools/rhythmmakertools/EvenRunRhythmMaker/EvenRunRhythmMaker
      tools/rhythmmakertools/NoteRhythmMaker/NoteRhythmMaker
      tools/rhythmmakertools/OutputBurnishedTaleaRhythmMaker/OutputBurnishedTaleaRhythmMaker
      tools/rhythmmakertools/OutputIncisedNoteRhythmMaker/OutputIncisedNoteRhythmMaker
      tools/rhythmmakertools/OutputIncisedRestRhythmMaker/OutputIncisedRestRhythmMaker
      tools/rhythmmakertools/RestRhythmMaker/RestRhythmMaker
      tools/rhythmmakertools/SkipRhythmMaker/SkipRhythmMaker
      tools/rhythmmakertools/TaleaRhythmMaker/TaleaRhythmMaker
      tools/rhythmmakertools/TupletMonadRhythmMaker/TupletMonadRhythmMaker

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/rhythmmakertools/BurnishedRhythmMaker/BurnishedRhythmMaker
      tools/rhythmmakertools/DivisionIncisedRhythmMaker/DivisionIncisedRhythmMaker
      tools/rhythmmakertools/IncisedRhythmMaker/IncisedRhythmMaker
      tools/rhythmmakertools/OutputIncisedRhythmMaker/OutputIncisedRhythmMaker
      tools/rhythmmakertools/RhythmMaker/RhythmMaker

   Concrete Classes
   ----------------

   .. toctree::

      tools/rhythmmakertools/DivisionBurnishedTaleaRhythmMaker/DivisionBurnishedTaleaRhythmMaker
      tools/rhythmmakertools/DivisionIncisedNoteRhythmMaker/DivisionIncisedNoteRhythmMaker
      tools/rhythmmakertools/DivisionIncisedRestRhythmMaker/DivisionIncisedRestRhythmMaker
      tools/rhythmmakertools/EqualDivisionRhythmMaker/EqualDivisionRhythmMaker
      tools/rhythmmakertools/EvenRunRhythmMaker/EvenRunRhythmMaker
      tools/rhythmmakertools/NoteRhythmMaker/NoteRhythmMaker
      tools/rhythmmakertools/OutputBurnishedTaleaRhythmMaker/OutputBurnishedTaleaRhythmMaker
      tools/rhythmmakertools/OutputIncisedNoteRhythmMaker/OutputIncisedNoteRhythmMaker
      tools/rhythmmakertools/OutputIncisedRestRhythmMaker/OutputIncisedRestRhythmMaker
      tools/rhythmmakertools/RestRhythmMaker/RestRhythmMaker
      tools/rhythmmakertools/SkipRhythmMaker/SkipRhythmMaker
      tools/rhythmmakertools/TaleaRhythmMaker/TaleaRhythmMaker
      tools/rhythmmakertools/TupletMonadRhythmMaker/TupletMonadRhythmMaker

:py:mod:`rhythmtreetools <abjad.tools.rhythmtreetools>`
=======================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/rhythmtreetools/RhythmTreeNode/RhythmTreeNode

   --------

   .. toctree::
      :maxdepth: 1

      tools/rhythmtreetools/RhythmTreeContainer/RhythmTreeContainer
      tools/rhythmtreetools/RhythmTreeLeaf/RhythmTreeLeaf
      tools/rhythmtreetools/RhythmTreeParser/RhythmTreeParser

   --------

   .. toctree::
      :maxdepth: 1

      tools/rhythmtreetools/parse_rtm_syntax

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/rhythmtreetools/RhythmTreeNode/RhythmTreeNode

   Concrete Classes
   ----------------

   .. toctree::

      tools/rhythmtreetools/RhythmTreeContainer/RhythmTreeContainer
      tools/rhythmtreetools/RhythmTreeLeaf/RhythmTreeLeaf
      tools/rhythmtreetools/RhythmTreeParser/RhythmTreeParser

   Functions
   ---------

   .. toctree::

      tools/rhythmtreetools/parse_rtm_syntax

:py:mod:`schemetools <abjad.tools.schemetools>`
===============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/schemetools/Scheme/Scheme
      tools/schemetools/SchemeAssociativeList/SchemeAssociativeList
      tools/schemetools/SchemeColor/SchemeColor
      tools/schemetools/SchemeMoment/SchemeMoment
      tools/schemetools/SchemePair/SchemePair
      tools/schemetools/SchemeVector/SchemeVector
      tools/schemetools/SchemeVectorConstant/SchemeVectorConstant

   --------

   .. toctree::
      :maxdepth: 1

      tools/schemetools/format_scheme_value

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/schemetools/Scheme/Scheme
      tools/schemetools/SchemeAssociativeList/SchemeAssociativeList
      tools/schemetools/SchemeColor/SchemeColor
      tools/schemetools/SchemeMoment/SchemeMoment
      tools/schemetools/SchemePair/SchemePair
      tools/schemetools/SchemeVector/SchemeVector
      tools/schemetools/SchemeVectorConstant/SchemeVectorConstant

   Functions
   ---------

   .. toctree::

      tools/schemetools/format_scheme_value

:py:mod:`scoretemplatetools <abjad.tools.scoretemplatetools>`
=============================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/scoretemplatetools/ScoreTemplate/ScoreTemplate

   --------

   .. toctree::
      :maxdepth: 1

      tools/scoretemplatetools/GroupedRhythmicStavesScoreTemplate/GroupedRhythmicStavesScoreTemplate
      tools/scoretemplatetools/GroupedStavesScoreTemplate/GroupedStavesScoreTemplate
      tools/scoretemplatetools/StringQuartetScoreTemplate/StringQuartetScoreTemplate
      tools/scoretemplatetools/TwoStaffPianoScoreTemplate/TwoStaffPianoScoreTemplate

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/scoretemplatetools/ScoreTemplate/ScoreTemplate

   Concrete Classes
   ----------------

   .. toctree::

      tools/scoretemplatetools/GroupedRhythmicStavesScoreTemplate/GroupedRhythmicStavesScoreTemplate
      tools/scoretemplatetools/GroupedStavesScoreTemplate/GroupedStavesScoreTemplate
      tools/scoretemplatetools/StringQuartetScoreTemplate/StringQuartetScoreTemplate
      tools/scoretemplatetools/TwoStaffPianoScoreTemplate/TwoStaffPianoScoreTemplate

:py:mod:`scoretools <abjad.tools.scoretools>`
=============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/scoretools/GrandStaff/GrandStaff
      tools/scoretools/InstrumentationSpecifier/InstrumentationSpecifier
      tools/scoretools/Performer/Performer
      tools/scoretools/PerformerInventory/PerformerInventory
      tools/scoretools/PianoStaff/PianoStaff
      tools/scoretools/Score/Score
      tools/scoretools/StaffGroup/StaffGroup

   --------

   .. toctree::
      :maxdepth: 1

      tools/scoretools/add_double_bar_to_end_of_score
      tools/scoretools/add_markup_to_end_of_score
      tools/scoretools/list_performer_names
      tools/scoretools/list_primary_performer_names
      tools/scoretools/make_empty_piano_score
      tools/scoretools/make_piano_score_from_leaves
      tools/scoretools/make_piano_sketch_score_from_leaves

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/scoretools/GrandStaff/GrandStaff
      tools/scoretools/InstrumentationSpecifier/InstrumentationSpecifier
      tools/scoretools/Performer/Performer
      tools/scoretools/PerformerInventory/PerformerInventory
      tools/scoretools/PianoStaff/PianoStaff
      tools/scoretools/Score/Score
      tools/scoretools/StaffGroup/StaffGroup

   Functions
   ---------

   .. toctree::

      tools/scoretools/add_double_bar_to_end_of_score
      tools/scoretools/add_markup_to_end_of_score
      tools/scoretools/list_performer_names
      tools/scoretools/list_primary_performer_names
      tools/scoretools/make_empty_piano_score
      tools/scoretools/make_piano_score_from_leaves
      tools/scoretools/make_piano_sketch_score_from_leaves

:py:mod:`selectiontools <abjad.tools.selectiontools>`
=====================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/selectiontools/Selection/Selection
      tools/selectiontools/SelectionInventory/SelectionInventory

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/selectiontools/Selection/Selection
      tools/selectiontools/SelectionInventory/SelectionInventory

:py:mod:`sequencetools <abjad.tools.sequencetools>`
===================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/sequencetools/CyclicList/CyclicList
      tools/sequencetools/CyclicMatrix/CyclicMatrix
      tools/sequencetools/CyclicTree/CyclicTree
      tools/sequencetools/CyclicTuple/CyclicTuple
      tools/sequencetools/Matrix/Matrix
      tools/sequencetools/Tree/Tree

   --------

   .. toctree::
      :maxdepth: 1

      tools/sequencetools/all_are_assignable_integers
      tools/sequencetools/all_are_equal
      tools/sequencetools/all_are_integer_equivalent_exprs
      tools/sequencetools/all_are_integer_equivalent_numbers
      tools/sequencetools/all_are_nonnegative_integer_equivalent_numbers
      tools/sequencetools/all_are_nonnegative_integer_powers_of_two
      tools/sequencetools/all_are_nonnegative_integers
      tools/sequencetools/all_are_numbers
      tools/sequencetools/all_are_pairs
      tools/sequencetools/all_are_pairs_of_types
      tools/sequencetools/all_are_positive_integer_equivalent_numbers
      tools/sequencetools/all_are_positive_integers
      tools/sequencetools/all_are_unequal
      tools/sequencetools/count_length_two_runs_in_sequence
      tools/sequencetools/divide_sequence_elements_by_greatest_common_divisor
      tools/sequencetools/flatten_sequence
      tools/sequencetools/flatten_sequence_at_indices
      tools/sequencetools/get_indices_of_sequence_elements_equal_to_true
      tools/sequencetools/get_sequence_degree_of_rotational_symmetry
      tools/sequencetools/get_sequence_element_at_cyclic_index
      tools/sequencetools/get_sequence_elements_at_indices
      tools/sequencetools/get_sequence_elements_frequency_distribution
      tools/sequencetools/get_sequence_period_of_rotation
      tools/sequencetools/increase_sequence_elements_at_indices_by_addenda
      tools/sequencetools/increase_sequence_elements_cyclically_by_addenda
      tools/sequencetools/interlace_sequences
      tools/sequencetools/is_fraction_equivalent_pair
      tools/sequencetools/is_integer_equivalent_n_tuple
      tools/sequencetools/is_integer_equivalent_pair
      tools/sequencetools/is_integer_equivalent_singleton
      tools/sequencetools/is_integer_n_tuple
      tools/sequencetools/is_integer_pair
      tools/sequencetools/is_integer_singleton
      tools/sequencetools/is_monotonically_decreasing_sequence
      tools/sequencetools/is_monotonically_increasing_sequence
      tools/sequencetools/is_n_tuple
      tools/sequencetools/is_null_tuple
      tools/sequencetools/is_pair
      tools/sequencetools/is_permutation
      tools/sequencetools/is_repetition_free_sequence
      tools/sequencetools/is_restricted_growth_function
      tools/sequencetools/is_singleton
      tools/sequencetools/is_strictly_decreasing_sequence
      tools/sequencetools/is_strictly_increasing_sequence
      tools/sequencetools/iterate_sequence_cyclically
      tools/sequencetools/iterate_sequence_cyclically_from_start_to_stop
      tools/sequencetools/iterate_sequence_forward_and_backward_nonoverlapping
      tools/sequencetools/iterate_sequence_forward_and_backward_overlapping
      tools/sequencetools/iterate_sequence_nwise_cyclic
      tools/sequencetools/iterate_sequence_nwise_strict
      tools/sequencetools/iterate_sequence_nwise_wrapped
      tools/sequencetools/iterate_sequence_pairwise_cyclic
      tools/sequencetools/iterate_sequence_pairwise_strict
      tools/sequencetools/iterate_sequence_pairwise_wrapped
      tools/sequencetools/join_subsequences
      tools/sequencetools/join_subsequences_by_sign_of_subsequence_elements
      tools/sequencetools/map_sequence_elements_to_canonic_tuples
      tools/sequencetools/map_sequence_elements_to_numbered_sublists
      tools/sequencetools/merge_duration_sequences
      tools/sequencetools/negate_absolute_value_of_sequence_elements_at_indices
      tools/sequencetools/negate_absolute_value_of_sequence_elements_cyclically
      tools/sequencetools/negate_sequence_elements_at_indices
      tools/sequencetools/negate_sequence_elements_cyclically
      tools/sequencetools/overwrite_sequence_elements_at_indices
      tools/sequencetools/pair_duration_sequence_elements_with_input_pair_values
      tools/sequencetools/partition_sequence_by_backgrounded_weights
      tools/sequencetools/partition_sequence_by_counts
      tools/sequencetools/partition_sequence_by_ratio_of_lengths
      tools/sequencetools/partition_sequence_by_ratio_of_weights
      tools/sequencetools/partition_sequence_by_restricted_growth_function
      tools/sequencetools/partition_sequence_by_sign_of_elements
      tools/sequencetools/partition_sequence_by_value_of_elements
      tools/sequencetools/partition_sequence_by_weights_at_least
      tools/sequencetools/partition_sequence_by_weights_at_most
      tools/sequencetools/partition_sequence_by_weights_exactly
      tools/sequencetools/partition_sequence_extended_to_counts
      tools/sequencetools/permute_sequence
      tools/sequencetools/remove_sequence_elements_at_indices
      tools/sequencetools/remove_sequence_elements_at_indices_cyclically
      tools/sequencetools/remove_subsequence_of_weight_at_index
      tools/sequencetools/repeat_runs_in_sequence_to_count
      tools/sequencetools/repeat_sequence_elements_at_indices
      tools/sequencetools/repeat_sequence_elements_at_indices_cyclically
      tools/sequencetools/repeat_sequence_elements_n_times_each
      tools/sequencetools/repeat_sequence_n_times
      tools/sequencetools/repeat_sequence_to_length
      tools/sequencetools/repeat_sequence_to_weight_at_least
      tools/sequencetools/repeat_sequence_to_weight_at_most
      tools/sequencetools/repeat_sequence_to_weight_exactly
      tools/sequencetools/replace_sequence_elements_cyclically_with_new_material
      tools/sequencetools/retain_sequence_elements_at_indices
      tools/sequencetools/retain_sequence_elements_at_indices_cyclically
      tools/sequencetools/reverse_sequence
      tools/sequencetools/reverse_sequence_elements
      tools/sequencetools/rotate_sequence
      tools/sequencetools/splice_new_elements_between_sequence_elements
      tools/sequencetools/split_sequence_by_weights
      tools/sequencetools/split_sequence_extended_to_weights
      tools/sequencetools/sum_consecutive_sequence_elements_by_sign
      tools/sequencetools/sum_sequence_elements_at_indices
      tools/sequencetools/truncate_runs_in_sequence
      tools/sequencetools/truncate_sequence_to_sum
      tools/sequencetools/truncate_sequence_to_weight
      tools/sequencetools/yield_all_combinations_of_sequence_elements
      tools/sequencetools/yield_all_k_ary_sequences_of_length
      tools/sequencetools/yield_all_pairs_between_sequences
      tools/sequencetools/yield_all_partitions_of_sequence
      tools/sequencetools/yield_all_permutations_of_sequence
      tools/sequencetools/yield_all_permutations_of_sequence_in_orbit
      tools/sequencetools/yield_all_restricted_growth_functions_of_length
      tools/sequencetools/yield_all_rotations_of_sequence
      tools/sequencetools/yield_all_set_partitions_of_sequence
      tools/sequencetools/yield_all_subsequences_of_sequence
      tools/sequencetools/yield_all_unordered_pairs_of_sequence
      tools/sequencetools/yield_outer_product_of_sequences
      tools/sequencetools/zip_sequences_cyclically
      tools/sequencetools/zip_sequences_without_truncation

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/sequencetools/CyclicList/CyclicList
      tools/sequencetools/CyclicMatrix/CyclicMatrix
      tools/sequencetools/CyclicTree/CyclicTree
      tools/sequencetools/CyclicTuple/CyclicTuple
      tools/sequencetools/Matrix/Matrix
      tools/sequencetools/Tree/Tree

   Functions
   ---------

   .. toctree::

      tools/sequencetools/all_are_assignable_integers
      tools/sequencetools/all_are_equal
      tools/sequencetools/all_are_integer_equivalent_exprs
      tools/sequencetools/all_are_integer_equivalent_numbers
      tools/sequencetools/all_are_nonnegative_integer_equivalent_numbers
      tools/sequencetools/all_are_nonnegative_integer_powers_of_two
      tools/sequencetools/all_are_nonnegative_integers
      tools/sequencetools/all_are_numbers
      tools/sequencetools/all_are_pairs
      tools/sequencetools/all_are_pairs_of_types
      tools/sequencetools/all_are_positive_integer_equivalent_numbers
      tools/sequencetools/all_are_positive_integers
      tools/sequencetools/all_are_unequal
      tools/sequencetools/count_length_two_runs_in_sequence
      tools/sequencetools/divide_sequence_elements_by_greatest_common_divisor
      tools/sequencetools/flatten_sequence
      tools/sequencetools/flatten_sequence_at_indices
      tools/sequencetools/get_indices_of_sequence_elements_equal_to_true
      tools/sequencetools/get_sequence_degree_of_rotational_symmetry
      tools/sequencetools/get_sequence_element_at_cyclic_index
      tools/sequencetools/get_sequence_elements_at_indices
      tools/sequencetools/get_sequence_elements_frequency_distribution
      tools/sequencetools/get_sequence_period_of_rotation
      tools/sequencetools/increase_sequence_elements_at_indices_by_addenda
      tools/sequencetools/increase_sequence_elements_cyclically_by_addenda
      tools/sequencetools/interlace_sequences
      tools/sequencetools/is_fraction_equivalent_pair
      tools/sequencetools/is_integer_equivalent_n_tuple
      tools/sequencetools/is_integer_equivalent_pair
      tools/sequencetools/is_integer_equivalent_singleton
      tools/sequencetools/is_integer_n_tuple
      tools/sequencetools/is_integer_pair
      tools/sequencetools/is_integer_singleton
      tools/sequencetools/is_monotonically_decreasing_sequence
      tools/sequencetools/is_monotonically_increasing_sequence
      tools/sequencetools/is_n_tuple
      tools/sequencetools/is_null_tuple
      tools/sequencetools/is_pair
      tools/sequencetools/is_permutation
      tools/sequencetools/is_repetition_free_sequence
      tools/sequencetools/is_restricted_growth_function
      tools/sequencetools/is_singleton
      tools/sequencetools/is_strictly_decreasing_sequence
      tools/sequencetools/is_strictly_increasing_sequence
      tools/sequencetools/iterate_sequence_cyclically
      tools/sequencetools/iterate_sequence_cyclically_from_start_to_stop
      tools/sequencetools/iterate_sequence_forward_and_backward_nonoverlapping
      tools/sequencetools/iterate_sequence_forward_and_backward_overlapping
      tools/sequencetools/iterate_sequence_nwise_cyclic
      tools/sequencetools/iterate_sequence_nwise_strict
      tools/sequencetools/iterate_sequence_nwise_wrapped
      tools/sequencetools/iterate_sequence_pairwise_cyclic
      tools/sequencetools/iterate_sequence_pairwise_strict
      tools/sequencetools/iterate_sequence_pairwise_wrapped
      tools/sequencetools/join_subsequences
      tools/sequencetools/join_subsequences_by_sign_of_subsequence_elements
      tools/sequencetools/map_sequence_elements_to_canonic_tuples
      tools/sequencetools/map_sequence_elements_to_numbered_sublists
      tools/sequencetools/merge_duration_sequences
      tools/sequencetools/negate_absolute_value_of_sequence_elements_at_indices
      tools/sequencetools/negate_absolute_value_of_sequence_elements_cyclically
      tools/sequencetools/negate_sequence_elements_at_indices
      tools/sequencetools/negate_sequence_elements_cyclically
      tools/sequencetools/overwrite_sequence_elements_at_indices
      tools/sequencetools/pair_duration_sequence_elements_with_input_pair_values
      tools/sequencetools/partition_sequence_by_backgrounded_weights
      tools/sequencetools/partition_sequence_by_counts
      tools/sequencetools/partition_sequence_by_ratio_of_lengths
      tools/sequencetools/partition_sequence_by_ratio_of_weights
      tools/sequencetools/partition_sequence_by_restricted_growth_function
      tools/sequencetools/partition_sequence_by_sign_of_elements
      tools/sequencetools/partition_sequence_by_value_of_elements
      tools/sequencetools/partition_sequence_by_weights_at_least
      tools/sequencetools/partition_sequence_by_weights_at_most
      tools/sequencetools/partition_sequence_by_weights_exactly
      tools/sequencetools/partition_sequence_extended_to_counts
      tools/sequencetools/permute_sequence
      tools/sequencetools/remove_sequence_elements_at_indices
      tools/sequencetools/remove_sequence_elements_at_indices_cyclically
      tools/sequencetools/remove_subsequence_of_weight_at_index
      tools/sequencetools/repeat_runs_in_sequence_to_count
      tools/sequencetools/repeat_sequence_elements_at_indices
      tools/sequencetools/repeat_sequence_elements_at_indices_cyclically
      tools/sequencetools/repeat_sequence_elements_n_times_each
      tools/sequencetools/repeat_sequence_n_times
      tools/sequencetools/repeat_sequence_to_length
      tools/sequencetools/repeat_sequence_to_weight_at_least
      tools/sequencetools/repeat_sequence_to_weight_at_most
      tools/sequencetools/repeat_sequence_to_weight_exactly
      tools/sequencetools/replace_sequence_elements_cyclically_with_new_material
      tools/sequencetools/retain_sequence_elements_at_indices
      tools/sequencetools/retain_sequence_elements_at_indices_cyclically
      tools/sequencetools/reverse_sequence
      tools/sequencetools/reverse_sequence_elements
      tools/sequencetools/rotate_sequence
      tools/sequencetools/splice_new_elements_between_sequence_elements
      tools/sequencetools/split_sequence_by_weights
      tools/sequencetools/split_sequence_extended_to_weights
      tools/sequencetools/sum_consecutive_sequence_elements_by_sign
      tools/sequencetools/sum_sequence_elements_at_indices
      tools/sequencetools/truncate_runs_in_sequence
      tools/sequencetools/truncate_sequence_to_sum
      tools/sequencetools/truncate_sequence_to_weight
      tools/sequencetools/yield_all_combinations_of_sequence_elements
      tools/sequencetools/yield_all_k_ary_sequences_of_length
      tools/sequencetools/yield_all_pairs_between_sequences
      tools/sequencetools/yield_all_partitions_of_sequence
      tools/sequencetools/yield_all_permutations_of_sequence
      tools/sequencetools/yield_all_permutations_of_sequence_in_orbit
      tools/sequencetools/yield_all_restricted_growth_functions_of_length
      tools/sequencetools/yield_all_rotations_of_sequence
      tools/sequencetools/yield_all_set_partitions_of_sequence
      tools/sequencetools/yield_all_subsequences_of_sequence
      tools/sequencetools/yield_all_unordered_pairs_of_sequence
      tools/sequencetools/yield_outer_product_of_sequences
      tools/sequencetools/zip_sequences_cyclically
      tools/sequencetools/zip_sequences_without_truncation

:py:mod:`sievetools <abjad.tools.sievetools>`
=============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/sievetools/BaseResidueClass/BaseResidueClass

   --------

   .. toctree::
      :maxdepth: 1

      tools/sievetools/ResidueClass/ResidueClass
      tools/sievetools/Sieve/Sieve

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/sievetools/BaseResidueClass/BaseResidueClass

   Concrete Classes
   ----------------

   .. toctree::

      tools/sievetools/ResidueClass/ResidueClass
      tools/sievetools/Sieve/Sieve

:py:mod:`skiptools <abjad.tools.skiptools>`
===========================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/skiptools/Skip/Skip

   --------

   .. toctree::
      :maxdepth: 1

      tools/skiptools/make_repeated_skips_from_time_signature
      tools/skiptools/make_repeated_skips_from_time_signatures
      tools/skiptools/make_skips_with_multiplied_durations
      tools/skiptools/replace_leaves_in_expr_with_skips

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/skiptools/Skip/Skip

   Functions
   ---------

   .. toctree::

      tools/skiptools/make_repeated_skips_from_time_signature
      tools/skiptools/make_repeated_skips_from_time_signatures
      tools/skiptools/make_skips_with_multiplied_durations
      tools/skiptools/replace_leaves_in_expr_with_skips

:py:mod:`spannertools <abjad.tools.spannertools>`
=================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/spannertools/DirectedSpanner/DirectedSpanner
      tools/spannertools/Spanner/Spanner

   --------

   .. toctree::
      :maxdepth: 1

      tools/spannertools/BeamSpanner/BeamSpanner
      tools/spannertools/BracketSpanner/BracketSpanner
      tools/spannertools/ComplexBeamSpanner/ComplexBeamSpanner
      tools/spannertools/ComplexGlissandoSpanner/ComplexGlissandoSpanner
      tools/spannertools/CrescendoSpanner/CrescendoSpanner
      tools/spannertools/DecrescendoSpanner/DecrescendoSpanner
      tools/spannertools/DuratedComplexBeamSpanner/DuratedComplexBeamSpanner
      tools/spannertools/DynamicTextSpanner/DynamicTextSpanner
      tools/spannertools/GlissandoSpanner/GlissandoSpanner
      tools/spannertools/HairpinSpanner/HairpinSpanner
      tools/spannertools/HiddenStaffSpanner/HiddenStaffSpanner
      tools/spannertools/HorizontalBracketSpanner/HorizontalBracketSpanner
      tools/spannertools/MeasuredComplexBeamSpanner/MeasuredComplexBeamSpanner
      tools/spannertools/MultipartBeamSpanner/MultipartBeamSpanner
      tools/spannertools/OctavationSpanner/OctavationSpanner
      tools/spannertools/PhrasingSlurSpanner/PhrasingSlurSpanner
      tools/spannertools/PianoPedalSpanner/PianoPedalSpanner
      tools/spannertools/SlurSpanner/SlurSpanner
      tools/spannertools/StaffLinesSpanner/StaffLinesSpanner
      tools/spannertools/TextScriptSpanner/TextScriptSpanner
      tools/spannertools/TextSpanner/TextSpanner
      tools/spannertools/TieSpanner/TieSpanner
      tools/spannertools/TrillSpanner/TrillSpanner

   --------

   .. toctree::
      :maxdepth: 1

      tools/spannertools/apply_octavation_spanner_to_pitched_components
      tools/spannertools/detach_spanners_attached_to_component
      tools/spannertools/detach_spanners_attached_to_components_in_expr
      tools/spannertools/find_index_of_spanner_component_at_score_offset
      tools/spannertools/find_spanner_component_starting_at_exactly_score_offset
      tools/spannertools/fracture_spanners_attached_to_component
      tools/spannertools/fracture_spanners_that_cross_components
      tools/spannertools/get_nth_leaf_in_spanner
      tools/spannertools/get_spanners_attached_to_any_improper_child_of_component
      tools/spannertools/get_spanners_attached_to_any_improper_parent_of_component
      tools/spannertools/get_spanners_attached_to_any_proper_child_of_component
      tools/spannertools/get_spanners_attached_to_any_proper_parent_of_component
      tools/spannertools/get_spanners_attached_to_component
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
      tools/spannertools/iterate_components_in_spanner
      tools/spannertools/make_covered_spanner_schema
      tools/spannertools/make_dynamic_spanner_below_with_nib_at_right
      tools/spannertools/make_solid_text_spanner_above_with_nib_at_right
      tools/spannertools/make_solid_text_spanner_below_with_nib_at_right
      tools/spannertools/make_spanner_schema
      tools/spannertools/move_spanners_from_component_to_children_of_component
      tools/spannertools/withdraw_components_from_spanners_covered_by_components

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/spannertools/DirectedSpanner/DirectedSpanner
      tools/spannertools/Spanner/Spanner

   Concrete Classes
   ----------------

   .. toctree::

      tools/spannertools/BeamSpanner/BeamSpanner
      tools/spannertools/BracketSpanner/BracketSpanner
      tools/spannertools/ComplexBeamSpanner/ComplexBeamSpanner
      tools/spannertools/ComplexGlissandoSpanner/ComplexGlissandoSpanner
      tools/spannertools/CrescendoSpanner/CrescendoSpanner
      tools/spannertools/DecrescendoSpanner/DecrescendoSpanner
      tools/spannertools/DuratedComplexBeamSpanner/DuratedComplexBeamSpanner
      tools/spannertools/DynamicTextSpanner/DynamicTextSpanner
      tools/spannertools/GlissandoSpanner/GlissandoSpanner
      tools/spannertools/HairpinSpanner/HairpinSpanner
      tools/spannertools/HiddenStaffSpanner/HiddenStaffSpanner
      tools/spannertools/HorizontalBracketSpanner/HorizontalBracketSpanner
      tools/spannertools/MeasuredComplexBeamSpanner/MeasuredComplexBeamSpanner
      tools/spannertools/MultipartBeamSpanner/MultipartBeamSpanner
      tools/spannertools/OctavationSpanner/OctavationSpanner
      tools/spannertools/PhrasingSlurSpanner/PhrasingSlurSpanner
      tools/spannertools/PianoPedalSpanner/PianoPedalSpanner
      tools/spannertools/SlurSpanner/SlurSpanner
      tools/spannertools/StaffLinesSpanner/StaffLinesSpanner
      tools/spannertools/TextScriptSpanner/TextScriptSpanner
      tools/spannertools/TextSpanner/TextSpanner
      tools/spannertools/TieSpanner/TieSpanner
      tools/spannertools/TrillSpanner/TrillSpanner

   Functions
   ---------

   .. toctree::

      tools/spannertools/apply_octavation_spanner_to_pitched_components
      tools/spannertools/detach_spanners_attached_to_component
      tools/spannertools/detach_spanners_attached_to_components_in_expr
      tools/spannertools/find_index_of_spanner_component_at_score_offset
      tools/spannertools/find_spanner_component_starting_at_exactly_score_offset
      tools/spannertools/fracture_spanners_attached_to_component
      tools/spannertools/fracture_spanners_that_cross_components
      tools/spannertools/get_nth_leaf_in_spanner
      tools/spannertools/get_spanners_attached_to_any_improper_child_of_component
      tools/spannertools/get_spanners_attached_to_any_improper_parent_of_component
      tools/spannertools/get_spanners_attached_to_any_proper_child_of_component
      tools/spannertools/get_spanners_attached_to_any_proper_parent_of_component
      tools/spannertools/get_spanners_attached_to_component
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
      tools/spannertools/iterate_components_in_spanner
      tools/spannertools/make_covered_spanner_schema
      tools/spannertools/make_dynamic_spanner_below_with_nib_at_right
      tools/spannertools/make_solid_text_spanner_above_with_nib_at_right
      tools/spannertools/make_solid_text_spanner_below_with_nib_at_right
      tools/spannertools/make_spanner_schema
      tools/spannertools/move_spanners_from_component_to_children_of_component
      tools/spannertools/withdraw_components_from_spanners_covered_by_components

:py:mod:`stafftools <abjad.tools.stafftools>`
=============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/stafftools/RhythmicStaff/RhythmicStaff
      tools/stafftools/Staff/Staff

   --------

   .. toctree::
      :maxdepth: 1

      tools/stafftools/make_rhythmic_sketch_staff

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/stafftools/RhythmicStaff/RhythmicStaff
      tools/stafftools/Staff/Staff

   Functions
   ---------

   .. toctree::

      tools/stafftools/make_rhythmic_sketch_staff

:py:mod:`stringtools <abjad.tools.stringtools>`
===============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/stringtools/add_terminal_newlines
      tools/stringtools/arg_to_bidirectional_direction_string
      tools/stringtools/arg_to_bidirectional_lilypond_symbol
      tools/stringtools/arg_to_tridirectional_direction_string
      tools/stringtools/arg_to_tridirectional_lilypond_symbol
      tools/stringtools/arg_to_tridirectional_ordinal_constant
      tools/stringtools/capitalize_string_start
      tools/stringtools/format_input_lines_as_doc_string
      tools/stringtools/format_input_lines_as_regression_test
      tools/stringtools/is_dash_case_file_name
      tools/stringtools/is_dash_case_string
      tools/stringtools/is_lower_camel_case_string
      tools/stringtools/is_snake_case_file_name
      tools/stringtools/is_snake_case_file_name_with_extension
      tools/stringtools/is_snake_case_package_name
      tools/stringtools/is_snake_case_string
      tools/stringtools/is_space_delimited_lowercase_string
      tools/stringtools/is_upper_camel_case_string
      tools/stringtools/pluralize_string
      tools/stringtools/snake_case_to_lower_camel_case
      tools/stringtools/snake_case_to_upper_camel_case
      tools/stringtools/space_delimited_lowercase_to_upper_camel_case
      tools/stringtools/string_to_accent_free_snake_case
      tools/stringtools/string_to_space_delimited_lowercase
      tools/stringtools/strip_diacritics_from_binary_string
      tools/stringtools/upper_camel_case_to_snake_case
      tools/stringtools/upper_camel_case_to_space_delimited_lowercase

.. only:: latex

   Functions
   ---------

   .. toctree::

      tools/stringtools/add_terminal_newlines
      tools/stringtools/arg_to_bidirectional_direction_string
      tools/stringtools/arg_to_bidirectional_lilypond_symbol
      tools/stringtools/arg_to_tridirectional_direction_string
      tools/stringtools/arg_to_tridirectional_lilypond_symbol
      tools/stringtools/arg_to_tridirectional_ordinal_constant
      tools/stringtools/capitalize_string_start
      tools/stringtools/format_input_lines_as_doc_string
      tools/stringtools/format_input_lines_as_regression_test
      tools/stringtools/is_dash_case_file_name
      tools/stringtools/is_dash_case_string
      tools/stringtools/is_lower_camel_case_string
      tools/stringtools/is_snake_case_file_name
      tools/stringtools/is_snake_case_file_name_with_extension
      tools/stringtools/is_snake_case_package_name
      tools/stringtools/is_snake_case_string
      tools/stringtools/is_space_delimited_lowercase_string
      tools/stringtools/is_upper_camel_case_string
      tools/stringtools/pluralize_string
      tools/stringtools/snake_case_to_lower_camel_case
      tools/stringtools/snake_case_to_upper_camel_case
      tools/stringtools/space_delimited_lowercase_to_upper_camel_case
      tools/stringtools/string_to_accent_free_snake_case
      tools/stringtools/string_to_space_delimited_lowercase
      tools/stringtools/strip_diacritics_from_binary_string
      tools/stringtools/upper_camel_case_to_snake_case
      tools/stringtools/upper_camel_case_to_space_delimited_lowercase

:py:mod:`tempotools <abjad.tools.tempotools>`
=============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/tempotools/report_integer_tempo_rewrite_pairs
      tools/tempotools/rewrite_duration_under_new_tempo
      tools/tempotools/rewrite_integer_tempo

.. only:: latex

   Functions
   ---------

   .. toctree::

      tools/tempotools/report_integer_tempo_rewrite_pairs
      tools/tempotools/rewrite_duration_under_new_tempo
      tools/tempotools/rewrite_integer_tempo

:py:mod:`timeintervaltools <abjad.tools.timeintervaltools>`
===========================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/timeintervaltools/TimeIntervalAggregateMixin/TimeIntervalAggregateMixin
      tools/timeintervaltools/TimeIntervalMixin/TimeIntervalMixin

   --------

   .. toctree::
      :maxdepth: 1

      tools/timeintervaltools/TimeInterval/TimeInterval
      tools/timeintervaltools/TimeIntervalTree/TimeIntervalTree
      tools/timeintervaltools/TimeIntervalTreeDictionary/TimeIntervalTreeDictionary

   --------

   .. toctree::
      :maxdepth: 1

      tools/timeintervaltools/all_are_intervals_or_trees_or_empty
      tools/timeintervaltools/all_intervals_are_contiguous
      tools/timeintervaltools/all_intervals_are_nonoverlapping
      tools/timeintervaltools/calculate_density_of_attacks_in_interval
      tools/timeintervaltools/calculate_density_of_releases_in_interval
      tools/timeintervaltools/calculate_depth_centroid_of_intervals
      tools/timeintervaltools/calculate_depth_centroid_of_intervals_in_interval
      tools/timeintervaltools/calculate_depth_density_of_intervals
      tools/timeintervaltools/calculate_depth_density_of_intervals_in_interval
      tools/timeintervaltools/calculate_mean_attack_of_intervals
      tools/timeintervaltools/calculate_mean_release_of_intervals
      tools/timeintervaltools/calculate_min_mean_and_max_depth_of_intervals
      tools/timeintervaltools/calculate_min_mean_and_max_durations_of_intervals
      tools/timeintervaltools/calculate_sustain_centroid_of_intervals
      tools/timeintervaltools/clip_interval_durations_to_range
      tools/timeintervaltools/compute_depth_of_intervals
      tools/timeintervaltools/compute_depth_of_intervals_in_interval
      tools/timeintervaltools/compute_logical_and_of_intervals
      tools/timeintervaltools/compute_logical_and_of_intervals_in_interval
      tools/timeintervaltools/compute_logical_not_of_intervals
      tools/timeintervaltools/compute_logical_not_of_intervals_in_interval
      tools/timeintervaltools/compute_logical_or_of_intervals
      tools/timeintervaltools/compute_logical_or_of_intervals_in_interval
      tools/timeintervaltools/compute_logical_xor_of_intervals
      tools/timeintervaltools/compute_logical_xor_of_intervals_in_interval
      tools/timeintervaltools/concatenate_trees
      tools/timeintervaltools/explode_intervals_compactly
      tools/timeintervaltools/explode_intervals_into_n_trees_heuristically
      tools/timeintervaltools/explode_intervals_uncompactly
      tools/timeintervaltools/fuse_overlapping_intervals
      tools/timeintervaltools/fuse_tangent_or_overlapping_intervals
      tools/timeintervaltools/get_all_unique_bounds_in_intervals
      tools/timeintervaltools/group_overlapping_intervals_and_yield_groups
      tools/timeintervaltools/group_tangent_or_overlapping_intervals_and_yield_groups
      tools/timeintervaltools/make_monophonic_percussion_score_from_nonoverlapping_intervals
      tools/timeintervaltools/make_polyphonic_percussion_score_from_nonoverlapping_trees
      tools/timeintervaltools/make_test_intervals
      tools/timeintervaltools/make_voice_from_nonoverlapping_intervals
      tools/timeintervaltools/mask_intervals_with_intervals
      tools/timeintervaltools/resolve_overlaps_between_nonoverlapping_trees
      tools/timeintervaltools/round_interval_bounds_to_nearest_multiple_of_rational
      tools/timeintervaltools/scale_aggregate_duration_by_rational
      tools/timeintervaltools/scale_aggregate_duration_to_rational
      tools/timeintervaltools/scale_interval_durations_by_rational
      tools/timeintervaltools/scale_interval_durations_to_rational
      tools/timeintervaltools/scale_interval_offsets_by_rational
      tools/timeintervaltools/shift_aggregate_offset_by_rational
      tools/timeintervaltools/shift_aggregate_offset_to_rational
      tools/timeintervaltools/split_intervals_at_rationals

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/timeintervaltools/TimeIntervalAggregateMixin/TimeIntervalAggregateMixin
      tools/timeintervaltools/TimeIntervalMixin/TimeIntervalMixin

   Concrete Classes
   ----------------

   .. toctree::

      tools/timeintervaltools/TimeInterval/TimeInterval
      tools/timeintervaltools/TimeIntervalTree/TimeIntervalTree
      tools/timeintervaltools/TimeIntervalTreeDictionary/TimeIntervalTreeDictionary

   Functions
   ---------

   .. toctree::

      tools/timeintervaltools/all_are_intervals_or_trees_or_empty
      tools/timeintervaltools/all_intervals_are_contiguous
      tools/timeintervaltools/all_intervals_are_nonoverlapping
      tools/timeintervaltools/calculate_density_of_attacks_in_interval
      tools/timeintervaltools/calculate_density_of_releases_in_interval
      tools/timeintervaltools/calculate_depth_centroid_of_intervals
      tools/timeintervaltools/calculate_depth_centroid_of_intervals_in_interval
      tools/timeintervaltools/calculate_depth_density_of_intervals
      tools/timeintervaltools/calculate_depth_density_of_intervals_in_interval
      tools/timeintervaltools/calculate_mean_attack_of_intervals
      tools/timeintervaltools/calculate_mean_release_of_intervals
      tools/timeintervaltools/calculate_min_mean_and_max_depth_of_intervals
      tools/timeintervaltools/calculate_min_mean_and_max_durations_of_intervals
      tools/timeintervaltools/calculate_sustain_centroid_of_intervals
      tools/timeintervaltools/clip_interval_durations_to_range
      tools/timeintervaltools/compute_depth_of_intervals
      tools/timeintervaltools/compute_depth_of_intervals_in_interval
      tools/timeintervaltools/compute_logical_and_of_intervals
      tools/timeintervaltools/compute_logical_and_of_intervals_in_interval
      tools/timeintervaltools/compute_logical_not_of_intervals
      tools/timeintervaltools/compute_logical_not_of_intervals_in_interval
      tools/timeintervaltools/compute_logical_or_of_intervals
      tools/timeintervaltools/compute_logical_or_of_intervals_in_interval
      tools/timeintervaltools/compute_logical_xor_of_intervals
      tools/timeintervaltools/compute_logical_xor_of_intervals_in_interval
      tools/timeintervaltools/concatenate_trees
      tools/timeintervaltools/explode_intervals_compactly
      tools/timeintervaltools/explode_intervals_into_n_trees_heuristically
      tools/timeintervaltools/explode_intervals_uncompactly
      tools/timeintervaltools/fuse_overlapping_intervals
      tools/timeintervaltools/fuse_tangent_or_overlapping_intervals
      tools/timeintervaltools/get_all_unique_bounds_in_intervals
      tools/timeintervaltools/group_overlapping_intervals_and_yield_groups
      tools/timeintervaltools/group_tangent_or_overlapping_intervals_and_yield_groups
      tools/timeintervaltools/make_monophonic_percussion_score_from_nonoverlapping_intervals
      tools/timeintervaltools/make_polyphonic_percussion_score_from_nonoverlapping_trees
      tools/timeintervaltools/make_test_intervals
      tools/timeintervaltools/make_voice_from_nonoverlapping_intervals
      tools/timeintervaltools/mask_intervals_with_intervals
      tools/timeintervaltools/resolve_overlaps_between_nonoverlapping_trees
      tools/timeintervaltools/round_interval_bounds_to_nearest_multiple_of_rational
      tools/timeintervaltools/scale_aggregate_duration_by_rational
      tools/timeintervaltools/scale_aggregate_duration_to_rational
      tools/timeintervaltools/scale_interval_durations_by_rational
      tools/timeintervaltools/scale_interval_durations_to_rational
      tools/timeintervaltools/scale_interval_offsets_by_rational
      tools/timeintervaltools/shift_aggregate_offset_by_rational
      tools/timeintervaltools/shift_aggregate_offset_to_rational
      tools/timeintervaltools/split_intervals_at_rationals

:py:mod:`timerelationtools <abjad.tools.timerelationtools>`
===========================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/timerelationtools/TimeRelation/TimeRelation

   --------

   .. toctree::
      :maxdepth: 1

      tools/timerelationtools/CompoundInequality/CompoundInequality
      tools/timerelationtools/OffsetTimespanTimeRelation/OffsetTimespanTimeRelation
      tools/timerelationtools/SimpleInequality/SimpleInequality
      tools/timerelationtools/TimespanTimespanTimeRelation/TimespanTimespanTimeRelation

   --------

   .. toctree::
      :maxdepth: 1

      tools/timerelationtools/offset_happens_after_timespan_starts
      tools/timerelationtools/offset_happens_after_timespan_stops
      tools/timerelationtools/offset_happens_before_timespan_starts
      tools/timerelationtools/offset_happens_before_timespan_stops
      tools/timerelationtools/offset_happens_during_timespan
      tools/timerelationtools/offset_happens_when_timespan_starts
      tools/timerelationtools/offset_happens_when_timespan_stops
      tools/timerelationtools/timespan_2_contains_timespan_1_improperly
      tools/timerelationtools/timespan_2_curtails_timespan_1
      tools/timerelationtools/timespan_2_delays_timespan_1
      tools/timerelationtools/timespan_2_happens_during_timespan_1
      tools/timerelationtools/timespan_2_intersects_timespan_1
      tools/timerelationtools/timespan_2_is_congruent_to_timespan_1
      tools/timerelationtools/timespan_2_overlaps_all_of_timespan_1
      tools/timerelationtools/timespan_2_overlaps_only_start_of_timespan_1
      tools/timerelationtools/timespan_2_overlaps_only_stop_of_timespan_1
      tools/timerelationtools/timespan_2_overlaps_start_of_timespan_1
      tools/timerelationtools/timespan_2_overlaps_stop_of_timespan_1
      tools/timerelationtools/timespan_2_starts_after_timespan_1_starts
      tools/timerelationtools/timespan_2_starts_after_timespan_1_stops
      tools/timerelationtools/timespan_2_starts_before_timespan_1_starts
      tools/timerelationtools/timespan_2_starts_before_timespan_1_stops
      tools/timerelationtools/timespan_2_starts_during_timespan_1
      tools/timerelationtools/timespan_2_starts_when_timespan_1_starts
      tools/timerelationtools/timespan_2_starts_when_timespan_1_stops
      tools/timerelationtools/timespan_2_stops_after_timespan_1_starts
      tools/timerelationtools/timespan_2_stops_after_timespan_1_stops
      tools/timerelationtools/timespan_2_stops_before_timespan_1_starts
      tools/timerelationtools/timespan_2_stops_before_timespan_1_stops
      tools/timerelationtools/timespan_2_stops_during_timespan_1
      tools/timerelationtools/timespan_2_stops_when_timespan_1_starts
      tools/timerelationtools/timespan_2_stops_when_timespan_1_stops
      tools/timerelationtools/timespan_2_trisects_timespan_1

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/timerelationtools/TimeRelation/TimeRelation

   Concrete Classes
   ----------------

   .. toctree::

      tools/timerelationtools/CompoundInequality/CompoundInequality
      tools/timerelationtools/OffsetTimespanTimeRelation/OffsetTimespanTimeRelation
      tools/timerelationtools/SimpleInequality/SimpleInequality
      tools/timerelationtools/TimespanTimespanTimeRelation/TimespanTimespanTimeRelation

   Functions
   ---------

   .. toctree::

      tools/timerelationtools/offset_happens_after_timespan_starts
      tools/timerelationtools/offset_happens_after_timespan_stops
      tools/timerelationtools/offset_happens_before_timespan_starts
      tools/timerelationtools/offset_happens_before_timespan_stops
      tools/timerelationtools/offset_happens_during_timespan
      tools/timerelationtools/offset_happens_when_timespan_starts
      tools/timerelationtools/offset_happens_when_timespan_stops
      tools/timerelationtools/timespan_2_contains_timespan_1_improperly
      tools/timerelationtools/timespan_2_curtails_timespan_1
      tools/timerelationtools/timespan_2_delays_timespan_1
      tools/timerelationtools/timespan_2_happens_during_timespan_1
      tools/timerelationtools/timespan_2_intersects_timespan_1
      tools/timerelationtools/timespan_2_is_congruent_to_timespan_1
      tools/timerelationtools/timespan_2_overlaps_all_of_timespan_1
      tools/timerelationtools/timespan_2_overlaps_only_start_of_timespan_1
      tools/timerelationtools/timespan_2_overlaps_only_stop_of_timespan_1
      tools/timerelationtools/timespan_2_overlaps_start_of_timespan_1
      tools/timerelationtools/timespan_2_overlaps_stop_of_timespan_1
      tools/timerelationtools/timespan_2_starts_after_timespan_1_starts
      tools/timerelationtools/timespan_2_starts_after_timespan_1_stops
      tools/timerelationtools/timespan_2_starts_before_timespan_1_starts
      tools/timerelationtools/timespan_2_starts_before_timespan_1_stops
      tools/timerelationtools/timespan_2_starts_during_timespan_1
      tools/timerelationtools/timespan_2_starts_when_timespan_1_starts
      tools/timerelationtools/timespan_2_starts_when_timespan_1_stops
      tools/timerelationtools/timespan_2_stops_after_timespan_1_starts
      tools/timerelationtools/timespan_2_stops_after_timespan_1_stops
      tools/timerelationtools/timespan_2_stops_before_timespan_1_starts
      tools/timerelationtools/timespan_2_stops_before_timespan_1_stops
      tools/timerelationtools/timespan_2_stops_during_timespan_1
      tools/timerelationtools/timespan_2_stops_when_timespan_1_starts
      tools/timerelationtools/timespan_2_stops_when_timespan_1_stops
      tools/timerelationtools/timespan_2_trisects_timespan_1

:py:mod:`timesignaturetools <abjad.tools.timesignaturetools>`
=============================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/timesignaturetools/MetricalHierarchy/MetricalHierarchy
      tools/timesignaturetools/MetricalHierarchyInventory/MetricalHierarchyInventory
      tools/timesignaturetools/MetricalKernel/MetricalKernel

   --------

   .. toctree::
      :maxdepth: 1

      tools/timesignaturetools/duration_and_possible_denominators_to_time_signature
      tools/timesignaturetools/establish_metrical_hierarchy
      tools/timesignaturetools/fit_metrical_hierarchies_to_expr
      tools/timesignaturetools/make_gridded_test_rhythm

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/timesignaturetools/MetricalHierarchy/MetricalHierarchy
      tools/timesignaturetools/MetricalHierarchyInventory/MetricalHierarchyInventory
      tools/timesignaturetools/MetricalKernel/MetricalKernel

   Functions
   ---------

   .. toctree::

      tools/timesignaturetools/duration_and_possible_denominators_to_time_signature
      tools/timesignaturetools/establish_metrical_hierarchy
      tools/timesignaturetools/fit_metrical_hierarchies_to_expr
      tools/timesignaturetools/make_gridded_test_rhythm

:py:mod:`timespantools <abjad.tools.timespantools>`
===================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/timespantools/Timespan/Timespan
      tools/timespantools/TimespanInventory/TimespanInventory

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/timespantools/Timespan/Timespan
      tools/timespantools/TimespanInventory/TimespanInventory

:py:mod:`tonalitytools <abjad.tools.tonalitytools>`
===================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/tonalitytools/ChordClass/ChordClass
      tools/tonalitytools/ChordQualityIndicator/ChordQualityIndicator
      tools/tonalitytools/ExtentIndicator/ExtentIndicator
      tools/tonalitytools/InversionIndicator/InversionIndicator
      tools/tonalitytools/Mode/Mode
      tools/tonalitytools/OmissionIndicator/OmissionIndicator
      tools/tonalitytools/QualityIndicator/QualityIndicator
      tools/tonalitytools/Scale/Scale
      tools/tonalitytools/ScaleDegree/ScaleDegree
      tools/tonalitytools/SuspensionIndicator/SuspensionIndicator
      tools/tonalitytools/TonalFunction/TonalFunction

   --------

   .. toctree::
      :maxdepth: 1

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

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/tonalitytools/ChordClass/ChordClass
      tools/tonalitytools/ChordQualityIndicator/ChordQualityIndicator
      tools/tonalitytools/ExtentIndicator/ExtentIndicator
      tools/tonalitytools/InversionIndicator/InversionIndicator
      tools/tonalitytools/Mode/Mode
      tools/tonalitytools/OmissionIndicator/OmissionIndicator
      tools/tonalitytools/QualityIndicator/QualityIndicator
      tools/tonalitytools/Scale/Scale
      tools/tonalitytools/ScaleDegree/ScaleDegree
      tools/tonalitytools/SuspensionIndicator/SuspensionIndicator
      tools/tonalitytools/TonalFunction/TonalFunction

   Functions
   ---------

   .. toctree::

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

:py:mod:`tuplettools <abjad.tools.tuplettools>`
===============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/tuplettools/FixedDurationTuplet/FixedDurationTuplet
      tools/tuplettools/Tuplet/Tuplet

   --------

   .. toctree::
      :maxdepth: 1

      tools/tuplettools/change_augmented_tuplets_in_expr_to_diminished
      tools/tuplettools/change_diminished_tuplets_in_expr_to_augmented
      tools/tuplettools/change_fixed_duration_tuplets_in_expr_to_tuplets
      tools/tuplettools/change_tuplets_in_expr_to_fixed_duration_tuplets
      tools/tuplettools/fix_contents_of_tuplets_in_expr
      tools/tuplettools/fuse_tuplets
      tools/tuplettools/leaf_to_tuplet_with_n_notes_of_equal_written_duration
      tools/tuplettools/leaf_to_tuplet_with_ratio
      tools/tuplettools/make_tuplet_from_duration_and_ratio
      tools/tuplettools/make_tuplet_from_nonreduced_ratio_and_nonreduced_fraction
      tools/tuplettools/move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet
      tools/tuplettools/remove_trivial_tuplets_in_expr
      tools/tuplettools/scale_contents_of_tuplets_in_expr_by_multiplier
      tools/tuplettools/set_denominator_of_tuplets_in_expr_to_at_least

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/tuplettools/FixedDurationTuplet/FixedDurationTuplet
      tools/tuplettools/Tuplet/Tuplet

   Functions
   ---------

   .. toctree::

      tools/tuplettools/change_augmented_tuplets_in_expr_to_diminished
      tools/tuplettools/change_diminished_tuplets_in_expr_to_augmented
      tools/tuplettools/change_fixed_duration_tuplets_in_expr_to_tuplets
      tools/tuplettools/change_tuplets_in_expr_to_fixed_duration_tuplets
      tools/tuplettools/fix_contents_of_tuplets_in_expr
      tools/tuplettools/fuse_tuplets
      tools/tuplettools/leaf_to_tuplet_with_n_notes_of_equal_written_duration
      tools/tuplettools/leaf_to_tuplet_with_ratio
      tools/tuplettools/make_tuplet_from_duration_and_ratio
      tools/tuplettools/make_tuplet_from_nonreduced_ratio_and_nonreduced_fraction
      tools/tuplettools/move_prolation_of_tuplet_to_contents_of_tuplet_and_remove_tuplet
      tools/tuplettools/remove_trivial_tuplets_in_expr
      tools/tuplettools/scale_contents_of_tuplets_in_expr_by_multiplier
      tools/tuplettools/set_denominator_of_tuplets_in_expr_to_at_least

:py:mod:`voicetools <abjad.tools.voicetools>`
=============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/voicetools/Voice/Voice

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/voicetools/Voice/Voice

:py:mod:`wellformednesstools <abjad.tools.wellformednesstools>`
===============================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/wellformednesstools/Check/Check

   --------

   .. toctree::
      :maxdepth: 1

      tools/wellformednesstools/BeamedQuarterNoteCheck/BeamedQuarterNoteCheck
      tools/wellformednesstools/DiscontiguousSpannerCheck/DiscontiguousSpannerCheck
      tools/wellformednesstools/DuplicateIdCheck/DuplicateIdCheck
      tools/wellformednesstools/EmptyContainerCheck/EmptyContainerCheck
      tools/wellformednesstools/IntermarkedHairpinCheck/IntermarkedHairpinCheck
      tools/wellformednesstools/MisduratedMeasureCheck/MisduratedMeasureCheck
      tools/wellformednesstools/MisfilledMeasureCheck/MisfilledMeasureCheck
      tools/wellformednesstools/MispitchedTieCheck/MispitchedTieCheck
      tools/wellformednesstools/MisrepresentedFlagCheck/MisrepresentedFlagCheck
      tools/wellformednesstools/MissingParentCheck/MissingParentCheck
      tools/wellformednesstools/NestedMeasureCheck/NestedMeasureCheck
      tools/wellformednesstools/OverlappingBeamCheck/OverlappingBeamCheck
      tools/wellformednesstools/OverlappingGlissandoCheck/OverlappingGlissandoCheck
      tools/wellformednesstools/OverlappingOctavationCheck/OverlappingOctavationCheck
      tools/wellformednesstools/ShortHairpinCheck/ShortHairpinCheck

   --------

   .. toctree::
      :maxdepth: 1

      tools/wellformednesstools/is_well_formed_component
      tools/wellformednesstools/list_badly_formed_components_in_expr
      tools/wellformednesstools/list_checks
      tools/wellformednesstools/tabulate_well_formedness_violations_in_expr

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/wellformednesstools/Check/Check

   Concrete Classes
   ----------------

   .. toctree::

      tools/wellformednesstools/BeamedQuarterNoteCheck/BeamedQuarterNoteCheck
      tools/wellformednesstools/DiscontiguousSpannerCheck/DiscontiguousSpannerCheck
      tools/wellformednesstools/DuplicateIdCheck/DuplicateIdCheck
      tools/wellformednesstools/EmptyContainerCheck/EmptyContainerCheck
      tools/wellformednesstools/IntermarkedHairpinCheck/IntermarkedHairpinCheck
      tools/wellformednesstools/MisduratedMeasureCheck/MisduratedMeasureCheck
      tools/wellformednesstools/MisfilledMeasureCheck/MisfilledMeasureCheck
      tools/wellformednesstools/MispitchedTieCheck/MispitchedTieCheck
      tools/wellformednesstools/MisrepresentedFlagCheck/MisrepresentedFlagCheck
      tools/wellformednesstools/MissingParentCheck/MissingParentCheck
      tools/wellformednesstools/NestedMeasureCheck/NestedMeasureCheck
      tools/wellformednesstools/OverlappingBeamCheck/OverlappingBeamCheck
      tools/wellformednesstools/OverlappingGlissandoCheck/OverlappingGlissandoCheck
      tools/wellformednesstools/OverlappingOctavationCheck/OverlappingOctavationCheck
      tools/wellformednesstools/ShortHairpinCheck/ShortHairpinCheck

   Functions
   ---------

   .. toctree::

      tools/wellformednesstools/is_well_formed_component
      tools/wellformednesstools/list_badly_formed_components_in_expr
      tools/wellformednesstools/list_checks
      tools/wellformednesstools/tabulate_well_formedness_violations_in_expr

**************************
Demos and example packages
**************************

.. toctree::
   :maxdepth: 1


:py:mod:`desordre <abjad.demos.desordre>`
=========================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      demos/desordre/make_desordre_cell
      demos/desordre/make_desordre_lilypond_file
      demos/desordre/make_desordre_measure
      demos/desordre/make_desordre_pitches
      demos/desordre/make_desordre_score
      demos/desordre/make_desordre_staff

.. only:: latex

   Functions
   ---------

   .. toctree::

      demos/desordre/make_desordre_cell
      demos/desordre/make_desordre_lilypond_file
      demos/desordre/make_desordre_measure
      demos/desordre/make_desordre_pitches
      demos/desordre/make_desordre_score
      demos/desordre/make_desordre_staff

:py:mod:`ferneyhough <abjad.demos.ferneyhough>`
===============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      demos/ferneyhough/configure_lilypond_file
      demos/ferneyhough/configure_score
      demos/ferneyhough/make_lilypond_file
      demos/ferneyhough/make_nested_tuplet
      demos/ferneyhough/make_row_of_nested_tuplets
      demos/ferneyhough/make_rows_of_nested_tuplets

.. only:: latex

   Functions
   ---------

   .. toctree::

      demos/ferneyhough/configure_lilypond_file
      demos/ferneyhough/configure_score
      demos/ferneyhough/make_lilypond_file
      demos/ferneyhough/make_nested_tuplet
      demos/ferneyhough/make_row_of_nested_tuplets
      demos/ferneyhough/make_rows_of_nested_tuplets

:py:mod:`mozart <abjad.demos.mozart>`
=====================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      demos/mozart/choose_mozart_measures
      demos/mozart/make_mozart_lilypond_file
      demos/mozart/make_mozart_measure
      demos/mozart/make_mozart_measure_corpus
      demos/mozart/make_mozart_score

.. only:: latex

   Functions
   ---------

   .. toctree::

      demos/mozart/choose_mozart_measures
      demos/mozart/make_mozart_lilypond_file
      demos/mozart/make_mozart_measure
      demos/mozart/make_mozart_measure_corpus
      demos/mozart/make_mozart_score

:py:mod:`part <abjad.demos.part>`
=================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      demos/part/PartCantusScoreTemplate/PartCantusScoreTemplate

   --------

   .. toctree::
      :maxdepth: 1

      demos/part/add_bell_music_to_score
      demos/part/add_string_music_to_score
      demos/part/apply_bowing_marks
      demos/part/apply_dynamic_marks
      demos/part/apply_expressive_marks
      demos/part/apply_final_bar_lines
      demos/part/apply_page_breaks
      demos/part/apply_rehearsal_marks
      demos/part/configure_lilypond_file
      demos/part/configure_score
      demos/part/create_pitch_contour_reservoir
      demos/part/durate_pitch_contour_reservoir
      demos/part/edit_bass_voice
      demos/part/edit_cello_voice
      demos/part/edit_first_violin_voice
      demos/part/edit_second_violin_voice
      demos/part/edit_viola_voice
      demos/part/make_part_lilypond_file
      demos/part/shadow_pitch_contour_reservoir

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      demos/part/PartCantusScoreTemplate/PartCantusScoreTemplate

   Functions
   ---------

   .. toctree::

      demos/part/add_bell_music_to_score
      demos/part/add_string_music_to_score
      demos/part/apply_bowing_marks
      demos/part/apply_dynamic_marks
      demos/part/apply_expressive_marks
      demos/part/apply_final_bar_lines
      demos/part/apply_page_breaks
      demos/part/apply_rehearsal_marks
      demos/part/configure_lilypond_file
      demos/part/configure_score
      demos/part/create_pitch_contour_reservoir
      demos/part/durate_pitch_contour_reservoir
      demos/part/edit_bass_voice
      demos/part/edit_cello_voice
      demos/part/edit_first_violin_voice
      demos/part/edit_second_violin_voice
      demos/part/edit_viola_voice
      demos/part/make_part_lilypond_file
      demos/part/shadow_pitch_contour_reservoir

***********************
Abjad internal packages
***********************

.. toctree::
   :maxdepth: 1


:py:mod:`abctools <abjad.tools.abctools>`
=========================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/abctools/AbjadObject/AbjadObject
      tools/abctools/AttributeEqualityAbjadObject/AttributeEqualityAbjadObject
      tools/abctools/ContextManager/ContextManager
      tools/abctools/ImmutableAbjadObject/ImmutableAbjadObject
      tools/abctools/Maker/Maker
      tools/abctools/Parser/Parser
      tools/abctools/SortableAttributeEqualityAbjadObject/SortableAttributeEqualityAbjadObject

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/abctools/AbjadObject/AbjadObject
      tools/abctools/AttributeEqualityAbjadObject/AttributeEqualityAbjadObject
      tools/abctools/ContextManager/ContextManager
      tools/abctools/ImmutableAbjadObject/ImmutableAbjadObject
      tools/abctools/Maker/Maker
      tools/abctools/Parser/Parser
      tools/abctools/SortableAttributeEqualityAbjadObject/SortableAttributeEqualityAbjadObject

:py:mod:`abjadbooktools <abjad.tools.abjadbooktools>`
=====================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/abjadbooktools/OutputFormat/OutputFormat

   --------

   .. toctree::
      :maxdepth: 1

      tools/abjadbooktools/AbjadBookProcessor/AbjadBookProcessor
      tools/abjadbooktools/AbjadBookScript/AbjadBookScript
      tools/abjadbooktools/CodeBlock/CodeBlock
      tools/abjadbooktools/HTMLOutputFormat/HTMLOutputFormat
      tools/abjadbooktools/LaTeXOutputFormat/LaTeXOutputFormat
      tools/abjadbooktools/ReSTOutputFormat/ReSTOutputFormat

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/abjadbooktools/OutputFormat/OutputFormat

   Concrete Classes
   ----------------

   .. toctree::

      tools/abjadbooktools/AbjadBookProcessor/AbjadBookProcessor
      tools/abjadbooktools/AbjadBookScript/AbjadBookScript
      tools/abjadbooktools/CodeBlock/CodeBlock
      tools/abjadbooktools/HTMLOutputFormat/HTMLOutputFormat
      tools/abjadbooktools/LaTeXOutputFormat/LaTeXOutputFormat
      tools/abjadbooktools/ReSTOutputFormat/ReSTOutputFormat

:py:mod:`configurationtools <abjad.tools.configurationtools>`
=============================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/configurationtools/Configuration/Configuration

   --------

   .. toctree::
      :maxdepth: 1

      tools/configurationtools/AbjadConfiguration/AbjadConfiguration

   --------

   .. toctree::
      :maxdepth: 1

      tools/configurationtools/get_abjad_revision_string
      tools/configurationtools/get_abjad_startup_string
      tools/configurationtools/get_abjad_version_string
      tools/configurationtools/get_lilypond_minimum_version_string
      tools/configurationtools/get_lilypond_version_string
      tools/configurationtools/get_python_version_string
      tools/configurationtools/get_tab_width
      tools/configurationtools/get_text_editor
      tools/configurationtools/list_abjad_environment_variables
      tools/configurationtools/list_package_dependency_versions
      tools/configurationtools/read_abjad_user_config_file

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/configurationtools/Configuration/Configuration

   Concrete Classes
   ----------------

   .. toctree::

      tools/configurationtools/AbjadConfiguration/AbjadConfiguration

   Functions
   ---------

   .. toctree::

      tools/configurationtools/get_abjad_revision_string
      tools/configurationtools/get_abjad_startup_string
      tools/configurationtools/get_abjad_version_string
      tools/configurationtools/get_lilypond_minimum_version_string
      tools/configurationtools/get_lilypond_version_string
      tools/configurationtools/get_python_version_string
      tools/configurationtools/get_tab_width
      tools/configurationtools/get_text_editor
      tools/configurationtools/list_abjad_environment_variables
      tools/configurationtools/list_package_dependency_versions
      tools/configurationtools/read_abjad_user_config_file

:py:mod:`datastructuretools <abjad.tools.datastructuretools>`
=============================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/datastructuretools/BreakPointFunction/BreakPointFunction
      tools/datastructuretools/Digraph/Digraph
      tools/datastructuretools/ImmutableDictionary/ImmutableDictionary
      tools/datastructuretools/ObjectInventory/ObjectInventory
      tools/datastructuretools/OrdinalConstant/OrdinalConstant
      tools/datastructuretools/SortedCollection/SortedCollection
      tools/datastructuretools/TreeContainer/TreeContainer
      tools/datastructuretools/TreeNode/TreeNode

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/datastructuretools/BreakPointFunction/BreakPointFunction
      tools/datastructuretools/Digraph/Digraph
      tools/datastructuretools/ImmutableDictionary/ImmutableDictionary
      tools/datastructuretools/ObjectInventory/ObjectInventory
      tools/datastructuretools/OrdinalConstant/OrdinalConstant
      tools/datastructuretools/SortedCollection/SortedCollection
      tools/datastructuretools/TreeContainer/TreeContainer
      tools/datastructuretools/TreeNode/TreeNode

:py:mod:`decoratortools <abjad.tools.decoratortools>`
=====================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/decoratortools/requires

.. only:: latex

   Functions
   ---------

   .. toctree::

      tools/decoratortools/requires

:py:mod:`developerscripttools <abjad.tools.developerscripttools>`
=================================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/developerscripttools/DeveloperScript/DeveloperScript
      tools/developerscripttools/DirectoryScript/DirectoryScript

   --------

   .. toctree::
      :maxdepth: 1

      tools/developerscripttools/AbjDevScript/AbjDevScript
      tools/developerscripttools/AbjGrepScript/AbjGrepScript
      tools/developerscripttools/AbjUpScript/AbjUpScript
      tools/developerscripttools/BuildApiScript/BuildApiScript
      tools/developerscripttools/CleanScript/CleanScript
      tools/developerscripttools/CountLinewidthsScript/CountLinewidthsScript
      tools/developerscripttools/CountToolsScript/CountToolsScript
      tools/developerscripttools/MakeNewClassTemplateScript/MakeNewClassTemplateScript
      tools/developerscripttools/MakeNewFunctionTemplateScript/MakeNewFunctionTemplateScript
      tools/developerscripttools/PyTestScript/PyTestScript
      tools/developerscripttools/RenameModulesScript/RenameModulesScript
      tools/developerscripttools/ReplaceInFilesScript/ReplaceInFilesScript
      tools/developerscripttools/ReplacePromptsScript/ReplacePromptsScript
      tools/developerscripttools/RunDoctestsScript/RunDoctestsScript
      tools/developerscripttools/SvnAddAllScript/SvnAddAllScript
      tools/developerscripttools/SvnCommitScript/SvnCommitScript
      tools/developerscripttools/SvnMessageScript/SvnMessageScript
      tools/developerscripttools/SvnUpdateScript/SvnUpdateScript
      tools/developerscripttools/TestAndRebuildScript/TestAndRebuildScript

   --------

   .. toctree::
      :maxdepth: 1

      tools/developerscripttools/get_developer_script_classes
      tools/developerscripttools/run_abjadbook
      tools/developerscripttools/run_abjdev

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/developerscripttools/DeveloperScript/DeveloperScript
      tools/developerscripttools/DirectoryScript/DirectoryScript

   Concrete Classes
   ----------------

   .. toctree::

      tools/developerscripttools/AbjDevScript/AbjDevScript
      tools/developerscripttools/AbjGrepScript/AbjGrepScript
      tools/developerscripttools/AbjUpScript/AbjUpScript
      tools/developerscripttools/BuildApiScript/BuildApiScript
      tools/developerscripttools/CleanScript/CleanScript
      tools/developerscripttools/CountLinewidthsScript/CountLinewidthsScript
      tools/developerscripttools/CountToolsScript/CountToolsScript
      tools/developerscripttools/MakeNewClassTemplateScript/MakeNewClassTemplateScript
      tools/developerscripttools/MakeNewFunctionTemplateScript/MakeNewFunctionTemplateScript
      tools/developerscripttools/PyTestScript/PyTestScript
      tools/developerscripttools/RenameModulesScript/RenameModulesScript
      tools/developerscripttools/ReplaceInFilesScript/ReplaceInFilesScript
      tools/developerscripttools/ReplacePromptsScript/ReplacePromptsScript
      tools/developerscripttools/RunDoctestsScript/RunDoctestsScript
      tools/developerscripttools/SvnAddAllScript/SvnAddAllScript
      tools/developerscripttools/SvnCommitScript/SvnCommitScript
      tools/developerscripttools/SvnMessageScript/SvnMessageScript
      tools/developerscripttools/SvnUpdateScript/SvnUpdateScript
      tools/developerscripttools/TestAndRebuildScript/TestAndRebuildScript

   Functions
   ---------

   .. toctree::

      tools/developerscripttools/get_developer_script_classes
      tools/developerscripttools/run_abjadbook
      tools/developerscripttools/run_abjdev

:py:mod:`documentationtools <abjad.tools.documentationtools>`
=============================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/documentationtools/Documenter/Documenter
      tools/documentationtools/GraphvizObject/GraphvizObject
      tools/documentationtools/ReSTDirective/ReSTDirective
      tools/documentationtools/ToolsPackageDocumenter/ToolsPackageDocumenter

   --------

   .. toctree::
      :maxdepth: 1

      tools/documentationtools/APICrawler/APICrawler
      tools/documentationtools/AbjadAPIGenerator/AbjadAPIGenerator
      tools/documentationtools/ClassCrawler/ClassCrawler
      tools/documentationtools/ClassDocumenter/ClassDocumenter
      tools/documentationtools/FunctionCrawler/FunctionCrawler
      tools/documentationtools/FunctionDocumenter/FunctionDocumenter
      tools/documentationtools/GraphvizEdge/GraphvizEdge
      tools/documentationtools/GraphvizGraph/GraphvizGraph
      tools/documentationtools/GraphvizNode/GraphvizNode
      tools/documentationtools/GraphvizSubgraph/GraphvizSubgraph
      tools/documentationtools/InheritanceGraph/InheritanceGraph
      tools/documentationtools/ModuleCrawler/ModuleCrawler
      tools/documentationtools/Pipe/Pipe
      tools/documentationtools/ReSTAutodocDirective/ReSTAutodocDirective
      tools/documentationtools/ReSTDocument/ReSTDocument
      tools/documentationtools/ReSTHeading/ReSTHeading
      tools/documentationtools/ReSTHorizontalRule/ReSTHorizontalRule
      tools/documentationtools/ReSTInheritanceDiagram/ReSTInheritanceDiagram
      tools/documentationtools/ReSTLineageDirective/ReSTLineageDirective
      tools/documentationtools/ReSTOnlyDirective/ReSTOnlyDirective
      tools/documentationtools/ReSTParagraph/ReSTParagraph
      tools/documentationtools/ReSTTOCDirective/ReSTTOCDirective
      tools/documentationtools/ReSTTOCItem/ReSTTOCItem

   --------

   .. toctree::
      :maxdepth: 1

      tools/documentationtools/compare_images
      tools/documentationtools/make_ligeti_example_lilypond_file
      tools/documentationtools/make_reference_manual_graphviz_graph
      tools/documentationtools/make_reference_manual_lilypond_file
      tools/documentationtools/make_text_alignment_example_lilypond_file

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/documentationtools/Documenter/Documenter
      tools/documentationtools/GraphvizObject/GraphvizObject
      tools/documentationtools/ReSTDirective/ReSTDirective
      tools/documentationtools/ToolsPackageDocumenter/ToolsPackageDocumenter

   Concrete Classes
   ----------------

   .. toctree::

      tools/documentationtools/APICrawler/APICrawler
      tools/documentationtools/AbjadAPIGenerator/AbjadAPIGenerator
      tools/documentationtools/ClassCrawler/ClassCrawler
      tools/documentationtools/ClassDocumenter/ClassDocumenter
      tools/documentationtools/FunctionCrawler/FunctionCrawler
      tools/documentationtools/FunctionDocumenter/FunctionDocumenter
      tools/documentationtools/GraphvizEdge/GraphvizEdge
      tools/documentationtools/GraphvizGraph/GraphvizGraph
      tools/documentationtools/GraphvizNode/GraphvizNode
      tools/documentationtools/GraphvizSubgraph/GraphvizSubgraph
      tools/documentationtools/InheritanceGraph/InheritanceGraph
      tools/documentationtools/ModuleCrawler/ModuleCrawler
      tools/documentationtools/Pipe/Pipe
      tools/documentationtools/ReSTAutodocDirective/ReSTAutodocDirective
      tools/documentationtools/ReSTDocument/ReSTDocument
      tools/documentationtools/ReSTHeading/ReSTHeading
      tools/documentationtools/ReSTHorizontalRule/ReSTHorizontalRule
      tools/documentationtools/ReSTInheritanceDiagram/ReSTInheritanceDiagram
      tools/documentationtools/ReSTLineageDirective/ReSTLineageDirective
      tools/documentationtools/ReSTOnlyDirective/ReSTOnlyDirective
      tools/documentationtools/ReSTParagraph/ReSTParagraph
      tools/documentationtools/ReSTTOCDirective/ReSTTOCDirective
      tools/documentationtools/ReSTTOCItem/ReSTTOCItem

   Functions
   ---------

   .. toctree::

      tools/documentationtools/compare_images
      tools/documentationtools/make_ligeti_example_lilypond_file
      tools/documentationtools/make_reference_manual_graphviz_graph
      tools/documentationtools/make_reference_manual_lilypond_file
      tools/documentationtools/make_text_alignment_example_lilypond_file

:py:mod:`exceptiontools <abjad.tools.exceptiontools>`
=====================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/exceptiontools/AssignabilityError
      tools/exceptiontools/ClefError
      tools/exceptiontools/ContainmentError
      tools/exceptiontools/ContextContainmentError
      tools/exceptiontools/ContiguityError
      tools/exceptiontools/CyclicNodeError
      tools/exceptiontools/DurationError
      tools/exceptiontools/ExtraMarkError
      tools/exceptiontools/ExtraNamedComponentError
      tools/exceptiontools/ExtraNoteHeadError
      tools/exceptiontools/ExtraPitchError
      tools/exceptiontools/ExtraSpannerError
      tools/exceptiontools/GraceContainerError
      tools/exceptiontools/ImpreciseTempoError
      tools/exceptiontools/InputSpecificationError
      tools/exceptiontools/InstrumentError
      tools/exceptiontools/IntervalError
      tools/exceptiontools/LilyPondParserError
      tools/exceptiontools/LineBreakError
      tools/exceptiontools/MarkError
      tools/exceptiontools/MeasureContiguityError
      tools/exceptiontools/MeasureError
      tools/exceptiontools/MissingComponentError
      tools/exceptiontools/MissingInstrumentError
      tools/exceptiontools/MissingMarkError
      tools/exceptiontools/MissingMeasureError
      tools/exceptiontools/MissingNamedComponentError
      tools/exceptiontools/MissingNoteHeadError
      tools/exceptiontools/MissingPitchError
      tools/exceptiontools/MissingSpannerError
      tools/exceptiontools/MissingTempoError
      tools/exceptiontools/MusicContentsError
      tools/exceptiontools/NoteHeadError
      tools/exceptiontools/OverfullContainerError
      tools/exceptiontools/ParallelError
      tools/exceptiontools/PartitionError
      tools/exceptiontools/PitchError
      tools/exceptiontools/SchemeParserFinishedException
      tools/exceptiontools/SpacingError
      tools/exceptiontools/SpannerError
      tools/exceptiontools/SpannerPopulationError
      tools/exceptiontools/StaffContainmentError
      tools/exceptiontools/TempoError
      tools/exceptiontools/TieChainError
      tools/exceptiontools/TimeSignatureAssignmentError
      tools/exceptiontools/TimeSignatureError
      tools/exceptiontools/TonalHarmonyError
      tools/exceptiontools/TupletError
      tools/exceptiontools/TupletFuseError
      tools/exceptiontools/TypographicWhitespaceError
      tools/exceptiontools/UnboundedTimeIntervalError
      tools/exceptiontools/UndefinedSpacingError
      tools/exceptiontools/UnderfullContainerError
      tools/exceptiontools/VoiceContainmentError

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/exceptiontools/AssignabilityError
      tools/exceptiontools/ClefError
      tools/exceptiontools/ContainmentError
      tools/exceptiontools/ContextContainmentError
      tools/exceptiontools/ContiguityError
      tools/exceptiontools/CyclicNodeError
      tools/exceptiontools/DurationError
      tools/exceptiontools/ExtraMarkError
      tools/exceptiontools/ExtraNamedComponentError
      tools/exceptiontools/ExtraNoteHeadError
      tools/exceptiontools/ExtraPitchError
      tools/exceptiontools/ExtraSpannerError
      tools/exceptiontools/GraceContainerError
      tools/exceptiontools/ImpreciseTempoError
      tools/exceptiontools/InputSpecificationError
      tools/exceptiontools/InstrumentError
      tools/exceptiontools/IntervalError
      tools/exceptiontools/LilyPondParserError
      tools/exceptiontools/LineBreakError
      tools/exceptiontools/MarkError
      tools/exceptiontools/MeasureContiguityError
      tools/exceptiontools/MeasureError
      tools/exceptiontools/MissingComponentError
      tools/exceptiontools/MissingInstrumentError
      tools/exceptiontools/MissingMarkError
      tools/exceptiontools/MissingMeasureError
      tools/exceptiontools/MissingNamedComponentError
      tools/exceptiontools/MissingNoteHeadError
      tools/exceptiontools/MissingPitchError
      tools/exceptiontools/MissingSpannerError
      tools/exceptiontools/MissingTempoError
      tools/exceptiontools/MusicContentsError
      tools/exceptiontools/NoteHeadError
      tools/exceptiontools/OverfullContainerError
      tools/exceptiontools/ParallelError
      tools/exceptiontools/PartitionError
      tools/exceptiontools/PitchError
      tools/exceptiontools/SchemeParserFinishedException
      tools/exceptiontools/SpacingError
      tools/exceptiontools/SpannerError
      tools/exceptiontools/SpannerPopulationError
      tools/exceptiontools/StaffContainmentError
      tools/exceptiontools/TempoError
      tools/exceptiontools/TieChainError
      tools/exceptiontools/TimeSignatureAssignmentError
      tools/exceptiontools/TimeSignatureError
      tools/exceptiontools/TonalHarmonyError
      tools/exceptiontools/TupletError
      tools/exceptiontools/TupletFuseError
      tools/exceptiontools/TypographicWhitespaceError
      tools/exceptiontools/UnboundedTimeIntervalError
      tools/exceptiontools/UndefinedSpacingError
      tools/exceptiontools/UnderfullContainerError
      tools/exceptiontools/VoiceContainmentError

:py:mod:`formattools <abjad.tools.formattools>`
===============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/formattools/get_all_format_contributions
      tools/formattools/get_all_mark_format_contributions
      tools/formattools/get_articulation_format_contributions
      tools/formattools/get_comment_format_contributions_for_slot
      tools/formattools/get_context_mark_format_contributions_for_slot
      tools/formattools/get_context_mark_format_pieces
      tools/formattools/get_context_setting_format_contributions
      tools/formattools/get_grob_override_format_contributions
      tools/formattools/get_grob_revert_format_contributions
      tools/formattools/get_lilypond_command_mark_format_contributions_for_slot
      tools/formattools/get_markup_format_contributions
      tools/formattools/get_spanner_format_contributions
      tools/formattools/get_stem_tremolo_format_contributions
      tools/formattools/is_formattable_context_mark_for_component
      tools/formattools/report_component_format_contributions
      tools/formattools/report_spanner_format_contributions

.. only:: latex

   Functions
   ---------

   .. toctree::

      tools/formattools/get_all_format_contributions
      tools/formattools/get_all_mark_format_contributions
      tools/formattools/get_articulation_format_contributions
      tools/formattools/get_comment_format_contributions_for_slot
      tools/formattools/get_context_mark_format_contributions_for_slot
      tools/formattools/get_context_mark_format_pieces
      tools/formattools/get_context_setting_format_contributions
      tools/formattools/get_grob_override_format_contributions
      tools/formattools/get_grob_revert_format_contributions
      tools/formattools/get_lilypond_command_mark_format_contributions_for_slot
      tools/formattools/get_markup_format_contributions
      tools/formattools/get_spanner_format_contributions
      tools/formattools/get_stem_tremolo_format_contributions
      tools/formattools/is_formattable_context_mark_for_component
      tools/formattools/report_component_format_contributions
      tools/formattools/report_spanner_format_contributions

:py:mod:`importtools <abjad.tools.importtools>`
===============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/importtools/get_public_function_names_in_module
      tools/importtools/import_contents_of_public_packages_in_path_into_namespace
      tools/importtools/import_public_names_from_filesystem_path_into_namespace
      tools/importtools/import_structured_package
      tools/importtools/remove_modules_from_namespace

.. only:: latex

   Functions
   ---------

   .. toctree::

      tools/importtools/get_public_function_names_in_module
      tools/importtools/import_contents_of_public_packages_in_path_into_namespace
      tools/importtools/import_public_names_from_filesystem_path_into_namespace
      tools/importtools/import_structured_package
      tools/importtools/remove_modules_from_namespace

:py:mod:`introspectiontools <abjad.tools.introspectiontools>`
=============================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/introspectiontools/class_to_tools_package_qualified_class_name
      tools/introspectiontools/get_current_function_name

.. only:: latex

   Functions
   ---------

   .. toctree::

      tools/introspectiontools/class_to_tools_package_qualified_class_name
      tools/introspectiontools/get_current_function_name

:py:mod:`lilypondparsertools <abjad.tools.lilypondparsertools>`
===============================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/lilypondparsertools/Music/Music
      tools/lilypondparsertools/SimultaneousMusic/SimultaneousMusic

   --------

   .. toctree::
      :maxdepth: 1

      tools/lilypondparsertools/ContextSpeccedMusic/ContextSpeccedMusic
      tools/lilypondparsertools/GuileProxy/GuileProxy
      tools/lilypondparsertools/LilyPondDuration/LilyPondDuration
      tools/lilypondparsertools/LilyPondEvent/LilyPondEvent
      tools/lilypondparsertools/LilyPondFraction/LilyPondFraction
      tools/lilypondparsertools/LilyPondLexicalDefinition/LilyPondLexicalDefinition
      tools/lilypondparsertools/LilyPondParser/LilyPondParser
      tools/lilypondparsertools/LilyPondSyntacticalDefinition/LilyPondSyntacticalDefinition
      tools/lilypondparsertools/ReducedLyParser/ReducedLyParser
      tools/lilypondparsertools/SchemeParser/SchemeParser
      tools/lilypondparsertools/SequentialMusic/SequentialMusic
      tools/lilypondparsertools/SyntaxNode/SyntaxNode

   --------

   .. toctree::
      :maxdepth: 1

      tools/lilypondparsertools/lilypond_enharmonic_transpose
      tools/lilypondparsertools/list_known_contexts
      tools/lilypondparsertools/list_known_grobs
      tools/lilypondparsertools/list_known_languages
      tools/lilypondparsertools/list_known_markup_functions
      tools/lilypondparsertools/list_known_music_functions
      tools/lilypondparsertools/parse_reduced_ly_syntax

.. only:: latex

   Abstract Classes
   ----------------

   .. toctree::

      tools/lilypondparsertools/Music/Music
      tools/lilypondparsertools/SimultaneousMusic/SimultaneousMusic

   Concrete Classes
   ----------------

   .. toctree::

      tools/lilypondparsertools/ContextSpeccedMusic/ContextSpeccedMusic
      tools/lilypondparsertools/GuileProxy/GuileProxy
      tools/lilypondparsertools/LilyPondDuration/LilyPondDuration
      tools/lilypondparsertools/LilyPondEvent/LilyPondEvent
      tools/lilypondparsertools/LilyPondFraction/LilyPondFraction
      tools/lilypondparsertools/LilyPondLexicalDefinition/LilyPondLexicalDefinition
      tools/lilypondparsertools/LilyPondParser/LilyPondParser
      tools/lilypondparsertools/LilyPondSyntacticalDefinition/LilyPondSyntacticalDefinition
      tools/lilypondparsertools/ReducedLyParser/ReducedLyParser
      tools/lilypondparsertools/SchemeParser/SchemeParser
      tools/lilypondparsertools/SequentialMusic/SequentialMusic
      tools/lilypondparsertools/SyntaxNode/SyntaxNode

   Functions
   ---------

   .. toctree::

      tools/lilypondparsertools/lilypond_enharmonic_transpose
      tools/lilypondparsertools/list_known_contexts
      tools/lilypondparsertools/list_known_grobs
      tools/lilypondparsertools/list_known_languages
      tools/lilypondparsertools/list_known_markup_functions
      tools/lilypondparsertools/list_known_music_functions
      tools/lilypondparsertools/parse_reduced_ly_syntax

:py:mod:`lilypondproxytools <abjad.tools.lilypondproxytools>`
=============================================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/lilypondproxytools/LilyPondComponentPlugIn/LilyPondComponentPlugIn
      tools/lilypondproxytools/LilyPondContextProxy/LilyPondContextProxy
      tools/lilypondproxytools/LilyPondContextSettingComponentPlugIn/LilyPondContextSettingComponentPlugIn
      tools/lilypondproxytools/LilyPondGrobOverrideComponentPlugIn/LilyPondGrobOverrideComponentPlugIn
      tools/lilypondproxytools/LilyPondGrobProxy/LilyPondGrobProxy
      tools/lilypondproxytools/LilyPondGrobProxyContextWrapper/LilyPondGrobProxyContextWrapper
      tools/lilypondproxytools/LilyPondObjectProxy/LilyPondObjectProxy
      tools/lilypondproxytools/LilyPondTweakReservoir/LilyPondTweakReservoir

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/lilypondproxytools/LilyPondComponentPlugIn/LilyPondComponentPlugIn
      tools/lilypondproxytools/LilyPondContextProxy/LilyPondContextProxy
      tools/lilypondproxytools/LilyPondContextSettingComponentPlugIn/LilyPondContextSettingComponentPlugIn
      tools/lilypondproxytools/LilyPondGrobOverrideComponentPlugIn/LilyPondGrobOverrideComponentPlugIn
      tools/lilypondproxytools/LilyPondGrobProxy/LilyPondGrobProxy
      tools/lilypondproxytools/LilyPondGrobProxyContextWrapper/LilyPondGrobProxyContextWrapper
      tools/lilypondproxytools/LilyPondObjectProxy/LilyPondObjectProxy
      tools/lilypondproxytools/LilyPondTweakReservoir/LilyPondTweakReservoir

:py:mod:`offsettools <abjad.tools.offsettools>`
===============================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/offsettools/update_offset_values_of_component
      tools/offsettools/update_offset_values_of_component_in_seconds

.. only:: latex

   Functions
   ---------

   .. toctree::

      tools/offsettools/update_offset_values_of_component
      tools/offsettools/update_offset_values_of_component_in_seconds

:py:mod:`testtools <abjad.tools.testtools>`
===========================================

.. only:: html

   .. toctree::
      :maxdepth: 1

      tools/testtools/BenchmarkScoreMaker/BenchmarkScoreMaker

   --------

   .. toctree::
      :maxdepth: 1

      tools/testtools/apply_additional_layout
      tools/testtools/read_test_output
      tools/testtools/write_test_output

.. only:: latex

   Concrete Classes
   ----------------

   .. toctree::

      tools/testtools/BenchmarkScoreMaker/BenchmarkScoreMaker

   Functions
   ---------

   .. toctree::

      tools/testtools/apply_additional_layout
      tools/testtools/read_test_output
      tools/testtools/write_test_output
