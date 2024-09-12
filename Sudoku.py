import copy as c
import random as rn

testBrett = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 8
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 9
]
debugBrett = [
    "003020600\n",
    "900305001\n",
    "001806400\n",
    "008102900\n",
    "700000008\n",
    "006708200\n",
    "002609500\n",
    "800203009\n",
    "005010300\n",
]


def make_board(b):
    print(f"""      
      0 1 2   3 4 5   6 7 8   
    +-------+-------+-------+    
  0 | {b[0][0]} {b[0][1]} {b[0][2]} | {b[0][3]} {b[0][4]} {b[0][5]} | {b[0][6]} {b[0][7]} {b[0][8]} |
  1 | {b[1][0]} {b[1][1]} {b[1][2]} | {b[1][3]} {b[1][4]} {b[1][5]} | {b[1][6]} {b[1][7]} {b[1][8]} |
  2 | {b[2][0]} {b[2][1]} {b[2][2]} | {b[2][3]} {b[2][4]} {b[2][5]} | {b[2][6]} {b[2][7]} {b[2][8]} |
    +-------+-------+-------+ 
  3 | {b[3][0]} {b[3][1]} {b[3][2]} | {b[3][3]} {b[3][4]} {b[3][5]} | {b[3][6]} {b[3][7]} {b[3][8]} |
  4 | {b[4][0]} {b[4][1]} {b[4][2]} | {b[4][3]} {b[4][4]} {b[4][5]} | {b[4][6]} {b[4][7]} {b[4][8]} |
  5 | {b[5][0]} {b[5][1]} {b[5][2]} | {b[5][3]} {b[5][4]} {b[5][5]} | {b[5][6]} {b[5][7]} {b[5][8]} |
    +-------+-------+-------+ 
  6 | {b[6][0]} {b[6][1]} {b[6][2]} | {b[6][3]} {b[6][4]} {b[6][5]} | {b[6][6]} {b[6][7]} {b[6][8]} |
  7 | {b[7][0]} {b[7][1]} {b[7][2]} | {b[7][3]} {b[7][4]} {b[7][5]} | {b[7][6]} {b[7][7]} {b[7][8]} |
  8 | {b[8][0]} {b[8][1]} {b[8][2]} | {b[8][3]} {b[8][4]} {b[8][5]} | {b[8][6]} {b[8][7]} {b[8][8]} |
    +-------+-------+-------+ 
""")


def make_cubeBoard(b):
    cube = [[], [], [], [], [], [], [], [], []]
    for i in range(len(b)):
        for j in range(len(b[i])):
            if j < 3 and i < 3:
                cube[0].append(b[i][j])
            if 3 <= j < 6 and i < 3:
                cube[1].append(b[i][j])
            if 6 <= j < 9 and i < 3:
                cube[2].append(b[i][j])
            if j < 3 and 3 <= i < 6:
                cube[3].append(b[i][j])
            if 3 <= j < 6 and 3 <= i < 6:
                cube[4].append(b[i][j])
            if 6 <= j < 9 and 3 <= i < 6:
                cube[5].append(b[i][j])
            if j < 3 and 6 <= i < 9:
                cube[6].append(b[i][j])
            if 3 <= j < 6 and 6 <= i < 9:
                cube[7].append(b[i][j])
            if 6 <= j < 9 and 6 <= i < 9:
                cube[8].append(b[i][j])

    return cube


def checkCube(koo):
    rad = koo[0]
    kol = koo[1]

    if kol < 3 and rad < 3:
        return 0
    if 3 <= kol < 6 and rad < 3:
        return 1
    if 6 <= kol < 9 and rad < 3:
        return 2
    if kol < 3 and 3 <= rad < 6:
        return 3
    if 3 <= kol < 6 and 3 <= rad < 6:
        return 4
    if 6 <= kol < 9 and 3 <= rad < 6:
        return 5
    if kol < 3 and 6 <= rad < 9:
        return 6
    if 3 <= kol < 6 and 6 <= rad < 9:
        return 7
    if 6 <= kol < 9 and 6 <= rad < 9:
        return 8


