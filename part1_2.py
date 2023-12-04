from pathlib import Path

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


def tweak_df(df):
    return df.with_columns(
        first_digit=pl.col("column_1")
        .str.extract(r"(\d|zero|one|two|three|four|five|six|seven|eight|nine)")
        .replace(total_map),
        last_digit=pl.col("column_1")
        .str.split("")
        .list.reverse()
        .list.join("")
        .str.extract(r"(\d|orez|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)")
        .replace(total_map),
    ).select(
        result=pl.col("first_digit")
        .cast(pl.Int64)
        .mul(10)
        .add(pl.col("last_digit").cast(pl.Int64))
    )


file_path = Path(__file__).parent.parent / "data/input.txt"
raw_df = pl.read_csv(file_path, has_header=False)
df = tweak_df(raw_df)
result = df.sum()
print(f"{result=}")
