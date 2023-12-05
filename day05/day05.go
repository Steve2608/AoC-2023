package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

type long = int64

type Range struct {
	dst long
	src long
	len long
}

type Interval struct {
	start long
	end   long
}

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
	parts := strings.Split(line, " ")
	nums := make([]long, len(parts))
	for i, s := range parts {
		nums[i] = ParseInt(s)
	}
	return nums
}

func ParseRange(line string) Range {
	parts := strings.Split(line, " ")
	if len(parts) != 3 {
		panic("invalid range")
	}
	return Range{
		dst: ParseInt(parts[0]),
		src: ParseInt(parts[1]),
		len: ParseInt(parts[2]),
	}
}

func ParseInput(data string) ([]long, [][]Range) {
	segments := strings.Split(data, "\n\n")
	seeds := ParseInts(segments[0][len("seeds: "):])

	mappings := make([][]Range, len(segments)-1)
	for i, m := range segments[1:] {
		lines := strings.Split(m, "\n")
		ranges := make([]Range, len(lines)-1)
		for j, line := range lines[1:] {
			ranges[j] = ParseRange(line)
		}
		mappings[i] = ranges
	}

	return seeds, mappings
}

func SeedToLocation(value long, mappings [][]Range) long {
	for _, ranges := range mappings {
		for _, r := range ranges {
			if r.src <= value && value < r.src+r.len {
				value = r.dst + (value - r.src)
				break
			}
		}
	}
	return value
}

func Minimum(values []long) long {
	min := values[0]
	for _, v := range values[1:] {
		if v < min {
			min = v
		}
	}
	return min
}

func Part1(seeds []long, mappings [][]Range) long {
	locations := make([]long, len(seeds))
	for i, seed := range seeds {
		locations[i] = SeedToLocation(seed, mappings)
	}
	return Minimum(locations)
}

func Min(a, b long) long {
	if a < b {
		return a
	}
	return b
}

func Max(a, b long) long {
	if a > b {
		return a
	}
	return b
}

func MapRanges(intervals []Interval, mappings []Range) []Interval {
	done_intervals := make([]Interval, 0)
	for _, r := range mappings {
		if len(intervals) == 0 {
			return done_intervals
		}

		d_start := r.dst
		s_start := r.src
		s_end := r.src + r.len

		intervals_step := make([]Interval, 0)
		for _, interval := range intervals {
			i_start := interval.start
			i_end := interval.end

			if e := Min(i_end, s_start); e > i_start {
				intervals_step = append(intervals_step, Interval{i_start, e})
			}

			if e, s := Min(i_end, s_end), Max(i_start, s_start); e > s {
				overlap := Interval{
					d_start + (s - s_start),
					d_start + (e - s_start),
				}
				done_intervals = append(done_intervals, overlap)
			}

			if s := Max(i_start, s_end); i_end > s {
				intervals_step = append(intervals_step, Interval{s, i_end})
			}
		}
		intervals = intervals_step
	}
	return append(done_intervals, intervals...)
}

func SeedRangeToLocation(start, end long, mappings [][]Range) long {
	intervals := []Interval{{start, end}}
	for _, ranges := range mappings {
		intervals = MapRanges(intervals, ranges)
	}
	// get start for each interval
	starts := make([]long, len(intervals))
	for i, interval := range intervals {
		starts[i] = interval.start
	}
	return Minimum(starts)
}

func Part2(seeds []long, mappings [][]Range) long {
	locations := make([]long, len(seeds)/2)
	for i := 0; i < len(seeds); i += 2 {
		start := seeds[i]
		end := start + seeds[i+1]

		locations[i/2] = SeedRangeToLocation(start, end, mappings)
	}
	return Minimum(locations)
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

	text := ReadFile("inputs/day05.txt")
	seeds, mappings := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(seeds, mappings))
	fmt.Printf("Part2: %d\n", Part2(seeds, mappings))
}
