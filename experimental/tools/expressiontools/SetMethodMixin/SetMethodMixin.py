import copy
from abjad.tools import iotools
from abjad.tools.abctools import AbjadObject


class SetMethodMixin(AbjadObject):
    '''InputSetExpression-maker mix-in.

    Examples below use the score and segment specification defined here::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Equips classes with the composer set interface.
    '''

    ### PRIVATE METHODS ###

    def _all_are_expressions(self, expr):
        from experimental.tools import expressiontools
        if isinstance(expr, (tuple, list)):
            if all([isinstance(x, expressiontools.Expression) for x in expr]):
                return True
        return False

    def _expr_to_expression(self, expr):
        from abjad.tools import rhythmmakertools
        from experimental.tools import handlertools
        from experimental.tools import expressiontools
        from experimental.tools import expressiontools
        # probably precautionary: prune expr of any incoming references
        expr = copy.deepcopy(expr)
        if isinstance(expr, expressiontools.Expression):
            return expr
        elif self._all_are_expressions(expr):
            return expressiontools.ExpressionInventory(expr)
        elif isinstance(expr, (tuple, list)):
            return expressiontools.PayloadExpression(expr)
        elif isinstance(expr, (str)):
            component = iotools.p(expr)
            return expressiontools.StartPositionedRhythmPayloadExpression([component], start_offset=0)
        elif isinstance(expr, rhythmmakertools.RhythmMaker):
            return expressiontools.RhythmMakerPayloadExpression(expr)
        else:
            raise TypeError('do not know how to change {!r} to expression.'.format(expr))

    def _store_multiple_context_set_expression(self, attribute, source, contexts=None, persist=True, truncate=None):
        from experimental.tools import expressiontools
        source = self._expr_to_expression(source)
        assert self.score_specification is not None
        target_context_names = self.score_specification._context_token_to_context_names(contexts)
        multiple_context_set_expression = expressiontools.MultipleContextSetExpression(
            attribute=attribute,
            source=source,
            target_timespan=self._expression_abbreviation,
            target_context_names=target_context_names,
            persist=persist,
            truncate=truncate
            )
        multiple_context_set_expression._score_specification = self.score_specification
        self.score_specification.multiple_context_set_expressions.append(multiple_context_set_expression)
        return multiple_context_set_expression

    ### PUBLIC METHODS ###

    def set_aggregate(self, source, contexts=None, persist=True):
        r'''Set aggregate of `contexts` to `source`.

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'aggregate'
        return self._store_multiple_context_set_expression(attribute, source, 
            contexts=contexts, persist=persist)

    def set_articulations(self, source, contexts=None, persist=True):
        r'''Set articulations of `contexts` to `source`.

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'articulations'
        return self._store_multiple_context_set_expression(attribute, source, 
            contexts=contexts, persist=persist)

    def set_chord_treatment(self, source, contexts=None, persist=True):
        r'''Set chord treatment of `contexts` to `source`.

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'chord_treatment'
        return self._store_multiple_context_set_expression(attribute, source, 
            contexts=contexts, persist=persist)

    def set_divisions(self, source, contexts=None, persist=True, truncate=None):
        r'''Set divisions `contexts` to `source`::

            >>> set_expression = red_segment.set_divisions([(3, 16)], contexts=['Voice 1', 'Voice 3'])

        ::

            >>> z(set_expression)
            expressiontools.MultipleContextSetExpression(
                attribute='divisions',
                source=expressiontools.PayloadExpression(
                    ((3, 16),)
                    ),
                target_timespan='red',
                target_context_names=['Voice 1', 'Voice 3'],
                persist=True
                )

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'divisions'
        return self._store_multiple_context_set_expression(attribute, source,
            contexts=contexts, truncate=truncate, persist=persist)

    def set_dynamics(self, source, contexts=None, persist=True):
        r'''Set dynamics of `contexts` to `source`.

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'dynamics'
        return self._store_multiple_context_set_expression(attribute, source, 
            contexts=contexts, persist=persist)

    def set_marks(self, source, contexts=None, persist=True):
        r'''Set marks of `contexts` to `source`.

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'marks'
        return self._store_multiple_context_set_expression(attribute, source, 
            contexts=contexts, persist=persist)

    def set_markup(self, source, contexts=None, persist=True):
        r'''Set markup of `contexts` to `source`.

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'markup'
        return self._store_multiple_context_set_expression(attribute, source, 
            contexts=contexts, persist=persist)

    def set_pitch_class_application(self, source, contexts=None, persist=True):
        r'''Set pitch-class application of `contexts` to `source`.

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'pitch_class_application'
        return self._store_multiple_context_set_expression(attribute, source, 
            contexts=contexts, persist=persist)

    def set_pitch_class_transform(self, source, contexts=None, persist=True):
        r'''Set pitch-class transform of `contexts` to `source`.

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'pitch_class_transform'
        return self._store_multiple_context_set_expression(attribute, source, 
            contexts=contexts, persist=persist)

    def set_pitch_classes(self, source, contexts=None, persist=True):
        r'''Set pitch-classes of `contexts` to `source`.

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'pitch_classes'
        return self._store_multiple_context_set_expression(attribute, source, 
            contexts=contexts, persist=persist)

    def set_registration(self, source, contexts=None, persist=True):
        r'''Set registration of `contexts` to `source`.

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'registration'
        return self._store_multiple_context_set_expression(attribute, source, 
            contexts=contexts, persist=persist)

    def set_rhythm(self, source, contexts=None, persist=True):
        r'''Set rhythm of `contexts` to `source`.

            >>> set_expression = red_segment.set_rhythm(library.sixteenths)

        ::

            >>> z(set_expression)
            expressiontools.MultipleContextSetExpression(
                attribute='rhythm',
                source=expressiontools.RhythmMakerPayloadExpression(
                    payload=(TaleaRhythmMaker('sixteenths'),)
                    ),
                target_timespan='red',
                persist=True
                )

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'rhythm'
        return self._store_multiple_context_set_expression(attribute, source, contexts=contexts, persist=persist)

    def set_tempo(self, source, contexts=None, persist=True):
        r'''Set tempo of `contexts` to `source`.

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'tempo'
        return self._store_multiple_context_set_expression(attribute, source, 
            contexts=contexts, persist=persist)

    def set_time_signatures(self, source, contexts=None, persist=True):
        r'''Set time signatures of `contexts` to `source`.

            >>> set_expression = red_segment.set_time_signatures([(3, 8), (4, 8)])

        ::

            >>> z(set_expression)
            expressiontools.MultipleContextSetExpression(
                attribute='time_signatures',
                source=expressiontools.PayloadExpression(
                    ((3, 8), (4, 8))
                    ),
                target_timespan='red',
                persist=True
                )

        Create, store and return ``MultipleContextSetExpression``.
        '''
        attribute = 'time_signatures'
        return self._store_multiple_context_set_expression(attribute, source, contexts=contexts, persist=persist)
