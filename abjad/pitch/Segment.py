import abc
import collections
import types
from abjad import enums
from abjad import mathtools
from abjad.system.FormatSpecification import FormatSpecification
from abjad.utilities.Duration import Duration
from abjad.utilities.TypedTuple import TypedTuple


class Segment(TypedTuple):
    """
    Abstract segment.
    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_equivalence_markup',
        '_expression',
        )

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        import abjad
        prototype = (
            collections.Iterator,
            types.GeneratorType,
            )
        if isinstance(items, str):
            items = items.split()
        elif isinstance(items, prototype):
            items = [_ for _ in items]
        if item_class is None:
            item_class = self._named_item_class
            if items is not None:
                if (isinstance(items, abjad.TypedCollection) and
                    issubclass(items.item_class, self._parent_item_class)):
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
        if isinstance(item_class, str):
            import abjad
            globals_ = {'abjad': abjad}
            globals_.update(abjad.__dict__.copy())
            item_class = eval(item_class, globals_)
        assert issubclass(item_class, self._parent_item_class)
        TypedTuple.__init__(
            self,
            items=items,
            item_class=item_class,
            )
        self._equivalence_markup = None
        self._expression = None

    ### SPECIAL METHODS ###

    def __illustrate__(
        self,
        markup_direction=enums.Up,
        figure_name=None,
        **keywords
        ):
        """
        Illustrates segment.

        Returns LilyPond file.
        """
        import abjad
        notes = []
        for item in self:
            note = abjad.Note(item, Duration(1, 8))
            notes.append(note)
        markup = None
        if self._equivalence_markup:
            markup = self._equivalence_markup
        if isinstance(figure_name, str):
            figure_name = abjad.Markup(figure_name)
        if figure_name is not None:
            markup = figure_name
        if markup is not None:
            direction = markup_direction
            markup = abjad.new(markup, direction=direction)
            abjad.attach(markup, notes[0])
        voice = abjad.Voice(notes)
        staff = abjad.Staff([voice])
        score = abjad.Score([staff])
        score.add_final_bar_line()
        abjad.override(score).bar_line.transparent = True
        abjad.override(score).bar_number.stencil = False
        abjad.override(score).beam.stencil = False
        abjad.override(score).flag.stencil = False
        abjad.override(score).stem.stencil = False
        abjad.override(score).time_signature.stencil = False
        string = r'\override Score.BarLine.transparent = ##f'
        command = abjad.LilyPondLiteral(string, 'after')
        last_leaf = abjad.select(score).leaves()[-1]
        abjad.attach(command, last_leaf)
        moment = abjad.SchemeMoment((1, 12))
        abjad.setting(score).proportional_notation_duration = moment
        lilypond_file = abjad.LilyPondFile.new(music=score)
        if 'title' in keywords:
            title = keywords.get('title')
            if not isinstance(title, abjad.Markup):
                title = abjad.Markup(title)
            lilypond_file.header_block.title = title
        if 'subtitle' in keywords:
            markup = abjad.Markup(keywords.get('subtitle'))
            lilypond_file.header_block.subtitle = markup
        command = abjad.LilyPondLiteral(r'\accidentalStyle forget')
        lilypond_file.layout_block.items.append(command)
        lilypond_file.layout_block.indent = 0
        string = 'markup-system-spacing.padding = 8'
        command = abjad.LilyPondLiteral(string)
        lilypond_file.paper_block.items.append(command)
        string = 'system-system-spacing.padding = 10'
        command = abjad.LilyPondLiteral(string)
        lilypond_file.paper_block.items.append(command)
        string = 'top-markup-spacing.padding = 4'
        command = abjad.LilyPondLiteral(string)
        lilypond_file.paper_block.items.append(command)
        return lilypond_file

    def __str__(self):
        """
        Gets string representation of segment.

        Returns string.
        """
        items = [str(_) for _ in self]
        return '<{}>'.format(', '.join(items))

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
            items = [
                mathtools.integer_equivalent_number_to_integer(float(x.number))
                for x in self
                ]
        elif hasattr(self.item_class, '__abs__'):
            items = [abs(x) for x in self]
        else:
            message = 'invalid item class: {!r}.'
            message = message.format(self.item_class)
            raise ValueError(message)
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            repr_kwargs_names=['name'],
            repr_args_values=[items],
            storage_format_args_values=[tuple(self._collection)],
            )

    def _get_padded_string(self, width=2):
        strings = []
        for item in self:
            string = '{{!s:>{}}}'
            string = string.format(width)
            string = string.format(item)
            strings.append(string)
        return '<{}>'.format(', '.join(strings))

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        """
        Makes segment from `selection`.

        Returns new segment.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def has_duplicates(self):
        """
        Is true when segment has duplicates.

        Returns true or false.
        """
        raise NotImplementedError
