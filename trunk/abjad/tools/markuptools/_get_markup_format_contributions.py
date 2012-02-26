def _get_markup_format_contributions(component):
    '''.. versionadded:: 2.0
    '''
    from abjad.tools import markuptools

    result = []
    markup = markuptools.get_markup_attached_to_component(component)
    up_markup, down_markup, neutral_markup = [], [], []

    for markup_object in markup:
        if markup_object.direction == '^':
            up_markup.append(markup_object)
        elif markup_object.direction == '_':
            down_markup.append(markup_object)
        elif markup_object.direction in ('-', 'neutral', None):
            neutral_markup.append(markup_object)

    for markup_list in (up_markup, down_markup, neutral_markup):
        if not markup_list:
            pass
        elif 1 < len(markup_list):
            contents = [m._contents_string for m in markup_list]
            contents = ' '.join(contents)
            direction = markup_list[0].direction
            if direction is None:
                direction = '-'
            column = r'%s \markup { \column { %s } }' % (direction, contents)
            result.append(column)
        else:
            if markup_list[0].direction is None:
                result.append('- %s' % markup_list[0].format)
            else:
                result.append(markup_list[0].format)
    return ['markup', result]
