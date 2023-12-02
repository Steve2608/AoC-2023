package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

type Game struct {
	game_id   int
	max_red   int
	max_green int
	max_blue  int
}

func ReadFile(filename string) string {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return strings.TrimSpace(string(bytes))
}

func ParseInt(s string) int {
	i := 0
	for _, rune := range s {
		i *= 10
		i += int(rune - '0')
	}
	return i
}

func ParseGame(line string) Game {
	i := 5 // skip "Game "
	game_id := 0
	for '0' <= line[i] && line[i] <= '9' {
		game_id *= 10
		game_id += int(line[i] - '0')
		i++
	}
	i += 2 // skip ": "

	max_red, max_green, max_blue := 0, 0, 0
	amount := 0
	for i < len(line) {
		rune := line[i]
		switch rune {
		case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
			amount *= 10
			amount += int(rune - '0')
			i++
		case 'r':
			if amount > max_red {
				max_red = amount
			}
			amount = 0
			i += 3 // skip "red"
		case 'g':
			if amount > max_green {
				max_green = amount
			}
			amount = 0
			i += 5 // skip "green"
		case 'b':
			if amount > max_blue {
				max_blue = amount
			}
			amount = 0
			i += 4 // skip "blue"
		case ';', ',':
			i += 2
		case ' ':
			i++
		}
	}
	return Game{game_id, max_red, max_green, max_blue}
}

func ParseInput(data string) []Game {
	games_str := strings.Split(data, "\n")
	games := make([]Game, len(games_str))
	for n_game, line := range games_str {
		game := ParseGame(line)
		games[n_game] = game
	}
	return games
}

func IsValidGame(game Game, max_red int, max_green int, max_blue int) bool {
	return game.max_red <= max_red && game.max_green <= max_green && game.max_blue <= max_blue
}

func Part1(games []Game, max_red int, max_green int, max_blue int) int {
	sum := 0
	for _, game := range games {
		if IsValidGame(game, max_red, max_green, max_blue) {
			sum += game.game_id
		}
	}
	return sum
}

func MinimumCubes(game Game) int {
	return game.max_red * game.max_green * game.max_blue
}

func Part2(games []Game) int {
	sum := 0
	for _, game := range games {
		sum += MinimumCubes(game)
	}
	return sum
}

func PrintTime(start time.Time, msg string) {
	dur := float64(time.Since(start).Nanoseconds())
	switch {
	case dur < 1e3:
		fmt.Printf("%v %.3fns\n", msg, dur)
	case dur < 1e6:
		fmt.Printf("%v %.3fµs\n", msg, dur/1e3)
	case dur < 1e9:
		fmt.Printf("%v %.3fms\n", msg, dur/1e6)
	default:
		fmt.Printf("%v %.3fs\n", msg, dur/1e9)
	}
}

func main() {
	start := time.Now()
	defer PrintTime(start, "Elapsed time:")

	text := ReadFile("inputs/day02.txt")
	data := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(data, 12, 13, 14))
	fmt.Printf("Part2: %d\n", Part2(data))
}
