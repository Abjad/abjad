def _get_markup_format_contributions(component):
    '''.. versionadded:: 2.0
    '''
    from abjad.tools import markuptools

    result = []
    markup = markuptools.get_markup_attached_to_component(component)
    up_markup, down_markup, neutral_markup = [], [], []
    for markup_object in markup:
        if markup_object._direction_string == 'up':
            up_markup.append(markup_object)
        elif markup_object._direction_string == 'down':
            down_markup.append(markup_object)
        elif markup_object._direction_string in ('neutral', None):
            neutral_markup.append(markup_object)
    for markup_list in (up_markup, down_markup, neutral_markup):
        if not markup_list:
            pass
        elif 1 < len(markup_list):
            #markup_list.sort()
            #contents = ' '.join([m._contents_string for m in markup_list])
            contents = [m._contents_string for m in markup_list]
#         contents.sort()
            contents = ' '.join(contents)
            direction_symbol = m._direction_string_to_direction_symbol[m._direction_string]
            column = r'%s \markup { \column { %s } }' % (direction_symbol, contents)
            result.append(column)
        else:
            result.append(markup_list[0].format)
    return ['markup', result]
