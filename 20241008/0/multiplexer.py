from decimal import Decimal
from fractions import Fraction
def multiplexer(x, y, Type):
    return Type(x) * Type(y)
