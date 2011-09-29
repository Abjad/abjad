class _LilyPondParserComponent(object):

    def __init__(self, client):
        self._client = client

    ### PUBLIC ATTRIBUTES ###

    @property
    def grammar(self):
        return self._client._grammar

    @property
    def input_string(self):
        return self._client._input_string

    @property
    def symbol_table(self):
        return self._client._symbol_table
