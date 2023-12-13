package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

func ReadFile(filename string) string {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return strings.TrimSpace(string(bytes))
}

func ParseInput(data string) ([]int, []int, [][]int) {
	rows := make([]int, 0)
	cols := make([]int, 0)
	galaxies := make([][]int, 0)
	grid := strings.Split(data, "\n")
	for i, line := range grid {
		for j, val := range line {
			if val == '#' {
				galaxies = append(galaxies, []int{i, j})
			}
		}
	}
	for i := range grid {
		append_row := true
		for _, g := range galaxies {
			if i == g[0] {
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
			if j == g[1] {
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

func ManhattanDistance(a, b, rows, cols []int, expansion int) int {
	src_x, src_y := a[0], a[1]
	dst_x, dst_y := b[0], b[1]

	min_x := Min(src_x, dst_x)
	max_x := Max(src_x, dst_x)
	min_y := Min(src_y, dst_y)
	max_y := Max(src_y, dst_y)

	n_rows := 0
	for _, row := range rows {
		if min_x < row && row < max_x {
			n_rows++
		}
	}

	n_cols := 0
	for _, col := range cols {
		if min_y < col && col < max_y {
			n_cols++
		}
	}

	return (max_x - min_x) + (max_y - min_y) + (n_rows+n_cols)*expansion
}

func solve(rows, cols []int, galaxies [][]int, expansion int) int {
	sum := 0
	for i := range galaxies {
		for j := i + 1; j < len(galaxies); j++ {
			sum += ManhattanDistance(galaxies[i], galaxies[j], rows, cols, expansion-1)
		}
	}
	return sum
}

func Part1(rows, cols []int, galaxies [][]int) int {
	return solve(rows, cols, galaxies, 2)
}

func Part2(rows, cols []int, galaxies [][]int) int {
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
