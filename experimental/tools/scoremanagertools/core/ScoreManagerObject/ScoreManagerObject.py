import inspect
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.scoremanagertools.core.ScoreManagerConfiguration import \
    ScoreManagerConfiguration


class ScoreManagerObject(AbjadObject):

    ### CLASS ATTRIBUTES ###

    configuration = ScoreManagerConfiguration()

    ### INITIALIZER ###

    def __init__(self, session=None):
        from experimental.tools import scoremanagertools
        self._session = session or scoremanagertools.core.Session()
        self._io = scoremanagertools.core.IO(session=self.session)

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

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def io(self):
        return self._io

    @property
    def session(self):
        return self._session

    @property
    def transcript_signature(self):
        return self.session.complete_transcript.signature

    ### PUBLIC METHODS ###

    def where(self):
        if self.session.enable_where:
            return inspect.stack()[1]
