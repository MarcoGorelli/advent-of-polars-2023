import polars as pl

numbers_in_eng = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]
number_map = dict(zip(numbers_in_eng, map(str, range(10))))
total_map = number_map | {k[::-1]: v for k, v in number_map.items()}


def solve(df: pl.LazyFrame) -> pl.LazyFrame:
    df = df.with_columns(
        first_digit=pl.col("column_1")
        .str.extract(r"(\d|zero|one|two|three|four|five|six|seven|eight|nine)")
        .replace(total_map),
        last_digit=pl.col("column_1")
        .str.split("")
        .list.reverse()
        .list.join("")
        .str.extract(r"(\d|orez|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)")
        .replace(total_map),
    )
    return df.select(
        result=pl.col("first_digit")
        .cast(pl.Int64)
        .mul(10)
        .add(pl.col("last_digit").cast(pl.Int64))
    )


raw_df = pl.scan_csv('1.txt', has_header=False)
df = solve(raw_df)
result = df.sum().collect()
print(f"{result=}")
