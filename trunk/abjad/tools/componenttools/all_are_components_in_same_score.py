from abjad.tools.componenttools._Component import _Component
from abjad.tools.componenttools.component_to_score_root import component_to_score_root
from abjad.tools.componenttools.is_orphan_component import is_orphan_component
import types


def all_are_components_in_same_score(expr, klasses=None, allow_orphans=True):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all components in same score. Otherwise false::

        abjad> score = Score([Staff("c'8 d'8 e'8")])
        abjad> componenttools.all_are_components_in_same_score(score.leaves)
        True

    True when elements in `expr` are all `klasses` in same score. Otherwise false::

        abjad> score = Score([Staff("c'8 d'8 e'8")])
        abjad> componenttools.all_are_components_in_same_score(score.leaves, klasses = (Note, ))
        True

    Return boolean.
    '''

    if not isinstance(expr, (list, tuple, types.GeneratorType)):
        #raise TypeError('Must be list of Abjad components.')
        return False

    if klasses is None:
        klasses = _Component

    if len(expr) == 0:
        return True

    first = expr[0]
    if not isinstance(first, klasses):
        return False

    first_parent = first._parentage.parent
    first_score = component_to_score_root(first)
    for element in expr[1:]:
        if not isinstance(element, klasses):
            return False
        if component_to_score_root(element) is not first_score:
            if not (allow_orphans and is_orphan_component(element)):
                return False

    return True
