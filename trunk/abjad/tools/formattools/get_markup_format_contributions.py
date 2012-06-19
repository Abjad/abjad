def get_markup_format_contributions(component):
    '''.. versionadded:: 2.0

    Get markup format contributions for `component`.

    Return list.
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
        elif markup_object.direction in ('-', None):
            neutral_markup.append(markup_object)

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
            #column = r'%s \markup { \column { %s } }' % (direction, contents)
            markup = markuptools.Markup(command, direction=direction)
            #result.append(str(markup))
            result.extend(markup._get_format_pieces(is_indented=True))
        else:
            if markup_list[0].direction is None:
                markup = markuptools.Markup(markup_list[0])
                markup.direction = '-'
                #result.append('- %s' % markup_list[0].format)
                result.extend(markup._get_format_pieces(is_indented=True))
            else:
                result.extend(markup_list[0]._get_format_pieces(is_indented=True))

    return ['markup', result]
