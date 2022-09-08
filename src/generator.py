from qrcode import QRCode


def draw_rect(code, start, end, state=True):
  for y in range(start[1], end[1]+1):
    for x in range(start[0], end[0]+1):
      code.board[y][x].state = state

def add_trackers(code):

  # Draw small trackers
  locs = []
  ul = (6, 6)
  lr = (code.size-7, code.size-7)
  if code.version > 1:
    locs.append(lr)
    size = lr[0]-ul[0]
    steps = [ul[0]]
    for stepsize in [30, 28, 26, 24, 22, 20, 18, 16]:
      rem = size % stepsize
      if rem % 2 == 0 and (rem == 0 or rem == 24):
        if rem > 0:
          steps.append(rem)
        steps.extend([stepsize] * int(size / stepsize))
        y = 0
        for ys in steps:
          y += ys
          x = 0
          for xs in steps:
            x += xs
            if (x == ul[0] or x == lr[0]) and (y == ul[1] or y == lr[1]):
              continue
            locs.append((x, y))
        break



  for loc in locs:
    x, y = loc
    draw_rect(code, (x-2, y-2), (x+2, y+2), False)
    draw_rect(code, (x-1, y-1), (x+1, y+1), True)
    draw_rect(code, (x, y), (x, y), False)

  # Draw large trackers
  for start in [(0, 0), (0, code.size-7), (code.size-7, 0)]:
    sx, sy = start
    draw_rect(code, (sx+0, sy+0), (sx+6, sy+6), False)
    draw_rect(code, (sx+1, sy+1), (sx+5, sy+5), True)
    draw_rect(code, (sx+2, sy+2), (sx+4, sy+4), False)

  # Draw timings
  for i in range(6, code.size-7):
    code.board[i][6].state = i % 2
    code.board[6][i].state = i % 2

def generate(message):
  code = QRCode(10, True)

  add_trackers(code)

  print(message)
  return code