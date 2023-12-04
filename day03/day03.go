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

func ParseInt(line string, i int) int {
	// find start of number
	for i > 0 && '0' <= line[i-1] && line[i-1] <= '9' {
		i--
	}

	num := 0
	for ; i < len(line) && '0' <= line[i] && line[i] <= '9'; i++ {
		num *= 10
		num += int(line[i] - '0')
	}
	return num
}

func ParseInput(data *string) []string {
	return strings.Split(*data, "\n")
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

func Part1(lines *[]string) int {
	sum := 0
	for i, line := range *lines {
		for j, rune := range line {
			if rune == '.' || '0' <= rune && rune <= '9' {
				continue
			}

			for k := Max(0, i-1); k <= Min(i+1, len(*lines)); k++ {
				// new line always ends previous number
				prev_was_number := false
				for l := Max(0, j-1); l <= Min(j+1, len(line)); l++ {
					if k == i && l == j {
						// center point always ends previous number
						prev_was_number = false
						continue
					}

					if '0' <= (*lines)[k][l] && (*lines)[k][l] <= '9' {
						if !prev_was_number {
							sum += ParseInt((*lines)[k], l)
						}
						prev_was_number = true
					} else {
						prev_was_number = false
					}
				}
			}
		}
	}
	return sum
}

func Part2(lines *[]string) int {
	sum := 0
	for i, line := range *lines {
		for j, rune := range line {
			if rune != '*' {
				continue
			}

			gears := make([]int, 0)
			for k := Max(0, i-1); k <= Min(i+1, len(*lines)); k++ {
				// new line always ends previous number
				prev_was_number := false
				for l := Max(0, j-1); l <= Min(j+1, len(line)); l++ {
					if k == i && l == j {
						// center point always ends previous number
						prev_was_number = false
						continue
					}

					if '0' <= (*lines)[k][l] && (*lines)[k][l] <= '9' {
						if !prev_was_number {
							gears = append(gears, ParseInt((*lines)[k], l))
						}
						prev_was_number = true
					} else {
						prev_was_number = false
					}
				}
			}
			if len(gears) == 2 {
				sum += gears[0] * gears[1]
			}
		}
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

	text := ReadFile("inputs/day03.txt")
	data := ParseInput(&text)

	fmt.Printf("Part1: %d\n", Part1(&data))
	fmt.Printf("Part2: %d\n", Part2(&data))
}
