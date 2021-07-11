from .lilypondfile import LilyPondFile
from .storage import StorageFormatManager


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
        Is true if ``expr`` is a segment-maker with equivalent properties.
        """
        return StorageFormatManager.compare_objects(self, expr)

    def __hash__(self):
        """
        Hashes segment-maker.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        return hash(hash_values)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

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

    def run(self):
        """
        Runs segment-maker.
        """
        lilypond_file = self._make_lilypond_file()
        self._lilypond_file = lilypond_file
        assert isinstance(self._lilypond_file, LilyPondFile)
        return self._lilypond_file
