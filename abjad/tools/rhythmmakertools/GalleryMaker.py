# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import set_


class GalleryMaker(AbjadValueObject):
    r'''Gallery maker.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Illustration helpers'

    ### SPECIAL METHODS ###

    def __call__(self, configurations_by_class):
        r'''Calls gallery-maker.

        Returns LilyPond file.
        '''
        lilypond_file = lilypondfiletools.make_basic_lilypond_file()
        lilypond_file.items.remove(lilypond_file.header_block)
        lilypond_file.items.remove(lilypond_file.layout_block)
        lilypond_file.items.remove(lilypond_file.paper_block)
        lilypond_file.items.remove(lilypond_file.score_block)
        for class_ in configurations_by_class:
            configurations = configurations_by_class[class_]
            for i, configuration in enumerate(configurations):
                configuration_number = i + 1
                score_blocks = self._configuration_to_score_blocks(
                    configuration,
                    configuration_number,
                    )
                first_score_block = score_blocks[0]
                lilypond_file.items.extend(score_blocks)
                string = r'\pageBreak'
                lilypond_file.items.append(string)
        assert lilypond_file.items[-1] == string
        lilypond_file.items.pop(-1)
        lilypond_file.includes.append('stylesheet.ily')
        return lilypond_file

    ### PRIVATE METHODS ###

    def _add_class_name_header(self, rhythm_maker, score_block):
        header_block = lilypondfiletools.Block(name='header')
        class_name_markup = self._make_class_name_markup(rhythm_maker)
        header_block.title = class_name_markup
        score_block.items.append(header_block)

    @staticmethod
    def _add_final_bar_line(score):
        score.add_final_bar_line()
        selector = select().by_leaf(flatten=True)
        leaves = selector(score)
        leaves = leaves[-1:]
        last_leaf = leaves[0]
        string = "override Staff.BarLine.extra-offset = #'(1.6 . 0)"
        command = indicatortools.LilyPondCommand(
            string,
            'after',
            )
        attach(command, last_leaf)

    def _attach_configuration_markup(
        self,
        rhythm_maker,
        first_score,
        ):
        markup = self._make_configuration_markup(rhythm_maker)
        context = first_score['TimeSignatureContext']
        for leaf in iterate(context).by_class(scoretools.Leaf):
            break
        first_leaf = leaf
        attach(markup, first_leaf)

    @staticmethod
    def _check_score(score):
        if inspect_(score).is_well_formed():
            return
        violations = inspect_(score).tabulate_well_formedness_violations()
        message = 'score is not well-formed: {!r}.'
        message = message.format(score)
        message += '\n'
        message += violations
        raise Exception(message)

    def _configuration_to_score_blocks(
        self,
        configuration,
        configuration_number,
        ):
        assert isinstance(configuration, tuple) and len(configuration) == 2
        rhythm_maker = configuration[0]
        division_lists = configuration[1]
        score_blocks = []
        for i, division_list in enumerate(division_lists):
            score_number = i + 1
            score_number_markup = self._make_score_number_markup(
                configuration_number,
                score_number,
                )
            score = self._make_score(
                rhythm_maker,
                division_list,
                score_number_markup,
                )
            score_block = lilypondfiletools.Block(name='score')
            score_block.items.append(score)
            score_blocks.append(score_block)
        first_score_block = score_blocks[0]
        first_score = first_score_block.items[0]
        self._attach_configuration_markup(rhythm_maker, first_score)
        if configuration_number == 1:
            self._add_class_name_header(rhythm_maker, first_score_block)
        return score_blocks

    @staticmethod
    def _make_class_name_markup(rhythm_maker):
        class_ = type(rhythm_maker)
        string = class_.__name__
        string = stringtools.capitalize_start(string)
        pair = schemetools.SchemePair('font-name', 'Times')
        command = markuptools.MarkupCommand('override', pair, string)
        command = markuptools.MarkupCommand('fontsize', 4.5, command)
        markup = markuptools.Markup(command)
        return markup

    @staticmethod
    def _make_configuration_markup(rhythm_maker):
        string = format(rhythm_maker, 'storage')
        string = string.replace('rhythmmakertools.', '')
        lines = string.split('\n')
        command = markuptools.MarkupCommand('column', lines)
        command.force_quotes = True
        pair = schemetools.SchemePair('font-name', 'Courier')
        command = markuptools.MarkupCommand('override', pair, command)
        markup = markuptools.Markup(command, direction=Up)
        return markup

    def _make_score(
        self,
        rhythm_maker,
        division_list,
        score_number_markup,
        ):
        lists = rhythm_maker(division_list)
        selections = sequencetools.flatten_sequence(lists)
        measures = scoretools.make_spacer_skip_measures(division_list)
        time_signature_context = scoretools.Context(
            measures,
            context_name='TimeSignatureContext',
            name='TimeSignatureContext',
            )
        measures = scoretools.make_spacer_skip_measures(division_list)
        staff = scoretools.Staff(measures)
        set_(staff).instrument_name = score_number_markup
        staff.context_name = 'RhythmicStaff'
        staff.name = 'Note-entry staff'
        measures = mutate(staff).replace_measure_contents(selections)
        score = scoretools.Score()
        score.append(time_signature_context)
        score.append(staff)
        self._add_final_bar_line(score)
        self._check_score(score)
        return score

    @staticmethod
    def _make_score_number_markup(
        configuration_number,
        score_number,
        ):
        assert mathtools.is_nonnegative_integer(configuration_number)
        assert mathtools.is_nonnegative_integer(score_number)
        number_string = '{}-{}'.format(
            configuration_number,
            score_number,
            )
        command = markuptools.MarkupCommand('fontsize', 2, number_string)
        command = markuptools.MarkupCommand('italic', command)
        command = markuptools.MarkupCommand('box', command)
        pair = schemetools.SchemePair('box-padding', 0.75)
        command = markuptools.MarkupCommand('override', pair, command)
        width = 9
        command = markuptools.MarkupCommand('hcenter-in', width, command)
        markup = markuptools.Markup(command)
        return markup