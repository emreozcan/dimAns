from ..si_base.electric_current import ampere as _ampere
from ..si_base.time import second as _second
from ..metric_utils import make_metric_units as _make_metric_units

coulomb = (_ampere * _second).as_derived_unit("C")

(
    quettacoulomb,
    yottacoulomb,
    zettacoulomb,
    exacoulomb,
    petacoulomb,
    teracoulomb,
    gigacoulomb,
    megacoulomb,
    kilocoulomb,
    hectocoulomb,
    decacoulomb,
    decicoulomb,
    centicoulomb,
    millicoulomb,
    microcoulomb,
    nanocoulomb,
    picocoulomb,
    femtocoulomb,
    attocoulomb,
    zeptocoulomb,
    yoctocoulomb,
    rontocoulomb,
    quectocoulomb,
) = _make_metric_units(coulomb)
