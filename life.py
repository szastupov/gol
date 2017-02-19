def grid(w, h):
    for x in range(w):
        for y in range(h):
            yield x, y


def life(cells, w=40, h=20):
    def survives(cell):
        x, y = cell
        coords = [
            (x+1, y),
            (x+1, y+1),
            (x, y+1),
            (x-1, y+1),
            (x-1, y),
            (x-1, y-1),
            (x, y-1),
            (x+1, y-1)
        ]
        count = len([pos for pos in coords if pos in cells])
        if cell in cells:
            return 2 <= count <= 3
        else:
            return count == 3

    return {cell for cell in grid(w, h)
            if survives(cell)}
