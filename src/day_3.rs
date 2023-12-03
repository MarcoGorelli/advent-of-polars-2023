use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use polars::prelude::arity::try_ternary_elementwise;

fn find_numbers(line: &str) -> Vec<(i64, (i64, i64))>{
    let mut nums = vec![];
    let mut number = -1;
    let mut start_pos = -1;
    let mut end_pos = -1;
    line.chars().enumerate().for_each(
        |(i, c)| {
            if c.is_digit(10) {
                if number == -1 {
                    number = c.to_digit(10).unwrap() as i64;
                    start_pos = i as i64;
                } else {
                    number = number * 10 + c.to_digit(10).unwrap() as i64;
                }
                end_pos = i as i64;
            }
            else {
                if number != -1 {
                    nums.push((number, (start_pos, end_pos)));
                }
                number = -1;
                start_pos = -1;
                end_pos = -1;
            }
        }
    );
    if number != -1 {
        nums.push((number, (start_pos, end_pos)));
    }
    nums
}

#[polars_expr(output_type=Utf8)]
fn day_3(inputs: &[Series]) -> PolarsResult<Series> {
    let ca = inputs[0].utf8()?;
    let binding = inputs[0].shift(1);
    let next = binding.utf8()?;
    let binding = inputs[0].shift(-1);
    let previous = binding.utf8()?;

    let out: Int64Chunked = try_ternary_elementwise(ca, previous, next,
        |curr, prev, next| {
            let curr = curr.unwrap();

            let res = curr.chars().enumerate().fold(0, |acc, (i, c)| {
                if c == '*' {
                    let mut nums: Vec<(i64, (i64, i64))> = vec![];
                    if prev.is_some() {
                        nums.extend(find_numbers(prev.unwrap()));
                    }
                    nums.extend(find_numbers(curr));
                    if next.is_some() {
                        nums.extend(find_numbers(next.unwrap()));
                    }
                    let nums: Vec<(i64, (i64, i64))> = nums.into_iter().filter(|(n, (start, end))| {
                        start-1 <= (i as i64) && end+1 >= (i as i64)
                    }).collect();
                    if nums.len() == 2 {
                        acc + nums.get(0).unwrap().0 * nums.get(1).unwrap().0
                    } else {
                        acc
                    }
                } else {
                    acc
                }
            });

            Ok::<Option<i64>, PolarsError>(Some(res))
        }
    )?;

    Ok(out.into_series())
}