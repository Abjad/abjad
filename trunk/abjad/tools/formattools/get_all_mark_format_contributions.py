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
        marktools.StemTremolo:         ('stem tremolos', True),
    }

    contributions = {}

    marks = marktools.get_marks_attached_to_component(component)

    up_markup, down_markup, neutral_markup = [], [], []

    context_marks = set([])

    ### organize marks attached directly to component ###

    for mark in marks:

        ### non-printing marks are skipped (i.e. Annotation) ###

        if not hasattr(mark, 'lilypond_format'):
            continue

        ### a recognized mark class ###

        section, singleton = None, False
        if mark.__class__ in class_to_section:
            section, singleton = class_to_section[mark.__class__]

        ### context marks to be dealt with later ###

        elif isinstance(mark, contexttools.ContextMark):
            if is_formattable_context_mark_for_component(mark, component):
                context_marks.add(mark)
            continue

        ### markup to be dealt with later ###

        elif isinstance(mark, markuptools.Markup):
            if mark.direction == '^':
                up_markup.append(mark)
            elif mark.direction == '_':
                down_markup.append(mark)
            elif mark.direction in ('-', None):
                neutral_markup.append(mark)
            continue

        ### otherwise, test if mark is a subclass of a recognized mark ###

        else:
            mro = list(inspect.getmro(mark.__class__))
            while mro:
                if mro[-1] in class_to_section:
                    section, singleton = class_to_section[mro[-1]]
                mro.pop()
            if not section:
                section, singleton = 'other marks', False

        ### prepare the contributions dictionary ###

        format_slot = mark._format_slot
        if format_slot not in contributions:
            contributions[format_slot] = { }
        if section not in contributions[format_slot]:
            contributions[format_slot][section] = []

        ### add the mark contribution ###

        contribution_list = contributions[format_slot][section]
        if len(contribution_list) and singleton:
            raise ExtraMarkError
        result = mark.lilypond_format
        if isinstance(result, (list, tuple)):
            contribution_list.extend(result)
        else:
            contribution_list.append(result)

    ### handle context marks ###

    for parent in componenttools.get_proper_parentage_of_component(component):
        for mark in parent._marks_for_which_component_functions_as_start_component:
            if isinstance(mark, contexttools.ContextMark):
                if is_formattable_context_mark_for_component(mark, parent):
                    context_marks.add(mark)

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

    ### handle markup ###

    result = []
    for markup_list in (up_markup, down_markup, neutral_markup):
        if not markup_list:
            pass
        elif 1 < len(markup_list):
            contents = []
            for m in markup_list:
                contents += m.contents
            direction = markup_list[0].direction
            if direction is None:
                direction = '-'
            command = markuptools.MarkupCommand('column', contents)
            markup = markuptools.Markup(command, direction=direction)
            result.extend(markup._get_format_pieces(is_indented=True))
        else:
            if markup_list[0].direction is None:
                markup = markuptools.Markup(markup_list[0])
                markup.direction = '-'
                result.extend(markup._get_format_pieces(is_indented=True))
            else:
                result.extend(markup_list[0]._get_format_pieces(is_indented=True))

    if result:
        if 'right' not in contributions:
            contributions['right'] = {}
        contributions['right']['markup'] = result

    return contributions
