import tkinter as tk
import random
import math


class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vec({0}, {1})".format(self.x, self.y)

    def __sub__(self, v):
        return Vec(self.x - v.x, self.y - v.y)

    def __add__(self, v):
        return Vec(self.x + v.x, self.y + v.y)

    def __neg__(self):
        return Vec((-1) * self.x, (-1) * self.y)

    def __mul__(self, v):
        if isinstance(v, Vec):
            return self.x * v.x + self.y * v.y
        else:
            return Vec(v * self.x, v * self.y)

    def __str__(self):
        return f"{self.x:.16f} {self.y:.16f}"

    def length2(self):
        return self.x * self.x + self.y * self.y

    def length(self):
        return self.length2() ** (1 / 2)

    def dir(self):
        return self * (1 / self.length)

    def left(self):
        return Vec(self.y * (-1), self.x)

    def right(self):
        return Vec(self.y, self.x * (-1))

    def Ray_contains(p0, p1, p):
        V = p1 - p0
        if (Line.from_points(p0, p1)).contains(p):
            if V.x <= 0 and V.y <= 0 and p.x <= p0.x and p.y <= p0.y:
                return 1
            elif V.x >= 0 and V.y >= 0 and p.x >= p0.x and p.y >= p0.y:
                return 1
            elif V.x >= 0 and V.y <= 0 and p.x >= p0.x and p.y <= p0.y:
                return 1
            elif V.x <= 0 and V.y >= 0 and p.x <= p0.x and p.y >= p0.y:
                return 1
            else:
                return 0
        else:
            return 0

    def Line_sigm_contains(p0, p1, p):
        if Vec.Ray_contains(p0, p1, p) and Vec.Ray_contains(p1, p0, p):
            return 1
        else:
            return 0


class Line:
    def __init__(self, p0, n):
        self.n = n
        self.p0 = p0

    def __repr__(self):
        return "Line({0}, {1})".format(self.p0, self.n)

    def contains(self, p):
        return ((p - self.p0) * self.n) == 0

    def from_points(p0, p1):
        return Line(p0, (p1 - p0).left())

    def from_abc(a, b, c):
        n = Vec(a, b)
        p0 = n * (-c / n.length2())
        return Line(p0, n)

    def abc(self):
        a = self.n.x
        b = self.n.y
        c = -(self.p0 * self.n)
        return a, b, c

    def paral_lines_2(self, R):
        p02 = self.n * (R / self.n.length()) + self.p0
        p01 = self.n * ((-1) * R / self.n.length()) + self.p0
        return Line(p01, self.n), Line(p02, self.n)

    def bisector(L1, L2):
        a = L1.n * (1 / -L1.n.length())
        b = L2.n * (1 / -L2.n.length())
        return Line(L1.p0, a + b)


class Point(Vec):
    RADIUS = 5

    def __init__(self, x, y, canvas, butt):
        super().__init__(x, y)
        self.__parent = None
        self.__canvas = canvas
        self.__butt = butt
        r = Point.RADIUS
        self.__id = canvas.create_oval(x - r, y - r, x + r, y + r, fill='orange')
        self.__canvas.tag_bind(self.__id, f"<B{self.__butt}-Motion>", self.drag)

    def drag(self, event):
        self.x = event.x
        self.y = event.y
        self.update(self)

    def update(self, par):
        r = Point.RADIUS
        x, y, = self.x, self.y
        self.__canvas.coords(self.__id, x - r, y - r, x + r, y + r)
        if self.__parent and self.__parent != par:
            self.__parent.update(self)

    def set_parent(self, parent):
        self.__parent = parent


class UM_Point(Vec):
    RADIUS = 5

    def __init__(self, x, y, canvas, butt, color):
        super().__init__(x, y)
        self.__parent = None
        self.__canvas = canvas
        r = Point.RADIUS
        self.__id = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color)

    def drag(self, x, y):
        self.x = x
        self.y = y
        self.update(self)

    def update(self, par):
        r = Point.RADIUS
        x, y, = self.x, self.y
        self.__canvas.coords(self.__id, x - r, y - r, x + r, y + r)

    def set_parent(self, parent):
        self.__parent = parent


