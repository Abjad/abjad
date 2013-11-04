# -*- encoding: utf-8 -*-


def get_context_mark_format_pieces(mark):
    r'''Get context mark format pieces for `mark`.

    Returns list.
    '''

    from abjad.tools import marktools
    from abjad.tools import scoretools

    addenda = []
    mark_format = mark._lilypond_format
    if isinstance(mark_format, (tuple, list)):
        addenda.extend(mark_format)
    else:
        addenda.append(mark_format)

    # cosmetic mark is a hack to allow marks to format even 
    # without effective context;
    # currently used only in metric grid formatting
    if mark.effective_context is not None or \
        getattr(mark, '_is_cosmetic_mark', False) or \
        (isinstance(mark, marktools.TimeSignatureMark) and
        isinstance(mark.start_component, scoretools.Measure)):
        return addenda
    else:
        addenda = [r'%%% ' + addendum + r' %%%' for addendum in addenda]
        return addenda
