import aoc
import polars as pl

df = pl.scan_csv('3.txt', has_header=False)
print(df.select(res=pl.col('column_1').aoc.day_3().sum()).collect())
