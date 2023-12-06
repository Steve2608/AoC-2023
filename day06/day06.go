package main

import (
	"fmt"
	"math"
	"os"
	"strings"
	"time"
)

type long = int64

type Race struct {
	time     int
	distance int
}

func ReadFile(filename string) string {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return strings.TrimSpace(string(bytes))
}

func ParseInt(word string) int {
	num := 0
	for _, rune := range word {
		num *= 10
		num += int(rune - '0')
	}
	return num
}

func ParseInts(line string) []int {
	parts := strings.Fields(line)
	nums := make([]int, len(parts))
	for i, s := range parts {
		nums[i] = ParseInt(s)
	}
	return nums
}

func ParseInput(data string) ([]int, []int) {
	time_and_distance := strings.Split(data, "\n")
	time := time_and_distance[0]
	distance := time_and_distance[1]

	times := ParseInts(strings.TrimSpace(time[len("Time: "):]))
	distances := ParseInts(strings.TrimSpace(distance[len("Distance: "):]))

	return times, distances
}

func SolveClosedForm(time, distance int) (int, int) {
	time_f := float64(time)
	distance_f := float64(distance)

	discriminant := math.Sqrt(time_f*time_f - 4*distance_f)
	w_time_min := math.Floor((time_f-discriminant)/2 + 1)
	w_time_max := math.Ceil((time_f+discriminant)/2 - 1)
	
	return int(w_time_min), int(w_time_max)
}

func Part1(times, distances []int) int {
	prod := 1
	for i := 0; i < len(times); i++ {
		time := times[i]
		distance := distances[i]
		w_time_min, w_time_max := SolveClosedForm(time, distance)
		prod *= w_time_max - w_time_min + 1
	}
	return prod
}

func Part2(times, distances []int) int {
	time_str := fmt.Sprint(times)
	time := ParseInt(strings.ReplaceAll(time_str[1:len(time_str)-1], " ", ""))
	distance_str := fmt.Sprint(distances)
	distance := ParseInt(strings.ReplaceAll(distance_str[1:len(distance_str)-1], " ", ""))

	w_time_min, w_time_max := SolveClosedForm(time, distance)
	return w_time_max - w_time_min + 1
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

	text := ReadFile("inputs/day06.txt")
	times, distances := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(times, distances))
	fmt.Printf("Part2: %d\n", Part2(times, distances))
}
