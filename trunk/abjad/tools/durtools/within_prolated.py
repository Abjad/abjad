def within_prolated(timepoint, component):
   '''True when `timepoint` is within the duration of `component`.

   ::
   
      abjad> staff = Staff(construct.scale(4))
      abjad> leaf = staff.leaves[0]
      abjad> durtools.within_seconds(Rational(1, 16), leaf)
      True
      abjad> durtools.within_seconds(Rational(1, 12), leaf)
      True

   Otherwise false. ::

      abjad> durtools.within_seconds(Rational(1, 4), t)
      False
   '''

   return component.offset.prolated.start <= timepoint < \
      component.offset.prolated.stop
