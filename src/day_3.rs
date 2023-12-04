use polars::prelude::arity::try_ternary_elementwise;
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;

fn find_numbers(line: &str, nums: &mut Vec<(i64, (i64, i64))>) {
    // find all the numbers in a given line, along with their start and end positions
    let mut number = -1;
    let mut start_pos = -1;
    let mut end_pos = -1;
    line.chars().enumerate().for_each(|(i, c)| {
        if c.is_ascii_digit() {
            if number == -1 {
                number = c.to_digit(10).unwrap() as i64;
                start_pos = i as i64;
            } else {
                number = number * 10 + c.to_digit(10).unwrap() as i64;
            }
            end_pos = i as i64;
        } else {
            if number != -1 {
                nums.push((number, (start_pos, end_pos)));
            }
            number = -1;
            start_pos = -1;
            end_pos = -1;
        }
    });
    if number != -1 {
        nums.push((number, (start_pos, end_pos)));
    };
}

fn calculate_gear_ratio(
    curr: &str,
    prev: Option<&str>,
    next: Option<&str>,
    nums: &mut Vec<(i64, (i64, i64))>,
) -> i64 {
    let res = curr.chars().enumerate().fold(0, |acc, (i, c)| {
        let acc = if c == '*' {
            // find all numbers on this and neighbouring lines
            if let Some(prev) = prev {
                find_numbers(prev, nums);
            }
            find_numbers(curr, nums);
            if let Some(next) = next {
                find_numbers(next, nums);
            }
            // only keep neighbouring numbers
            nums.retain(|(_n, (start, end))| start - 1 <= (i as i64) && end + 1 >= (i as i64));
            // if there's only two neighbouring numbers, multiply them
            if nums.len() == 2 {
                acc + nums.first().unwrap().0 * nums.get(1).unwrap().0
            } else {
                acc
            }
        } else {
            acc
        };
        nums.clear();
        acc
    });
    res
}

#[polars_expr(output_type=Int64)]
fn day_3(inputs: &[Series]) -> PolarsResult<Series> {
    let ca = inputs[0].utf8()?;
    let binding = inputs[0].shift(1);
    let next = binding.utf8()?;
    let binding = inputs[0].shift(-1);
    let previous = binding.utf8()?;
    let mut nums: Vec<(i64, (i64, i64))> = vec![];

    let out: Int64Chunked = try_ternary_elementwise(ca, previous, next, |curr, prev, next| {
        let res = calculate_gear_ratio(curr.unwrap(), prev, next, &mut nums);
        Ok::<Option<i64>, PolarsError>(Some(res))
    })?;

    Ok(out.into_series())
}
