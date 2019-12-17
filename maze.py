#!/usr/bin/env python3

import svgwrite
import random
import svgwrite

rows = 20
cols = 20


def squares_touching_wall(w):
    s1 = w[0:2]
    if w[2] == 'N' and w[0] != 0:
        return [s1, (w[0] - 1, w[1])]
    elif w[2] == 'W' and w[1] != 0:
        return [s1, (w[0], w[1] - 1)]
    else:
        raise RuntimeError("bad wall")


# only record walls for north and west to avoid double-recording walls (i.e. one
# box's left wall is another box's right wall). don't record outer walls.
tmpwalls = []
for r in range(rows):
    for c in range(cols):
        if r != 0:
            tmpwalls.append((r, c, 'N'))
        if c != 0:
            tmpwalls.append((r, c, 'W'))
random.shuffle(tmpwalls)

# everything starts out in its own group (unique id)
connections = {(r, c): c + r * cols for r in range(rows) for c in range(cols)}

# solve
finalwalls = []
needtodo = rows * cols - 1
while needtodo > 0:
    w = tmpwalls.pop()
    sqs = squares_touching_wall(w)
    g1, g2 = connections[sqs[0]], connections[sqs[1]]
    if g1 == g2:
        finalwalls.append(w)
    else:
        needtodo -= 1
        # merge sets
        for k, v in connections.items():
            if v == g2:
                connections[k] = g1
# copy over remaining tmpwalls
finalwalls += tmpwalls

svgfile = 'maze.svg'
dwg = svgwrite.Drawing(svgfile, profile='tiny')

boxsize = 30

for w in finalwalls:
    r, c = w[0], w[1]
    if w[2] == 'N':
        s = (c * boxsize, r * boxsize)
        e = ((c + 1) * boxsize, r * boxsize)
    else:
        s = (c * boxsize, r * boxsize)
        e = (c * boxsize, (r + 1) * boxsize)
    dwg.add(dwg.line(s, e, stroke='black'))

# outline of maze, leaving start and end open at top-right and bottom-left.
dwg.add(dwg.line((boxsize, 0), (boxsize * cols, 0), stroke='black'))
dwg.add(
    dwg.line((0, boxsize * rows), (boxsize * (cols - 1), boxsize * rows),
             stroke='black'))
dwg.add(dwg.line((0, 0), (0, boxsize * rows), stroke='black'))
dwg.add(
    dwg.line((boxsize * cols, 0), (boxsize * cols, boxsize * rows),
             stroke='black'))

dwg.save()
print("saved to %s" % svgfile)
