use std::cmp::max;

struct Game {
    game_id: usize,
    max_red: usize,
    max_green: usize,
    max_blue: usize,
}

fn main() {
    let start = std::time::Instant::now();

    let text = std::fs::read_to_string("inputs/day02.txt").unwrap();
    let data = parse_input(&text);

    println!("part1: {}", part1(&data));
    println!("part2: {}", part2(&data));

    println!("Elapsed time: {:?}", start.elapsed());
}

fn parse_input(input: &str) -> Vec<Game> {
    let lines: Vec<&str> = input.trim().split('\n').collect();
    let games: Vec<Game> = lines
        .into_iter()
        .map(|line| {
            let colon_idx = line.find(':').unwrap();
            let game_id = line["Game ".len()..colon_idx].parse::<usize>().unwrap();

            let mut red = 0;
            let mut green = 0;
            let mut blue = 0;
            line[colon_idx + 2..].split(';').for_each(|part| {
                part.split(',').for_each(|sub_pull| {
                    let mut parts = sub_pull.trim().split(' ');
                    let amount = parts.next().unwrap().parse::<usize>().unwrap();
                    let color = parts.next().unwrap();
                    match color {
                        "red" => red = max(red, amount),
                        "green" => green = max(green, amount),
                        "blue" => blue = max(blue, amount),
                        _ => panic!(),
                    }
                })
            });

            return Game {
                game_id,
                max_red: red,
                max_green: green,
                max_blue: blue,
            };
        })
        .collect();
    return games;
}

fn part1(data: &Vec<Game>) -> usize {
    fn is_valid_game(game: &Game) -> bool {
        return game.max_red <= 12 && game.max_green <= 13 && game.max_blue <= 14;
    }

    return data
        .into_iter()
        .filter(|game| is_valid_game(game))
        .map(|game| game.game_id)
        .sum();
}

fn part2(data: &Vec<Game>) -> usize {
    fn minimum_cubes(game: &Game) -> usize {
        return game.max_red * game.max_green * game.max_blue;
    }

    return data.into_iter().map(|game| minimum_cubes(game)).sum();
}
