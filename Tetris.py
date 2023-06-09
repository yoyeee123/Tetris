import tkinter
from tkinter import messagebox
import random


ROW = 20  # 行数
COL = 14  # 列数
PointSize = 30  # 每个单元格的长度
height = ROW * PointSize  # 窗口高度
width = COL * PointSize  # 窗口宽度
score = 0   # 积分
level = 1   # 关卡数
seconds = 0   # 计时
is_paused = False   # 控制游戏及计时器的暂停与继续

# 存放不同形状和颜色的方块
SHAPES = {
    "O": [[(-1, -1), (0, -1), (-1, 0), (0, 0)], "yellow"],
    "Z": [[(-1, -1), (0, -1), (0, 0), (1, 0)], "blue"],
    "L": [[(-1, 0), (0, 0), (-1, -1), (-1, -2)], "green"],
    "J": [[(-1, 0), (0, 0), (0, -1), (0, -2)], "pink"],
    "T": [[(-1, -1), (0, -1), (0, 0), (1, -1)], "aqua"],
    "I": [[(0, 1), (0, 0), (0, -1), (0, -2)], "purple"],
    "P": [[(0, -2), (0, -1), (0, 0), (1, -2)], "red"]
}


LEVELS = [
    # 关卡1
    {
        'speed': 500,
        'grade': 80,
        'period': 60   # 关卡时间
    },
    # 关卡2
    {
        'speed': 400,
        'grade': 110,
        'period': 80
    },
    # 关卡3
    {
        'speed': 300,
        'grade': 150,
        'period': 90
    },
    # 关卡4
    {
        'speed': 250,
        'grade': 250,
        'period': 80
    },
    # 关卡5
    {
        'speed': 200,
        'grade': 280,
        'period': 80
    },
    # 关卡6
    {
        'speed': 200,
        'grade': 280,
        'period': 75
    }
]


blocks_list = []  # 二维列表，存放已经固定的方块的类型
for i in range(ROW):  # 初始化列表
    irow = []
    for j in range(COL):
        irow.append('')
    blocks_list.append(irow)


root = tkinter.Tk()  # 建立一个窗口
root.title(f"俄罗斯方块  第{level}关  SCORE：{score}  目标分数：{LEVELS[level-1]['grade']}")

timer_label = tkinter.Label(root, text="000", font=('Arial', 20))   # 计时器标签
timer_label.pack()

canvas = tkinter.Canvas(root, height=height, width=width)  # 创建一个画布
canvas.pack()  # 放置画布


def draw_point(canvas, c, r, color="#CCCCCC"):  # 在画布上绘制单个矩形方块
    # (x0,y0)(x1,y1)分别表示该方块在画布上左上角和右下角的位置坐标
    x0 = c * PointSize
    y0 = r * PointSize
    x1 = x0 + PointSize
    y1 = y0 + PointSize

    # 绘制单个矩形，width为矩形边界宽度
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=1)


def draw_background(canvas, block_list):  # 在画布上绘制所有空白方块
    for i in range(ROW):
        for j in range(COL):
            if block_list[i][j] == '':  # 该位置无方块，则按指定颜色绘制
                draw_point(canvas, j, i)
            else:  # 该位置无方块，则按默认颜色绘制
                draw_point(canvas, j, i, SHAPES[block_list[i][j]][1])


draw_background(canvas, blocks_list)


def draw_block(canvas, c, r, point_list, color="#CCCCCC"):  # 绘制指定颜色和形状的方块
    for point in point_list:   # point_list为指定方块的相对坐标
        x, y = point
        point_c = c + x  # 求每个单元方块的绝对坐标
        point_r = r + y
        if 0 <= c < COL and 0 <= r < ROW:
            draw_point(canvas, point_c, point_r, color)


