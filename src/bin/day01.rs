fn main() {
    let start = std::time::Instant::now();

    let text = std::fs::read_to_string("inputs/day01.txt").unwrap();
    let data = parse_input(&text);

    println!("part1: {}", part1(&data));
    println!("part2: {}", part2(&data));

    println!("Elapsed time: {:?}", start.elapsed());
}

fn parse_input(input: &str) -> Vec<&str> {
    input.trim().split('\n').collect()
}

fn part1(data: &Vec<&str>) -> usize {
    fn calibration_number(line: &str) -> u32 {
        let first = line
            .chars()
            .find(|c| c.is_digit(10))
            .unwrap()
            .to_digit(10)
            .unwrap();
        let last = line
            .chars()
            .rev()
            .find(|c| c.is_digit(10))
            .unwrap()
            .to_digit(10)
            .unwrap();
        return first * 10 + last;
    }

    return data
        .into_iter()
        .map(|line| calibration_number(line) as usize)
        .sum();
}

fn part2(data: &Vec<&str>) -> usize {
    fn parse_left(line: &str) -> u32 {
        let mut buf = String::new();
        for c in line.chars() {
            if c.is_digit(10) {
                return c.to_digit(10).unwrap();
            }
            if buf.len() == 5 {
                buf.remove(0);
            }
            buf.push(c);
            if buf.len() >= 3 {
                if buf.ends_with("one") {
                    return 1;
                }
                if buf.ends_with("two") {
                    return 2;
                }
                if buf.ends_with("six") {
                    return 6;
                }
            }
            if buf.len() >= 4 {
                if buf.ends_with("four") {
                    return 4;
                }
                if buf.ends_with("five") {
                    return 5;
                }
                if buf.ends_with("nine") {
                    return 9;
                }
            }
            if buf.len() >= 5 {
                if buf.ends_with("three") {
                    return 3;
                }
                if buf.ends_with("seven") {
                    return 7;
                }
                if buf.ends_with("eight") {
                    return 8;
                }
            }
        }
        panic!()
    }

    fn parse_right(line: &str) -> u32 {
        let mut buf = String::new();
        for c in line.chars().rev() {
            if c.is_digit(10) {
                return c.to_digit(10).unwrap();
            }
            if buf.len() == 5 {
                buf.remove(4);
            }
            buf.insert(0, c);
            if buf.len() >= 3 {
                if buf.starts_with("one") {
                    return 1;
                }
                if buf.starts_with("two") {
                    return 2;
                }
                if buf.starts_with("six") {
                    return 6;
                }
            }
            if buf.len() >= 4 {
                if buf.starts_with("four") {
                    return 4;
                }
                if buf.starts_with("five") {
                    return 5;
                }
                if buf.starts_with("nine") {
                    return 9;
                }
            }
            if buf.len() >= 5 {
                if buf.starts_with("three") {
                    return 3;
                }
                if buf.starts_with("seven") {
                    return 7;
                }
                if buf.starts_with("eight") {
                    return 8;
                }
            }
        }
        panic!()
    }

    return data
        .into_iter()
        .map(|line| {
            let first = parse_left(line);
            let last = parse_right(line);
            return (first * 10 + last) as usize;
        })
        .sum();
}
