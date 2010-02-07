from abjad.rational import Rational


def is_bar_line_crosser(leaf):
   r'''.. versionadded:: 1.1.2

   True when `leaf` crosses bar line. Otherwise false. ::

      abjad> t = Staff(construct.scale(4))
      abjad> t[2].duration.written *= 2
      abjad> meter = Meter(2, 8)
      abjad> meter.partial = Rational(1, 8)
      abjad> t.meter.forced = meter
      abjad> f(t)
      \new Staff {
              \time 2/8
              \partial 8
              c'8
              d'8
              e'4
              f'8
      }
      abjad> for leaf in t:
         print leaf, leaftools.is_bar_line_crosser(leaf)
      c'8 False
      d'8 False
      e'4 True
      f'8 False
   '''

   meter = leaf.meter.effective
   partial = meter.partial
   if meter.partial is None:
      partial = Rational(0)

   shifted_start = (leaf.offset.prolated.start - partial) % meter.duration
   shifted_stop = (leaf.offset.prolated.stop - partial) % meter.duration

   if meter.duration < shifted_start + leaf.duration.prolated:
      return True

   return False
