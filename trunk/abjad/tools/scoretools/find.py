from abjad.component.component import _Component
from abjad.tools import iterate


def find(expr, name = None, klass = None, context = None):
   '''Return a Python list of all components in `expr`, such that:

   * ``component.name == name``
   * ``isinstance(component, klass)``
   * ``component.context == context``

   Do not run tests where keyword is set to none.

   Example score. ::

      abjad> flute_staff = Staff(construct.scale(4))
      abjad> flute_staff.name = 'Flute'
      abjad> violin_staff = Staff(construct.scale(4))
      abjad> violin_staff.name = 'Violin'
      abjad> staff_group = StaffGroup([flute_staff, violin_staff])
      abjad> score = Score([staff_group])

   Find components by name. ::

      abjad> scoretools.find(score, name = 'Violin')
      [Staff{4}]

   Find components by class. ::

      abjad> scoretools.find(score, klass = Staff)
      [Staff{4}, Staff{4}]

   Find components by context. ::

      abjad> violin_staff.context = 'ViolinContext'
      abjad> scoretools.find(score, context = 'ViolinContext')
      [ViolinContext{4}]

   .. note:: For shallow traversal of container for numeric indices,
      use ``Container[i]`` instead.
   '''

   result = [ ]

   for component in iterate.naive_forward(expr, _Component):
      if name is None or component.name == name:
         if klass is None or isinstance(component, klass):
            if context is None or \
               getattr(component, 'context', None) == context:
               result.append(component)

   return result
