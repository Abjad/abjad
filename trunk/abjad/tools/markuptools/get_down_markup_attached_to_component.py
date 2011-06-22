from abjad.tools.markuptools.get_markup_attached_to_component import get_markup_attached_to_component


def get_down_markup_attached_to_component(component):
   '''.. versionadded:: 1.1.2

   Get down-markup attached to component::

      abjad> chord = Chord([-11, 2, 5], (1, 4))
      abjad> markuptools.Markup('UP', 'up')(chord)
      abjad> markuptools.Markup('DOWN', 'down')(chord)

   ::

      abjad> markuptools.get_down_markup_attached_to_component(t)
      (Markup('DOWN', 'down'),)

   Return tuple of zero or more markup objects.
   '''

   result = [ ]

   markups = get_markup_attached_to_component(component)
   for markup in markups:
      if markup._direction_string == 'down':
         result.append(markup)

   return tuple(result)
