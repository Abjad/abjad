from . import format as _format
from .lilypondfile import LilyPondFile


class SegmentMaker:
    """
    Segment-maker.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Segment-makers"

    __slots__ = (
        "_lilypond_file",
        "_score",
    )

    ### INITIALIZER ###

    def __init__(self):
        self._lilypond_file = None
        self._score = None

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        """
        Delegates to ``abjad.format.compare_objects()``.
        """
        return _format.compare_objects(self, expr)

    def __hash__(self):
        """
        Hashes segment-maker.
        """
        hash_values = _format.get_hash_values(self)
        return hash(hash_values)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return _format.get_repr(self)

    ### PRIVATE METHODS ###

    def _make_lilypond_file(self):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def score(self):
        """
        Gets score.
        """
        return self._score

    ### PUBLIC METHODS ###

    def run(self) -> LilyPondFile:
        """
        Runs segment-maker.
        """
        lilypond_file = self._make_lilypond_file()
        self._lilypond_file = lilypond_file
        assert isinstance(self._lilypond_file, LilyPondFile)
        return self._lilypond_file
