from experimental.tools import statalservertools
from experimental.tools.settingtools.PayloadCallbackMixin import PayloadCallbackMixin


class StatalServerRequest(PayloadCallbackMixin):
    r'''Statal server request.

    The purpose of a statal server request is to function as the source of a setting.
    '''

    ### INITIALIZER ###
    
    def __init__(self, statal_server, payload_callbacks=None):
        assert isinstance(server, statalservertools.StatalServer)
        PayloadCallbackMixin.__init__(self, payload_callbacks=payload_callbacks)
        self._statal_server = statal_server

    ### SPECIAL METHODS ###

    def __call__(self):
        return self.statal_server(self)

    ### PRIVATE METHODS ###

    def _get_payload(self, score_specification=None, voice_name=None):
        raise NotImplementedError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def statal_server(self):
        return self._statal_server
