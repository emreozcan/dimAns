from ..metric.byte import megabyte as _megabyte, terabyte as _terabyte
from ..metric.bit import bit as _bit

king_james_bible = (4.5 * _megabyte).as_derived_unit("King James Bible")
encyclopaedia_britannica = (300 * _megabyte).as_derived_unit(
    "Encyclopædia Britannica"
)
library_of_congress = (10 * _terabyte).as_derived_unit("Library of Congress")
nibble = (4 * _bit).as_derived_unit("nybl")
