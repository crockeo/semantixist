from lib.core import Entity
from lib.core import Function
from lib.core import Statement
from lib.core import Type
from lib.core import Variable
from lib.derivation import Node


def main():
    top_var = Variable()
    bot_var = Variable()

    # Structure & lexicon for 'Mary smiled'
    mary_smiled = Node(
        left_node=Node(
            value=Entity('Mary'),
            type=Type('e'),
        ),
        right_node=Node(
            value=Function(
                top_var,
                Statement([top_var, Entity('smiled')]),
            ),
            type=Type(Type('e'), Type('t')),
        ),
    )

    print(mary_smiled.get_value(), ':', mary_smiled.get_type())

    # Structure & lexicon for 'Mary likes John'
    mary_likes_john = Node(
        left_node=Node(
            value=Entity('Mary'),
            type=Type('e'),
        ),
        right_node=Node(
            left_node=Node(
                value=Function(
                    top_var,
                    Statement([
                        Function(
                            bot_var,
                            Statement([bot_var, Entity('likes'), top_var]),
                        ),
                    ]),
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

    # Structure & lexicon for 'green hat'
    green_and_hat = Node(
        left_node=Node(
            value=Function('y', Statement([top_var, Entity('is green')])),
            type=Type(Type('e'), Type('t')),
        ),
        right_node=Node(
            value=Function('y', Statement([bot_var, Entity('is a hat')])),
            type=Type(Type('e'), Type('t')),
        ),
    )

    print(green_and_hat.get_value(), ':', green_and_hat.get_type())


if __name__ == '__main__':
    main()
