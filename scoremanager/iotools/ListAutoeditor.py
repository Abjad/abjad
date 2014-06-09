# -*- encoding: utf-8 -*-
import types
from abjad.tools import datastructuretools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.iotools.CollectionAutoeditor import CollectionAutoeditor


class ListAutoeditor(CollectionAutoeditor):
    r'''List editor.

    ::

        >>> session = scoremanager.core.Session()
        >>> autoeditor = scoremanager.iotools.CollectionAutoeditor(
        ...     session=session,
        ...     )
        >>> autoeditor._target = ['first', 'second', 'third']
        >>> autoeditor
        <CollectionAutoeditor(target=list)>

    ::

        >>> autoeditor._run(input_='rm 1 q')

    ::

        >>> autoeditor
        <CollectionAutoeditor(target=list)>

    '''

    ### CLASS ATTRIBUTES ###

    pass