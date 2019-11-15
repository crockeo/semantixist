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
