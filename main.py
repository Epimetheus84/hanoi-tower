from argparse import ArgumentParser
from typing import Dict, Any

from puzzle import HanoiTowerPuzzle


def parse_cmdline() -> Dict[str, Any]:
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
    print(f'start state: \n'
          f'{puzzle.pegs}')
    print(f'costs: \n'
          f'{puzzle.costs}')
    print(f'check decision: \n'
          f'{puzzle.check_decision}')

    decision = puzzle.solve(dst_peg_index=1)

    print(f'check decision cost = {puzzle.calc_decision_cost(puzzle.check_decision)}')

    print(f'decision: \n'
          f'{decision}')
    print(f'decision cost = {puzzle.calc_decision_cost(decision)}')

    puzzle.test_decision(puzzle.check_decision)
