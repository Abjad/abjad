# -*- encoding: utf-8 -*-
from scoremanager.wranglers.PackageWrangler import PackageWrangler


class ScoreInternalPackageWrangler(PackageWrangler):
    r'''Score-internal package wrangler.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_method(self):
        superclass = super(ScoreInternalPackageWrangler, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            '<': self.go_to_previous_package,
            '>': self.go_to_next_package,
            #
            'vr*': self.version_every_package,
            })
        return result

    ### PUBLIC METHODS ###

    def go_to_next_package(self):
        r'''Goes to next package.

        Returns none.
        '''
        self._go_to_next_package()

    def go_to_previous_package(self):
        r'''Goes to previous package.

        Returns none.
        '''
        self._go_to_previous_package()

    def version_every_package(self, confirm=True, display=True):
        r'''Versions every package.

        Returns none.
        '''
        managers = self._list_visible_asset_managers()
        messages = []
        messages.append('will copy ...')
        messages.append('')
        for manager in managers:
            messages.extend(manager._make_version_package_messages())
        self._io_manager._display(messages)
        result = self._io_manager._confirm()
        if self._session.is_backtracking:
            return
        if not result:
            return
        for manager in self._list_visible_asset_managers():
            manager.version_package(confirm=False, display=False)
        self._io_manager._display('')
        self._session._hide_next_redraw = True