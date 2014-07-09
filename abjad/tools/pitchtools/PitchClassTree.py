# -*- encoding: utf-8 -*-
import os
import types
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
        from abjad.tools import durationtools
        from abjad.tools import indicatortools
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import attach
        from abjad.tools.topleveltools import inspect_
        from abjad.tools.topleveltools import override
        from scoremanager import idetools
        pcs = list(self.iterate_payload())
        pitches = [pitchtools.NamedPitch(_) for _ in pcs]
        leaves = scoretools.make_leaves(pitches, [durationtools.Duration(1, 8)])
        voice = scoretools.Voice(leaves)
        staff = scoretools.Staff([voice])
        score = scoretools.Score([staff])
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        configuration = idetools.Configuration()
        stylesheet = os.path.join(
            configuration.abjad_stylesheets_directory,
            'rhythm-letter-16.ily',
            )
        lilypond_file.file_initial_user_includes.append(stylesheet)
        voice.consists_commands.append('Horizontal_bracket_engraver')
        for level in (1, 2):
            level_sizes = []
            for x in self.iterate_at_level(level):
                size = len(list(x.iterate_payload()))
                level_sizes.append(size)
            for part in sequencetools.partition_sequence_by_counts(
                voice.select_leaves(), 
                level_sizes, 
                cyclic=False, 
                overhang=False,
                ):
                spanner = spannertools.HorizontalBracketSpanner()
                attach(spanner, part)
        current_group = 0
        for leaf in voice.select_leaves():
            spanner_classes = spannertools.HorizontalBracketSpanner
            brackets = inspect_(leaf).get_spanners(spanner_classes)
            brackets = tuple(brackets)
            if brackets[0][0] is leaf:
                if brackets[1][0] is leaf:
                    string = r'\bold {{ {} }}'.format(current_group)
                    markup = markuptools.Markup(string, Up)
                    attach(markup, leaf)
                    current_group += 1
        bar_line = score.add_final_bar_line()
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