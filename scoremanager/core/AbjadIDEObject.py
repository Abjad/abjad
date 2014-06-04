# -*- encoding: utf-8 -*-
import abc
from abjad.tools import stringtools


class AbjadIDEObject(object):
    r'''Abjad IDE object.

    '''

    ### CLASS VARIABLES ###

    __meta__ = abc.ABCMeta

    __slots__ = (
        '_configuration',
        '_controller_context',
        '_io_manager',
        '_session',
        '_transcript',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, session=None):
        from scoremanager import core
        from scoremanager import iotools
        self._configuration = core.AbjadIDEConfiguration()
        self._session = session or core.Session()
        self._io_manager = iotools.IOManager(
            client=self,
            session=self._session,
            )
        self._transcript = self._session.transcript
        self._controller_context = iotools.ControllerContext(controller=self)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when types are the same. Otherwise false.

        Returns boolean.
        '''
        return type(self) is type(expr)

    def __hash__(self):
        r'''Hashes score manager object.
        '''
        return hash((type(self), self._session))

    def __ne__(self, expr):
        r'''Is true when types are not the same. Otherwise false.

        Returns boolean.
        '''
        return not self == expr

    def __repr__(self):
        r'''Gets interpreter representation of score manager object.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _spaced_class_name(self):
        return stringtools.to_space_delimited_lowercase(type(self).__name__)
