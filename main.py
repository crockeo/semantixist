from enum import Enum


class Function:
    """
    Basic implemenetation of a lambda function
    """

    def __init__(self, variable, tokens):
        self.variable = variable
        if isinstance(tokens, str):
            self.tokens = tokens.split()
        else:
            self.tokens = tokens

    def __str__(self):
        return '[{}{}. {}]'.format(
            'λ',
            self.variable,
            ' '.join([str(token) for token in self.tokens]),
        )

    def __repr__(self):
        return str(self)

    def replace(self, variable, value):
        tokens = []
        for token in self.tokens:
            if isinstance(token, str):
                if token == variable:
                    tokens.append(value)
                else:
                    tokens.append(token)
            else:
                tokens.append(token.replace(variable, value))

        return Function(self.variable, tokens)

    def apply(self, value):
        tokens = self.replace(self.variable, value).tokens
        if len(tokens) == 1:
            return tokens[0]
        else:
            return tokens


class Entity:
    """
    Explicit Entity type, so that we can separate them from variable holes.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)

    def replace(self, variable, value):
        return self


class Type:
    """
    Wraps around types to explicate the kinds of things members of a semantic tree can be.
    """

    def __init__(self, from_type, to_type=None):
        self.from_type = from_type
        self.to_type = to_type

    def __eq__(self, other):
        if not isinstance(other, Type):
            return False
        return self.from_type == other.from_type and self.to_type == other.to_type

    def __str__(self):
        if self.to_type is None:
            return str(self.from_type)
        else:
            return '<{}, {}>'.format(self.from_type, self.to_type)

    def __repr__(self):
        return str(self)


class CompositionRule(Enum):
    """
    The set of rules by which we compose trees into their final truth conditions.
    """

    FunctionApplication = 0


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


class Composer(ComposerRoot):
    def _infer_composition_rule(self, type1: Type, type2: Type) -> CompositionRule:
        if type1.from_type == type2 or type2.from_type == type1:
            return CompositionRule.FunctionApplication

    def compose(self, left_node, right_node):
        left_type = left_node.get_type()
        right_type = right_node.get_type()
        rule = self._infer_composition_rule(left_type, right_type)

        if rule == CompositionRule.FunctionApplication:
            return FunctionApplicationComposer().compose(left_node, right_node)

        raise ValueError('Expected nodes to be composable by any composition rule')


class Node:
    def __init__(self, value=None, type=None, left_node=None, right_node=None):
        self._value = value
        self._type = type
        self._left_node = left_node
        self._right_node = right_node

    def __str__(self):
        return str(self.get_value())

    def __repr__(self):
        return str(self)

    def _derive(self):
        """
        Derives self._value and self._type from self._left_node and self._right_node.
        """
        self._value, self._type = Composer().compose(self._left_node, self._right_node)

    def get_value(self):
        if self._value is None:
            self._derive()
        return self._value

    def get_type(self):
        if self._type is None:
            self._derive()
        return self._type


# Structure & lexicon for 'Mary likes John'
mary_likes_john = Node(
    left_node=Node(
        value=Entity('Mary'),
        type=Type('e'),
    ),
    right_node=Node(
        left_node=Node(
            value=Function(
                'x',
                [
                    Function(
                        'y',
                        'y likes x',
                    ),
                ],
            ),
            type=Type(Type('e'), Type(Type('e'), Type('t'))),
        ),
        right_node=Node(
            value=Entity('John'),
            type=Type('e'),
        ),
    ),
)

print(mary_likes_john.get_value(), ':', mary_likes_john.get_type())
