from abjad.tools.componenttools._Component import _Component
from abjad.exceptions import MissingComponentError
from abjad.tools.componenttools.iterate_components_forward_in_expr import iterate_components_forward_in_expr


def get_first_component_in_expr_with_name(expr, name):
    '''.. versionadded:: 1.1

    Get first component in `expr` with `name`::

        abjad> flute_staff = Staff("c'8 d'8 e'8 f'8")
        abjad> flute_staff.name = 'Flute'
        abjad> violin_staff = Staff("c'8 d'8 e'8 f'8")
        abjad> violin_staff.name = 'Violin'
        abjad> staff_group = scoretools.StaffGroup([flute_staff, violin_staff])
        abjad> score = Score([staff_group])

    ::

        abjad> componenttools.get_first_component_in_expr_with_name(score, 'Violin')
        Staff-"Violin"{4}

    .. versionchanged:: 2.0
        Function returns first component found.
        Function previously returned tuple of all components found.

    .. versionchanged:: 2.0
        renamed ``scoretools.find()`` to
        ``componenttools.get_first_component_in_expr_with_name()``.

    .. versionchanged:: 2.0
        Removed `klass` and `context` keywords.
        Function operates only on component name.
    '''

    if not isinstance(expr, (_Component, list, tuple)):
        raise TypeError('must be tuple, list or Abjad comonent.')

    result = []

    for component in iterate_components_forward_in_expr(expr, _Component):
        if name is None or getattr(component, 'name', None) == name:
            return component

    raise MissingComponentError
