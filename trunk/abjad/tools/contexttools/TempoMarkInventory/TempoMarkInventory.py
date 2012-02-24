from abjad.tools.contexttools.TempoMark import TempoMark


class TempoMarkInventory(list):
    r'''.. versionadded:: 2.7

    Abjad model of an ordered list of tempo marks::

        abjad> contexttools.TempoMarkInventory([('Andante', Duration(1, 8), 72), ('Allegro', Duration(1, 8), 84)])
        TempoMarkInventory([TempoMark('Andante', Duration(1, 8), 72), TempoMark('Allegro', Duration(1, 8), 84)])

    Tempo mark inventories are mutable.
    '''

    def __init__(self, tempo_mark_tokens=None):
        list.__init__(self)
        tempo_mark_tokens = tempo_mark_tokens or []
        tempo_marks = []
        for tempo_mark_token in tempo_mark_tokens:
            tempo_marks.append(TempoMark(tempo_mark_token))
        self.extend(tempo_marks)

    ### OVERLOADS ###

    def __contains__(self, tempo_mark_token):
        tempo_mark = TempoMark(tempo_mark_token)
        return list.__contains__(self, tempo_mark)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, list.__repr__(self))

    ### PUBLIC METHODS ###

    def append(self, tempo_mark_token):
        '''Change `tempo_mark_token` to tempo mark and append::

            abjad> tempo_mark_inventory = contexttools.TempoMarkInventory([('Andante', Duration(1, 8), 72)])
            abjad> tempo_mark_inventory.append(('Allegro', Duration(1, 8), 84))

        ::

            abjad> tempo_mark_inventory
            TempoMarkInventory([TempoMark('Andante', Duration(1, 8), 72), TempoMark('Allegro', Duration(1, 8), 84)])

        Return none.
        '''
        tempo_mark = TempoMark(tempo_mark_token)
        list.append(self, tempo_mark)

    def extend(self, tempo_mark_tokens):
        '''Change `tempo_mark_tokens` to tempo marks and extend::

            abjad> tempo_mark_inventory = contexttools.TempoMarkInventory([('Andante', Duration(1, 8), 72)])
            abjad> tempo_mark_inventory.extend([(Duration(1, 8), 84), (Duration(1, 8), 96)])

        ::

            abjad> tempo_mark_inventory
            TempoMarkInventory([TempoMark('Andante', Duration(1, 8), 72), TempoMark(Duration(1, 8), 84), TempoMark(Duration(1, 8), 96)])

        Return none.
        '''
        tempo_marks = []
        for tempo_mark_token in tempo_mark_tokens:
            tempo_marks.append(TempoMark(tempo_mark_token))
        list.extend(self, tempo_marks)
