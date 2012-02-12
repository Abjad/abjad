import re


def parse_lilypond_input_string(note_entry_string):
    '''.. versionadded:: 2.0

    Parse LilyPond `note_entry_string`::

        abjad> note_entry_string = "g'2 a'2 g'4. fs'8 e'4 d'4"
        abjad> iotools.parse_lilypond_input_string(note_entry_string)
        {g'2, a'2, g'4., fs'8, e'4, d'4}

    Return container of note, rest and chord instances.

    Handle simple beaming, slurs and articulations.

    Do not parse tuplets, measures or other complex LilyPond input.
    '''
    from abjad.tools.containertools.Container import Container
    from abjad.tools import contexttools
    from abjad.tools import marktools
    from abjad.tools.lilypondfiletools._parse_chord_entry_token import _parse_chord_entry_token
    from abjad.tools.lilypondfiletools._parse_note_entry_token import _parse_note_entry_token
    from abjad.tools.spannertools import BeamSpanner
    from abjad.tools.spannertools import SlurSpanner
    from abjad.tools.tietools import TieSpanner
    from abjad.tools import componenttools
    from abjad.tools import leaftools
    from abjad.tools import spannertools

    container = Container([])
    tokens = note_entry_string.split()

    in_chord = False
    chord_tokens = []

    in_beam = False
    beam_start_leaf = None

    in_slur = False
    slur_start_leaf = None

    tie_next_leaf = False

    waiting_on_bar_string = False
    waiting_on_clef_string = False
    clef_string = None

    for token in tokens:

        if waiting_on_bar_string:
            bar_string = eval(token)
            last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
            marktools.BarLine(bar_string)(last_leaf)
            waiting_on_bar_string = False

        elif waiting_on_clef_string:
            clef_string = token
            if token.startswith(('\'', '\"')):
                clef_string = eval(token)
            waiting_on_clef_string = False

        elif in_chord: # currently inside a chord block, looking for pitches

            if re.match("[A-Za-z0-9,']+>[0-9]+", token) is not None:
                chord_tokens.append(token)
                leaf = _parse_chord_entry_token(' '.join(chord_tokens))
                if tie_next_leaf:
                    last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
                    componenttools.extend_in_parent_of_component_and_grow_spanners(last_leaf, [leaf])
                    tie_next_leaf = False
                else:
                    container.append(leaf)
                in_chord = False
                chord_tokens = []
                if clef_string:
                    last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
                    contexttools.ClefMark(clef_string)(last_leaf)
                    clef_string = None

            elif re.match('\w+', token) is not None:
                chord_tokens.append(token)

            else:
                pass

        else: # currently not inside a chord block

            if re.match('\w+', token) is not None:
                leaf = _parse_note_entry_token(token)
                if tie_next_leaf:
                    last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
                    componenttools.extend_in_parent_of_component_and_grow_spanners(last_leaf, [leaf])
                    tie_next_leaf = False
                else:
                    container.append(leaf)
                if clef_string:
                    last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
                    contexttools.ClefMark(clef_string)(last_leaf)
                    clef_string = None

            elif re.match('<\w+', token) is not None:
                in_chord = True
                chord_tokens.append(token)

            elif token == '~':
                last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
                try:
                    spannertools.get_the_only_spanner_attached_to_component(last_leaf, TieSpanner)
                except MissingSpannerError:
                    TieSpanner([last_leaf])
                tie_next_leaf = True

            elif token == r'\bar':
                waiting_on_bar_string = True

            elif token == r'\clef':
                waiting_on_clef_string = True

            elif token.startswith(('\\', '-', '^', '_')):
                last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
                try:
                    if 0 <= token.index('\\'):
                        marktools.Articulation(token)(last_leaf)
                except:
                    marktools.Articulation(token[1], token[0])(last_leaf)

            elif token == '(':
                if in_slur:
                    raise Exception('Attempting to create overlapping slurs.')
                in_slur = True
                slur_start_leaf = leaftools.get_nth_leaf_in_expr(container, -1)

            elif token == ')':
                if not in_slur:
                    raise Exception('Attempting to end a non-existent slur spanner.')
                in_slur = False
                slur_stop_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
                start_index = container.index(slur_start_leaf)
                stop_index = container.index(slur_stop_leaf)
                SlurSpanner(container[start_index:stop_index + 1])
                slur_start_leaf = None

            elif token == '[':
                if in_beam:
                    raise Exception('Attempting to create overlapping beams.')
                in_beam = True
                beam_start_leaf = leaftools.get_nth_leaf_in_expr(container, -1)

            elif token == ']':
                if not in_beam:
                    raise Exception('Attempting to end a non-existent beam spanner.')
                in_beam = False
                beam_stop_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
                start_index = container.index(beam_start_leaf)
                stop_index = container.index(beam_stop_leaf)
                BeamSpanner(container[start_index:stop_index + 1])
                beam_start_leaf = None

            elif token == '[]':
                if in_beam:
                    raise Exception('Attempting to create overlapping beams.')
                last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
                BeamSpanner(last_leaf)

            else:
                pass

    return container
