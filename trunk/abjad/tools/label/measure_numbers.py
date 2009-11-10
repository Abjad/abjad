from abjad.container import Container
from abjad.measure import _Measure


def measure_numbers(container, style = 'comment'):
   r'''Label measure numbers in `container` according to `style`.

   Turn measure number labels on with ``style = 'comment'``. ::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
      abjad> pitchtools.diatonicize(staff)
      abjad> label.measure_numbers(staff, style = 'comment')
      abjad> print staff.format
      \new Staff {
              % start measure 1
              {
                      \time 2/8
                      c'8
                      d'8
              }
              % stop measure 1
              % start measure 2
              {
                      \time 2/8
                      e'8
                      f'8
              }
              % stop measure 2
              % start measure 3
              {
                      \time 2/8
                      g'8
                      a'8
              }
              % stop measure 3
      }

   Turn measure number labels off with ``style = None``. ::

      abjad> label.measure_numbers(staff, style = None)
      abjad> print staff.format
      \new Staff {
              {
                      \time 2/8
                      c'8
                      d'8
              }
              {
                      \time 2/8
                      e'8
                      f'8
              }
              {
                      \time 2/8
                      g'8
                      a'8
              }
      }
   '''

   ## functionality implemented on _ContainerFormatterNumberInterface
   if isinstance(container, _Measure):
      container._formatter.number.self = style
   else:
      container._formatter.number.measures = style
