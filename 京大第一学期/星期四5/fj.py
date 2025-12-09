import tkinter
from tkinter import messagebox
import random

# 原有的默认参数
BOARD_WIDTH = 20
BOARD_HEIGHT = 10
MINE_NUM = 20

width = 0
height = 0
WIDTH_S = 10
HEIGHT_S = 8
WIDTH_M = 20
HEIGHT_M = 10
WIDTH_L = 30
HEIGHT_L = 12
MINE_NUM_S = 8
MINE_NUM_M = 20
MINE_NUM_L = 36

MINE_BG_COLOR = "pink"
FLAG_BG_COLOR = "gold"
EMPTY_BG_COLOR = "lightgray"

fg_color = {
    1: "blue",
    2: "green",
    3: "purple",
    4: "olive",
    5: "chocolate",
    6: "magenta",
    7: "darkorange",
    8: "red",
}

MINE = -1


# 原有功能：扫雷游戏类
class MineSweeper:
    def __init__(self, app, width, height, mine_num):
        self.app = app
        self.width = width
        self.height = height
        self.mine_num = mine_num
        self.clear_num = self.width * self.height - self.mine_num
        self.open_num = 0
        self.open_mine = False
        self.play_game = False
        self.flag_count = 0

        # 初始化棋盘
        self.cells = None
        self.labels = None
        self.initialize_board()

        # 创建界面
        self.create_widgets()

        # 绑定事件
        self.set_events()
        self.non_mine()
        self.play_game = True














###################################
###################################
    # 新增：封装棋盘初始化
    def initialize_board(self):
        self.clear_num = self.width * self.height - self.mine_num
        self.open_num = 0
        self.open_mine = False
        self.play_game = False
        self.cells = [[0] * self.width for _ in range(self.height)]
        self.place_mines()
        self.set_mine_num()
#######################################
#######################################




















    # 原有功能：布置地雷
    def place_mines(self):
        mine_num = 0
        while mine_num < self.mine_num:
            j = random.randint(0, self.height - 1)
            i = random.randint(0, self.width - 1)
            if self.cells[j][i] != MINE:
                self.cells[j][i] = MINE
                mine_num += 1

    # 原有功能：计算每个格子周围的地雷数
    def set_mine_num(self):
        for j in range(self.height):
            for i in range(self.width):
                if self.cells[j][i] == MINE:
                    continue
                num_mine = 0
                for y in range(-1, 2):
                    for x in range(-1, 2):
                        if y != 0 or x != 0:
                            is_mine = self.is_mine(i + x, j + y)
                            if is_mine:
                                num_mine += 1
                self.cells[j][i] = num_mine

    #search non mine and neighbor non mine point
    def non_mine(self):
        zerocells = None
        zero_cells = [[i, j] for i in range(len(self.cells)) for j in range(len(self.cells[i])) if self.cells[i][j] == 0]
        if len(zero_cells) == 0:
            zero_cells = [[i, j] for i in range(len(self.cells)) for j in range(len(self.cells[i])) if self.cells[i][j] == 1]
        a = random.randint(0, len(zero_cells) - 1)
        self.labels[zero_cells[a][0]][zero_cells[a][1]].config(bg="lightblue")

    # 原有功能：检查是否为地雷
    def is_mine(self, i, j):
        if j >= 0 and i >= 0 and j < self.height and i < self.width:
            if self.cells[j][i] == MINE:
                return True
        return False

    def create_widgets(self):
        self.labels = [[None] * self.width for j in range(self.height)]

        # 配置每一行和每一列的权重，让它们可以随着窗口大小调整
        for j in range(self.height):
            self.app.rowconfigure(j, weight=1)
            for i in range(self.width):
                self.app.columnconfigure(i, weight=1)

                # 创建一个 Label 作为格子
                label = tkinter.Label(
                    self.app,
                    width=2,  # 初始宽度
                    height=1,  # 初始高度
                    bg=EMPTY_BG_COLOR,
                    relief=tkinter.RAISED
                )
                # 使用 grid 放置组件
                label.grid(column=i, row=j, sticky="nsew")  # 启用组件扩展到网格
                self.labels[j][i] = label

        # 配置底部显示地雷数的标签
        self.mine_label = tkinter.Label(
            self.app,
            text=f"Mines Number: {self.mine_num}",
            font=("Arial", 12),
            bg="lightblue"
        )
        self.mine_label.grid(column=0, row=self.height, columnspan=self.width, sticky="ew")

        # 配置剩余地雷和插旗数显示的标签
        self.remaining_mines_label = tkinter.Label(
            self.app,
            text=f"Flags: {self.flag_count} / Mines Remaining: {self.mine_num - self.flag_count}",
            font=("Arial", 12),
            bg="lightblue"
        )
        self.remaining_mines_label.grid(column=0, row=self.height + 1, columnspan=self.width, sticky="ew")
        self.restart_button = tkinter.Button(
            self.app,
            text="Restart",
            font=("Arial", 12),
            bg="lightgreen",
            command=self.restart_game  # 点击时调用 restart_game 方法
        )
        self.restart_button.grid(column=0, row=self.height + 3, columnspan=self.width, sticky="ew")

    def restart_game(self):
        # 重置游戏状态
        self.open_num = 0
        self.open_mine = False
        self.flag_count = 0
        self.remaining_mines_label.config(
            text=f"Flags: {self.flag_count} / Mines Remaining: {self.mine_num - self.flag_count}"
        )

        # 清空棋盘
        for j in range(self.height):
            for i in range(self.width):
                self.cells[j][i] = 0
                label = self.labels[j][i]
                label.config(
                    text="",
                    bg=EMPTY_BG_COLOR,
                    relief=tkinter.RAISED
                )

        # 重新布置地雷和计算地雷数
        self.place_mines()
        self.set_mine_num()

        # 启用游戏
        self.play_game = True


















