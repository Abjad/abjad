def get_context_mark_format_pieces(mark):
    '''Get context mark format pieces for `mark`.

    Return list.
    '''

    from abjad.tools import contexttools
    from abjad.tools import measuretools

    #print mark, mark.lilypond_format
    addenda = []
    mark_format = mark.lilypond_format
    if isinstance(mark_format, (tuple, list)):
        addenda.extend(mark_format)
    else:
        addenda.append(mark_format)

    # cosmetic mark is a hack to allow marks to format even without effective context;
    # currently used only in metric grid formatting
    if mark.effective_context is not None or \
        getattr(mark, '_is_cosmetic_mark', False) or \
        (isinstance(mark, contexttools.TimeSignatureMark) and
        isinstance(mark.start_component, measuretools.Measure)):
        return addenda
        #result.extend(addenda)
    else:
        addenda = [r'%%% ' + addendum + r' %%%' for addendum in addenda]
        return addenda
        #result.extend(addenda)
