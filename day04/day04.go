package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

type Ticket struct {
	ticket_id int
	want      []int
	have      []int
	winning   []int
}

func ReadFile(filename string) string {
	bytes, err := os.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	return strings.TrimSpace(string(bytes))
}

func ParseInt(line string) int {
	num := 0
	for _, c := range line {
		num *= 10
		num += int(c - '0')
	}
	return num
}

func ParseInts(parts []string) []int {
	nums := make([]int, len(parts))
	for i, part := range parts {
		nums[i] = ParseInt(part)
	}
	return nums
}

func WinningNumbers(want []int, have []int) []int {
	winning := make([]int, 0)
	for _, have_num := range have {
		for _, want_num := range want {
			if have_num == want_num {
				winning = append(winning, have_num)
			}
		}
	}
	return winning
}

func ParseInput(data string) []Ticket {
	parts := strings.Split(data, "\n")
	tickets := make([]Ticket, len(parts))
	for i, part := range parts {
		colon_idx := strings.Index(part, ":")
		pipe_idx := strings.Index(part, "|")
		ticket_id := ParseInt(strings.TrimSpace(part[len("Card "):colon_idx]))

		want_numbers := ParseInts(strings.Fields(part[colon_idx+len(": ") : pipe_idx-1]))
		have_numbers := ParseInts(strings.Fields(part[pipe_idx+len("| "):]))
		ticket := Ticket{
			ticket_id, want_numbers, have_numbers, WinningNumbers(want_numbers, have_numbers),
		}
		tickets[i] = ticket
	}
	return tickets
}

func Part1(tickets []Ticket) int {
	sum := 0
	for _, ticket := range tickets {
		if len(ticket.winning) > 0 {
			sum += 1 << (len(ticket.winning) - 1)
		}
	}
	return sum
}

func CardTree(ticket_id int, tickets []Ticket, lookup []int) int {
	ticket := tickets[ticket_id]
	n := 1
	for i := ticket_id + 1; i < ticket.ticket_id+1+len(ticket.winning); i++ {
		if lookup[i-1] == 0 {
			n += CardTree(i, tickets, lookup)
		} else {
			n += lookup[i]
		}
	}
	lookup[ticket_id] = n
	return n
}

func Part2(tickets []Ticket) int {
	// since ticket.id is 1-indexed create one extra element at the start
	tickets_one_indexed := append([]Ticket{{}}, tickets...)
	lookup := make([]int, 1+len(tickets))
	for _, ticket := range tickets {
		CardTree(ticket.ticket_id, tickets_one_indexed, lookup)
	}

	sum := 0
	for _, n_tickets := range lookup {
		sum += n_tickets
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

	text := ReadFile("inputs/day04.txt")
	data := ParseInput(text)

	fmt.Printf("Part1: %d\n", Part1(data))
	fmt.Printf("Part2: %d\n", Part2(data))
}
