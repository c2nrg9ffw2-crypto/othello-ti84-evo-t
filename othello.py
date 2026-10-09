# Othello (Reversi) for the TI-84 Evo
# Put a disc so that you trap the other colour in a line: those discs flip
# to your colour. Most discs at the end wins.
# Keys: arrows = move, enter = place, clear = quit
import random
from ti_draw import clear, set_color, draw_text
from ti_draw import fill_rect as ti_fill_rect
try:
    from ti_draw import get_screen_dim
    SW, SH = get_screen_dim()
except:
    SW, SH = 319, 209

# Keep every box inside the screen and never stop the game over one box.
# The Evo draws boxes 1 pixel too small, so we ask for 1 pixel more.
def fill_rect(x, y, w, h):
    if x < 0:
        w, x = w + x, 0
    if y < 0:
        h, y = h + y, 0
    w, h = min(w, SW - x), min(h, SH - y)
    if w > 0 and h > 0:
        try:
            ti_fill_rect(x, y, w + 1, h + 1)
        except:
            pass
# Draw in a hidden buffer and show the finished picture at once: no flicker
try:
    from ti_draw import use_buffer, paint_buffer
    use_buffer()
except:
    paint_buffer = None
try:
    from ti_system import get_key as read_key
except:
    from ti_system import getKey as read_key
# On the Evo get_key wants one number. Find out once at the start.
try:
    read_key()
    key = read_key
except TypeError:
    def key():
        return read_key(0)
try:
    from ti_system import store_list, recall_list
except:
    store_list = recall_list = None
try:
    from time import sleep
except:
    from ti_system import sleep
try:
    import gc
except:
    gc = None

LEFT = (2, 24)
RIGHT = (1, 26)
UP = (3, 25)
DOWN = (4, 34)
OK = (5, 105)                 # enter
SECOND = (21, 22)             # 2nd, mode
QUIT = (9, 45)                # clear
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
YELLOW = (255, 220, 0)

def paint():
    if paint_buffer:
        paint_buffer()

def write(x, y, s):                    # text that can never stop the game
    try:
        draw_text(x, y, s)
    except:
        pass

def wait_for(keys):
    paint()
    while True:
        k = key()
        if k in keys:
            return k
        sleep(0.05)

# Numbers saved in a calculator list, so they stay after quitting
def load(name, n):
    try:
        l = [int(v) for v in recall_list(name)]
    except:
        l = []
    return (l + [0] * n)[:n]

def save(name, l):
    try:
        store_list(name, l)
    except:
        pass

# Text panel on the right side: rows 30 px high, the whole row is wiped first
def text(row, s, col=WHITE):
    set_color(*BLACK)
    fill_rect(TX, row * 30, SW - TX, 29)
    set_color(*col)
    write(TX, row * 30 + 22, s)

def box_frame(x, y, w, h, t, col):     # a frame t pixels thick
    set_color(*col)
    fill_rect(x, y, w, t)
    fill_rect(x, y + h - t, w, t)
    fill_rect(x, y, t, h)
    fill_rect(x + w - t, y, t, h)

