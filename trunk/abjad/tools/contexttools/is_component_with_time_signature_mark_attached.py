from abjad.tools.contexttools.TimeSignatureMark import TimeSignatureMark
from abjad.tools.contexttools.is_component_with_context_mark_attached import is_component_with_context_mark_attached


def is_component_with_time_signature_mark_attached(component):
   r'''.. versionadded:: 2.0

   True when time signature mark attaches to `component`::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> contexttools.TimeSignatureMark(4, 8)(staff[0])
      TimeSignatureMark(4, 8)(c'8)

   ::

      abjad> f(staff)
      \new Staff {
         \time 4/8
         c'8
         d'8
         e'8
         f'8
      }

   ::

      abjad> contexttools.is_component_with_time_signature_mark_attached(staff[0])
      True

   Otherwise false::

      abjad> contexttools.is_component_with_time_signature_mark_attached(staff)
      False

   Return boolean.
   '''

   klasses = (TimeSignatureMark, )
   return is_component_with_context_mark_attached(component, klasses)
