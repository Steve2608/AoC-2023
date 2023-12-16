package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

type Entry struct {
	coord     Coordinate
	direction string
}

type Coordinate struct {
	x, y int
}

func ReadFile(filename string) string {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return strings.TrimSpace(string(bytes))
}

func ParseInput(data string) []string {
	return strings.Split(data, "\n")
}

func FollowPath(data []string, x, y int, direction string, already_visited map[Entry]bool) {
	for 0 <= y && y < len(data) && 0 <= x && x < len(data[y]) {
		key := Entry{Coordinate{x, y}, direction}
		if _, ok := already_visited[key]; ok {
			return
		}
		already_visited[key] = true

		switch direction {
		case "right":
			switch data[y][x] {
			case '|':
				FollowPath(data, x, y-1, "up", already_visited)
				FollowPath(data, x, y+1, "down", already_visited)
			case '-':
				x++
			case '/':
				y--
				direction = "up"
			case '\\':
				y++
				direction = "down"
			case '.':
				x++
			}
		case "left":
			switch data[y][x] {
			case '|':
				FollowPath(data, x, y-1, "up", already_visited)
				FollowPath(data, x, y+1, "down", already_visited)
			case '-':
				x--
			case '/':
				y++
				direction = "down"
			case '\\':
				y--
				direction = "up"
			case '.':
				x--
			}
		case "up":
			switch data[y][x] {
			case '|':
				y--
			case '-':
				FollowPath(data, x-1, y, "left", already_visited)
				FollowPath(data, x+1, y, "right", already_visited)
			case '/':
				x++
				direction = "right"
			case '\\':
				x--
				direction = "left"
			case '.':
				y--
			}
		case "down":
			switch data[y][x] {
			case '|':
				y++
			case '-':
				FollowPath(data, x-1, y, "left", already_visited)
				FollowPath(data, x+1, y, "right", already_visited)
			case '/':
				x--
				direction = "left"
			case '\\':
				x++
				direction = "right"
			case '.':
				y++
			}
		}
	}
}

func PathLength(data []string, x, y int, direction string) int {
	already_visited := make(map[Entry]bool)
	FollowPath(data, x, y, direction, already_visited)
	visited := make(map[Coordinate]bool)
	for entry := range already_visited {
		visited[entry.coord] = true
	}
	return len(visited)
}

func Part1(data []string) int {
	return PathLength(data, 0, 0, "right")
}

func Max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func Part2(data []string) int {
	max_y := len(data) - 1
	max_x := len(data[0]) - 1
	max_energized := 0
	for y := 0; y <= max_y; y++ {
		max_energized = Max(max_energized, PathLength(data, 0, y, "right"))
		max_energized = Max(max_energized, PathLength(data, max_x, y, "left"))
	}
	for x := 0; x <= max_x; x++ {
		max_energized = Max(max_energized, PathLength(data, x, 0, "down"))
		max_energized = Max(max_energized, PathLength(data, x, max_y, "up"))
	}
	return max_energized
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

	text := ReadFile("inputs/day16.txt")
	data := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(data))
	fmt.Printf("Part2: %d\n", Part2(data))
}
