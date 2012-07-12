from abjad.tools.abctools.AbjadObject import AbjadObject
import copy


class Setting(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        mandatory_argument_values, keyword_argument_values = self._get_input_argument_values(*args, **kwargs)
        target, attribute, source = mandatory_argument_values
        self._target = target
        self._attribute = attribute
        self._source = source
        for name, value in zip(self._keyword_argument_names, keyword_argument_values):
            setattr(self, '_' + name, value)

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

    @property
    def _one_line_format(self):
        body = [
            self.target._one_line_format,
            self._get_one_line_source_format(self.source),
            ]
        if not self.persistent:
            body.append(self.persistent)
        body = ', '.join([str(x) for x in body])
        return '{}: {}'.format(self.attribute, body)

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

    def _get_one_line_source_format(self, source):
        if hasattr(source, '_one_line_format'):
            return source._one_line_format
        elif hasattr(source, 'name'):
            return source.name
        else:
            return str(source)
    
    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        return self._attribute

    @property
    def persistent(self):
        return self._persistent

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def truncate(self):
        return self._truncate

    ### PUBLIC METHODS ###

    def unpack(self):
        '''Unpacking a directive means exploding a directive into a list of settings.

        Return list of settings.
        '''
        from experimental import selectortools
        from experimental import settingtools
        from experimental import specificationtools
        settings = []
        assert self.target.contexts, repr(self.target.contexts)
        for context in self.target.contexts:
            target = selectortools.SingleContextTimespanSelector(context, 
                timespan=copy.deepcopy(self.target.timespan))
            setting = settingtools.ContextSetting(target, self.attribute, self.source, 
                persistent=self.persistent, truncate=self.truncate)
            settings.append(setting)
        return settings
