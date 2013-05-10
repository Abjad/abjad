import abc
import inspect
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.scoremanagertools.core.ScoreManagerConfiguration import \
    ScoreManagerConfiguration


class ScoreManagerObject(AbjadObject):

    ### CLASS ATTRIBUTES ###

    __meta__ = abc.ABCMeta
    configuration = ScoreManagerConfiguration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        self._session = session or scoremanagertools.core.Session()
        self._io = scoremanagertools.core.IO(session=self._session)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _backtracking_source(self):
        return

    @property
    def _space_delimited_lowercase_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(self._class_name)

    @property
    def _spaced_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(self._class_name)

    ### PUBLIC METHODS ###

    def where(self):
        if self._session.enable_where:
            return inspect.stack()[1]
