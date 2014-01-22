# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class LilyPondFormatBundle(AbjadObject):
    r'''LilyPond format bundle.

    Transient class created to hold the collection of all
    format contributions generated on behalf of a single component.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_before',
        '_after',
        '_opening',
        '_closing',
        '_right',
        '_context_settings',
        '_grob_overrides',
        '_grob_reverts',
        )

    ### INNER CLASS DEFINITION ###

    class SlotContributions(AbjadObject):
        r'''Slot contributions.
        '''

        __slots__ = (
            '_articulations',
            '_commands',
            '_comments',
            '_indicators',
            '_markup',
            '_spanners',
            '_stem_tremolos',
            )

        def __init__(self):
            self._articulations = []
            self._commands = []
            self._comments = []
            self._indicators = []
            self._markup = []
            self._spanners = []
            self._stem_tremolos = []

        @property
        def _storage_format_specification(self):
            from abjad.tools import systemtools
            keyword_argument_names = [
                'articulations',
                'commands',
                'comments',
                'indicators',
                'markup',
                'spanners',
                'stem_tremolos',
                ]
            keyword_argument_names = [x for x in keyword_argument_names
                if getattr(self, x)]
            return systemtools.StorageFormatSpecification(
                self,
                keyword_argument_names=keyword_argument_names,
                )

        @property
        def articulations(self):
            return self._articulations

        @property
        def comments(self):
            return self._comments

        @property
        def commands(self):
            return self._commands

        @property
        def has_contributions(self):
            contribution_categories = (
                'articulations',
                'commands',
                'comments',
                'indicators',
                'markup',
                'spanners',
                'stem_tremolos',
                )
            return any(getattr(self, contribution_category)
                for contribution_category in contribution_categories)

        @property
        def indicators(self):
            return self._indicators

        @property
        def markup(self):
            return self._markup

        @property
        def spanners(self):
            return self._spanners

        @property
        def stem_tremolos(self):
            return self._stem_tremolos

        def alphabetize(self):
            self._indicators.sort()

        def get(self, identifier):
            return getattr(self, identifier)

        def make_immutable(self):
            self._articulations = tuple(sorted(self.articulations))
            self._commands = tuple(self.commands)
            self._comments = tuple(self.comments)
            self._indicators = tuple(self.indicators)
            self._markup = tuple(self.markup)
            self._spanners = tuple(self.spanners)
            self._stem_tremolos = tuple(self.stem_tremolos)

        def update(self, slot_contributions):
            assert isinstance(slot_contributions, type(self))
            self.articulations.extend(slot_contributions.articulations)
            self.commands.extend(slot_contributions.commands)
            self.comments.extend(slot_contributions.comments)
            self.indicators.extend(slot_contributions.indicators)
            self.markup.extend(slot_contributions.markup)
            self.spanners.extend(slot_contributions.spanners)
            self.stem_tremolos.extend(slot_contributions.stem_tremolos)

    ### INITIALIZER ###

    def __init__(self):
        self._before = self.SlotContributions()
        self._after = self.SlotContributions()
        self._opening = self.SlotContributions()
        self._closing = self.SlotContributions()
        self._right = self.SlotContributions()
        self._context_settings = []
        self._grob_overrides = []
        self._grob_reverts = []

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        slot_contribution_names = (
            'before',
            'after',
            'opening',
            'closing',
            'right',
            )
        grob_contribution_names = (
            'context_settings',
            'grob_overrides',
            'grob_reverts',
            )
        keyword_argument_names = [x for x in slot_contribution_names
            if getattr(self, x).has_contributions]
        keyword_argument_names.extend(x for x in grob_contribution_names
            if getattr(self, x))
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def after(self):
        r'''After slot contributions.

        Returns slot contributions object.
        '''
        return self._after

    @property
    def before(self):
        r'''Before slot contributions.

        Returns slot contributions object.
        '''
        return self._before

    @property
    def closing(self):
        r'''Closing slot contributions.

        Returns slot contributions object.
        '''
        return self._closing

    @property
    def context_settings(self):
        r'''Context setting format contributions.

        Returns list.
        '''
        return self._context_settings

    @property
    def grob_overrides(self):
        r'''Grob override format contributions.

        Returns list.
        '''
        return self._grob_overrides

    @property
    def grob_reverts(self):
        r'''Grob revert format contributions.

        Returns list.
        '''
        return self._grob_reverts

    @property
    def opening(self):
        r'''Opening slot contributions.

        Returns slot contributions object.
        '''
        return self._opening

    @property
    def right(self):
        r'''Right slot contributions.

        Returns slot contributions object.
        '''
        return self._right

    ### PUBLIC METHODS ###

    def alphabetize(self):
        r'''Alphabetizes format contributions in each slot.

        Returns none.
        '''
        self.before.alphabetize()
        self.after.alphabetize()
        self.opening.alphabetize()
        self.closing.alphabetize()
        self.right.alphabetize()
        self._context_settings.sort()
        self._grob_overrides.sort()
        self._grob_reverts.sort()

    def get(self, identifier):
        r'''Gets `identifier`.

        Returns format contributions object or list.
        '''
        return getattr(self, identifier)

    def make_immutable(self):
        r'''Makes each slot immutable.

        Returns none.
        '''
        self.before.make_immutable()
        self.after.make_immutable()
        self.opening.make_immutable()
        self.closing.make_immutable()
        self.right.make_immutable()
        self._context_settings = tuple(self.context_settings)
        self._grob_overrides = tuple(self.grob_overrides)
        self._grob_reverts = tuple(self.grob_reverts)

    def update(self, format_bundle):
        r'''Updates format bundle with all format contributions in
        `format_bundle`.

        Returns none.
        '''
        assert isinstance(format_bundle, type(self))
        self.before.update(format_bundle.before)
        self.after.update(format_bundle.after)
        self.opening.update(format_bundle.opening)
        self.closing.update(format_bundle.closing)
        self.right.update(format_bundle.right)
        self.context_settings.extend(format_bundle.context_settings)
        self.grob_overrides.extend(format_bundle.grob_overrides)
        self.grob_reverts.extend(format_bundle.grob_reverts)