##################################################
##################################################
        # 新增：显示插旗数和剩余地雷数
        self.remaining_mines_label = tkinter.Label(
            self.app,
            text=f"Flags: {self.flag_count} / Mines Remaining: {self.mine_num - self.flag_count}",
            font=("Arial", 12),
            bg="lightblue"
        )
        self.remaining_mines_label.grid(column=0, row=self.height + 1, columnspan=self.width, sticky="ew")
###################################################
###################################################













    # 原有功能：绑定事件
    def set_events(self):
        for j in range(self.height):
            for i in range(self.width):
                label = self.labels[j][i]
                label.bind("<ButtonPress-1>", self.open_cell)  # 左键打开
                label.bind("<ButtonPress-3>", self.raise_flag)  # 右键插旗
################################################################################
################################################################################
    # 新增：右键插旗功能动态更新插旗数
    def raise_flag(self, event):
        if not self.play_game:
            return
        label = event.widget
        if label.cget("relief") != tkinter.RAISED:
            return
        if label.cget("text") != "F":
            bg = FLAG_BG_COLOR
            label.config(text="F", bg=bg)
            self.flag_count += 1  # 新增：插旗数加一
        else:
            bg = EMPTY_BG_COLOR
            label.config(text="", bg=bg)
            self.flag_count -= 1  # 新增：插旗数减一

        # 更新插旗数量和剩余地雷数
        self.remaining_mines_label.config(
            text=f"Flags: {self.flag_count} / Mines Remaining: {self.mine_num - self.flag_count}"
        )

    # 原有功能：左键打开格子
    def open_cell(self, event):
        if not self.play_game:
            return
        label = event.widget
        for y in range(self.height):
            for x in range(self.width):
                if self.labels[y][x] == label:
                    j = y
                    i = x
        cell = self.cells[j][i]
        if label.cget("relief") != tkinter.RAISED:
            return
        text, bg, fg = self.get_text_info(cell)
        if cell == MINE:
            self.open_mine = True
        label.config(
            text=text,
            bg=bg,
            fg=fg,
            relief=tkinter.SUNKEN
        )
        self.open_num += 1
        if cell == 0:
            self.open_neighbor(i - 1, j - 1)
            self.open_neighbor(i, j - 1)
            self.open_neighbor(i + 1, j - 1)
            self.open_neighbor(i - 1, j)
            self.open_neighbor(i + 1, j)
            self.open_neighbor(i - 1, j + 1)
            self.open_neighbor(i, j + 1)
            self.open_neighbor(i + 1, j + 1)

        if self.open_mine:
            self.app.after_idle(self.game_over)
        elif self.open_num == self.clear_num:
            self.app.after_idle(self.game_clear)

    # 原有功能：打开所有格子
    def open_all(self):
        for j in range(self.height):
            for i in range(self.width):
                label = self.labels[j][i]
                text, bg, fg = self.get_text_info(self.cells[j][i])
                label.config(
                    text=text,
                    bg=bg,
                    fg=fg,
                    relief=tkinter.SUNKEN
                )

    def open_neighbor(self, i, j):
        if self.open_mine:
            return
        if not (j >= 0 and i >= 0 and j < self.height and i < self.width):
            return
        label = self.labels[j][i]
        if label.cget("relief") != tkinter.RAISED:
            return
        if self.cells[j][i] == MINE:
            return
        text, bg, fg = self.get_text_info(self.cells[j][i])
        label.config(
            text=text,
            bg=bg,
            fg=fg,
            relief=tkinter.SUNKEN
        )
        self.open_num += 1
        if self.cells[j][i] == 0:
            self.open_neighbor(i - 1, j - 1)
            self.open_neighbor(i, j - 1)
            self.open_neighbor(i + 1, j - 1)
            self.open_neighbor(i - 1, j)
            self.open_neighbor(i + 1, j)
            self.open_neighbor(i - 1, j + 1)
            self.open_neighbor(i, j + 1)
            self.open_neighbor(i + 1, j + 1)

    # 原有功能：游戏结束
    def game_over(self):
        self.open_all()
        self.play_game = False
        messagebox.showerror("Game Over", "You hit a mine!")

    # 新增：胜利时弹窗显示 "Win"
    def game_clear(self):
        self.open_all()
        self.play_game = False
        messagebox.showinfo("Win", "Congratulations, you win!")

    # 原有功能：获取格子文本信息
    def get_text_info(self, num):
        if num == MINE:
            text = "X"
            bg = MINE_BG_COLOR
            fg = "darkred"
        elif num == 0:
            text = ""
            bg = EMPTY_BG_COLOR
            fg = "black"
        else:
            text = str(num)
            bg = EMPTY_BG_COLOR
            fg = fg_color[num]
        return (text, bg, fg)





