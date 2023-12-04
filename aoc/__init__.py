import polars as pl
from polars.type_aliases import IntoExpr
from polars.utils.udfs import _get_shared_lib_location

lib = _get_shared_lib_location(__file__)


@pl.api.register_expr_namespace("aoc")
class AOC:
    def __init__(self, expr: pl.Expr):
        self._expr = expr

    def day_3(self) -> pl.Expr:
        return self._expr.register_plugin(
            lib=lib,
            symbol="day_3",
            is_elementwise=True,
        )
