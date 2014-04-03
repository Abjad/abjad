# -*- encoding: utf-8 -*-
from scoremanager import iotools
from scoremanager.iotools.ListEditor import ListEditor
from scoremanager.managers.MaterialPackageManager import MaterialPackageManager


class ListMaterialManager(MaterialPackageManager):
    r'''List material manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(ListMaterialManager, self)
        superclass.__init__(path=path, session=session)

    ### PUBLIC METHODS ###

    @staticmethod
    def _check_output_material(material):
        return isinstance(material, list)

    def _get_output_material_editor(self, target=None):
        from scoremanager import iotools
        editor = iotools.ListEditor(
            session=self._session,
            target=target,
            )
        return editor

    def _has_output_material_editor(self):
        return True

    def _run_first_time(self):
        self._session._is_autoadding = True
        if self._session.pending_user_input:
            pending_user_input = 'me ' + self._session.pending_user_input
            self._session._pending_user_input = pending_user_input
        else:
            self._session._pending_user_input = 'me'
        self._run()
        self._session._is_autoadding = False