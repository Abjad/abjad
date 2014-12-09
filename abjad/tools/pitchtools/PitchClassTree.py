# -*- encoding: utf-8 -*-
import os
from abjad.tools.datastructuretools.PayloadTree import PayloadTree


class PitchClassTree(PayloadTree):
    r'''A pitch-class tree.

    ..  container:: example

        Numbered pitch-class tree::

            >>> tree = pitchtools.PitchClassTree(
            ...     items=[[0, 4, 7, 8], [9, 2, 3, 11]],
            ...     item_class=pitchtools.NumberedPitchClass,
            ...     )
            >>> print(format(tree, 'storage'))
            pitchtools.PitchClassTree(
                [
                    [
                        pitchtools.NumberedPitchClass(0),
                        pitchtools.NumberedPitchClass(4),
                        pitchtools.NumberedPitchClass(7),
                        pitchtools.NumberedPitchClass(8),
                        ],
                    [
                        pitchtools.NumberedPitchClass(9),
                        pitchtools.NumberedPitchClass(2),
                        pitchtools.NumberedPitchClass(3),
                        pitchtools.NumberedPitchClass(11),
                        ],
                    ]
                )

    ..  container:: example

        Named pitch-class tree::

            >>> tree = pitchtools.PitchClassTree(
            ...     items=[['c', 'e', 'g', 'af'], ['a', 'd', 'ef', 'b']],
            ...     item_class=pitchtools.NamedPitchClass,
            ...     )
            >>> print(format(tree, 'storage'))
            pitchtools.PitchClassTree(
                [
                    [
                        pitchtools.NamedPitchClass('c'),
                        pitchtools.NamedPitchClass('e'),
                        pitchtools.NamedPitchClass('g'),
                        pitchtools.NamedPitchClass('af'),
                        ],
                    [
                        pitchtools.NamedPitchClass('a'),
                        pitchtools.NamedPitchClass('d'),
                        pitchtools.NamedPitchClass('ef'),
                        pitchtools.NamedPitchClass('b'),
                        ],
                    ]
                )

    Pitch-class trees are treated as immutable.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        PayloadTree.__init__(
            self,
            expr=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __illustrate__(self, **kwargs):
        r'''Illustrates pitch-class tree.

        Returns LilyPond file.
        '''
        from abjad import abjad_configuration
        from abjad.tools import indicatortools
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import override
        voice = scoretools.Voice()
        staff = scoretools.Staff([voice])
        score = scoretools.Score([staff])
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        stylesheet = os.path.join(
            abjad_configuration.abjad_directory,
            'stylesheets',
            'rhythm-letter-16.ily',
            )
        lilypond_file.file_initial_user_includes.append(stylesheet)
        voice.consists_commands.append('Horizontal_bracket_engraver')
        leaf_list_stack = []
        self._bracket_inner_nodes(leaf_list_stack, self, voice)
        score.add_final_bar_line()
        override(score).bar_line.stencil = False
        override(score).flag.stencil = False
        override(score).stem.stencil = False
        override(score).text_script.staff_padding = 3
        override(score).time_signature.stencil = False
        if 'title' in kwargs:
            markup = markuptools.Markup(kwargs.get('title'))
            lilypond_file.header_block.title = markup
        if 'subtitle' in kwargs:
            markup = markuptools.Markup(kwargs.get('subtitle'))
            lilypond_file.header_block.subtitle = markup
        command = indicatortools.LilyPondCommand('accidentalStyle forget')
        lilypond_file.layout_block.items.append(command)
        return lilypond_file

    ### PRIVATE METHODS ###

    def _bracket_inner_nodes(self, leaf_list_stack, node, voice):
        from abjad.tools import durationtools
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import attach
        if len(node):
            if node.level:
                leaf_list_stack.append([])
            for child_node in node:
                self._bracket_inner_nodes(
                    leaf_list_stack,
                    child_node,
                    voice,
                    )
            if node.level:
                bracket = spannertools.HorizontalBracketSpanner()
                attach(bracket, leaf_list_stack[-1])
                if node.level == 1:
                    node_index = node.parent.index(node)
                    level_one_first_leaf = leaf_list_stack[-1][0]
                    string = r'\bold {{ {} }}'.format(node_index)
                    markup = markuptools.Markup(string, Up)
                    attach(markup, level_one_first_leaf)
                leaf_list_stack.pop()
        elif node.payload:
            note = scoretools.Note(
                node.payload,
                durationtools.Duration(1, 8),
                )
            voice.append(note)
            for leaf_list in leaf_list_stack:
                leaf_list.append(note)