from abjad.tools import iterate


def composite_offset_series(expr):
   r'''.. versionadded:: 1.1.2

   List unique offsets of leaves in arbitrary `expr`. ::

      abjad> staff_1 = Staff([FixedDurationTuplet((4, 8), construct.run(3))])
      abjad> staff_2 = Staff(construct.run(4))
      abjad> score = Score([staff_1, staff_2])
      abjad> pitchtools.diatonicize(score)
      abjad> f(score)
         \new Score <<
                 \new Staff {
                         \times 4/3 {
                                 c'8
                                 d'8
                                 e'8
                         }
                 }
                 \new Staff {
                         f'8
                         g'8
                         a'8
                         b'8
                 }
         >>
      abjad> leaftools.composite_offset_series(score)
      [Rational(0, 1), Rational(1, 8), Rational(1, 6), Rational(1, 4), Rational(1, 3), Rational(3, 8)]
   '''

   offsets = [ ]

   for leaf in iterate.leaves_forward_in(expr):
      offset = leaf.offset.prolated.start
      if offset not in offsets:
         offsets.append(offset)

   offsets.sort( )

   return offsets