def skrivTall():
    legal = False
    save = False

    while not legal and not save:
        a = input("Skriv inn rad: ")
        b = input("Skriv inn kolonne: ")
        c = input("Hva vil du endre til: ")

        if a.isdigit() and b.isdigit() and c.isdigit():
            if 0 <= int(a) <= 8 and 0 <= int(b) <= 8:
                if 1 <= int(c) <= 9:
                    legal = True
                else:
                    print("Tallet må mp være mellom 1 og 9")
            else:
                print("Radene og kolonnene må være gyldig")

        elif a.lower() == "save" or b.lower() == "save" or c.lower() == "save":
            save = True
        else:
            print("Vennligst skriv et tall")

    if save:
        return save, save, save
    else:
        return (int(a), int(b)), int(c), save


def lesSpillFil(game):
    if game.lower() == "random":
        g = randomGame()
        return g, g
    else:
        game = game + ".txt"

        with open(game, "r") as fil:
            x = fil.readlines()

        spillTo = []
        for i in range(9):
            rad = x[i][:-1]
            rad = list(rad)
            rad = [int(number) for number in rad]
            spillTo.append(rad)

        spill = c.deepcopy(spillTo)

        for j in range(len(spill)):
            for q in range(len(spill[j])):
                if spill[j][q] == 0:
                    spill[j][q] = " "
                    spillTo[j][q] = " "
                else:
                    spill[j][q] = "\u0332" + str(spill[j][q])

        return spillTo, spill


def legalNumber(a, c):
    if isinstance(a, tuple) and isinstance(c, int):
        rad = brett[a[0]]
        kol = a[1]
        kolonne = []
        kube = cubeBoard[checkCube(a)]

        for i in range(len(brett)):
            kolonne.append(brett[i][kol])

        if brett[a[0]][a[1]] == " ":
            if c in rad:
                print("Tallet finnes allerede i raden")
                return False
            elif c in kolonne:
                print("Tallet finnes allerede i kolonnen ")
                return False
            elif c in kube:
                print("Tallet finnes allerede i kuben")
                return False
            else:
                brett[a[0]][a[1]] = c
                underBrett[a[0]][a[1]] = c
                return True

        elif orgBrett[a[0]][a[1]] == " ":
            if c in rad:
                print("Tallet finnes allerede i raden")
                return False
            elif c in kolonne:
                print("Tallet finnes allerede i kolonnen ")
                return False
            elif c in kube:
                print("Tallet finnes allerede i kuben")
                return False
            else:
                brett[a[0]][a[1]] = c
                underBrett[a[0]][a[1]] = c
                return True
        else:
            print("Du kan ikke endre det tallet")
            return False
    else:
        return True


def checkWin(b):
    mellom = 0
    for i in range(len(b)):
        for j in range(len(b[i])):
            if b[i][j] == " ":
                mellom = 1
                break
        if mellom == 1:
            break
    if mellom == 1:
        return False
    else:
        return True


def saveGame(b):
    game = ""

    for i in range(len(b)):
        for j in range(len(b[i])):
            if b[i][j] == " ":
                b[i][j] = "0"
            else:
                b[i][j] = str(b[i][j])

        game += "".join(b[i]) + "\n"

    with open("saved.txt", "w") as f:
        f.write(game)


def randomGame():
    base = 3
    side = base * base
    b = []

    # pattern for a baseline valid solution
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    # randomize rows, columns and numbers (of valid base pattern)

    def shuffle(s):
        return rn.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    for line in board:
        b.append(line)

    liste = []
    for i in range(9):
        for j in range(9):
            liste.append((i, j))

    korr = rn.sample(liste, 80)

    for rad, kol in korr:
        b[rad][kol] = " "

    return b


print("\n\n\tVelkommen til Sudoku\n\n")

print('For å lagre spillet underveis skriver du "save" som input')
spillFil = input("Hva vil du spille [easy|medium|hard|saved|random]: ")

brett, underBrett = lesSpillFil(spillFil)
cubeBoard = make_cubeBoard(brett)
orgBrett = c.deepcopy(brett)

make_board(underBrett)
status = checkWin(brett)
save = False

while not status and not save:
    koordinat, tall, save = skrivTall()
    legalMove = legalNumber(koordinat, tall)

    while not legalMove:
        koordinat, tall, save = skrivTall()
        legalMove = legalNumber(koordinat, tall)

    make_board(underBrett)
    status = checkWin(brett)

if save:
    saveGame(brett)
    print("Da er spillet lagret")
else:
    print("\nGratulerer du klarte å fullføre brettet\n\n")
