from abjad.tools.abctools import AbjadObject


class SlotContributions(AbjadObject):
    r'''Slot contributions.
    '''

    __documentation_section__ = 'LilyPond formatting'

    __slots__ = (
        '_articulations',
        '_commands',
        '_comments',
        '_indicators',
        '_markup',
        '_spanners',
        '_spanner_starts',
        '_spanner_stops',
        '_stem_tremolos',
        '_trill_pitches',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._articulations = []
        self._commands = []
        self._comments = []
        self._indicators = []
        self._markup = []
        self._spanners = []
        self._spanner_starts = []
        self._spanner_stops = []
        self._stem_tremolos = []
        self._trill_pitches = []

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad.tools import systemtools
        names = [
            'articulations',
            'commands',
            'comments',
            'indicators',
            'markup',
            'spanners',
            'spanner_starts',
            'spanner_stops',
            'stem_tremolos',
            'trill_pitches',
            ]
        names = [x for x in names if getattr(self, x)]
        return systemtools.FormatSpecification(
            client=self,
            storage_format_kwargs_names=names,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def articulations(self):
        r'''Gets articulations.
        '''
        return self._articulations

    @property
    def commands(self):
        r'''Gets commands.
        '''
        return self._commands

    @property
    def comments(self):
        r'''Gets comments.
        '''
        return self._comments

    @property
    def has_contributions(self):
        r'''Is true when has contributions.
        '''
        contribution_categories = (
            'articulations',
            'commands',
            'comments',
            'indicators',
            'markup',
            'spanners',
            'spanner_starts',
            'spanner_stops',
            'stem_tremolos',
            'trill_pitches',
            )
        return any(getattr(self, contribution_category)
            for contribution_category in contribution_categories)

    @property
    def indicators(self):
        r'''Gets indicators.
        '''
        return self._indicators

    @property
    def markup(self):
        r'''Gets markup.
        '''
        return self._markup

    @property
    def spanner_starts(self):
        r'''Gets spanner starts.
        '''
        return self._spanner_starts

    @property
    def spanner_stops(self):
        r'''Gets spanner stops.
        '''
        return self._spanner_stops

    @property
    def spanners(self):
        r'''Gets spanners.
        '''
        return self._spanners

    @property
    def stem_tremolos(self):
        r'''Gets stem tremolos.
        '''
        return self._stem_tremolos

    @property
    def trill_pitches(self):
        '''Gets trill pitches.
        '''
        return self._trill_pitches

    ### PUBLIC METHODS ###

    def alphabetize(self):
        r'''Alphabetizes indicators.
        '''
        self._indicators.sort()

    def get(self, identifier):
        r'''Gets `identifier`.
        '''
        return getattr(self, identifier)

    def make_immutable(self):
        r'''Makes contributions immutable.
        '''
        self._articulations = tuple(sorted(self.articulations))
        self._commands = tuple(self.commands)
        self._comments = tuple(self.comments)
        self._indicators = tuple(self.indicators)
        self._markup = tuple(self.markup)
        self._spanners = tuple(self.spanners)
        self._spanner_starts = tuple(self.spanner_starts)
        self._spanner_stops = tuple(self.spanner_stops)
        self._stem_tremolos = tuple(self.stem_tremolos)
        self._trill_pitches = tuple(self.trill_pitches)

    def update(self, slot_contributions):
        r'''Updates contributions.
        '''
        assert isinstance(slot_contributions, type(self))
        self.articulations.extend(slot_contributions.articulations)
        self.commands.extend(slot_contributions.commands)
        self.comments.extend(slot_contributions.comments)
        self.indicators.extend(slot_contributions.indicators)
        self.markup.extend(slot_contributions.markup)
        self.spanners.extend(slot_contributions.spanners)
        self.spanner_starts.extend(slot_contributions.spanner_starts)
        self.spanner_stops.extend(slot_contributions.spanner_stops)
        self.stem_tremolos.extend(slot_contributions.stem_tremolos)
        self.trill_pitches.extend(slot_contributions.trill_pitches)