def create_new_block():  # 随机生成新的方块
    type = random.choice(list(SHAPES.keys()))
    new_point = [COL // 2, 0]
    new_block = {
        "type": type,
        "point_list": SHAPES[type][0],  # 指定形状的相对位置的列表
        "new_point": new_point  # 绝对位置
    }
    return new_block


def check_collision(block, direction=[0, 0]):  # 碰撞检测，检查方块是否可以移动
    current_c, current_r = block["new_point"]  # 绝对位置
    point_list = block["point_list"]  # 相对位置
    for point in point_list:
        x, y = point
        point_c = x + current_c + direction[0]   # 新的绝对坐标
        point_r = y + current_r + direction[1]

        if point_c >= COL or point_c < 0 or point_r >= ROW:     # 是否越界
            return False
        if point_r >= 0 and blocks_list[point_r][point_c] != '':    # 是否与其他方块冲突
            return False
    return True


def save_block(block):  # 记录无法移动的方块的每个位置
    global score

    point_list = block['point_list']
    current_c, current_r = block['new_point']

    for point in point_list:
        x, y = point
        point_c = x + current_c
        point_r = y + current_r
        blocks_list[point_r][point_c] = block['type']

    score = score + 4
    is_clear_screen()


def move_block(canvas, block, direction=[0, 0]):  # 绘制移动后的方块
    type = block['type']
    point_list = block['point_list']
    current_c, current_r = block['new_point']

    # 清除当前位置的方块
    draw_block(canvas, current_c, current_r, point_list)

    # 求新位置并绘制新位置方块
    new_c = current_c + direction[0]
    new_r = current_r + direction[1]
    block['new_point'] = [new_c, new_r]
    draw_block(canvas, new_c, new_r, point_list, SHAPES[type][1])


def Left(event):
    direction = [-1, 0]
    global current_block
    if check_collision(current_block, direction):
        move_block(canvas, current_block, direction)


def Right(event):
    direction = [1, 0]
    global current_block
    if check_collision(current_block, direction):
        move_block(canvas, current_block, direction)


def down(event):     # 方块直接下落到最低
    global current_block
    point_list = current_block['point_list']
    c, r = current_block['new_point']
    max_height = ROW   # 方块能下降的最大高度

    for point in point_list:  # 对方块中的每一个相对坐标遍历
        x, y = point
        current_c, current_r = x + c, y+r
        h = 0
        for i in range(current_r + 1, ROW):  # 对每一行遍历检查
            if blocks_list[i][current_c] != '':
                break
            else:
                h = h + 1
        if h < max_height:
            max_height = h

    direction = [0, max_height]
    if check_collision(current_block, direction):
        move_block(canvas, current_block, direction)


def rotate(event):   # 旋转方块
    global current_block
    point_list = current_block["point_list"]
    current_c, current_r = current_block['new_point']
    new_point_list = []

    for point in point_list:      # 改变相对坐标
        x, y = point
        new_point_list.append([y, -x])   # 逆时针旋转方块
    new_block = {
        "type": current_block["type"],
        "point_list": new_point_list,
        "new_point": current_block["new_point"]
    }

    if check_collision(new_block):
        # 清除当前位置的方块
        draw_block(canvas, current_c, current_r, point_list)
        # 记录新位置绘制新位置方块
        current_block = new_block
        draw_block(canvas, current_c, current_r, new_point_list, SHAPES[current_block["type"]][1])


def Full_Row(irow):
    for s in irow:
        if s == '':
            return False
    return True


def is_clear_row():  # 消除全部排满的行
    full_row = False   # 记录界面中是否存在满行
    global score
    rows = 0   # 消除的行数
    for i in range(len(blocks_list)):
        if Full_Row(blocks_list[i]):
            full_row = True
            rows += 1
            for cur_i in range(i, 0, -1):    # 从下往上进行更新
                blocks_list[cur_i] = blocks_list[cur_i - 1]
    for j in range(COL):
            blocks_list[0].append('')

    score = score + rows*COL
    is_clear_screen()

    if full_row:  # 如果消除了某行，则重新绘制画布
        draw_background(canvas, blocks_list)
        root.title(f"俄罗斯方块  第{level}关  SCORE：{score}  目标分数：{LEVELS[level-1]['grade']}")


def is_clear_screen():   # 当满足过关要求时，清屏，进入下一关
    global level
    global score
    global seconds
    if score >= LEVELS[level-1]['grade']:  # 判断分数
        level = level+1
        for irow in blocks_list:  # 清屏操作
            for i in range(len(irow)):
                irow[i] = ''
        draw_background(canvas, blocks_list)
        score = 0
        seconds = LEVELS[level-1]['period']
    root.title(f"俄罗斯方块  第{level}关  SCORE：{score}  目标分数：{LEVELS[level-1]['grade']}")


def paused(event):
    global is_paused
    is_paused = not is_paused
    if is_paused:   # 游戏暂停时输出提示信息
        messagebox.showinfo("游戏暂停", "请按空格键继续！")


def update_timer():   # 倒计时
    global seconds
    global is_paused

    if not is_paused:
        seconds -= 1
    timer_label.config(text=seconds)
    root.after(1000, update_timer)


def game_loop():
    root.update()
    global current_block
    global blocks_list
    global level
    global score
    global seconds
    global is_paused
    speed = LEVELS[level]['speed']

    if seconds <= 0:     # 倒计时结束，则游戏结束
        messagebox.showinfo("GAME OVER!", f"YOUR LEVEL IS:{level}  \nYOUR SCORE IS: {score}")
        root.destroy()
        return
    if current_block is None:  # 画布内不存在方块时
        if not is_paused:
            current_block = create_new_block()   # 绘制新方块
            move_block(canvas, current_block)
            for i in range(ROW):      # 当某列排满，则游戏结束
                for j in range(COL):
                    if (blocks_list[i][j] != '' and i <= 0) or (seconds <= 0):
                        messagebox.showinfo("GAME OVER!", f"YOUR LEVEL IS:{level}  \nYOUR SCORE IS: {score}")
                        root.destroy()
                        return
    else:  # 画布内有方块时
        if not is_paused:
            if check_collision(current_block, [0, 1]):  # 当可以继续向下移动时
                move_block(canvas, current_block, [0, 1])
            else:
                save_block(current_block)
                current_block = None

    is_clear_row()
    root.after(speed, game_loop)


canvas.focus_set()  # 将键盘的输入聚焦到canvas画板上


# 绑定方向键     第一个参数为按键，第二个参数为要执行的方法
canvas.bind("<Left>", Left)
canvas.bind("<Right>", Right)
canvas.bind("<Down>", down)
canvas.bind("<Up>", rotate)
canvas.bind("<space>", paused)

current_block = None  # 定义初始值
seconds = LEVELS[0]['period']
game_loop()
update_timer()
root.mainloop()  # 让窗口循环，一直显示
