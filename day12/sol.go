package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

type Record struct {
	record string
	groups []int
}

type State struct {
	r_i, g_i, streak int
}

func ReadFile(filename string) string {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return strings.TrimSpace(string(bytes))
}

func ParseInt(s string) int {
	n := 0
	for _, c := range s {
		n = n*10 + int(c-'0')
	}
	return n
}

func ParseInput(text string) []Record {
	lines := strings.Split(text, "\n")
	records := make([]Record, len(lines))
	for i, line := range lines {
		fields := strings.Split(line, " ")

		record := fields[0]
		groups_str := strings.Split(fields[1], ",")
		groups := make([]int, len(groups_str))
		for j, group_str := range groups_str {
			groups[j] = ParseInt(group_str)
		}

		records[i] = Record{record, groups}
	}
	return records
}

func Solve(record Record, cache map[State]int, r_i, g_i, streak int) int {
	state := State{r_i, g_i, streak}
	if val, ok := cache[state]; ok {
		return val
	}

	if r_i >= len(record.record) {
		if streak == 0 && g_i == len(record.groups) {
			return 1
		}
		if g_i == len(record.groups)-1 && streak == record.groups[g_i] {
			return 1
		}
		return 0
	}

	n := 0
	switch record.record[r_i] {
	case '.':
		if streak == 0 {
			n = Solve(record, cache, r_i+1, g_i, 0)
		} else if g_i < len(record.groups) && streak == record.groups[g_i] {
			n = Solve(record, cache, r_i+1, g_i+1, 0)
		}
	case '#':
		n = Solve(record, cache, r_i+1, g_i, streak+1)
	case '?':
		if streak == 0 {
			n = Solve(record, cache, r_i+1, g_i, 0)
		} else if g_i < len(record.groups) && streak == record.groups[g_i] {
			n = Solve(record, cache, r_i+1, g_i+1, 0)
		}
		n += Solve(record, cache, r_i+1, g_i, streak+1)
	}

	cache[state] = n
	return n
}

func Part1(records []Record) int {
	sum := 0
	for _, record := range records {
		sum += Solve(record, make(map[State]int), 0, 0, 0)
	}
	return sum
}

func Part2(records []Record) int {
	sum := 0
	for _, record := range records {
		r := make([]byte, len(record.record)*5)
		for i := 0; i < 5; i++ {
			copy(r[i*len(record.record):(i+1)*len(record.record)], record.record)
		}
		g := make([]int, len(record.groups)*5)
		for i := 0; i < 5; i++ {
			copy(g[i*len(record.groups):(i+1)*len(record.groups)], record.groups)
		}

		sum += Solve(Record{string(r), g}, make(map[State]int), 0, 0, 0)
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

	text := ReadFile("inputs/day12.txt")
	records := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(records))
	fmt.Printf("Part2: %d\n", Part2(records))
}
