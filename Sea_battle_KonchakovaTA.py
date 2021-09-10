from random import randint
from random import choice

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __eq__(self, next_point):
        return self.x == next_point.x and self.y == next_point.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class BattleError(Exception):
    pass

class OutError(BattleError):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class DblFireError(BattleError):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class WrongBoatError(BattleError):
    pass

class Boat:
    def __init__(self, first, le, ang):
        self.first = first
        self.le = le
        self.ang = ang
        self.hp = le

    @property
    def boat_points(self):
        bp = []
        for i in range(self.le):
            cur_x = self.first.x
            cur_y = self.first.y

            if self.ang == 0:
                cur_x += i

            elif self.ang == 1:
                cur_y += i

            bp.append(Point(cur_x, cur_y))
        return bp

    def fire(self, d):
        return d in self.boat_points

class Play_Field:
    def __init__(self, hid = False, size = 6):
        self.hid = hid
        self.size = size
        self.stroka = [["O"]*size for _ in range(size)]
        self.busy = []
        self.boats = []
        self.count = 0
        self.weight = [[1]*size for _ in range(size)]


    def __str__(self):
        s = self.size

        field = [' | ']
        f = ''

        for i in range(s):
            field.append(i + 1)
            field.append(" | ")
            a = " " + f.join(map(str, field)) + "\n"

        for num, val in enumerate(self.stroka):
            a += f"{num + 1} | " + " | ".join(val) + " |\n"

        if self.hid:
            a = a.replace("■", "O")
        return a


    def max_weight(self):

        max_weight = 0
        MW = []

        for x in range(self.size):
            for y in range(self.size):
                if self.weight[x][y] > max_weight:
                    #print(self.weight[x][y])
                    max_weight = self.weight[x][y]
        for x in range(self.size):
            for y in range(self.size):
                if self.weight[x][y] == max_weight:
                    MW.append(Point(x,y))
        #print(MW)
        return MW



    def vne(self, d):

        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))


    def shot(self, d):

        if self.vne(d):
            raise OutError()

        if d in self.busy:
            raise DblFireError()

        self.busy.append(d)

        for boat in self.boats:
            if d in boat.boat_points:
                boat.hp -= 1
                self.stroka[d.x][d.y] = "X"
                self.weight[d.x][d.y] = 0
                if boat.hp == 0:
                    self.count += 1
                    self.ramka(boat, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    self.weight[d.x][d.y] = 0
                    if d.x - 1 >= 0:
                        self.weight[d.x - 1][d.y] *= 10
                        if d.y - 1 >= 0:
                            self.weight[d.x-1][d.y-1] = 0

                        if d.y + 1 < self.size:
                            self.weight[d.x - 1][d.y+1] = 0
                    if d.y - 1 >= 0:
                        self.weight[d.x][d.y-1] *= 10
                    if d.y + 1 < self.size:
                        self.weight[d.x][d.y+1] *= 10
                    if d.x + 1 < self.size:
                        self.weight[d.x + 1][d.y] *= 10
                        if d.y - 1 >= 0:
                            self.weight[d.x + 1][d.y-1] = 0
                        if d.y + 1 < self.size:
                            self.weight[d.x + 1][d.y+1] = 0
                    return True

        self.stroka[d.x][d.y] = "."
        self.weight[d.x][d.y] = 0
        print("Мимо!")
        return False


    def begin(self):
        self.busy = []

    def add_boat(self, boat):

        for d in boat.boat_points:
            if self.vne(d) or d in self.busy:
                raise WrongBoatError()
        for d in boat.boat_points:
            self.stroka[d.x][d.y] = "■"
            self.busy.append(d)

        self.boats.append(boat)
        self.ramka(boat)
        for x in range(self.size):
            for y in range(self.size):
                self.weight[x][y] = 1

    def ramka(self, boat, verb = False):
        out = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in boat.boat_points:
            for dx, dy in out:
                cur = Point(d.x + dx, d.y + dy)
                if not (self.vne(cur)) and cur not in self.busy:
                    if verb:
                        self.stroka[cur.x][cur.y] = "."
                        self.weight[cur.x][cur.y] = 0
                    self.busy.append(cur)

class Player:
    def __init__(self, Play_Field1, Play_Field2):
        self.size = size
        self.Play_Field1 = Play_Field1
        self.Play_Field2 = Play_Field2

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.Play_Field2.shot(target)
                return repeat
            except BattleError as e:
                print(e)


class Comp(Player):
    def ask(self):
        d = choice(self.Play_Field2.max_weight())
        print(f'Ход компьютера: {d.x + 1} {d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Point(x - 1, y - 1)


class Game:
    def __init__(self, size):
        self.size = size
        pl = self.random_play_field()
        co = self.random_play_field()
        co.hid = True

        self.comp_ = Comp(co, pl)
        self.user_ = User(pl, co)

    def random_play_field(self):
        play_field = None
        while  play_field is None:
            play_field = self.random_place()
        return  play_field

    def random_place(self):
        Lens = [3, 2, 2, 1, 1, 1, 1]
        play_field = Play_Field(size=self.size)
        attempts = 0
        for l in Lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                boat = Boat(Point(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                   play_field.add_boat(boat)
                   break
                except WrongBoatError:
                   pass
        play_field.begin()
        return play_field

    def game_process(self):
        n = 0
        while True:
            print("Ваше игровое поле:")
            print(self.user_.Play_Field1)
            print("Игровое поле компьютера:")
            print(self.comp_.Play_Field1)
            if n % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь: ")
                repeat = self.user_.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.comp_.move()
            if repeat:
                n -= 1

            if self.comp_.Play_Field1.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.user_.Play_Field1.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            n += 1


    def start(self):
        self.game_process()

def info() :
        print('''
        Привет! Это игра "Морской бой".
        Чтобы сделать ход, введи координаты клетки,
        куда хочешь сделать выстрел: 
        Х - номер строки
        Y - номер столбца  
        ''')

info()
size = int(input('Введите размер игрового поля в диапазоне от 5 до 10: '))
g = Game(size)
g.start()






