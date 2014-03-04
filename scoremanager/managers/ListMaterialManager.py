# -*- encoding: utf-8 -*-
from scoremanager import iotools
from scoremanager.editors.ListEditor import ListEditor
from scoremanager.managers.MaterialManager import MaterialManager


class ListMaterialManager(MaterialManager):

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(ListMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._generic_output_name = 'list'

    ### PUBLIC METHODS ###

    @staticmethod
    def _check_output_material(material):
        return isinstance(material, list)

    @staticmethod
    def _get_output_material_editor(target=None, session=None):
        from scoremanager import editors
        editor = editors.ListEditor(
            session=session,
            target=target,
            )
        return editor

    def _run_first_time(self):
        self._session._is_autoadding = True
        self._run(pending_user_input='omi')
        self._session._is_autoadding = False
