from __future__ import annotations

import re
from typing import List, Tuple, Optional

# (disk_index, source_pin_number, destination_pin_number)
Step = Tuple[int, int, int]
Decision = List[Step]


class HanoiTowerPuzzleException(RuntimeError):
    pass


class HanoiTowerPuzzle:
    def __init__(self, disks_number: int, costs: List[int], check_decision: Decision = None, src_peg_index: int = 0,
                 dst_peg_index: int = 1):
        self.costs = costs
        self.disks_number = disks_number
        self.src_peg_index = src_peg_index
        self.dst_peg_index = dst_peg_index
        self.check_decision = check_decision
        self.decision = []
        self.pegs = []
        self._reset_pegs()

    def solve(self, dst_peg_index: int = None) -> Optional[Decision]:
        if not dst_peg_index:
            dst_peg_index = self._get_optimal_peg([self.src_peg_index])
        disks_number = len(self.pegs[self.src_peg_index])
        pegs_number = len(self.pegs)
        if pegs_number == 4:
            free_peg_index_1 = self._get_optimal_peg([self.src_peg_index, dst_peg_index])
            free_peg_index_2 = self._get_optimal_peg([self.src_peg_index, dst_peg_index, free_peg_index_1])
            self._move_stack_reve(disks_number, self.src_peg_index, dst_peg_index, free_peg_index_1, free_peg_index_2)
        else:
            self._move_stack(disks_number, self.src_peg_index, dst_peg_index)
        return self.decision

    def calc_decision_cost(self, decision: Decision) -> int:
        cost = 0
        for (_, _, dest_peg_number) in decision:
            cost += self.costs[dest_peg_number]
        return cost

    def _reset_pegs(self):
        self.pegs = []
        for peg_index in range(len(self.costs)):
            self.pegs.append([])
        self.pegs[0] = [(self.disks_number - 1 - disk_index) for disk_index in range(self.disks_number)]

    def test_decision(self, decision: Decision):
        self._reset_pegs()
        for (ring_number, src_reg_number, dest_peg_number) in decision:
            self._move_disk(src_reg_number, dest_peg_number, ring_number)

        if len(self.pegs[self.dst_peg_index]) != self.disks_number:
            raise Exception("The problem isn't solved, some rings are still not moved")

    @staticmethod
    def load_from_file(path: str) -> HanoiTowerPuzzle:
        pegs_number = None
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
                    _, key, pegs_number = block_split
                    if key != 'NPARTS':
                        raise HanoiTowerPuzzleException('Incorrect input data')
                elif block.startswith('COST'):
                    split = block_split
                    costs = list(map(lambda x: int(x), split[1:]))
                elif block.startswith('ORDER'):
                    order_content = block_split[1:]
                    orders = [
                        tuple(map(lambda x: int(x), order_content[i:i + 3]))
                        for i in range(0, len(order_content), 3)
                    ]
                else:
                    key, pegs_number = block_split
                    if key != 'NPARTS':
                        raise HanoiTowerPuzzleException('Incorrect input data')
        if not pegs_number or not costs or not orders:
            raise HanoiTowerPuzzleException('Incorrect input data')
        return HanoiTowerPuzzle(int(pegs_number), costs, orders)

    def _move_stack(self, stack_size: int, src_peg_index: int, dst_peg_index: int):
        if stack_size == 0:
            return
        optimal_peg_index = self._get_optimal_peg([src_peg_index, dst_peg_index])
        self._move_stack(stack_size - 1, src_peg_index, optimal_peg_index)
        step = self._move_disk(src_peg_index, dst_peg_index)
        self.decision.append(step)
        self._move_stack(stack_size - 1, optimal_peg_index, dst_peg_index)

    def _move_stack_reve(self, stack_size, src_peg_index, dst_peg_index, free_peg_index_1, free_peg_index_2):
        if stack_size == 0:
            return
        if stack_size == 1:
            step = self._move_disk(src_peg_index, dst_peg_index)
            self.decision.append(step)
            return
        self._move_stack_reve(stack_size - 2, src_peg_index, free_peg_index_1, free_peg_index_2, dst_peg_index)

        step = self._move_disk(src_peg_index, free_peg_index_2)
        self.decision.append(step)
        step = self._move_disk(src_peg_index, dst_peg_index)
        self.decision.append(step)
        step = self._move_disk(free_peg_index_2, dst_peg_index)
        self.decision.append(step)

        self._move_stack_reve(stack_size - 2, free_peg_index_1, dst_peg_index, src_peg_index, free_peg_index_2)

    def _get_optimal_peg(self, exclude_indices: List[int] = None) -> int:
        max_int = 2147483647
        src_peg_top = max_int
        optimal_peg_index = 0
        optimal_peg_cost = max_int
        for peg_index, peg_disks in enumerate(self.pegs):
            if (exclude_indices is not None) and (peg_index in exclude_indices):
                continue
            peg_top = peg_disks[-1] if len(peg_disks) > 0 else -1
            peg_cost = self.costs[peg_index]
            if peg_top < src_peg_top and peg_cost < optimal_peg_cost:
                optimal_peg_index = peg_index
                optimal_peg_cost = peg_cost
        return optimal_peg_index

    def _move_disk(self, src_peg_index, dst_peg_index, test_disk_number = None) -> Step:
        if src_peg_index == dst_peg_index:
            raise Exception("The ring cannot be transferred to the same peg")

        disk = self.pegs[src_peg_index].pop()

        if test_disk_number:
            test_disk_number = int(test_disk_number)

            if disk < test_disk_number:
                raise Exception("Ring " + str(test_disk_number) +
                                " cannot be moved until ring " + str(test_disk_number - 1) + " is moved")

            if disk > test_disk_number:
                raise Exception("Ring " + str(test_disk_number) + " isn't located in peg " + str(dst_peg_index + 1))

        self.pegs[dst_peg_index].append(disk)
        return disk, src_peg_index, dst_peg_index
