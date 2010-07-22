from abjad.component import _Component
from abjad.exceptions import MissingComponentError
from abjad.tools import iterate


def find(expr, name = None, klass = None, context = None):
   '''Return the first component in `expr`, such that:

   * ``component.name == name``
   * ``isinstance(component, klass)``
   * ``component.context == context``

   Do not run tests where keyword is set to none.

   Example score. ::

      abjad> flute_staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> flute_staff.name = 'Flute'
      abjad> violin_staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> violin_staff.name = 'Violin'
      abjad> staff_group = StaffGroup([flute_staff, violin_staff])
      abjad> score = Score([staff_group])

   Find components by name. ::

      abjad> scoretools.find(score, name = 'Violin')
      Staff-"Violin"{4}

   Find components by class. ::

      abjad> scoretools.find(score, klass = Staff)
      Staff-"Flute"{4}

   Find components by context. ::

      abjad> violin_staff.context = 'ViolinContext'
      abjad> scoretools.find(score, context = 'ViolinContext')
      ViolinContext-"Violin"{4},

   .. note:: For shallow traversal use ``Container[i]`` instead.

   .. versionchanged:: 1.1.2
      Function returns first component found.
      Function previously returned tuple of all components found.
   '''

   if not isinstance(expr, (_Component, list, tuple)):
      raise TypeError('must be tuple, list or Abjad comonent.')

   result = [ ]

   for component in iterate.naive_forward_in_expr(expr, _Component):
      if name is None or component.name == name:
         if klass is None or isinstance(component, klass):
            if context is None or \
               getattr(component, 'context', None) == context:
               return component

   raise MissingComponentError
