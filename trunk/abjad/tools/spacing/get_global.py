from abjad.component.component import _Component


def get_global(component):
   '''Return ``global_spacing`` of effective score of ``compoment``.
      If no explicit effective score, return ``None``.'''

   assert isinstance(component, _Component)
   effective_score = component.score.effective
   if effective_score is not None:
      return effective_score.global_spacing
