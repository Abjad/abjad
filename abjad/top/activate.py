def activate(text, tag, skipped=False):
    r"""
    Activates ``tag`` in ``text``.

    ..  container:: example

        Writes (deactivated) tag with ``'%@%'`` prefix into LilyPond
        input:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> markup = abjad.Markup('Allegro').with_color('red')
        >>> abjad.attach(
        ...     markup,
        ...     staff[0],
        ...     deactivate=True,
        ...     tag='RED_MARKUP',
        ...     )

        >>> text = format(staff, 'lilypond')
        >>> text = abjad.LilyPondFormatManager.left_shift_tags(text)
        >>> print(text)
        \new Staff {
            c'4
        %@% - \markup {         %! RED_MARKUP
        %@%     \with-color     %! RED_MARKUP
        %@%         #red        %! RED_MARKUP
        %@%         Allegro     %! RED_MARKUP
        %@%     }               %! RED_MARKUP
            d'4
            e'4
            f'4
        }

        >>> abjad.show(staff) # doctest: +SKIP

        Activates tag:

        >>> text, count = abjad.activate(text, 'RED_MARKUP')
        >>> print(text)
        \new Staff {
            c'4
            - \markup {         %! RED_MARKUP %@%
                \with-color     %! RED_MARKUP %@%
                    #red        %! RED_MARKUP %@%
                    Allegro     %! RED_MARKUP %@%
                }               %! RED_MARKUP %@%
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
        %@% - \markup {         %! RED_MARKUP 
        %@%     \with-color     %! RED_MARKUP 
        %@%         #red        %! RED_MARKUP 
        %@%         Allegro     %! RED_MARKUP 
        %@%     }               %! RED_MARKUP 
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
            - \markup {         %! RED_MARKUP  %@%
                \with-color     %! RED_MARKUP  %@%
                    #red        %! RED_MARKUP  %@%
                    Allegro     %! RED_MARKUP  %@%
                }               %! RED_MARKUP  %@%
            d'4
            e'4
            f'4
        }

        >>> lines = [_.strip('\n') for _ in text.split('\n')]
        >>> lilypond_file = abjad.LilyPondFile.new(lines)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

    Tags can toggle indefinitely.

    Returns text, count pair.

    Count gives number of activated tags.
    """
    import abjad
    assert isinstance(tag, str) or callable(tag), repr(tag)
    lines, count, skipped_count = [], 0, 0
    treated_last_line = False
    found_already_active_on_last_line = False
    text_lines = text.split('\n')
    text_lines = [_ + '\n' for _ in text_lines[:-1]] + text_lines[-1:]
    lines = []
    for line in text_lines:
        first_nonwhitespace_index = len(line) - len(line.lstrip())
        index = first_nonwhitespace_index
        if not abjad.Line(line).match(tag):
            lines.append(line)
            treated_last_line = False
            found_already_active_on_last_line = False
            continue
        if line[index:index+4] in ('%%% ', '%@% '):
            if '%@% ' in line:
                line = line.replace('%@%', '   ')
                suffix = ' %@%'
            else:
                line = line.replace('%%%', '   ')
                suffix = None
            assert line.endswith('\n'), repr(line)
            if suffix:
                line = line.strip('\n') + suffix + '\n'
            if not treated_last_line:
                count += 1
            treated_last_line = True
            found_already_active_on_last_line = False
        else:
            if not found_already_active_on_last_line:
                skipped_count += 1
            found_already_active_on_last_line = True
            treated_last_line = False
        lines.append(line)
    text = ''.join(lines)
    if skipped is True:
        return text, count, skipped_count
    else:
        return text, count
