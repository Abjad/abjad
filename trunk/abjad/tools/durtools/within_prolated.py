from abjad.rational import Rational


def within_prolated(timepoint, component):
   '''True when `timepoint` is within the prolated 
   duration of `component`. ::
   
      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> leaf = staff.leaves[0]
      abjad> durtools.within_prolated(Rational(1, 16), leaf)
      True
      abjad> durtools.within_prolated(Rational(1, 12), leaf)
      True

   Otherwise false. ::

      abjad> durtools.within_prolated(Rational(1, 4), t)
      False
   '''

   try:
      timepoint = Rational(timepoint)
   except TypeError:
      pass

   return component.offset.prolated.start <= timepoint < \
      component.offset.prolated.stop
