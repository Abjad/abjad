from abjad.components import Rest


def set_vertical_positioning_pitch_on_rest(rest, pitch):
   r'''.. versionadded:: 1.1.2

   Set vertical positioning `pitch` on `rest`::

      abjad> rest = Rest((1, 4))
      abjad> resttools.set_vertical_positioning_pitch_on_rest(rest, 14)
      Rest(4)
      abjad> f(rest)
      d''4 \rest

   Return `rest`.
   ''' 
   from abjad.tools import pitchtools

   if not isinstance(rest, Rest):
      raise TypeError('\n\tMust be rest: "%s".' % rest)

   if pitch is not None:
      pitch = pitchtools.NamedChromaticPitch(pitch)

   rest._vertical_positioning_pitch = pitch

   return rest
