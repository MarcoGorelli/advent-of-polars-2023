import polars as pl

df = pl.read_csv("2.txt", separator="|", has_header=False)
columns = [
    pl.col('column_1').str.extract_all(rf'\d+ {colour}').list.join('').str.extract_all('\d+')
    .cast(pl.List(pl.Int64))
    .list.max().alias(colour)
    for colour in ('blue', 'green', 'red')
]

result = df.with_columns(
    *columns,
    id_=pl.col('column_1').str.extract_groups(r'Game (\d+)').struct.field('1').cast(pl.UInt32),
)
print(result)
result = result.filter(
    pl.col('blue') <= 14,
    pl.col('green') <= 13,
    pl.col('red') <= 12,
)
print(result)
print(result.select(pl.col('id_').sum()))
