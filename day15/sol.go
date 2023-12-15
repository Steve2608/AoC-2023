package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

type Lens struct {
	name         string
	local_length int
}

func ReadFile(filename string) string {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return strings.TrimSpace(string(bytes))
}

func ParseInput(data string) []string {
	return strings.Split(data, ",")
}

func Part1(data []string) int {
	score := 0
	for _, code := range data {
		s := 0
		for _, c := range code {
			s += int(c)
			s *= 17
			s %= 256
		}
		score += s
	}
	return score
}

func IsAlpha(b byte) bool {
	return ('a' <= b && b <= 'z') || ('A' <= b && b <= 'Z')
}

func Part2(data []string) int {
	boxes := make([][]Lens, 256)
	for _, code := range data {
		i, hash := 0, 0
		for ; i < len(code) && IsAlpha(code[i]); i++ {
			hash += int(code[i])
			hash *= 17
			hash %= 256
		}
		lens_id := code[:i]

		box := boxes[hash]
		switch code[i] {
		case '-':
			for j, lens := range box {
				if lens.name == lens_id {
					boxes[hash] = append(box[:j], box[j+1:]...)
					break
				}
			}
		case '=':
			focal_length := int(code[i+1] - '0')
			replaced := false
			for j, lens := range box {
				if lens.name == lens_id {
					box[j].local_length = focal_length
					replaced = true
					break
				}
			}
			if !replaced {
				boxes[hash] = append(box, Lens{lens_id, focal_length})
			}
		}
	}

	score := 0
	for box_score, box := range boxes {
		for slot_score, lens := range box {
			score += (box_score + 1) * (slot_score + 1) * lens.local_length
		}
	}
	return score
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

	text := ReadFile("inputs/day15.txt")
	data := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(data))
	fmt.Printf("Part2: %d\n", Part2(data))
}
