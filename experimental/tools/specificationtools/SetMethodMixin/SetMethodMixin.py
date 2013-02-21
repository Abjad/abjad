import copy
from abjad.tools import iotools
from abjad.tools.abctools import AbjadObject


class SetMethodMixin(AbjadObject):
    '''Set method mixin.
    '''

    ### PRIVATE METHODS ###

    def _all_are_expressions(self, expr):
        from experimental.tools import specificationtools
        if isinstance(expr, (tuple, list)):
            if all([isinstance(x, specificationtools.Expression) for x in expr]):
                return True
        return False

    def _attribute_to_set_expression_class(self, attribute):
        from experimental.tools import specificationtools
        return {
            'note_head_color': specificationtools.NoteHeadColorSetExpression,
            'pitch': specificationtools.PitchSetExpression,
            'pitch_class_transform': specificationtools.PitchClassTransformSetExpression,
            }[attribute]

    def _expr_to_expression(self, expr):
        from abjad.tools import rhythmmakertools
        from experimental.tools import handlertools
        from experimental.tools import specificationtools
        from experimental.tools import specificationtools
        if isinstance(expr, specificationtools.Expression):
            return expr
        elif self._all_are_expressions(expr):
            return specificationtools.ExpressionInventory(expr)
        elif isinstance(expr, (tuple, list)):
            return specificationtools.IterablePayloadExpression(expr)
        elif isinstance(expr, (str)):
            component = iotools.p(expr)
            return specificationtools.StartPositionedRhythmPayloadExpression([component], start_offset=0)
        elif isinstance(expr, rhythmmakertools.RhythmMaker):
            return specificationtools.RhythmMakerExpression(expr)
        elif isinstance(expr, specificationtools.StatalServerCursor):
            return specificationtools.StatalServerCursorExpression(expr)
        elif isinstance(expr, specificationtools.PitchClassTransformExpression):
            return specificationtools.PitchClassTransformSetExpression(expr)
        elif isinstance(expr, specificationtools.NoteHeadColorExpression):
            return specificationtools.NoteHeadColorSetExpression(expr)
        else:
            raise TypeError('do not know how to change {!r} to expression.'.format(expr))

    def _store_generalized_set_expression(self, attribute, source_expression):
        from experimental.tools import specificationtools
        set_expression_class = self._attribute_to_set_expression_class(attribute)
        source_expression = self._expr_to_expression(source_expression)
        if isinstance(self, specificationtools.SelectExpression):
            target_select_expression_inventory = specificationtools.SelectExpressionInventory([self])
        elif isinstance(self, specificationtools.SelectExpressionInventory):
            target_select_expression_inventory = self
        else:
            raise TypeError(self)
        generalized_set_expression = set_expression_class(
            source_expression=source_expression,
            target_select_expression_inventory=target_select_expression_inventory
            )
        assert self.score_specification is not None
        generalized_set_expression._score_specification = self.score_specification
        generalized_set_expression._lexical_rank = self.score_specification._next_lexical_rank
        self.score_specification._next_lexical_rank += 1
        if isinstance(generalized_set_expression, specificationtools.PitchSetExpression):
            self.score_specification.pitch_set_expressions.append(generalized_set_expression)
        elif isinstance(generalized_set_expression, specificationtools.PitchClassTransformSetExpression):
            self.score_specification.pitch_set_expressions.append(generalized_set_expression)
        elif isinstance(generalized_set_expression, specificationtools.NoteHeadColorSetExpression):
            self.score_specification.pitch_set_expressions.append(generalized_set_expression)
        else:
            self.score_specification.generalized_set_expressions.append(generalized_set_expression)
        return generalized_set_expression

    ### PUBLIC METHODS ###

    def set_note_head_color(self, source_expression):
        r'''Set note head color to `source_expression`.

        Return some sort of set expression.
        '''
        from experimental.tools import specificationtools
        source_expression = specificationtools.NoteHeadColorExpression(source_expression)
        attribute = 'note_head_color'
        return self._store_generalized_set_expression(attribute, source_expression)

    def set_pitch_class_transform(self, source_expression):
        r'''Set pitch class transform to `source_expression`.

        Return some sort of set expression.
        '''
        from experimental.tools import specificationtools
        source_expression = specificationtools.PitchClassTransformExpression(source_expression)
        attribute = 'pitch_class_transform'
        return self._store_generalized_set_expression(attribute, source_expression)

    def set_pitches(self, source_expression):
        r'''Set pitches to `source_expression`.

        Return pitch set expression.
        '''
        attribute = 'pitch'
        return self._store_generalized_set_expression(attribute, source_expression)
