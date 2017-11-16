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

    def tag(self, tag, deactivate):
        r'''Tags contributions.
        '''
        tag = ' %! ' + tag
        deactivation = '%%% '
        articulations = [_ + tag for _ in self.articulations]
        if deactivate:
            articulations = [deactivation + _ for _ in articulations]
        self._articulations = articulations
        commands = [_ + tag for _ in self.commands]
        if deactivate:
            commands = [deactivation + _ for _ in commands]
        self._commands = commands
        comments = [_ + tag for _ in self.comments]
        if deactivate:
            comments = [deactivation + _ for _ in comments]
        self._comments = comments
        indicators = [_ + tag for _ in self.indicators]
        if deactivate:
            indicators = [deactivation + _ for _ in indicators]
        self._indicators = indicators
        markup = [_ + tag for _ in self.markup]
        if deactivate:
            markup = [deactivation + _ for _ in markup]
        self._markup = markup
        spanners = [_ + tag for _ in self.spanners]
        if deactivate:
            spanners = [deactivation + _ for _ in spanners]
        self._spanners = spanners
        spanner_starts = [_ + tag for _ in self.spanner_starts]
        if deactivate:
            spanner_starts = [deactivation + _ for _ in spanner_starts]
        self._spanner_starts = spanner_starts
        spanner_stops = [_ + tag for _ in self.spanner_stops]
        if deactivate:
            spanner_stops = [deactivation + _ for _ in spanner_stops]
        self._spanner_stops = spanner_stops
        stem_tremolos = [_ + tag for _ in self.stem_tremolos]
        if deactivate:
            stem_tremolos = [deactivation + _ for _ in stem_tremolos]
        self._stem_tremolos = stem_tremolos
        trill_pitches = [_ + tag for _ in self.trill_pitches]
        if deactivate:
            trill_pitches = [deactivation + _ for _ in trill_pitches]
        self._trill_pitches = trill_pitches

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
