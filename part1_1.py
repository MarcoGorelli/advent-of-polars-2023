import polars as pl


df = pl.scan_csv("1.txt", has_header=False, new_columns=["input_text"])
result = df.select(
    pl.col("input_text")
    # Extract all digits
    .str.extract_all(r"(\d)")
    # Only keep the first and last ones
    .list.gather([0, -1])
    .cast(pl.List(pl.Int64))
    # Combine the digits into a 2-digit number
    .list.eval(pl.element().get(0) * 10 + pl.element().get(1))
    # We now have a single-element list, so take the first (and only) element
    .list.first()
    .sum()
)
print(result.collect())
