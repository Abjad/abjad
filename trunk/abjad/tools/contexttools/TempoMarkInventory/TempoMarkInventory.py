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
        return '{}({})'.format(self._class_name, list.__repr__(self))

    ### PRIVATE ATTRIBUTES ###

    @property
    def _class_name(self):
        return type(self).__name__

    @property
    def _class_name_with_tools_package(self):
        return '{}.{}'.format(self._tools_package, self._class_name)

    @property
    def _contents_repr_with_tools_package(self):
        part_reprs = []
        for element in self:
            part_repr = getattr(element, '_repr_with_tools_package', repr(element))
            part_reprs.append(part_repr)
        return ', '.join(part_reprs)

    @property
    def _repr_with_tools_package(self):
        return '{}([{}])'.format(
            self._class_name_with_tools_package, self._contents_repr_with_tools_package)

    @property
    def _tools_package(self):
        for part in reversed(self.__module__.split('.')):
            if not part == self._class_name:
                return part
        
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
