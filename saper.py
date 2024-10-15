import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import random

    

# Размеры поля
rows = 20
cols = 20
mins = rows*cols//10 * 2


timer_id=None
elapsed_time=0

#WINDOW

cell_has_flag = [[False for _ in range(cols)] for _ in range(rows)]

def create_game_field():
    global array,buttons, cell_has_flag, all_cells, random_cells, zeros, opened, elapsed_time, timer_id
    array = np.zeros((rows, cols), dtype = int)
    cell_has_flag = [[False for _ in range(cols)] for _ in range(rows)]

    # Получаем все возможные координаты (индексы) клеток массива
    all_cells = [(i, j) for i in range(rows) for j in range(cols)]
    # Случайно выбираем n мин
    random_cells = random.sample(all_cells, mins)

    # Вывод выбранных клеток(мин)
    print("\nМины:")
    print(random_cells)
    
    elapsed_time=0
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None
    
    update_timer()

    for cell in random_cells:
        array[cell]=9

    x = 0
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in random_cells:
                if i-1>=0 and j-1>=0 and array[i-1][j-1]==9:
                    x+=1
                if i-1>=0 and array[i-1][j]==9:
                    x+=1
                if i-1>=0 and j+1<cols and array[i-1][j+1]==9:
                    x+=1
                if j-1>=0 and array[i][j-1]==9:
                    x+=1
                if j+1<cols and array[i][j+1]==9:
                    x+=1
                if j-1>=0 and i+1<rows and array[i+1][j-1]==9:
                    x+=1
                if i+1<rows and array[i+1][j]==9:
                    x+=1
                if i+1<rows and j+1<cols and array[i+1][j+1]==9:
                    x+=1
                array[i][j] = x
            x = 0
                

    zeros=[]

    opened=[]
    buttons = [[None for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            button = tk.Button(game_frame, text="",borderwidth=0, highlightthickness=0, command=lambda r=row, c=col: on_click(r, c))
            button.bind("<Button-3>", lambda event, r=row, c=col: on_right_click(event, r, c))
            button.bind("<Enter>", lambda event, r=row, c=col: entered(event, r, c))
            button.bind("<Leave>", lambda event, r=row, c=col: left(event, r, c))
            if (row+col)%2==0:
                button["bg"]="#aad751"
            else:
                button["bg"]="#a2d149"
            button.grid(row=row, column=col, sticky="nsew")    
            buttons[row][col] = button

def on_click(row, col):
    global cell_has_flag, opened
    if cell_has_flag[row][col]:
        return
    button_width = buttons[row][col].winfo_width()
    button_height = buttons[row][col].winfo_height()
    opened.append((row,col))
    #buttons[row][col]["state"]="disabled"
    if buttons[row][col]["state"] == "disabled":
        return
    print(f"Размер кнопки ({row},{col}): {button_width}x{button_height} пикселей")
    print(f"Клетка ({row+1}, {col+1}) нажата")
    if cell_has_flag[row][col]==True:
        return
    if (row+col)%2==0:
        buttons[row][col]["bg"] = "#e5c29f"
    else:
        buttons[row][col]["bg"] = "#d7b899"
        
    buttons[row][col].config(relief="flat", state="normal")
    
    
    if array[row][col]==0:
        buttons[row][col]["text"]=''
    elif array[row][col]==1:
        buttons[row][col]["fg"]="#1976d2"
    elif array[row][col]==2:
        buttons[row][col]["fg"]="#388e3c"
    elif array[row][col]==3:
        buttons[row][col]["fg"]="#d33131"
    elif array[row][col]==4:
        buttons[row][col]["fg"]="#7e23a3"
    elif array[row][col]==5:
        buttons[row][col]["fg"]="#D83DE9"
    elif array[row][col]==6:
        buttons[row][col]["fg"]="#FF0022"
    elif array[row][col]==7:
        buttons[row][col]["fg"]="FF0022"
    elif array[row][col]==8:
        buttons[row][col]["fg"]="#FF3AF3"
    elif array[row][col]==9:
        buttons[row][col].config(image=mine_photo, text="") 
        root.after(1000, loose)
    if array[row][col]!=0 and array[row][col]!=9:
        buttons[row][col]["text"]=array[row][col]
    
    if array[row][col]==0:
        if (row, col) not in random_cells:
            if row-1>=0 and col-1>=0 and (row-1,col-1) not in zeros:
                zeros.append((row-1,col-1))
                on_click(row-1,col-1)
                
           
            if row-1>=0 and (row-1,col) not in zeros:
                zeros.append((row-1,col))
                on_click(row-1,col)
                
            
            if row-1>=0 and col+1<cols and (row-1,col+1) not in zeros:
                zeros.append((row-1,col+1))
                on_click(row-1,col+1)
                
            
            if col-1>=0 and (row,col-1) not in zeros:
                zeros.append((row,col-1))
                on_click(row,col-1)
                
            
            if col+1<cols and (row,col+1) not in zeros:
                zeros.append((row,col+1))
                on_click(row,col+1)
                
            
            if col-1>=0 and row+1<rows and (row+1,col-1) not in zeros:
                zeros.append((row+1,col-1))
                on_click(row+1,col-1)
                
          
            if row+1<rows and (row+1,col) not in zeros:
                zeros.append((row+1,col))
                on_click(row+1,col)
                
            
            if row+1<rows and col+1<cols and (row+1,col+1) not in zeros:
                zeros.append((row+1,col+1))
                on_click(row+1,col+1)
                
          
        zeros.append((row,col))
        
    else:
        return
    #buttons[row][col]["state"] ="readonly"
    


# Создание основного окна
root = tk.Tk()
root.title("Игра Сапёр")

flag_image = Image.open("flag1.png")
flag_image = flag_image.resize((30, 30), Image.Resampling.LANCZOS)  # Установим размер изображения под кнопку
flag_photo = ImageTk.PhotoImage(flag_image) 

mine_image = Image.open("mine.png")
mine_image = mine_image.resize((30, 30), Image.Resampling.LANCZOS)
mine_photo = ImageTk.PhotoImage(mine_image) 

cell_has_flag = [[False for _ in range(cols)] for _ in range(rows)]

def on_right_click(event, row, col):
    global cell_has_flag
    if (row,col) not in opened:
        if not cell_has_flag[row][col]:
            buttons[row][col].config(image=flag_photo, text="")  # Устанавливаем флажок
            cell_has_flag[row][col] = True
            print("ПКМ")
        else:
            buttons[row][col].config(image='')  # Убираем флажок (клетка пустая)
            cell_has_flag[row][col] = False
            print("Убрал ФЛАГ")
        
def entered(event,row,col): 
    if (row,col) not in opened:
        if (row+col) % 2 == 0:
            buttons[row][col]["bg"] ="#bfe17d"
        else:
            buttons[row][col]["bg"] ="#b9dd77"
 
def left(event,row,col):
    if (row,col) not in opened:
        if (row+col) % 2 == 0:
            buttons[row][col]["bg"] ="#aad751"
        else:
            buttons[row][col]["bg"] ="#a2d149"
            
            
def update_timer():
    global elapsed_time, timer_id
    minutes, seconds = divmod(elapsed_time, 60)
    timer_label.config(text=f"{minutes:02}:{seconds:02}")
    loose_timer.config(text=f"{minutes:02}:{seconds:02}")
    elapsed_time += 1
    timer_id = root.after(1000, update_timer)


    
def loose():
    global timer_id
    game_frame.pack_forget()
    loose_frame.pack(fill="both",expand="True")  
    root.after_cancel(timer_id)

button_size = 32


menu_frame = tk.Frame(root, height=50, bg="#4a752c")
menu_frame.pack(fill="x")

game_frame = tk.Frame(root)
game_frame.pack()

settings_frame =tk.Frame(root,bg="#4a752c")

set_button=tk.Button(settings_frame, text="Settings",bg="white")
set_button.pack(side="left",padx=10,pady=5)

restart_button=tk.Button(menu_frame, text="Restart",bg="white", command=lambda: restart_game())
restart_button.pack(side="left",padx=10,pady=5)

menu_button=tk.Button(menu_frame, text="Menu",bg="white")
menu_button.pack(side="left",padx=10,pady=5)
menu_button.bind("<Button-1>",lambda event:settings_click(event))

close_button=tk.Button(settings_frame, text="CLOSE",bg="white")
close_button.pack(side="left",padx=10,pady=5)
close_button.bind("<Button-1>",lambda event:close_menu(event))

timer_label = tk.Label(menu_frame, text="00:00", font=("Helvetica", 16), bg="white")
timer_label.pack(side="left", padx=10, pady=5)

loose_frame =tk.Frame(root,bg="#4a752c")
loose_text = tk.Label(loose_frame, text="Your time: ", bg="white")
loose_text.pack(side="left", padx=10, pady=5)
loose_timer = tk.Label(loose_frame, text="00:00", font=("Helvetica", 16), bg="white")
loose_timer.pack(side="left", padx=10, pady=5)

loose_restart_button=tk.Button(loose_frame, text="Restart",bg="white", command=lambda: loose_restart_game())
loose_restart_button.pack(side="left",padx=10,pady=5)



def loose_restart_game():
    loose_frame.pack_forget()
    game_frame.pack()
    restart_game()

def restart_game():
    # Удаляем все кнопки из игрового фрейма
    for widget in game_frame.winfo_children():
        widget.destroy()
    # Заново создаем игровое поле
    create_game_field()


def settings_click(event):
    game_frame.pack_forget()
    settings_frame.pack(fill="both",expand="True")
    
def close_menu(event):
    settings_frame.pack_forget()
    game_frame.pack()

for row in range(rows):
    root.grid_rowconfigure(row, minsize=button_size)  # Задаем высоту строки
    for col in range(cols):
        root.grid_columnconfigure(col, minsize=button_size)
# Создание сетки кнопок


        
for row in range(rows):
    game_frame.grid_rowconfigure(row, minsize=button_size)
for col in range(cols):
    game_frame.grid_columnconfigure(col, minsize=button_size)
#root.geometry("600x600")
#   root.geometry(f"{cols*button_size}x{rows*button_size+50}")

create_game_field()

root.update()
window_width = root.winfo_width()
window_height = root.winfo_height()
root.geometry(f"{window_width}x{window_height}")    
root.wm_resizable(False, False)
# Запуск приложения
root.mainloop()
