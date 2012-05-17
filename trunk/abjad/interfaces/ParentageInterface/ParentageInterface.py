from abjad.interfaces._Interface import _Interface


class ParentageInterface(_Interface):

    ### INITIALIZER ###

    def __init__(self, _client):
        _Interface.__init__(self, _client)

    ### PRIVATE METHODS ###

    def _cut(self):
        '''Client and parent cut completely.
        '''
        client, parent = self._client, self._client.parent
        if parent is not None:
            index = parent.index(client)
            parent._music.pop(index)
        self._ignore()

    def _ignore(self):
        '''Client forgets parent (but parent remembers client).
        '''
        self._client._mark_entire_score_tree_for_later_update('prolated')
        self._client._parent = None

    def _switch(self, new_parent):
        '''Remove client from parent and give client to new_parent.
        '''
        self._cut()
        self._client._parent = new_parent
        self._client._mark_entire_score_tree_for_later_update('prolated')
