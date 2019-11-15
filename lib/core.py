from typing import Any
from typing import List
from typing import Optional
import uuid


class Token:
    """
    Superclass for each token that can appear in a sentence.
    """

    def __str__(self):
        return self.serialize()

    def __repr__(self):
        return self.serialize()

    def replace(self, variable: 'Variable', value: 'Token') -> 'Token':
        raise NotImplementedError('Token.replace not implemented')

    def serialize(self) -> str:
        raise NotImplementedError('Token.serialize not implemented')


class Variable(Token):
    """
    Represents a Variable within a lambda function. Uses UUIDs to maintain uniqueness across all
    functions.
    """

    def __init__(self):
        self.uuid = uuid.uuid4()

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.uuid == other.uuid

    def replace(self, variable: 'Variable', value: Token) -> Token:
        if self == variable:
            return value
        else:
            return self

    def serialize(self) -> str:
        return 'x'


class Entity(Token):
    """
    Explicit Entity type, so that we can separate them from variable holes.
    """

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        return self.value == other.value

    def replace(self, variable: Variable, value: Token) -> Token:
        return self

    def serialize(self) -> str:
        return str(self.value)


class Statement(Token):
    """
    A list of tokens that collectively represent a statement.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    def __eq__(self, other):
        if not isinstance(other, Statement):
            return False

        if len(self.tokens) != len(other.tokens):
            return False

        for i in range(len(self.tokens)):
            if self.tokens[i] != other.tokens[i]:
                return False

        return True

    def replace(self, variable: Variable, value: Token) -> Token:
        replaced_tokens = [token.replace(variable, value)
                           for token in self.tokens]
        if len(replaced_tokens) == 1 and isinstance(replaced_tokens[0], Function):
            return replaced_tokens[0]
        return Statement(replaced_tokens)

    def serialize(self) -> str:
        return ' '.join([token.serialize() for token in self.tokens])


class Function(Token):
    """
    Basic implemenetation of a lambda function
    """

    def __init__(self, variable: Variable, statement: Statement):
        self.variable = variable
        self.statement = statement

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False
        return self.variable == other.variable and self.statement == other.statement

    def replace(self, variable: Variable, value: Token) -> Token:
        replaced_statement = self.statement.replace(variable, value)
        if variable == self.variable:
            return replaced_statement
        return Function(self.variable, replaced_statement)

    def serialize(self) -> str:
        return '[λ{}. {}]'.format(
            self.variable.serialize(),
            self.statement.serialize(),
        )

    def apply(self, value: Token) -> Token:
        return self.replace(self.variable, value)


class Type:
    """
    Wraps around types to explicate the kinds of things members of a semantic tree can be.
    """

    def __init__(self, from_type: 'Type', to_type: Optional['Type'] = None):
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
