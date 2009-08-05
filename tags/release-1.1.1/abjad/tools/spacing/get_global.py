from abjad.component.component import _Component


def get_global(component):
   '''Return ``global_spacing`` of explicit score of ``compoment``.
      If no explicit score, return ``None``.'''

   assert isinstance(component, _Component)
   explicit_score = component.score.explicit
   if explicit_score is not None:
      return explicit_score.global_spacing
