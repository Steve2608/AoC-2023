package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

type Point struct {
	x, y int
}

func ReadFile(filename string) string {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return strings.TrimSpace(string(bytes))
}

func ParseInput(data string) ([]int, []int, []Point) {
	rows := make([]int, 0)
	cols := make([]int, 0)
	galaxies := make([]Point, 0)
	grid := strings.Split(data, "\n")
	for i, line := range grid {
		for j, val := range line {
			if val == '#' {
				galaxies = append(galaxies, Point{i, j})
			}
		}
	}
	for i := range grid {
		append_row := true
		for _, g := range galaxies {
			if i == g.x {
				append_row = false
				break
			}
		}
		if append_row {
			rows = append(rows, i)
		}
	}
	for j := range grid[0] {
		append_col := true
		for _, g := range galaxies {
			if j == g.y {
				append_col = false
				break
			}
		}
		if append_col {
			cols = append(cols, j)
		}
	}

	return rows, cols, galaxies
}

func Min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func Max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func Abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func ManhattanDistance(a, b Point) int {
	return Abs(a.x-b.x) + Abs(a.y-b.y)
}

func solve(rows, cols []int, galaxies []Point, expansion int) int {
	galaxies_adjusted := make([]Point, len(galaxies))
	copy(galaxies_adjusted, galaxies)

	for i, g := range galaxies {
		n_r := 0
		for _, row := range rows {
			if g.x > row {
				n_r++
			}
		}
		galaxies_adjusted[i].x += (expansion - 1) * n_r

		n_c := 0
		for _, col := range cols {
			if g.y > col {
				n_c++
			}
		}
		galaxies_adjusted[i].y += (expansion - 1) * n_c
	}

	sum := 0
	for i := range galaxies_adjusted {
		for j := i + 1; j < len(galaxies_adjusted); j++ {
			sum += ManhattanDistance(galaxies_adjusted[i], galaxies_adjusted[j])
		}
	}
	return sum
}

func Part1(rows, cols []int, galaxies []Point) int {
	return solve(rows, cols, galaxies, 2)
}

func Part2(rows, cols []int, galaxies []Point) int {
	return solve(rows, cols, galaxies, 1_000_000)
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

	text := ReadFile("inputs/day11.txt")
	rows, cols, data := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(rows, cols, data))
	fmt.Printf("Part2: %d\n", Part2(rows, cols, data))
}
