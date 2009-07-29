from abjad.core.grobhandler import _GrobHandler


def promote(grob_handler, attribute, context):
   r'''Promote `attribute` to LilyPond `context`.
   Both `attribute` and `context` must be strings. ::

      abjad> staff = Staff(construct.scale(4))
      abjad> staff[0].clef.color = 'red'
      abjad> overridetools.promote(staff[0].clef, 'color', 'Staff')

      abjad> print staff.format
      \new Staff {
              \once \override Staff.Clef #'color = #red
              c'8
              d'8
              e'8
              f'8
      }

   This code overrides the color of the clef preceding the first
   note in staff and then promotes that color override to the 
   LilyPond staff context. This is important because the LilyPond
   engraver that creates clef symbols lives at the staff context
   and does not live at the lower level of the voice context.
   '''

   assert isinstance(grob_handler, _GrobHandler)
   assert isinstance(context, str)

   if hasattr(grob_handler, attribute):
      grob_handler._promotions[attribute] = context
   else:
      raise AttributeError('no %s attribute.' % attribute)
