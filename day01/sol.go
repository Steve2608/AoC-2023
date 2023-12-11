package main

import (
	"errors"
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

func ParseInput(data string) []string {
	return strings.Split(data, "\n")
}

func Reverse(s string) string {
	n := len(s)
	chunk := make([]rune, n)
	for _, rune := range s {
		n--
		chunk[n] = rune
	}
	return string(chunk[n:])
}

func IsDigit(r rune) bool {
	return '0' <= r && r <= '9'
}

func ParseInt(r rune) int {
	return int(r - '0')
}

func CalibrationNumber(line string) int {
	for _, r := range line {
		if IsDigit(r) {
			return ParseInt(r)
		}
	}
	return -1
}

func Part1(lines []string) int {
	sum := 0
	for _, line := range lines {
		first := CalibrationNumber(line)
		second := CalibrationNumber(Reverse(line))
		sum += first*10 + second
	}
	return sum
}

func ParseNumberLeft(line string) int {
	chunk := make([]rune, 0)
	for _, r := range line {
		if IsDigit(r) {
			return ParseInt(r)
		}

		if len(chunk) >= 5 {
			chunk = append(chunk[1:], r)
		} else {
			chunk = append(chunk, r)
		}

		str := string(chunk)
		if len(str) >= 3 {
			if strings.HasSuffix(str, "one") {
				return 1
			}
			if strings.HasSuffix(str, "two") {
				return 2
			}
			if strings.HasSuffix(str, "six") {
				return 6
			}
		}
		if len(str) >= 4 {
			if strings.HasSuffix(str, "four") {
				return 4
			}
			if strings.HasSuffix(str, "five") {
				return 5
			}
			if strings.HasSuffix(str, "nine") {
				return 9
			}
		}
		if str == "three" {
			return 3
		}
		if str == "seven" {
			return 7
		}
		if str == "eight" {
			return 8
		}
	}
	panic(errors.New("illegal state reached"))
}

func ParseNumberRight(line string) int {
	chunk := make([]rune, 0)
	for _, r := range line {
		if IsDigit(r) {
			return ParseInt(r)
		}

		if len(chunk) >= 5 {
			chunk = append([]rune{r}, chunk[:4]...)
		} else {
			chunk = append([]rune{r}, chunk...)
		}

		str := string(chunk)
		if len(str) >= 3 {
			if strings.HasPrefix(str, "one") {
				return 1
			}
			if strings.HasPrefix(str, "two") {
				return 2
			}
			if strings.HasPrefix(str, "six") {
				return 6
			}
		}
		if len(str) >= 4 {
			if strings.HasPrefix(str, "four") {
				return 4
			}
			if strings.HasPrefix(str, "five") {
				return 5
			}
			if strings.HasPrefix(str, "nine") {
				return 9
			}
		}
		if str == "three" {
			return 3
		}
		if str == "seven" {
			return 7
		}
		if str == "eight" {
			return 8
		}
	}
	panic(errors.New("illegal state reached"))
}

func Part2(lines []string) int {
	sum := 0
	for _, line := range lines {
		first := ParseNumberLeft(line)
		second := ParseNumberRight(Reverse(line))
		sum += first*10 + second
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

	text := ReadFile("inputs/day01.txt")
	data := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(data))
	fmt.Printf("Part2: %d\n", Part2(data))
}
