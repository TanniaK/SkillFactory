def info():
    print('''
Привет! Это игра "Крестики-нолики".
Чтобы сделать ход, введи координаты клетки,
куда хочешь поставить свой символ:   
''')

def play_field(pole):
    #pole = [[' - '*3] for i in range(3)]
    print('    0 1 2')
    for i in range(len(pole)):
        print(str(i),' ', *pole[i])

def game_input(pole, Player):
    while True:
        turn = (input(f'Ход игрока {Player}, введите координаты через пробел: ')).split()
        if len(turn) != 2:
            print('Некорректный ввод. Введите две координаты через пробел')
            continue
        if not (turn[0].isdigit() and turn[1].isdigit()):
           print('Некорректный ввод. Введите целые числа в диапазоне от 0 до 2: ')
           continue
        x, y = map(int, turn)
        #print(x, ' ', y)
        if (x>2 or y>2):
            print('Неверно заданы координаты. Диапазон игрового поля 0..2')
            continue
        if pole[x][y] != '-':
            print('Клетка занята')
            continue
        break
    return x, y

def winner_comb(pole, Player):
    win_var = [[0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
                [0, 3, 6],
                [1, 4, 7],
                [2, 5, 8],
                [0, 4, 8],
                [2, 4, 6]]

    a = len(pole)
    b = []
    for i in range(a):
        b += list(pole[i])
    win = set([i for i, x in enumerate(b) if x == Player])
    for n in win_var:
        if len(win.intersection(set(n)))==3:
            return True
    return False

def game_process(pole):
    info()
    n = 0
    while True:
        play_field(pole)
        if n % 2 == 0:
            Player = 'X'
        else:
            Player = 'O'
        if n < 9:
            x, y = game_input(pole, Player)
            pole[x][y] = Player
            winner_comb(pole, Player)
        else:
            n == 9
            print('Ничья')
            break
        if winner_comb(pole, Player):
            print(f"Победил игрок {Player} !!!")
            break
        n += 1

pole = [['-'] * 3 for _ in range(3)]

game_process(pole)