class Circle:
    def __init__(self, center, second_point, canvas):
        center.set_parent(self)
        second_point.set_parent(self)
        self.c = center
        self.__sp = second_point
        c = self.__canvas = canvas
        r = self.__r = (center - second_point).length() // 1
        x, y, = center.x, center.y
        self.__id = c.create_oval(x - r, y - r, x + r, y + r, outline="red")

    def update(self, child):
        r = self.__r = (self.c - self.__sp).length() // 1
        x, y = self.c.x, self.c.y
        if child != self.__sp:
            self.__sp.update(self)
        if child != self.c:
            self.c.update(self)
        self.__canvas.coords(self.__id, x - r, y - r, x + r, y + r)
        if self != win.circle2:
            self.find_coords(win.circle2)
        if self != win.circle1:
            self.find_coords(win.circle1)

    def set_n_points(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def find_coords(self, circle3):
        r0 = self.__r
        r1 = circle3.__r
        x0 = self.c.x
        y0 = self.c.y
        x1 = circle3.c.x
        y1 = circle3.c.y
        d = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        if d > r0 + r1:
            self.p1.drag(0, 0)
            self.p2.drag(0, 0)
        elif d == r0 + r1:
            if x0 != x1:
                N = (r1 * r1 - r0 * r0 + x0 * x0 + y0 * y0 - x1 * x1 - y1 * y1) / (2 * (x0 - x1))
                M = (y1 - y0) / (x0 - x1)
                A = (M * M + 1)
                B = N - x0 - y0
                C = (N - x0) ** 2 + y0 ** 2 - r0 ** 2
                Y = -B / A
                X = M * Y + N
            elif y0 != y1:
                Y = (r0 ** 2 - r1 ** 2 + (y1 - y0) * (y1 + y0)) / (2 * (y1 - y0))
                X = x0
            else:
                Y = y0
                X = x0
            self.p1.drag(X, Y)
            self.p2.drag(X, Y)
        elif d < r0 + r1:
            if x0 != x1:
                N = (r1 * r1 - r0 * r0 + x0 * x0 + y0 * y0 - x1 * x1 - y1 * y1) / (2 * (x0 - x1))
                M = 2 * (y1 - y0) / (x0 - x1)
                A = (M * M + 1)
                B = 2 * (N - x0 - y0)
                C = (N - x0) ** 2 + y0 ** 2 - r0 ** 2
                Y0 = (-B + (B ** 2 - 4 * C * A) ** 0.5) / (2 * A)
                Y1 = (-B - (B ** 2 - 4 * C * A) ** 0.5) / (2 * A)
                X0 = M * Y0 + N
                X1 = M * Y1 + N
            elif y0 != y1:
                Y0 = Y1 = (r0 ** 2 - r1 ** 2 + (y1 - y0) * (y1 + y0)) / (2 * (y1 - y0))
                X0 = X1 = x0
            else:
                Y1 = Y0 = y0
                X1 = X0 = x0
            self.p1.drag(X0 // 1, Y0 // 1)
            self.p2.drag(X1 // 1, Y1 // 1)

class Arc:
    def __init__(self, r, x0, y0, ang0, ang1, canvas):
        self.x0 = x0 - r
        self.y0 = y0 - r
        self.x1 = x0 + r
        self.y1 = y0 + r
        self.start = ang0
        self.extent = ang1 - ang0
        self.__canvas = canvas
        self.__id = self.__canvas.create_arc(self.x0, self.y0, self.x1, self.y1, start=self.start, extent=self.extent, outline="green", style=tk.ARC, width=4)


class Section:
    def __init__(self, x0, y0, x1, y1, color, canvas):
        self.__id = canvas.create_line(x0, y0, x1, y1, width=4, fill=color)


class Square:
    def __init__(self, x0, y0, x1, y1, color, canvas):
        self.__id0 = canvas.create_line(x0 + 1, y0 + 1, x0 + 1, y1 - 1, width=2, fill=color)
        self.__id1 = canvas.create_line(x1 - 1, y1 - 1, x0 + 1, y1 - 1, width=2, fill=color)
        self.__id2 = canvas.create_line(x1 - 1, y1 - 1, x1 - 1, y0 + 1, width=2, fill=color)
        self.__id3 = canvas.create_line(x0 + 1, y1 - 1, x1 - 1, y1 - 1, width=2, fill=color)


class Cell:
    def __init__(self, type, x, y, side, canvas, coming0, coming1):
        self.coming0 = coming0
        self.coming1 = coming1
        self.type = type
        self.x0 = x * side
        self.y0 = y * side
        self.x1 = (x + 1) * side
        self.y1 = (y + 1) * side
        self.__canvas = canvas
        self.square = Square(self.x0, self.y0, self.x1, self.y1, 'grey', self.__canvas)
        if self.type == 0:
            self.arc0 = Arc(side / 2, self.x0, self.y1, 0, 90, canvas)
            self.arc1 = Arc(side / 2, self.x1, self.y0, 180, 270, canvas)
        elif self.type == 1:
            self.section0 = Section((self.x0 + self.x1) / 2, self.y0, (self.x0 + self.x1) / 2, self.y1, 'green', self.__canvas)
            self.section1 = Section(self.x0, (self.y0 + self.y1) / 2, self.x1, (self.y0 + self.y1) / 2, 'green', self.__canvas)
        elif self.type == 2:
            self.arc0 = Arc(side / 2, self.x0, self.y1, 0, 90, canvas)
            self.arc1 = Arc(side / 2, self.x1, self.y0, 180, 270, canvas)
            self.section0 = Section(self.x0, self.y0, self.x1, self.y1, 'red', self.__canvas)
        else:
            assert(False)


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("sticky brains")
        #tk.Label(self, text='CoNvaS', font=('cOnVAs', 16)).pack()
        self.string_input0 = tk.Entry(self, width=100)
        self.string_input1 = tk.Entry(self, width=100)
        self.b0 = tk.Button(text="Ввод", width=80, height=1, command=self.show_braids)
        self.string_input0.pack()
        self.string_input1.pack()
        self.b0.pack()
        self.__canvas = tk.Canvas(self, width=1000, height=500, bg='black')
        self.__canvas.pack(fill=tk.BOTH, expand=True)

    def show_braids(self):
        str0 = self.string_input0.get()
        str1 = self.string_input1.get()
        n = len(str0)
        m = len(str1)
        self.cells = [[Cell(0, 0, 0, 0, self.__canvas, 0, 0) for _ in range(m)] for __ in range(n)]
        for i in range(n):
            for j in range(m):
                if i == 0 and j == 0:
                    coming0 = n - 1
                    coming1 = n
                elif i == 0:
                    if self.cells[0][j - 1].type == 1:
                        coming0 = self.cells[0][j - 1].coming0
                    else:
                        coming0 = self.cells[0][j - 1].coming1
                    coming1 = n + j
                elif j == 0:
                    if self.cells[0][j - 1].type == 1:
                        coming1 = self.cells[i - 1][0].coming1
                    else:
                        coming1 = self.cells[i - 1][0].coming0
                    coming0 = n - i - 1
                else:
                    if self.cells[i - 1][j].type == 1:
                        coming1 = self.cells[i - 1][j].coming1
                    else:
                        coming1 = self.cells[i - 1][j].coming0
                    if self.cells[i][j - 1].type == 1:
                        coming0 = self.cells[i][j - 1].coming0
                    else:
                        coming0 = self.cells[i][j - 1].coming1
                if str0[i] == str1[j]:
                    self.cells[i][j] = Cell(2, i, j, 30, self.__canvas, coming0, coming1)
                else:
                    self.cells[i][j] = Cell(coming1 > coming0, i, j, 30, self.__canvas, coming0, coming1)


if __name__ == "__main__":
    win = Window()
    win.mainloop()