def title_screen(name, col, line):
    clear()
    set_color(*BLACK)
    fill_rect(0, 0, SW, SH)
    set_color(*col)
    write(SW // 2 - 80, 25, name)
    set_color(*WHITE)
    write(SW // 2 - 80, 55, line)

# A menu on the start screen. Returns the chosen number, or -1 for clear.
def menu(options, choice, hint):
    x = SW // 2 - 80
    set_color(*BLACK)
    fill_rect(0, 64, SW, SH - 64)
    set_color(*WHITE)
    write(x, 202, hint)
    while True:
        for i in range(len(options)):
            set_color(*BLACK)
            fill_rect(x - 20, 64 + i * 28, 230, 27)
            set_color(*(YELLOW if i == choice else GREY))
            write(x, 90 + i * 28, ("> " if i == choice else "  ") + options[i])
        k = wait_for(UP + DOWN + OK + QUIT)
        if k in QUIT:
            return -1
        if k in OK:
            return choice
        if k in UP:
            choice = (choice - 1) % len(options)
        if k in DOWN:
            choice = (choice + 1) % len(options)

N = 8
C = 25                        # square size
X0 = 4
Y0 = (SH - N * C) // 2
TX = X0 + N * C + 8           # text panel (black, so text is fine)
BOARD = (0, 130, 60)
HINT = (0, 90, 40)            # small dot: you may play here
DISC = {1: BLACK, 2: WHITE}   # 1 = black (starts), 2 = white
NAME = {1: "Black", 2: "White"}
ROUND = [".###.", "#####", "#####", "#####", ".###."]   # 5 x 5 blocks of 4 px

board = [0] * 64
# For every square, the squares in each of the 8 directions (for flipping)
RAYS = []
for i in range(64):
    r, c = divmod(i, 8)
    rays = []
    for dr, dc in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        ray, rr, cc = [], r + dr, c + dc
        while 0 <= rr < 8 and 0 <= cc < 8:
            ray.append(rr * 8 + cc)
            rr, cc = rr + dr, cc + dc
        if len(ray) >= 2:
            rays.append(ray)
    RAYS.append(rays)

def flips(i, p):                       # discs that flip if p plays at i
    out = []
    o = 3 - p
    for ray in RAYS[i]:
        if board[ray[0]] != o:
            continue
        for k in range(1, len(ray)):
            v = board[ray[k]]
            if v == p:
                out += ray[:k]
                break
            if v != o:
                break
    return out

def moves(p):
    return [i for i in ORDER if board[i] == 0 and flips(i, p)]     # best squares first

# ---------- computer player ----------
# Corners are very good, squares next to corners are bad.
WEIGHT = [100, -20, 10, 5, 5, 10, -20, 100,
          -20, -50, -2, -2, -2, -2, -50, -20,
          10, -2, 1, 1, 1, 1, -2, 10,
          5, -2, 1, 0, 0, 1, -2, 5,
          5, -2, 1, 0, 0, 1, -2, 5,
          10, -2, 1, 1, 1, 1, -2, 10,
          -20, -50, -2, -2, -2, -2, -50, -20,
          100, -20, 10, 5, 5, 10, -20, 100]
# Try the best squares first: then the search can skip more bad moves
ORDER = sorted(range(64), key=lambda i: -WEIGHT[i])
score = [0]                            # running score: + good for black
WIN = 100000

def do(i, p, fl):                      # play p at i, flipping fl
    board[i] = p
    s = WEIGHT[i]
    for j in fl:
        board[j] = p
        s += 2 * WEIGHT[j]
    score[0] += s if p == 1 else -s

def undo(i, p, fl):
    board[i] = 0
    s = WEIGHT[i]
    for j in fl:
        board[j] = 3 - p
        s += 2 * WEIGHT[j]
    score[0] -= s if p == 1 else -s

def final(me):                         # game over: who has more discs?
    d = board.count(me) - board.count(3 - me)
    return WIN + d if d > 0 else -WIN + d if d < 0 else 0

def search(me, depth, alpha, beta, passed=False):
    if depth == 0:
        return score[0] if me == 1 else -score[0]
    ms = moves(me)
    if not ms:
        if passed:
            return final(me)           # nobody can move
        return -search(3 - me, depth - 1, -beta, -alpha, True)
    best = -WIN * 2
    for i in ms:
        fl = flips(i, me)
        do(i, me, fl)
        v = -search(3 - me, depth - 1, -beta, -alpha)
        undo(i, me, fl)
        if v > best:
            best = v
        if best > alpha:
            alpha = best
        if alpha >= beta:
            break
    return best

def recount():
    s = 0
    for i in range(64):
        if board[i]:
            s += WEIGHT[i] if board[i] == 1 else -WEIGHT[i]
    score[0] = s

# level 1 = easy, 2 = medium, 3 = hard
def ai_move(me, level):
    recount()
    ms = moves(me)
    if level == 1 and random.random() < 0.3:
        return random.choice(ms)
    depth = (1, 2, 4)[level - 1]
    best, move = -WIN * 3, ms[0]
    for i in ms:
        fl = flips(i, me)
        do(i, me, fl)
        v = -search(3 - me, depth - 1, -WIN * 3, WIN * 3)
        undo(i, me, fl)
        v += random.random() * (8 if level == 1 else 1)
        if v > best:
            best, move = v, i
    return move

# ---------- drawing ----------
def disc(x, y, col):
    set_color(*col)
    for r in range(5):
        row = ROUND[r]
        a = row.index("#")
        b = row.rindex("#") + 1
        fill_rect(x + a * 4, y + r * 4, (b - a) * 4, 4)

def cell(i, hint=False):
    r, c = divmod(i, 8)
    x, y = X0 + c * C, Y0 + r * C
    set_color(*BOARD)
    fill_rect(x, y, C - 1, C - 1)
    if board[i]:
        disc(x + 2, y + 2, DISC[board[i]])
    elif hint:
        set_color(*HINT)
        fill_rect(x + 9, y + 9, 6, 6)

def cursor(i):
    r, c = divmod(i, 8)
    box_frame(X0 + c * C, Y0 + r * C, C - 1, C - 1, 3, YELLOW)

def counts():
    text(4, "Black " + str(board.count(1)))
    text(5, "White " + str(board.count(2)))

# Returns 0-2 = computer level, 3 = 2 players, -1 = quit
def start_screen(stats):
    title_screen("OTHELLO", (0, 200, 90),
                 "Black " + str(stats[0]) + "  White " + str(stats[1]) + "  Draw " + str(stats[2]))
    while True:
        p = menu(["1 player", "2 players"], 0, "UP/DOWN + ENTER")
        if p < 0:
            return -1
        if p == 1:
            return 3
        level = menu(["Easy", "Medium", "Hard"], 1, "CLEAR: back")
        if level >= 0:
            return level

def game(mode):                        # returns 1 black, 2 white, 3 draw, 0 quit
    for i in range(64):
        board[i] = 0
    board[27] = board[36] = 2
    board[28] = board[35] = 1
    clear()
    set_color(*BLACK)
    fill_rect(0, 0, SW, SH)
    turn, cur, hints = 1, 19, []
    for i in range(64):
        cell(i)
    text(0, "OTHELLO")
    text(6, "CLEAR:quit")
    passes = 0
    while True:
        ms = moves(turn)
        counts()
        if not ms:
            passes += 1
            if passes == 2:            # nobody can move: game over
                b, w = board.count(1), board.count(2)
                return 1 if b > w else 2 if w > b else 3
            text(2, NAME[turn], DISC[turn] if turn == 2 else GREY)
            text(3, "must pass")
            wait_for(OK + QUIT) if not (mode < 3 and turn == 2) else sleep(1)
            turn = 3 - turn
            continue
        passes = 0
        computer = mode < 3 and turn == 2
        text(2, NAME[turn], DISC[turn] if turn == 2 else GREY)
        text(3, "thinking" if computer else "your turn")
        new_hints = [] if computer else ms
        for i in set(hints) | set(new_hints):     # only redraw changed dots
            if (i in hints) != (i in new_hints):
                cell(i, i in new_hints)
        hints = new_hints
        if computer:
            paint()
            i = ai_move(2, mode + 1)
        else:
            cursor(cur)
            paint()
            while True:
                k = key()
                if not k:
                    sleep(0.03)
                    continue
                if k in QUIT:
                    return 0
                old = cur
                r, c = divmod(cur, 8)
                if k in LEFT:
                    c = (c - 1) % 8
                elif k in RIGHT:
                    c = (c + 1) % 8
                elif k in UP:
                    r = (r - 1) % 8
                elif k in DOWN:
                    r = (r + 1) % 8
                elif k in OK and cur in ms:
                    break
                cur = r * 8 + c
                cell(old, old in hints)
                cursor(cur)
                paint()
            i = cur
        fl = flips(i, turn)
        board[i] = turn
        for j in fl:
            board[j] = turn
        for i2 in hints:               # take away the dots, they change next turn
            if i2 != i:
                cell(i2)
        hints = []
        cell(i)
        for j in fl:
            cell(j)
        turn = 3 - turn

# --- start ---
stats = load("OTHEL", 3)
mode = start_screen(stats)
while mode >= 0:
    w = game(mode)
    if w == 0:
        break
    stats[w - 1] += 1
    save("OTHEL", stats)
    text(2, {1: "Black", 2: "White", 3: "Draw!"}[w], {1: GREY, 2: WHITE, 3: WHITE}[w])
    text(3, "wins!" if w < 3 else "")
    text(6, "ENTER:again")
    if wait_for(OK + QUIT) in QUIT:
        break
paint()
