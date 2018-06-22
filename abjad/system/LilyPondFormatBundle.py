from abjad.system.AbjadObject import AbjadObject


class LilyPondFormatBundle(AbjadObject):
    """
    LilyPond format bundle.

    Transient class created to hold the collection of all
    format contributions generated on behalf of a single component.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'LilyPond formatting'

    __slots__ = (
        '_absolute_after',
        '_absolute_before',
        '_after',
        '_before',
        '_closing',
        '_context_settings',
        '_grob_overrides',
        '_grob_reverts',
        '_opening',
        )

    ### INITIALIZER ###

    def __init__(self):
        import abjad
        self._absolute_after = abjad.SlotContributions()
        self._absolute_before = abjad.SlotContributions()
        self._before = abjad.SlotContributions()
        self._after = abjad.SlotContributions()
        self._opening = abjad.SlotContributions()
        self._closing = abjad.SlotContributions()
        self._context_settings = []
        self._grob_overrides = []
        self._grob_reverts = []

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        slot_contribution_names = (
            'absolute_before',
            'absolute_after',
            'before',
            'after',
            'opening',
            'closing',
            )
        grob_contribution_names = (
            'context_settings',
            'grob_overrides',
            'grob_reverts',
            )
        names = [_ for _ in slot_contribution_names
            if getattr(self, _).has_contributions]
        names.extend(_ for _ in grob_contribution_names
            if getattr(self, _))
        return abjad.FormatSpecification(
            client=self,
            storage_format_kwargs_names=names,
            )

    ### PUBLIC METHODS ###

    def get(self, identifier):
        """
        Gets ``identifier``.

        Returns format contributions object or list.
        """
        return getattr(self, identifier)

    def sort_overrides(self):
        """
        Makes each slot immutable.

        Returns none.
        """
        self._context_settings = tuple(sorted(set(self.context_settings)))
        self._grob_overrides = tuple(sorted(set(self.grob_overrides)))
        self._grob_reverts = tuple(sorted(set(self.grob_reverts)))

    def tag_format_contributions(self, tag, deactivate=None):
        """
        Tags format contributions with string ``tag``.

        Returns none.
        """
        import abjad
        self.absolute_before.tag(tag, deactivate)
        self.absolute_after.tag(tag, deactivate)
        self.before.tag(tag, deactivate)
        self.after.tag(tag, deactivate)
        self.opening.tag(tag, deactivate)
        self.closing.tag(tag, deactivate)
        self._context_settings = abjad.LilyPondFormatManager.tag(
            self.context_settings,
            tag,
            deactivate,
            )
        self._grob_overrides = abjad.LilyPondFormatManager.tag(
            self.grob_overrides,
            tag,
            deactivate,
            )
        self._grob_reverts = abjad.LilyPondFormatManager.tag(
            self.grob_reverts,
            tag,
            deactivate,
            )

    def update(self, format_bundle):
        """
        Updates format bundle with all format contributions in
        ``format_bundle``.

        Returns none.
        """
        if hasattr(format_bundle, '_get_lilypond_format_bundle'):
            format_bundle = format_bundle._get_lilypond_format_bundle()
        assert isinstance(format_bundle, type(self))
        self.absolute_before.update(format_bundle.absolute_before)
        self.absolute_after.update(format_bundle.absolute_after)
        self.before.update(format_bundle.before)
        self.after.update(format_bundle.after)
        self.opening.update(format_bundle.opening)
        self.closing.update(format_bundle.closing)
        self.context_settings.extend(format_bundle.context_settings)
        self.grob_overrides.extend(format_bundle.grob_overrides)
        self.grob_reverts.extend(format_bundle.grob_reverts)

    ### PUBLIC PROPERTIES ###

    @property
    def absolute_after(self):
        """
        Aboslute after slot contributions.

        Returns slot contributions object.
        """
        return self._absolute_after

    @property
    def absolute_before(self):
        """
        Absolute before slot contributions.

        Returns slot contributions object.
        """
        return self._absolute_before

    @property
    def after(self):
        """
        After slot contributions.

        Returns slot contributions object.
        """
        return self._after

    @property
    def before(self):
        """
        Before slot contributions.

        Returns slot contributions object.
        """
        return self._before

    @property
    def closing(self):
        """
        Closing slot contributions.

        Returns slot contributions object.
        """
        return self._closing

    @property
    def context_settings(self):
        """
        Context setting format contributions.

        Returns list.
        """
        return self._context_settings

    @property
    def grob_overrides(self):
        """
        Grob override format contributions.

        Returns list.
        """
        return self._grob_overrides

    @property
    def grob_reverts(self):
        """
        Grob revert format contributions.

        Returns list.
        """
        return self._grob_reverts

    @property
    def opening(self):
        """
        Opening slot contributions.

        Returns slot contributions object.
        """
        return self._opening

#    @property
#    def right(self):
#        """
#        Right slot contributions.
#
#        Returns slot contributions object.
#        """
#        return self._right
