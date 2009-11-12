def within_seconds(timepoint, component):
   '''True when `timepoint` is within the duration 
   of `component` in seconds. ::
   
      abjad> staff = Staff(construct.scale(4))
      abjad> tempo_indication = tempotools.TempoIndication(Rational(1, 2), 60)
      abjad> staff.tempo.forced = tempo_indication
      abjad> leaf = staff.leaves[0]
      abjad> durtools.within_seconds(0.1, leaf)
      True
      abjad> durtools.within_seconds(0.333, leaf)
      True

   Otherwise false. ::

      abjad> durtools.within_seconds(0.5, t)
      False
   '''

   return component.offset.seconds.start <= timepoint < \
      component.offset.seconds.stop
