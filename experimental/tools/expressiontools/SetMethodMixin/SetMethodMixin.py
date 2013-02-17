import copy
from abjad.tools import iotools
from abjad.tools.abctools import AbjadObject


class SetMethodMixin(AbjadObject):
    '''Set method mixin.

    Segment definition for examples:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Add to classes that implement the set method interface.
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

    def _store_multiple_context_set_expression(self, attribute, source_expression, 
        contexts=None, persist=True, truncate=None):
        from experimental.tools import expressiontools
        source_expression = self._expr_to_expression(source_expression)
        assert self.score_specification is not None
        target_context_names = self.score_specification._context_token_to_context_names(contexts)
        multiple_context_set_expression = expressiontools.MultipleContextSetExpression(
            attribute=attribute,
            source_expression=source_expression,
            target_timespan=self._expression_abbreviation,
            target_context_names=target_context_names,
            persist=persist,
            truncate=truncate
            )
        multiple_context_set_expression._score_specification = self.score_specification
        multiple_context_set_expression._lexical_rank = self.score_specification._next_lexical_rank
        self.score_specification._next_lexical_rank += 1
        self.score_specification.multiple_context_set_expressions.append(multiple_context_set_expression)
        return multiple_context_set_expression

    ### PUBLIC METHODS ###

    def set_aggregate(self, source_expression, contexts=None, persist=True):
        r'''Set aggregate to `source_expression` for target timespan over all `contexts`.

        Return multiple-context set expression.
        '''
        attribute = 'aggregate'
        return self._store_multiple_context_set_expression(attribute, source_expression, 
            contexts=contexts, persist=persist)

    def set_articulations(self, source_expression, contexts=None, persist=True):
        r'''Set articulations to `source_expression` for target timespan over all `contexts`.

        Return multiple-context set expression.
        '''
        attribute = 'articulations'
        return self._store_multiple_context_set_expression(attribute, source_expression, 
            contexts=contexts, persist=persist)

    def set_chord_treatment(self, source_expression, contexts=None, persist=True):
        r'''Set chord treatment to `source_expression` for target timespan over all `contexts`.

        Return multiple-context set expression.
        '''
        attribute = 'chord_treatment'
        return self._store_multiple_context_set_expression(attribute, source_expression, 
            contexts=contexts, persist=persist)

    def set_divisions(self, source_expression, contexts=None, persist=True, truncate=None):
        r'''Set divisions to `source_expression` for target timespan over all `contexts`:

        Example. Set divisions to ``3/16`` for red segment timespan over contexts
        ``'Voice 1'`` and ``'Voice 3'``:

        ::

            >>> set_expression = red_segment.set_divisions([(3, 16)], contexts=['Voice 1', 'Voice 3'])

        ::

            >>> z(set_expression)
            expressiontools.MultipleContextSetExpression(
                attribute='divisions',
                source_expression=expressiontools.PayloadExpression(
                    ((3, 16),)
                    ),
                target_timespan='red',
                target_context_names=['Voice 1', 'Voice 3'],
                persist=True
                )

        Return multiple-context set expression.
        '''
        attribute = 'divisions'
        return self._store_multiple_context_set_expression(attribute, source_expression,
            contexts=contexts, truncate=truncate, persist=persist)

    def set_dynamics(self, source_expression, contexts=None, persist=True):
        r'''Set dynamics to `source_expression` for target timespan over all `contexts`.

        Return multiple-context set expression.
        '''
        attribute = 'dynamics'
        return self._store_multiple_context_set_expression(attribute, source_expression, 
            contexts=contexts, persist=persist)

    def set_marks(self, source_expression, contexts=None, persist=True):
        r'''Set marks to `source_expression` for target timespan over all `contexts`.

        Return multiple-context set expression.
        '''
        attribute = 'marks'
        return self._store_multiple_context_set_expression(attribute, source_expression, 
            contexts=contexts, persist=persist)

    def set_markup(self, source_expression, contexts=None, persist=True):
        r'''Set markup to `source_expression` for target timespan over all `contexts`.

        Return multiple-context set expression.
        '''
        attribute = 'markup'
        return self._store_multiple_context_set_expression(attribute, source_expression, 
            contexts=contexts, persist=persist)

    def set_pitch_class_application(self, source_expression, contexts=None, persist=True):
        r'''Set pitch-class application to `source_expression` for target timespan over all `contexts`.

        Return multiple-context set expression.
        '''
        attribute = 'pitch_class_application'
        return self._store_multiple_context_set_expression(attribute, source_expression, 
            contexts=contexts, persist=persist)

    def set_pitch_class_transform(self, source_expression, contexts=None, persist=True):
        r'''Set pitch-class transform to `source_expression` for target timespan over all `contexts`.

        Return multiple-context set expression.
        '''
        attribute = 'pitch_class_transform'
        return self._store_multiple_context_set_expression(attribute, source_expression, 
            contexts=contexts, persist=persist)

    def set_pitch_classes(self, source_expression, contexts=None, persist=True):
        r'''Set pitch-classes to `source_expression` for target timespan over all `contexts`.

        Return multiple-context set expression.
        '''
        attribute = 'pitch_classes'
        return self._store_multiple_context_set_expression(attribute, source_expression, 
            contexts=contexts, persist=persist)

    def set_registration(self, source_expression, contexts=None, persist=True):
        r'''Set registration to `source_expression` for target timespan over all `contexts`.

        Return multiple-context set expression.
        '''
        attribute = 'registration'
        return self._store_multiple_context_set_expression(attribute, source_expression, 
            contexts=contexts, persist=persist)

    def set_rhythm(self, source_expression, contexts=None, persist=True):
        r'''Set rhythm to `source_expression` for target timespan over all `contexts`.

        Example. Set rhythm to sixteenths for red segment target timespan
        over all contexts:

        ::

            >>> set_expression = red_segment.set_rhythm(library.sixteenths)

        ::

            >>> z(set_expression)
            expressiontools.MultipleContextSetExpression(
                attribute='rhythm',
                source_expression=expressiontools.RhythmMakerPayloadExpression(
                    payload=(TaleaRhythmMaker('sixteenths'),)
                    ),
                target_timespan='red',
                persist=True
                )

        Return multiple-context set expression.
        '''
        attribute = 'rhythm'
        return self._store_multiple_context_set_expression(attribute, source_expression, contexts=contexts, persist=persist)

    def set_tempo(self, source_expression, contexts=None, persist=True):
        r'''Set tempo to `source_expression` for target timespan over all `contexts`.

        Return multiple-context set expression.
        '''
        attribute = 'tempo'
        return self._store_multiple_context_set_expression(attribute, source_expression, 
            contexts=contexts, persist=persist)

    def set_time_signatures(self, source_expression, contexts=None, persist=True):
        r'''Set time signatures to `source_expression` for target timespan over all `contexts`.

        Example. Set time signatures to ``3/8``, ``4/8`` for red segment timespan
        over all contexts:

        ::

            >>> set_expression = red_segment.set_time_signatures([(3, 8), (4, 8)])

        ::

            >>> z(set_expression)
            expressiontools.MultipleContextSetExpression(
                attribute='time_signatures',
                source_expression=expressiontools.PayloadExpression(
                    ((3, 8), (4, 8))
                    ),
                target_timespan='red',
                persist=True
                )

        Return multiple-context set expression.
        '''
        attribute = 'time_signatures'
        return self._store_multiple_context_set_expression(attribute, source_expression, contexts=contexts, persist=persist)
