def deactivate(text, tag):
    r'''Deactivates `tag` in `text`.

    ..  container:: example

        Writes (active) tag into LilyPond input:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup('Allegro').with_color('red')
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     tag='RED_MARKUP',
        ...     )

        >>> text = format(staff, 'lilypond:strict')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> print(text)
        \new Staff {
            c'4
            - \markup {     %! RED_MARKUP
                \with-color %! RED_MARKUP
                    #red    %! RED_MARKUP
                    Allegro %! RED_MARKUP
                }           %! RED_MARKUP
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

        Deactivates tag:

        >>> text = format(staff, 'lilypond:strict')
        >>> text, count = abjad.deactivate(text, 'RED_MARKUP')
        >>> print(text)
        \new Staff {
            c'4
        %%% - \markup {     %! RED_MARKUP
        %%%     \with-color %! RED_MARKUP
        %%%         #red    %! RED_MARKUP
        %%%         Allegro %! RED_MARKUP
        %%%     }           %! RED_MARKUP
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file = abjad.LilyPondFile.new(lines)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Activates tag again:

        >>> text, count = abjad.activate(text, 'RED_MARKUP')
        >>> print(text)
        \new Staff {
            c'4
            - \markup {     %! RED_MARKUP
                \with-color %! RED_MARKUP
                    #red    %! RED_MARKUP
                    Allegro %! RED_MARKUP
                }           %! RED_MARKUP
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file = abjad.LilyPondFile.new(lines)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        Deactivates tag again:

        >>> text, count = abjad.deactivate(text, 'RED_MARKUP')
        >>> print(text)
        \new Staff {
            c'4
        %%% - \markup {     %! RED_MARKUP
        %%%     \with-color %! RED_MARKUP
        %%%         #red    %! RED_MARKUP
        %%%         Allegro %! RED_MARKUP
        %%%     }           %! RED_MARKUP
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file = abjad.LilyPondFile.new(lines)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    Tags can toggle indefinitely.

    Returns text, count pair.

    Count gives number of deactivated tags.
    '''
    import abjad
    assert isinstance(tag, str) or callable(tag)
    lines, count = [], 0
    treated_last_line, last_index = False, None
    text_lines = text.split('\n')
    text_lines = [_ + '\n' for _ in text_lines[:-1]] + text_lines[-1:]
    lines = []
    for line in text_lines:
        first_nonwhitespace_index = len(line) - len(line.lstrip())
        index = first_nonwhitespace_index
        if not abjad.Line(line).match(tag) or line[index] == '%':
            lines.append(line)
            treated_last_line, last_index = False, None
            continue
        if last_index is None:
            last_index = index
        if ' %@%' in line:
            prefix = '%@% '
            line = line.replace(' %@%', '')
        else:
            prefix = '%%% '
        target = line[last_index-4:last_index]
        assert target == '    ', repr((line, target, index, tag))
        characters = list(line)
        characters[last_index-4:last_index] = list(prefix)
        line = ''.join(characters)
        lines.append(line)
        if not treated_last_line:
            count += 1
        treated_last_line = True
    text = ''.join(lines)
    return text, count
