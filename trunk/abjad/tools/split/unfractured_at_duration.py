from abjad.tools.split._at_duration import _at_duration as split__at_duration


def unfractured_at_duration(component, duration):

   return split__at_duration(component, duration, spanners = 'unfractured')
