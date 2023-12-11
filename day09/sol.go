package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

type long = int64

func ReadFile(filename string) string {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return strings.TrimSpace(string(bytes))
}

func ParseInt(word string) long {
	num := long(0)
	for _, rune := range word {
		num *= 10
		num += long(rune - '0')
	}
	return num
}

func ParseInts(line string) []long {
	parts := strings.Fields(line)
	nums := make([]long, len(parts))
	for i, s := range parts {
		if s[0] == '-' {
			nums[i] = -ParseInt(s[1:])
		} else {
			nums[i] = ParseInt(s)
		}
	}
	return nums
}

func ParseInput(data string) [][]long {
	lines := strings.Split(data, "\n")
	sequences := make([][]long, len(lines))
	for i, line := range lines {
		sequences[i] = ParseInts(line)
	}
	return sequences
}

func AllZero(sequence []long) bool {
	for _, value := range sequence {
		if value != 0 {
			return false
		}
	}
	return true
}

func Differences(sequence []long) []long {
	diffs := make([]long, len(sequence)-1)
	for i := 0; i < len(sequence)-1; i++ {
		diffs[i] = sequence[i+1] - sequence[i]
	}
	return diffs
}

func NextForward(sequence []long) long {
	if AllZero(sequence) {
		return long(0)
	}
	return sequence[len(sequence)-1] + NextForward(Differences(sequence))
}

func Part1(sequences [][]long) long {
	sum := long(0)
	for _, sequence := range sequences {
		sum += NextForward(sequence)
	}
	return sum
}

func NextBackward(sequence []long) long {
	if AllZero(sequence) {
		return long(0)
	}
	return sequence[0] - NextBackward(Differences(sequence))
}

func Part2(sequences [][]long) long {
	sum := long(0)
	for _, sequence := range sequences {
		sum += NextBackward(sequence)
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

	text := ReadFile("inputs/day09.txt")
	data := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(data))
	fmt.Printf("Part2: %d\n", Part2(data))
}
