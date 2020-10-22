MAX_RINGS_COUNT = 5
# вынес для удобства
TOWERS_COUNT = 3


class Tower:
    rings_count = 0
    rings = [0] * MAX_RINGS_COUNT

    def __init__(self, rings_count=0):
        if rings_count == 0:
            return

        self.rings_count = rings_count
        for i in range(rings_count):
            self.rings[i] = rings_count - i

    def move_ring(self, dest_tower):
        if self.rings_count <= 0:
            raise Exception("Invalid number of rings.")

        if dest_tower.rings_count > MAX_RINGS_COUNT:
            raise Exception("Destination tower has more than " + str(MAX_RINGS_COUNT) + " rings.")

        if dest_tower.rings_count > 0 and self.rings[self.rings_count - 1] > self.rings[self.rings_count - 1]:
            raise Exception("Ring cannot be moved to smaller ring.")

        self.rings_count = self.rings_count - 1

        dest_tower.rings[dest_tower.rings_count] = self.rings[self.rings_count]
        self.rings[self.rings_count] = 0

        dest_tower.rings_count = dest_tower.rings_count + 1


def get_free_tower(src_tower_index, dst_tower_index):  # получаем свободную башню
    if src_tower_index == dst_tower_index:
        raise Exception("Ring cannot be moved to the same tower.")

    if src_tower_index not in range(TOWERS_COUNT) \
            or dst_tower_index not in range(TOWERS_COUNT):
        raise Exception("Invalid indexes.")

    # в теории можно прикрутить распределение стека для случая, где TOWERS_COUNT > 3
    # но это уже просто ради креатива :)
    for i in range(TOWERS_COUNT):
        if i not in [src_tower_index, dst_tower_index]:
            return i


def move_stack(stack_size, src_tower_index, dst_tower_index):
    if stack_size == 0:
        return

    free_tower_index = get_free_tower(src_tower_index, dst_tower_index)
    move_stack(stack_size - 1, src_tower_index, free_tower_index)
    print(str(MAX_RINGS_COUNT + 1 - stack_size) + ":" + str(src_tower_index) + " - " + str(dst_tower_index))
    towers[src_tower_index].move_ring(towers[dst_tower_index])
    move_stack(stack_size - 1, free_tower_index, dst_tower_index)


def read_params(file):
    params = {}
    lines = file.readlines()
    key = ''
    for line in lines:
        line = line.strip(" \n\r/")
        if line in ['NPARTS', 'COST', 'ORDER']:
            key = line
            params[line] = []
            continue
        line = line.split('--')
        line = line[0]
        line = line.strip(" \n\r/")
        if line.__len__() == 0:
            continue
        line = line.split()
        params[key].append([int(n) for n in line])

    print(params)


def solve():
    file = open('input.txt', mode='r', encoding='utf-8-sig')
    read_params(file)
    file.close()
    towers[0] = Tower(MAX_RINGS_COUNT)
    move_stack(MAX_RINGS_COUNT, 0, 1)


towers = [Tower()] * TOWERS_COUNT
solve()
