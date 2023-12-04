use std::cmp::{max, min};

fn main() {
    let start = std::time::Instant::now();

    let text = std::fs::read_to_string("inputs/day03.txt").unwrap();
    let data = parse_input(&text);

    println!("part1: {}", part1(&data));
    println!("part2: {}", part2(&data));

    println!("Elapsed time: {:?}", start.elapsed());
}

fn parse_input(input: &str) -> Vec<Vec<char>> {
    return input
        .trim()
        .split('\n')
        .map(|line| line.chars().collect())
        .collect();
}

fn parse_int(input: &Vec<char>, i: usize) -> usize {
    let mut start = i;
    while start > 0 && '0' <= input[start - 1] && input[start - 1] <= '9' {
        start -= 1;
    }

    let mut stop = i;
    while stop < input.len() - 1 && '0' <= input[stop + 1] && input[stop + 1] <= '9' {
        stop += 1;
    }

    let mut num = 0;
    for j in start..=stop {
        num *= 10;
        num += input[j] as usize - '0' as usize;
    }
    return num;
}

fn part1(data: &[Vec<char>]) -> usize {
    let mut sum = 0;
    data.iter().enumerate().for_each(|(i, line)| {
        line.into_iter().enumerate().for_each(|(j, &char)| {
            if char == '.' || '0' <= char && char <= '9' {
                return;
            }

            for k in max(0, i - 1)..=min(data.len(), i + 1) {
                let mut prev_was_number = false;
                for l in max(0, j - 1)..=min(line.len(), j + 1) {
                    if k == i && l == j {
                        prev_was_number = false;
                        continue;
                    }
                    if '0' <= data[k][l] && data[k][l] <= '9' {
                        if !prev_was_number {
                            sum += parse_int(&data[k], l);
                        }
                        prev_was_number = true;
                    } else {
                        prev_was_number = false;
                    }
                }
            }
        });
    });
    return sum;
}

fn part2(data: &[Vec<char>]) -> usize {
    let mut sum = 0;
    data.into_iter().enumerate().for_each(|(i, line)| {
        line.into_iter().enumerate().for_each(|(j, &char)| {
            if char != '*' {
                return;
            }

            let mut nums = vec![];
            for k in max(0, i - 1)..=min(data.len(), i + 1) {
                let mut prev_was_number = false;
                for l in max(0, j - 1)..=min(line.len(), j + 1) {
                    if k == i && l == j {
                        prev_was_number = false;
                        continue;
                    }
                    if '0' <= data[k][l] && data[k][l] <= '9' {
                        if !prev_was_number {
                            let num = parse_int(&data[k], l);
                            nums.push(num);
                        }
                        prev_was_number = true;
                    } else {
                        prev_was_number = false;
                    }
                }
            }
            if nums.len() == 2 {
                sum += nums[0] * nums[1];
            }
        });
    });
    return sum;
}
