package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

type Junction struct {
	left, right string
}

func ReadFile(filename string) string {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return strings.TrimSpace(string(bytes))
}

func ParseInput(text string) (string, map[string]Junction) {
	parts := strings.Split(text, "\n\n")
	directions := parts[0]
	lines := parts[1]
	nodes := make(map[string]Junction)

	for _, line := range strings.Split(lines, "\n") {
		key := line[:3]
		left := line[7:10]
		right := line[12:15]
		nodes[key] = Junction{left, right}
	}
	return directions, nodes
}

func PeriodLength(current, directions string, nodes map[string]Junction, IsEnd func(string) bool) int {
	for i := 0; ; i++ {
		if IsEnd(current) {
			return i
		}

		if directions[i%len(directions)] == 'L' {
			current = nodes[current].left
		} else {
			current = nodes[current].right
		}
	}
}

func Part1(times string, distances map[string]Junction) int {
	return PeriodLength("AAA", times, distances, func(node string) bool { return node == "ZZZ" })
}

func GCD(a, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func LCM(a, b int, ints ...int) int {
	result := a / GCD(a, b) * b
	for _, val := range ints {
		result = result / GCD(result, val) * val
	}
	return result
}

func Part2(times string, distances map[string]Junction) int {
	isEnd := func(node string) bool { return node[len(node)-1] == 'Z' }
	periods := make([]int, 0)
	for node := range distances {
		if node[len(node)-1] == 'A' {
			periods = append(periods, PeriodLength(node, times, distances, isEnd))
		}
	}
	return LCM(periods[0], periods[1], periods[2:]...)
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

	text := ReadFile("inputs/day08.txt")
	times, distances := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(times, distances))
	fmt.Printf("Part2: %d\n", Part2(times, distances))
}
