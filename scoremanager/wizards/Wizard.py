# -*- encoding: utf-8 -*-
import abc
from scoremanager.core.Controller import Controller


class Wizard(Controller):
    r'''Wizard.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_selector',
        '_target',
        '_target_editor_class_name_suffix',
        )

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        Controller.__init__(self, session=session)
        self._selector = None
        self._target = target
        self._target_editor_class_name_suffix = 'Autoeditor'

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _breadcrumb(self):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def target(self):
        r'''Gets wizard target.

        Returns object or none.
        '''
        return self._target