from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.ContextSelection.ContextSelection import ContextSelection
from experimental.specificationtools.Selection.Selection import Selection
from experimental.specificationtools.ContextSetting.ContextSetting import ContextSetting
import copy


class Directive(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        mandatory_argument_values, keyword_argument_values = self._get_input_argument_values(*args, **kwargs)
        target, attribute, source = mandatory_argument_values
        persistent, truncate = keyword_argument_values
        self.target = target
        self.attribute = attribute
        self.source = source
        self.persistent = persistent
        self.truncate = truncate

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if not self._mandatory_argument_values == expr._mandatory_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return (
            'persistent',
            'truncate',
            )

    @property
    def _mandatory_argument_values(self):
        return (
            self.target,
            self.attribute,
            self.source,
            )

    ### PRIVATE METHODS ###

    def _get_input_argument_values(self, *args, **kwargs):
        if len(args) == 1:
            assert isinstance(args[0], type(self)), repr(args[0])
            mandatory_argument_values = args[0]._mandatory_argument_values
            keyword_argument_values = args[0]._keyword_argument_values
            if kwargs.get('persistent') is not None:
                keyword_argment_values[0] = kwargs.get('persistent')
            if kwargs.get('truncate') is not None:
                keyword_argument_values[1] = kwargs.get('truncate')
        else:
            assert len(args) == 3, repr(args)
            mandatory_argument_values = args
            keyword_argument_values = []
            keyword_argument_values.append(kwargs.get('persistent', True))
            keyword_argument_values.append(kwargs.get('truncate', False))
        return mandatory_argument_values, keyword_argument_values
    
    ### PUBLIC METHODS ###

    def unpack(self):
        '''Unpacking a directive means exploding a directive into a list of settings.

        Return list of settings.
        '''
        settings = []
        assert self.target.contexts, repr(self.target.contexts)
        for context in self.target.contexts:
            target = ContextSelection(context, timespan=copy.deepcopy(self.target.timespan))
            setting = ContextSetting(target, self.attribute, self.source, 
                persistent=self.persistent, truncate=self.truncate)
            settings.append(setting)
        return settings
