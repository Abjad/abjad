from abjad.tools import iterate
from abjad.measure.rigid.measure import RigidMeasure
from make_underfull_spacer_skip import make_underfull_spacer_skip


def remedy_underfull_measures(expr):
   r'''.. versionadded:: 1.1.1

   Iterate rigid measures in `expr`.

   Create and append spacer skip for each underfull measure. ::

      abjad> t = Staff(RigidMeasure((3, 8), construct.scale(3)) * 3)
      abjad> t[1].meter.forced = Meter(4, 8)
      abjad> t[2].meter.forced = Meter(5, 8)

   ::

      abjad> t[1].duration.is_underfull
      True
      abjad> t[2].duration.is_underfull

   ::

      abjad> measuretools.remedy_underfull_measures(t)
      abjad> print t.format
      \new Staff {
              {
                      \time 3/8
                      c'8
                      d'8
                      e'8
              }
              {
                      \time 4/8
                      c'8
                      d'8
                      e'8
                      s1 * 1/8
              }
              {
                      \time 5/8
                      c'8
                      d'8
                      e'8
                      s1 * 1/4
              }
      }
   '''

   for rigid_measure in iterate.naive_forward(expr, RigidMeasure):
      if rigid_measure.duration.is_underfull:
         spacer_skip = make_underfull_spacer_skip(rigid_measure)
         rigid_measure.append(spacer_skip)
