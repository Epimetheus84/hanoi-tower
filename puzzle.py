from __future__ import annotations

import re
from typing import List, Tuple

# (disk_index, source_pin_number, destination_pin_number)
Step = Tuple[int, int, int]
Decision = List[Step]


class HanoiTowerPuzzleException(RuntimeError):
    pass


class HanoiTowerPuzzle:
    def __init__(self, disks_number: int, costs: List[int], test_decision: Decision = None):
        self.pins = []
        for pin_index in range(len(costs)):
            self.pins.append([])
        self.pins[0] = [(disks_number - 1 - disk_index) for disk_index in range(disks_number)]
        self.costs = costs
        self.test_decision = test_decision

    def solve(self) -> Decision:
        pass

    def calc_decision_cost(self, decision: Decision) -> int:
        cost = 0
        for (_, _, dest_pin_number) in decision:
            cost += dest_pin_number * self.costs[dest_pin_number]
        return cost

    @staticmethod
    def load_from_file(path: str) -> HanoiTowerPuzzle:
        pins_number = None
        costs = []
        orders = []
        with open(path, 'r') as input_file:
            file_content_lines = input_file.readlines()
            file_content = ''
            for line in file_content_lines:
                commentary_index = line.find('--')
                if commentary_index >= 0:
                    file_content += line[:commentary_index] + ' '
                else:
                    file_content += line + ' '
            file_content = re.sub('[ \n\r]+', ' ', file_content)
            blocks = list(map(lambda x: x.strip(), file_content.split('/')))[:-1]
            for block in blocks:
                block_split = block.split(' ')
                if block.startswith('INIT'):
                    _, key, pins_number = block_split
                    if key != 'NPARTS':
                        raise HanoiTowerPuzzleException('Incorrect input data')
                elif block.startswith('COST'):
                    split = block_split
                    costs = list(map(lambda x: int(x), split[1:]))
                elif block.startswith('ORDER'):
                    order_content = block_split[1:]
                    orders = [
                        list(map(lambda x: int(x), order_content[i:i + 3]))
                        for i in range(0, len(order_content), 3)
                    ]
                else:
                    key, pins_number = block_split
                    if key != 'NPARTS':
                        raise HanoiTowerPuzzleException('Incorrect input data')
        if not pins_number or not costs or not orders:
            raise HanoiTowerPuzzleException('Incorrect input data')
        return HanoiTowerPuzzle(int(pins_number), costs, orders)
