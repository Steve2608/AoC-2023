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

func ParseInput(data string) [][]rune {
	grid := strings.Split(data, "\n")
	result := make([][]rune, len(grid))
	for i, line := range grid {
		result[i] = []rune(line)
	}
	return result
}

func StepNorth(state [][]rune) {
	has_changed := true
	for has_changed {
		has_changed = false
		for y := 1; y < len(state); y++ {
			for x, val := range state[y] {
				if val == 'O' && state[y-1][x] == '.' {
					i := y - 1
					for i >= 1 && state[i-1][x] == '.' {
						i--
					}

					state[i][x] = 'O'
					state[y][x] = '.'
					has_changed = true
				}
			}
		}
	}
}

func Score(state [][]rune) int {
	s := 0
	for i, row := range state {
		for _, val := range row {
			if val == 'O' {
				s += len(state) - i
			}
		}
	}
	return s
}

func clone(data [][]rune) [][]rune {
	result := make([][]rune, len(data))
	for i, row := range data {
		result[i] = make([]rune, len(row))
		copy(result[i], row)
	}
	return result
}

func Part1(data [][]rune) int {
	return Score(clone(data))
}

func StepWest(state [][]rune) {
    has_changed := true
	for has_changed {
		has_changed = false
		for _, row := range state {
			for x := 1; x < len(row); x++ {
				val := row[x]
				if val == 'O' && row[x-1] == '.' {
					i := x - 1
					for i >= 1 && row[i-1] == '.' {
						i--
					}

					row[i] = 'O'
					row[x] = '.'
					has_changed = true
				}
			}
		}
	}
}

func StepSouth(state [][]rune) {
    has_changed := true
	for has_changed {
        has_changed = false
		for y := len(state) - 2; y >= 0; y-- {
            for x, val := range state[y] {
                if val == 'O' && state[y+1][x] == '.' {
                    i := y + 1
					for i < len(state)-1 && state[i+1][x] == '.' {
                        i++
					}
                    
					state[i][x] = 'O'
					state[y][x] = '.'
					has_changed = true
				}
			}
		}
	}
}

func StepEast(state [][]rune) {
    has_changed := true
    for has_changed {
        has_changed = false
        for _, row := range state {
            for x := len(row) - 2; x >= 0; x-- {
                val := row[x]
                if val == 'O' && row[x+1] == '.' {
                    i := x + 1
                    for i < len(row)-1 && row[i+1] == '.' {
                        i++
                    }

                    row[i] = 'O'
                    row[x] = '.'
                    has_changed = true
                }
            }
        }
    }
}

func Cycle(state [][]rune) {
    StepNorth(state)
	StepWest(state)
	StepSouth(state)
	StepEast(state)
}

func ToString(data [][]rune) string {
	s := make([]rune, (len(data)+1)*len(data[0]))
	i := 0
	for _, row := range data {
		copy(s[i:], row)
		i += len(row)
        // make it printable as well :)
		s[i] = '\n'
		i++
	}
	return string(s)
}

func Part2(data [][]rune, n_cycles int) int {
	state_to_iteration := make(map[string]int)
	iteration_to_state := make([][][]rune, 0)

	state := data
	for i := 0; ; i++ {
		str := ToString(state)
		if _, ok := state_to_iteration[str]; ok {
			break
		}
		state_to_iteration[str] = i
		iteration_to_state = append(iteration_to_state, clone(state))

		Cycle(state)
	}

	first_reached := state_to_iteration[ToString(data)]
	cycles_remaining := n_cycles - first_reached
	cycles_remaining %= len(iteration_to_state) - first_reached

	state = iteration_to_state[first_reached+cycles_remaining]
	return Score(state)
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

	text := ReadFile("inputs/day14.txt")
	data := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(data))
	fmt.Printf("Part2: %d\n", Part2(data, 1_000_000_000))
}
