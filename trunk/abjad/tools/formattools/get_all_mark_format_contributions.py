from get_context_mark_format_pieces import get_context_mark_format_pieces
from is_formattable_context_mark_for_component import is_formattable_context_mark_for_component
import inspect


def get_all_mark_format_contributions(component):
    '''Get all mark format contributions as nested dictionaries.

    The first level of keys represent format slots.

    The second level of keys represent format contributor ('articulations', 'markup', etc.).

    Return dict.
    '''

    from abjad.tools import componenttools
    from abjad.tools import contexttools
    from abjad.tools import marktools
    from abjad.tools import markuptools

    class_to_section = {
        marktools.Articulation:        ('articulations', False),
        marktools.BendAfter:           ('articulations', False),
        marktools.LilyPondCommandMark: ('lilypond command marks', False),
        marktools.LilyPondComment:     ('comments', False),
        marktools.StemTremolo:         ('stem tremolo', True),
        markuptools.Markup:            ('markup', False),
    }

    contributions = {}

    marks = marktools.get_marks_attached_to_component(component)

    context_marks = set([])
    for parent in componenttools.get_proper_parentage_of_component(component):
        for mark in parent._marks_for_which_component_functions_as_start_component:
            if isinstance(mark, contexttools.ContextMark):
                if is_formattable_context_mark_for_component(mark, parent):
                    context_marks.add(mark)

    for mark in marks:

        print mark

        if not hasattr(mark, 'lilypond_format'):
            continue

        section, singleton = None, False
        if mark.__class__ in class_to_section:
            section, singleton = class_to_section[mark.__class__]

        elif isinstance(mark, contexttools.ContextMark):
            if is_formattable_context_mark_for_component(mark, component):
                context_marks.add(mark)
            continue

        else:
            mro = list(inspect.getmro(mark.__class__))
            while mro:
                if mro[-1] in class_to_section:
                    section, singleton = class_to_section[mro[-1]]
                mro.pop()
            if not section:
                section, singleton = 'other marks', False

        format_slot = mark._format_slot
        if format_slot not in contributions:
            contributions[format_slot] = { }
        if section not in contributions[format_slot]:
            contributions[format_slot][section] = []

        contribution_list = contributions[format_slot][section]
        if len(contribution_list) and singleton:
            raise ExtraMarkError
        result = mark.lilypond_format
        if isinstance(result, (list, tuple)):
            contribution_list.extend(result)
        else:
            contribution_list.append(result)

    section = 'context marks'
    for mark in context_marks:
        print mark
        format_slot = mark._format_slot
        result = get_context_mark_format_pieces(mark)
        if format_slot not in contributions:
            contributions[format_slot] = { }
        if section not in contributions[format_slot]:
            contributions[format_slot][section] = []
        contributions[format_slot][section].extend(result)

    return contributions
