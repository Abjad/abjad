# -*- coding: utf-8 -*-
import abc
import collections
import types
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.datastructuretools import TypedTuple


class Segment(TypedTuple):
    r'''Segment base class.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        item_class=None,
        ):
        from abjad.tools import datastructuretools
        prototype = (
            collections.Iterator,
            types.GeneratorType,
            )
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, prototype):
            items = [item for item in items]
        if item_class is None:
            item_class = self._named_item_class
            if items is not None:
                if isinstance(items, datastructuretools.TypedCollection) and \
                    issubclass(items.item_class, self._parent_item_class):
                    item_class = items.item_class
                elif len(items):
                    if isinstance(items, collections.Set):
                        items = tuple(items)
                    if isinstance(items[0], str):
                        item_class = self._named_item_class
                    elif isinstance(items[0], (int, float)):
                        item_class = self._numbered_item_class
                    elif isinstance(items[0], self._parent_item_class):
                        item_class = type(items[0])
        assert issubclass(item_class, self._parent_item_class)
        TypedTuple.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __illustrate__(self, **kwargs):
        r'''Illustrates segment.

        Returns LilyPond file.
        '''
        from abjad.tools import durationtools
        from abjad.tools import indicatortools
        from abjad.tools import lilypondfiletools
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        from abjad.tools import schemetools
        from abjad.tools.topleveltools import attach
        from abjad.tools.topleveltools import override
        from abjad.tools.topleveltools import select
        from abjad.tools.topleveltools import set_
        notes = []
        for item in self:
            note = scoretools.Note(item, durationtools.Duration(1, 8))
            notes.append(note)
        voice = scoretools.Voice(notes)
        staff = scoretools.Staff([voice])
        score = scoretools.Score([staff])
        score.add_final_bar_line()
        override(score).bar_line.transparent = True
        override(score).bar_number.stencil = False
        override(score).beam.stencil = False
        override(score).flag.stencil = False
        override(score).stem.stencil = False
        override(score).time_signature.stencil = False
        string = 'override Score.BarLine.transparent = ##f'
        command = indicatortools.LilyPondCommand(string, format_slot='after')
        last_leaf = select().by_leaf()(score)[-1][-1]
        attach(command, last_leaf)
        moment = schemetools.SchemeMoment((1, 12))
        set_(score).proportional_notation_duration = moment
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(
            global_staff_size=12,
            music=score,
            )
        if 'title' in kwargs:
            title = kwargs.get('title')
            if not isinstance(title, markuptools.Markup):
                title = markuptools.Markup(title)
            lilypond_file.header_block.title = title
        if 'subtitle' in kwargs:
            markup = markuptools.Markup(kwargs.get('subtitle'))
            lilypond_file.header_block.subtitle = markup
        command = indicatortools.LilyPondCommand('accidentalStyle forget')
        lilypond_file.layout_block.items.append(command)
        lilypond_file.layout_block.indent = 0
        string = 'markup-system-spacing.padding = 8'
        command = indicatortools.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        string = 'system-system-spacing.padding = 10'
        command = indicatortools.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        string = 'top-markup-spacing.padding = 4'
        command = indicatortools.LilyPondCommand(string, prefix='')
        lilypond_file.paper_block.items.append(command)
        return lilypond_file

    def __str__(self):
        r'''Gets string representation of segment.

        Returns string.
        '''
        parts = [str(x) for x in self]
        return '<{}>'.format(', '.join(parts))

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        items = []
        if self.item_class.__name__.startswith('Named'):
            items = [str(x) for x in self]
        elif hasattr(self.item_class, 'pitch_number'):
            items = [x.pitch_number for x in self]
        elif hasattr(self.item_class, 'pitch_class_number'):
            items = [x.pitch_class_number for x in self]
        elif self.item_class.__name__.startswith('Numbered'):
            items = [mathtools.integer_equivalent_number_to_integer(float(x))
                for x in self]
        elif hasattr(self.item_class, '__abs__'):
            items = [abs(x) for x in self]
        else:
            raise ValueError
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_kwargs_names=[],
            repr_args_values=[items],
            storage_format_args_values=[tuple(self._collection)],
            )

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes segment from `selection`.

        Returns new segment.
        '''
        raise NotImplementedError

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        return self._item_class

    @abc.abstractproperty
    def _named_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _numbered_item_class(self):
        raise NotImplementedError

    @abc.abstractproperty
    def _parent_item_class(self):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def has_duplicates(self):
        r'''Is true when segment has duplicates. Otherwise false.

        Returns true or false.
        '''
        raise NotImplementedError
