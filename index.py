MAX_RINGS_COUNT = 4
# вынес для удобства
TOWERS_COUNT = 4
TOTAL_MOVEMENTS = 0


class Tower:
    rings_count = 0
    rings = [0] * MAX_RINGS_COUNT
    cost = 0

    def __init__(self, rings_count=0, cost=0):
        if rings_count == 0:
            return

        self.cost = 0
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


def get_free_tower(exclude_indexes):  # получаем свободную башню
    # находим башню с минимальной стоимостью на перестановку
    free_tower_index = 0
    min_cost = 0
    for i in range(TOWERS_COUNT):
        if i not in exclude_indexes:
            temp_cost = towers[i].cost * towers[i].rings_count
            # print(i, temp_cost)
            if min_cost == 0 or min_cost > temp_cost:
                min_cost = temp_cost
                free_tower_index = i

    return free_tower_index


# для 3 и 5+
def move_stack(stack_size, src_tower_index, dst_tower_index):
    if stack_size == 0:
        return

    free_tower_index = get_free_tower([src_tower_index, dst_tower_index])
    move_stack(stack_size - 2, src_tower_index, free_tower_index)
    towers[src_tower_index].move_ring(towers[dst_tower_index])
    move_stack(stack_size - 2, free_tower_index, dst_tower_index)


# для 4
def move_stack_reve(stack_size, src_tower_index, dst_tower_index, free_tower_index_1, free_tower_index_2):
    if stack_size == 0:
        return

    if stack_size == 1:
        towers[src_tower_index].move_ring(towers[dst_tower_index])
        return

    move_stack_reve(stack_size - 2, src_tower_index, free_tower_index_1, free_tower_index_2, dst_tower_index)

    towers[src_tower_index].move_ring(towers[free_tower_index_2])
    towers[src_tower_index].move_ring(towers[dst_tower_index])
    towers[free_tower_index_2].move_ring(towers[dst_tower_index])

    move_stack_reve(stack_size - 2, free_tower_index_1, dst_tower_index, src_tower_index, free_tower_index_2)


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
    src_tower_index = 0
    dst_tower_index = 1

    if TOWERS_COUNT == 4:
        free_tower_index_1 = get_free_tower([src_tower_index, dst_tower_index])
        free_tower_index_2 = get_free_tower([src_tower_index, dst_tower_index, free_tower_index_1])
        move_stack_reve(MAX_RINGS_COUNT, src_tower_index, dst_tower_index, free_tower_index_1, free_tower_index_2)
    else:
        move_stack(MAX_RINGS_COUNT, src_tower_index, dst_tower_index)


towers = [Tower()] * TOWERS_COUNT
towers[0].cost = 1
towers[1].cost = 2
towers[2].cost = 4
towers[3].cost = 6
solve()
