from timing_util import Timing


def get_data(data: str) -> list[str]:
    return data.split(",")


def part1(data: list[str]) -> int:
    score = 0
    for code in data:
        s = 0
        for c in code:
            s += ord(c)
            s *= 17
            s %= 256
        score += s
    return score


def part2(data: list[str]) -> int:
    boxes = [[] for _ in range(256)]
    for code in data:
        i, h = 0, 0
        while code[i].isalpha():
            h += ord(code[i])
            h *= 17
            h %= 256
            i += 1
        lens_id = code[:i]

        box = boxes[h]
        match code[i]:
            case "-":
                for j, (box_lens_id, _) in enumerate(box):
                    if box_lens_id == lens_id:
                        box.pop(j)
                        break
            case "=":
                focal_length = int(code[i + 1])
                for j, (box_lens_id, _) in enumerate(box):
                    if box_lens_id == lens_id:
                        box[j] = (lens_id, focal_length)
                        break
                else:
                    box.append((lens_id, focal_length))

    score = 0
    for box_score, box in enumerate(boxes, 1):
        for slot_score, (_, focal_score) in enumerate(box, 1):
            score += box_score * slot_score * focal_score
    return score


if __name__ == "__main__":
    with Timing("Elapsed time: "):
        with open("inputs/day15.txt") as in_file:
            data = get_data(in_file.read().strip())

        print(f"part1: {part1(data)}")
        print(f"part2: {part2(data)}")
