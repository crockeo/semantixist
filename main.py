from lib.core import Entity
from lib.core import Function
from lib.core import Type
from lib.derivation import Node

def main():
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

    green_and_hat = Node(
        left_node=Node(
            value=Function('y', 'y is green'),
            type=Type(Type('e'), Type('t')),
        ),
        right_node=Node(
            value=Function('y', 'y is a hat'),
            type=Type(Type('e'), Type('t')),
        ),
    )

    print(green_and_hat.get_value(), ':', green_and_hat.get_type())

if __name__ == '__main__':
    main()
