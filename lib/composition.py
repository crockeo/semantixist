from enum import Enum

from lib.core import Function
from lib.core import Type

class CompositionRule(Enum):
    """
    The set of rules by which we compose trees into their final truth conditions.
    """

    FunctionApplication = 0
    PredicateModification = 1


class ComposerRoot:
    def compose(self, left_node, right_node):
        raise NotImplementedError()


class FunctionApplicationComposer(ComposerRoot):
    def compose(self, left_node, right_node):
        left_value = left_node.get_value()
        left_type = left_node.get_type()
        right_value = right_node.get_value()
        right_type = right_node.get_type()

        if left_type.from_type == right_type:
            return left_value.apply(right_value), left_type.to_type
        if right_type.from_type == left_type:
            return right_value.apply(left_value), right_type.to_type

        raise ValueError(
            'Expected nodes to be composable by FunctionApplication')


class PredicateModificationComposer(ComposerRoot):
    def compose(self, left_node, right_node):
        left_value = left_node.get_value()
        left_type = left_node.get_type()
        right_value = right_node.get_value()
        right_type = right_node.get_type()

        if left_type != right_type or right_type != Type(Type('e'), Type('t')):
            raise ValueError('Expected noes to be composable by PredicateModification')

        # TODO: This is broken, if either of the nodes have 'x' inside of them, then it'll be
        # replaced with this x that we use instead.
        return Function(
            'x',
            [
                ' '.join(left_value.apply('x')),
                'and',
                ' ' .join(right_value.apply('x')),
            ]
        ), Type(Type('e'), Type('t'))


class Composer(ComposerRoot):
    def _infer_composition_rule(self, type1: Type, type2: Type) -> CompositionRule:
        if type1.from_type == type2 or type2.from_type == type1:
            return CompositionRule.FunctionApplication
        if type1 == type2 and type2 == Type(Type('e'), Type('t')):
            return CompositionRule.PredicateModification

    def compose(self, left_node, right_node):
        left_type = left_node.get_type()
        right_type = right_node.get_type()
        rule = self._infer_composition_rule(left_type, right_type)

        if rule == CompositionRule.FunctionApplication:
            return FunctionApplicationComposer().compose(left_node, right_node)
        if rule == CompositionRule.PredicateModification:
            return PredicateModificationComposer().compose(left_node, right_node)

        raise ValueError('Expected nodes to be composable by any composition rule')
