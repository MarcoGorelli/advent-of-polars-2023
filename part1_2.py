import polars as pl

df = pl.read_csv('1.txt', has_header=False, new_columns=['input_text'])

result = df.with_columns(
    t=pl.concat_list(
        pl.col("input_text")
        .str.replace_all(r'(one|two|three|four|five|six|seven|eight|nine)', '*$1*')
        .str.replace_all('\*(one)\*', '1')
        .str.replace_all('\*(two)\*', '2')
        .str.replace_all('\*(three)\*', '3')
        .str.replace_all('\*(four)\*', '4')
        .str.replace_all('\*(five)\*', '5')
        .str.replace_all('\*(six)\*', '6')
        .str.replace_all('\*(seven)\*', '7')
        .str.replace_all('\*(eight)\*', '8')
        .str.replace_all('\*(nine)\*', '9')
        # Extract first digit
        .str.extract(r"(\d)")
        .cast(pl.Int64),
        pl.col("input_text")
        # Reverse the string
        .str.split('').list.reverse().list.join('')
        .str.replace_all(r'(eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)', '*$1*')
        .str.replace_all('\*(eno)\*', '1')
        .str.replace_all('\*(owt)\*', '2')
        .str.replace_all('\*(eerht)\*', '3')
        .str.replace_all('\*(ruof)\*', '4')
        .str.replace_all('\*(evif)\*', '5')
        .str.replace_all('\*(xis)\*', '6')
        .str.replace_all('\*(neves)\*', '7')
        .str.replace_all('\*(thgie)\*', '8')
        .str.replace_all('\*(enin)\*', '9')
        # Extract first digit
        .str.extract(r"(\d)")
        .cast(pl.Int64)
    )
    # Combine the digits into a 2-digit number
    .list.eval(pl.element().get(0) * 10 + pl.element().get(1))
    # We now have a single-element list, so take the first (and only) element
    .list.first()
)
print(result)
print(result.select('t').sum())