#######################################################
############################################################
# 新增：玩家选择棋盘大小
def select_board_size():
    def set_size(size):
        global WIDTH, HEIGHT, MINE_NUM
        if size == "small":
            WIDTH, HEIGHT, MINE_NUM = WIDTH_S, HEIGHT_S, MINE_NUM_S
        elif size == "medium":
            WIDTH, HEIGHT, MINE_NUM = WIDTH_M, HEIGHT_M, MINE_NUM_M
        elif size == "large":
            WIDTH, HEIGHT, MINE_NUM = WIDTH_L, HEIGHT_L, MINE_NUM_L
        size_window.destroy()

    size_window = tkinter.Toplevel()  # 改为使用 Toplevel
    size_window.title("Select Board Size")

    tkinter.Button(size_window, text="Small", command=lambda: set_size("small")).pack(fill="x")
    tkinter.Button(size_window, text="Medium", command=lambda: set_size("medium")).pack(fill="x")
    tkinter.Button(size_window, text="Large", command=lambda: set_size("large")).pack(fill="x")

    size_window.grab_set()  # 防止用户与其他窗口交互
    size_window.wait_window()  # 等待窗口关闭
##########################################################
##########################################################







# 主程序入口
app = tkinter.Tk()
select_board_size()  # 玩家选择棋盘大小
game = MineSweeper(app, WIDTH, HEIGHT, MINE_NUM)
app.mainloop()

