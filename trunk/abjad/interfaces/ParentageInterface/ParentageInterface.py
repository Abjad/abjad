from abjad.interfaces._Interface import _Interface


class ParentageInterface(_Interface):
    '''Bundle attributes relating to the containers within which any Abjad component nests.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_parent', )

    ### INITIALIZER ###

    def __init__(self, _client):
        _Interface.__init__(self, _client)
        self._parent = None

    ### PRIVATE METHODS ###

    def _cut(self):
        '''Client and parent cut completely.'''
        client, parent = self._client, self.parent
        if parent is not None:
            index = parent.index(client)
            parent._music.pop(index)
        self._ignore()

    def _ignore(self):
        '''Client forgets parent (but parent remembers client).'''
        self._client._mark_entire_score_tree_for_later_update('prolated')
        self._parent = None

    def _switch(self, new_parent):
        '''Remove client from parent and give client to new_parent.'''
        self._cut()
        self._parent = new_parent
        self._client._mark_entire_score_tree_for_later_update('prolated')

    ### PUBLIC PROPERTIES ###

    @property
    def parent(self):
        '''Read-only reference to immediate parent of `component`.

        ::

            abjad> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
            abjad> staff = Staff([tuplet])
            abjad> note = staff.leaves[0]
            abjad> note._parentage.parent
            FixedDurationTuplet(1/4, [c'8, d'8, e'8])

        Equivalent to ``component._parentage.proper_parentage[0]`` for those components
        with proper parentage. Otherwise ``None``.
        '''

        return self._parent
