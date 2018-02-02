from typing import Callable
from typing import List
from typing import Tuple
from typing import Union
from .Path import Path
from .Tags import Tags
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.datastructuretools.String import String
abjad_tags = Tags()


class Job(AbjadObject):
    r'''Job.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_activate',
        '_deactivate',
        '_deactivate_first',
        '_message_zero',
        '_path',
        '_title',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        activate: Tuple[Union[str, Callable], str] = None,
        deactivate: Tuple[Union[str, Callable], str] = None,
        deactivate_first: bool = None,
        message_zero: bool = None,
        path: Path = None,
        title: str = None,
        ) -> None:
        self._activate: Tuple[Union[str, Callable], str] = activate
        self._deactivate: Tuple[Union[str, Callable], str] = deactivate
        self._deactivate_first: bool = deactivate_first
        self._message_zero: bool = message_zero
        self._path: Path = path
        self._title: str = title

    ### SPECIAL METHODS ###

    def __call__(self) -> List[str]:
        r'''Calls job on job ``path``.
        '''
        messages = []
        if self.title is not None:
            messages.append(String(self.title).capitalize_start())
        total_count = 0
        if self.deactivate_first is True:
            if self.deactivate is not None:
                assert isinstance(self.deactivate, tuple)
                match, name = self.deactivate
                if match is not None:
                    count, skipped, messages_ = self.path.deactivate(
                        match,
                        indent=1,
                        message_zero=True,
                        name=name,
                        )
                    messages.extend(messages_)
                    total_count += count
        if self.activate is not None:
            assert isinstance(self.activate, tuple)
            match, name = self.activate
            if match is not None:
                count, skipped, messages_ = self.path.activate(
                    match,
                    indent=1,
                    message_zero=True,
                    name=name,
                    )
                messages.extend(messages_)
                total_count += count
        if self.deactivate_first is not True:
            if self.deactivate is not None:
                assert isinstance(self.deactivate, tuple)
                match, name = self.deactivate
                if match is not None:
                    count, skipped, messages_ = self.path.deactivate(
                        match,
                        indent=1,
                        message_zero=True,
                        name=name,
                        )
                    messages.extend(messages_)
                    total_count += count
        if total_count == 0 and not self.message_zero:
            messages = []
        return messages

    ### PUBLIC PROPERTIES ###

    @property
    def activate(self) -> Tuple[Union[str, Callable], str]:
        r'''Gets activate match / message pair.
        '''
        return self._activate

    @property
    def deactivate(self) -> Tuple[Union[str, Callable], str]:
        r'''Gets deactivate match / message pair.
        '''
        return self._deactivate

    @property
    def deactivate_first(self) -> bool:
        r'''Is true when deactivate runs first.
        '''
        return self._deactivate_first

    @property
    def message_zero(self) -> bool:
        r'''Is true when job returns messages even when no matches are found.
        '''
        return self._message_zero

    @property
    def path(self) -> Path:
        r'''Gets path.
        '''
        return self._path

    @property
    def title(self) -> str:
        r'''Gets title.
        '''
        return self._title

    ### PUBLIC METHODS ###

    @staticmethod
    def broken_spanner_join_job(path) -> 'Job':
        r'''Makes broken spanner join job.
        '''
        def activate(tags):
            tags_ = [
                abjad_tags.LEFT_BROKEN_REPEAT_TIE,
                abjad_tags.RIGHT_BROKEN_TIE,
                ]
            return bool(set(tags) & set(tags_))
        def deactivate(tags):
            tags_ = [
                abjad_tags.LEFT_BROKEN_TRILL,
                abjad_tags.RIGHT_BROKEN_TRILL,
                ]
            return bool(set(tags) & set(tags_))
        return Job(
            activate=(activate, 'broken spanner expression'),
            deactivate=(deactivate, 'broken spanner suppression'),
            path=path,
            title='joining broken spanners ...',
            )

    @staticmethod
    def clef_color_job(path, undo=False) -> 'Job':
        r'''Makes clef color job.
        '''
        name = 'clef color'
        def match(tags):
            tags_ = abjad_tags.clef_color_tags(path)
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title='uncoloring clefs ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title='coloring clefs ...',
                )

    @staticmethod
    def clock_time_markup_job(path, undo=False) -> 'Job':
        r'''Makes clock time markup job.
        '''
        name = 'clock time markup'
        def match(tags) -> bool:
            tags_ = [abjad_tags.CLOCK_TIME_MARKUP]
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title=f'hiding {name} ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title=f'showing {name} ...',
                )

    @staticmethod
    def document_specific_job(path) -> 'Job':
        r'''Makes document-specific job.
        '''
        def deactivate(tags) -> bool:
            for tag in tags:
                if tag.startswith('+'):
                    return True
            return False
        def activate(tags) -> bool:
            if path.parent.is_segment():
                my_name = 'SEGMENT'
            else:
                my_name = path.name
            this_document = f'+{String(my_name).to_shout_case()}'
            not_this_document = f'-{String(my_name).to_shout_case()}'
            tags_ = [this_document, not_this_document]
            return bool(set(tags) & set(tags_))
        return Job(
            activate=(activate, 'this-document'),
            deactivate=(deactivate, 'document-specific'),
            deactivate_first=True,
            path=path,
            title='handling document-specific tags ...',
            )

    @staticmethod
    def dynamic_color_job(path, undo=False) -> 'Job':
        r'''Makes dynamic color job.
        '''
        name = 'dynamic color'
        def match(tags):
            tags_ = abjad_tags.dynamic_color_tags(path)
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title='uncoloring dynamics ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title='coloring dynamics ...',
                )

    @staticmethod
    def fermata_bar_line_job(path) -> 'Job':
        r'''Makes fermata bar line job.
        '''
        def activate(tags):
            return bool(set(tags) & set([abjad_tags.EOL_FERMATA]))
        # then deactivate non-EOL tags:
        bol_measure_numbers = path.get_metadatum('bol_measure_numbers')
        if bol_measure_numbers:
            eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
            last_measure_number = path.get_metadatum('last_measure_number')
            if last_measure_number is not None:
                eol_measure_numbers.append(last_measure_number)
            eol_measure_numbers = [f'MEASURE_{_}' for _ in eol_measure_numbers]
            tag = abjad_tags.EOL_FERMATA
            tags_ = eol_measure_numbers
            def deactivate(tags):
                if abjad_tags.EOL_FERMATA in tags:
                    if not bool(set(tags) & set(eol_measure_numbers)):
                        return True
                return False
        else:
            deactivate = None
        return Job(
            activate=(activate, 'bar line adjustment'),
            deactivate=(deactivate, 'EOL fermata bar line'),
            path=path,
            title='handling fermata bar lines ...',
            )

    @staticmethod
    def figure_name_markup_job(path, undo=False) -> 'Job':
        r'''Makes figure name markup job.
        '''
        name = 'figure name markup'
        def match(tags) -> bool:
            tags_ = [abjad_tags.FIGURE_NAME_MARKUP]
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title=f'hiding {name} ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title=f'showing {name} ...',
                )

    @staticmethod
    def instrument_color_job(path, undo=False) -> 'Job':
        r'''Makes instrument color job.
        '''
        name = 'instrument color'
        def match(tags):
            tags_ = abjad_tags.instrument_color_tags(path)
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title='uncoloring instruments ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title='coloring instruments ...',
                )

    @staticmethod
    def margin_markup_color_job(path, undo=False) -> 'Job':
        r'''Makes margin markup color job.
        '''
        name = 'margin markup color'
        def match(tags):
            tags_ = abjad_tags.margin_markup_color_tags(path)
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title='uncoloring margin markup ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title='coloring margin markup ...',
                )

    @staticmethod
    def measure_index_markup_job(path, undo=False) -> 'Job':
        r'''Makes measure index markup job.
        '''
        name = 'measure index markup'
        def match(tags) -> bool:
            tags_ = [abjad_tags.MEASURE_INDEX_MARKUP]
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title=f'hiding {name} ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title=f'showing {name} ...',
                )

    @staticmethod
    def measure_number_markup_job(path, undo=False) -> 'Job':
        r'''Makes measure number markup job.
        '''
        name = 'measure number markup'
        def match(tags) -> bool:
            tags_ = [abjad_tags.MEASURE_NUMBER_MARKUP]
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title=f'hiding {name} ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title=f'showing {name} ...',
                )

    @staticmethod
    def metronome_mark_color_job(path, undo=False) -> 'Job':
        r'''Makes metronome mark color job.
        '''
        def activate(tags):
            tags_ = abjad_tags.metronome_mark_color_expression_tags(path)
            return bool(set(tags) & set(tags_))
        def deactivate(tags):
            tags_ = abjad_tags.metronome_mark_color_suppression_tags(path)
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                activate=(deactivate, 'metronome mark color suppression'),
                deactivate=(activate, 'metronome mark color expression'),
                path=path,
                title='uncoloring metronome marks ...',
                )
        else:
            return Job(
                activate=(activate, 'metronome mark color expression'),
                deactivate=(deactivate, 'metronome mark color suppression'),
                path=path,
                title='coloring metronome marks ...',
                )

    @staticmethod
    def music_annotation_job(path, undo=False) -> 'Job':
        r'''Makes music annotation job.
        '''
        name = 'music annotation'
        def match(tags) -> bool:
            tags_ = abjad_tags.music_annotation_tags()
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title=f'hiding {name}s ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title=f'showing {name}s ...',
                )

    @staticmethod
    def persistent_indicator_color_job(path, undo=False) -> 'Job':
        r'''Makes persistent indicator color job.
        '''
        name = 'persistent indicator'
        activate_name = 'persistent indicator color expression'
        def activate(tags):
            tags_ = abjad_tags.persistent_indicator_color_expression_tags(path)
            return bool(set(tags) & set(tags_))
        deactivate_name = 'persistent indicator color suppression'
        def deactivate(tags):
            tags_ = abjad_tags.persistent_indicator_color_suppression_tags(
                path)
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                activate=(deactivate, deactivate_name),
                deactivate=(activate, activate_name),
                path=path,
                title=f'uncoloring {name}s ...',
                )
        else:
            return Job(
                activate=(activate, activate_name),
                deactivate=(deactivate, deactivate_name),
                path=path,
                title=f'coloring {name}s ...',
                )

    @staticmethod
    def shifted_clef_job(path) -> 'Job':
        r'''Makes shifted clef job.
        '''
        def activate(tags):
            return abjad_tags.SHIFTED_CLEF in tags
        # then deactivate shifted clefs at BOL:
        bol_measure_numbers = path.get_metadatum('bol_measure_numbers')
        if bol_measure_numbers:
            bol_measure_numbers = [f'MEASURE_{_}' for _ in bol_measure_numbers]
            def deactivate(tags):
                if abjad_tags.SHIFTED_CLEF not in tags:
                    return False
                if any(_ in tags for _ in bol_measure_numbers):
                    return True
                return False
        else:
            deactivate = None
        return Job(
            activate=(activate, 'shifted clef'),
            deactivate=(deactivate, 'BOL clef'),
            path=path,
            title='handling shifted clefs ...',
            )

    @staticmethod
    def spacing_markup_job(path, undo=False) -> 'Job':
        r'''Makes spacing markup job.
        '''
        name = 'spacing markup'
        def match(tags) -> bool:
            tags_ = abjad_tags.spacing_markup_tags()
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title=f'hiding {name} ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title=f'showing {name} ...',
                )

    @staticmethod
    def staff_lines_color_job(path, undo=False) -> 'Job':
        r'''Makes staff lines color job.
        '''
        name = 'staff lines color'
        def match(tags):
            tags_ = abjad_tags.staff_lines_color_tags(path)
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title='uncoloring staff lines ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title='coloring staff lines ...',
                )

    @staticmethod
    def stage_number_markup_job(path, undo=False) -> 'Job':
        r'''Makes stage number markup job.
        '''
        name = 'stage number markup'
        def match(tags) -> bool:
            tags_ = [abjad_tags.STAGE_NUMBER_MARKUP]
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title=f'hiding {name} ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title=f'showing {name} ...',
                )

    @staticmethod
    def time_signature_color_job(path, undo=False) -> 'Job':
        r'''Makes time signature color job.
        '''
        name = 'time signature color'
        def match(tags):
            tags_ = abjad_tags.time_signature_color_tags(path)
            return bool(set(tags) & set(tags_))
        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title='uncoloring time signatures ...',
                )
        else:
            return Job(
                activate=(match, name),
                path=path,
                title='coloring time signatures ...',
                )
