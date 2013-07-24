spannertools
============

.. automodule:: abjad.tools.spannertools

Abstract classes
----------------

.. autosummary::

   ~abjad.tools.spannertools.DirectedSpanner.DirectedSpanner.DirectedSpanner
   ~abjad.tools.spannertools.Spanner.Spanner.Spanner

Concrete classes
----------------

.. autosummary::

   ~abjad.tools.spannertools.BeamSpanner.BeamSpanner.BeamSpanner
   ~abjad.tools.spannertools.BracketSpanner.BracketSpanner.BracketSpanner
   ~abjad.tools.spannertools.ComplexBeamSpanner.ComplexBeamSpanner.ComplexBeamSpanner
   ~abjad.tools.spannertools.ComplexGlissandoSpanner.ComplexGlissandoSpanner.ComplexGlissandoSpanner
   ~abjad.tools.spannertools.CrescendoSpanner.CrescendoSpanner.CrescendoSpanner
   ~abjad.tools.spannertools.DecrescendoSpanner.DecrescendoSpanner.DecrescendoSpanner
   ~abjad.tools.spannertools.DuratedComplexBeamSpanner.DuratedComplexBeamSpanner.DuratedComplexBeamSpanner
   ~abjad.tools.spannertools.DynamicTextSpanner.DynamicTextSpanner.DynamicTextSpanner
   ~abjad.tools.spannertools.GlissandoSpanner.GlissandoSpanner.GlissandoSpanner
   ~abjad.tools.spannertools.HairpinSpanner.HairpinSpanner.HairpinSpanner
   ~abjad.tools.spannertools.HiddenStaffSpanner.HiddenStaffSpanner.HiddenStaffSpanner
   ~abjad.tools.spannertools.HorizontalBracketSpanner.HorizontalBracketSpanner.HorizontalBracketSpanner
   ~abjad.tools.spannertools.MeasuredComplexBeamSpanner.MeasuredComplexBeamSpanner.MeasuredComplexBeamSpanner
   ~abjad.tools.spannertools.MultipartBeamSpanner.MultipartBeamSpanner.MultipartBeamSpanner
   ~abjad.tools.spannertools.OctavationSpanner.OctavationSpanner.OctavationSpanner
   ~abjad.tools.spannertools.PhrasingSlurSpanner.PhrasingSlurSpanner.PhrasingSlurSpanner
   ~abjad.tools.spannertools.PianoPedalSpanner.PianoPedalSpanner.PianoPedalSpanner
   ~abjad.tools.spannertools.SlurSpanner.SlurSpanner.SlurSpanner
   ~abjad.tools.spannertools.StaffLinesSpanner.StaffLinesSpanner.StaffLinesSpanner
   ~abjad.tools.spannertools.TextScriptSpanner.TextScriptSpanner.TextScriptSpanner
   ~abjad.tools.spannertools.TextSpanner.TextSpanner.TextSpanner
   ~abjad.tools.spannertools.TieSpanner.TieSpanner.TieSpanner
   ~abjad.tools.spannertools.TrillSpanner.TrillSpanner.TrillSpanner

Functions
---------

.. autosummary::

   ~abjad.tools.spannertools.apply_octavation_spanner_to_pitched_components.apply_octavation_spanner_to_pitched_components
   ~abjad.tools.spannertools.detach_spanners_attached_to_component.detach_spanners_attached_to_component
   ~abjad.tools.spannertools.detach_spanners_attached_to_components_in_expr.detach_spanners_attached_to_components_in_expr
   ~abjad.tools.spannertools.find_index_of_spanner_component_at_score_offset.find_index_of_spanner_component_at_score_offset
   ~abjad.tools.spannertools.find_spanner_component_starting_at_exactly_score_offset.find_spanner_component_starting_at_exactly_score_offset
   ~abjad.tools.spannertools.fracture_spanners_attached_to_component.fracture_spanners_attached_to_component
   ~abjad.tools.spannertools.fracture_spanners_that_cross_components.fracture_spanners_that_cross_components
   ~abjad.tools.spannertools.get_nth_leaf_in_spanner.get_nth_leaf_in_spanner
   ~abjad.tools.spannertools.get_spanners_attached_to_any_improper_child_of_component.get_spanners_attached_to_any_improper_child_of_component
   ~abjad.tools.spannertools.get_spanners_attached_to_any_improper_parent_of_component.get_spanners_attached_to_any_improper_parent_of_component
   ~abjad.tools.spannertools.get_spanners_attached_to_any_proper_child_of_component.get_spanners_attached_to_any_proper_child_of_component
   ~abjad.tools.spannertools.get_spanners_attached_to_any_proper_parent_of_component.get_spanners_attached_to_any_proper_parent_of_component
   ~abjad.tools.spannertools.get_spanners_attached_to_component.get_spanners_attached_to_component
   ~abjad.tools.spannertools.get_spanners_contained_by_components.get_spanners_contained_by_components
   ~abjad.tools.spannertools.get_spanners_covered_by_components.get_spanners_covered_by_components
   ~abjad.tools.spannertools.get_spanners_on_components_or_component_children.get_spanners_on_components_or_component_children
   ~abjad.tools.spannertools.get_spanners_that_cross_components.get_spanners_that_cross_components
   ~abjad.tools.spannertools.get_spanners_that_dominate_component_pair.get_spanners_that_dominate_component_pair
   ~abjad.tools.spannertools.get_spanners_that_dominate_components.get_spanners_that_dominate_components
   ~abjad.tools.spannertools.get_spanners_that_dominate_container_components_from_to.get_spanners_that_dominate_container_components_from_to
   ~abjad.tools.spannertools.get_the_only_spanner_attached_to_any_improper_parent_of_component.get_the_only_spanner_attached_to_any_improper_parent_of_component
   ~abjad.tools.spannertools.get_the_only_spanner_attached_to_component.get_the_only_spanner_attached_to_component
   ~abjad.tools.spannertools.is_component_with_spanner_attached.is_component_with_spanner_attached
   ~abjad.tools.spannertools.iterate_components_in_spanner.iterate_components_in_spanner
   ~abjad.tools.spannertools.make_covered_spanner_schema.make_covered_spanner_schema
   ~abjad.tools.spannertools.make_dynamic_spanner_below_with_nib_at_right.make_dynamic_spanner_below_with_nib_at_right
   ~abjad.tools.spannertools.make_solid_text_spanner_above_with_nib_at_right.make_solid_text_spanner_above_with_nib_at_right
   ~abjad.tools.spannertools.make_solid_text_spanner_below_with_nib_at_right.make_solid_text_spanner_below_with_nib_at_right
   ~abjad.tools.spannertools.make_spanner_schema.make_spanner_schema
   ~abjad.tools.spannertools.move_spanners_from_component_to_children_of_component.move_spanners_from_component_to_children_of_component
   ~abjad.tools.spannertools.withdraw_components_from_spanners_covered_by_components.withdraw_components_from_spanners_covered_by_components
