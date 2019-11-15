import pytest

from lib.core import *
from lib.derivation import Node


def test_function_application_single():
    """
    Tests that Function Application, with only a single layer, works correctly. Runs on a function
    of type <e, t>.
    """

    var = Variable()

    mary_smiled = Node(
        left_node=Node(value=Entity("Mary"), type=Type("e"),),
        right_node=Node(
            value=Function(var, Statement([var, Entity("smiled")]),),
            type=Type(Type("e"), Type("t")),
        ),
    )

    assert Statement([Entity("Mary"), Entity("smiled")]) == mary_smiled.get_value()
    assert Type("t") == mary_smiled.get_type()


def test_function_application_multiple():
    """
    Tests that Function Application, with multiple layers, works correctly. Runs on a function of
    type <e, <e, t>>.
    """

    top_var = Variable()
    bot_var = Variable()

    mary_likes_john = Node(
        left_node=Node(value=Entity("Mary"), type=Type("e"),),
        right_node=Node(
            left_node=Node(
                value=Function(
                    top_var,
                    Statement(
                        [
                            Function(
                                bot_var, Statement([bot_var, Entity("likes"), top_var]),
                            ),
                        ]
                    ),
                ),
                type=Type(Type("e"), Type(Type("e"), Type("t"))),
            ),
            right_node=Node(value=Entity("John"), type=Type("e"),),
        ),
    )

    assert (
        Statement([Entity("Mary"), Entity("likes"), Entity("John"),])
        == mary_likes_john.get_value()
    )
    assert Type("t") == mary_likes_john.get_type()


def test_predicate_modification():
    """
    Tests that Predicate Modification can compose two functions of type <e, t> into another
    function of type <e, t>.
    """

    v1 = Variable()
    v2 = Variable()

    green_hat = Node(
        left_node=Node(
            value=Function(
                v1,
                Statement([
                    v1,
                    Entity('is green'),
                ]),
            ),
            type=Type(Type('e'), Type('t')),
        ),
        right_node=Node(
            value=Function(
                v2,
                Statement([
                    v2,
                    Entity('is a hat'),
                ]),
            ),
            type=Type(Type('e'), Type('t')),
        ),
    )

    value = green_hat.get_value()

    for entity in value.statement.tokens:
        print(entity)

    assert Function(
        value.variable,
        Statement([
            Statement([value.variable, Entity('is green')]),
            Entity('and'),
            Statement([value.variable, Entity('is a hat')]),
        ]),
    ) == value
    assert Type(Type('e'), Type('t')) == green_hat.get_type()
