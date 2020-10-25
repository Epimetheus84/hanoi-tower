from argparse import ArgumentParser
from typing import Dict

from puzzle import HanoiTowerPuzzle


def parse_cmdline() -> Dict[str, object]:
    parser = ArgumentParser(description='Solves "Tower of Hanoi" puzzle')
    parser.add_argument('input_file', type=str, help='An input file path')
    args = parser.parse_args()
    return {
        'input_file': args.input_file
    }


if __name__ == '__main__':
    args = parse_cmdline()
    input_file = args['input_file']
    puzzle = HanoiTowerPuzzle.load_from_file(input_file)
    print(puzzle.pins)
    print(puzzle.costs)
    print(puzzle.test_decision)
