import polars as pl

df = pl.scan_csv("2.txt", separator="|", has_header=False)
columns = [
    pl.col("column_1")
    .str.extract_all(rf"\d+ {colour}")
    .list.join("")
    .str.extract_all(r"\d+")
    .cast(pl.List(pl.Int64))
    .list.max()
    .alias(colour)
    for colour in ("blue", "green", "red")
]
result = df.with_columns(columns).select(
    power=pl.concat_list("blue", "green", "red")
    .list.eval(pl.element().product())
    .list.first()
    .sum()
)
print(result.collect())
