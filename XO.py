from tkinter import *
import time
import numpy as np
can_click=True
def tpl_int(coordonnees):
    result=[]
    for coordonnee in coordonnees:
        result.append((int(coordonnee[1]),int(coordonnee[3])))
    return result
try:
    file_strategies=open("strategies.txt","r+")
except:
    file_strategies=open("strategies.txt","w")
lines=file_strategies.readlines()
len_lines=0
n_l=-1
ints=[]
strategies_robot={"X":[],"O":[]}
strategies={"X":[],"O":[]}
for line in lines:
    list_line=[]
    list_strategie=[]
    n_l+=1
    len_lines+=len(line)
    strategie_line,case_line=line.split("|")
    for char in strategie_line:
        if char in["X","O"]:
            x_o=char
        if char in list(map(str,list(range(0,9)))):
            ints.append(char)
        if len(ints)==2:
            list_strategie.append((int(ints[0]),int(ints[1])))
            list_line.append(f"({ints[0]},{ints[1]})")
            ints=[]
    if len(case_line)>15:
        strategies_robot[x_o].append((list_strategie,[(int(case_line[1]),int(case_line[3])),(int(case_line[7]),int(case_line[9])),(int(case_line[13]),int(case_line[15]))]))
    else:
        strategies_robot[x_o].append((list_strategie,[(int(case_line[1]),int(case_line[3])),(int(case_line[7]),int(case_line[9]))]))
    strategies[x_o].append(list_line)
file_strategies.close()
def the_one_player():
    global stat_win,canvas_start,frame_buttons
    stat_win=["PILE","FACE"][round(np.random.normal()*10**10)%2]
    canvas_start=Canvas(window,bg="black",bd=2,width=400,height=200)
    frame_buttons=Frame(window)
    button_pile=Button(frame_buttons,text="PILE",font=("courrier",20),bg="blue",fg="yellow",command=Pile)
    button_face=Button(frame_buttons,text="FACE",font=("courrier",20),bg="yellow",fg="blue",command=Face)
    button_pile.grid(column=0,row=0)
    button_face.grid(column=1,row=0)
    canvas_start.pack()
    frame_buttons.pack()
def show_black_board(choix:str):
    global is_robot_first_player,stat_win
    canvas_result=Canvas(canvas_start,bg="pink",width="380",height="180")
    is_robot_first_player=choix!=stat_win
    if  not is_robot_first_player:
        commanter="vous jouez le premier"
    else:
        commanter="robot joue le premier"
    canvas_result.create_text(200,50,text=f"          {stat_win}\n{commanter}",font=("courrier",20),fill="blue")
    canvas_result.pack()
    window.update()
def Face():
    global canvas_start,frame_buttons
    show_black_board("FACE")
    time.sleep(1.5)
    canvas_start.destroy()
    frame_buttons.destroy()
    create_table()
def Pile():
    show_black_board("PILE")
    time.sleep(1.5)
    canvas_start.destroy()
    frame_buttons.destroy()
    create_table()    
def create_table():
    global canvas,nombre_tours,button,label,table,button_menu,strategie,is_robot_first_player,taille,nombre_players
    canvas=Canvas(window,width=width,height=height)
    strategie={"X":[],"O":[]}
    nombre_tours=0
    button.destroy()
    button_menu.destroy()
    label.destroy()
    for y in range(0,height,height//3):
      for x in range(0,width,width//3):
          canvas.create_rectangle(x,y,x+width//3,height//3+y,fill="white")
    canvas.pack()
    canvas.bind("<Button-1>",click)
    table=[[""]*3 for _ in range(3)]
    window.update()
    if  nombre_players==1 and is_robot_first_player:
        taille=height//3
        time.sleep(0.5)
        virtual_player(table)
def menu():
    global frame_start,button,label,button_menu
    button.destroy()
    button_menu.destroy()
    label.destroy()
    frame_start=Frame(window)
    frame_cases=Frame(frame_start,bg="yellow")
    button_one_player=Button(frame_cases,text="un joueur",font=("courrier",25),fg="red",bg="blue",border=1,width=20,command=one_player)
    button_two_players=Button(frame_cases,text="deux joueurs",font=("courrier",25),fg="red",bg="blue",border=1,width=20,command=two_players)
    frame_start.pack()
    frame_cases.pack(pady=200)
    button_one_player.pack(pady=3,padx=3)
    button_two_players.pack(pady=3,padx=3)
def click(event):
    global height,width,nombre_tours,table,taille,nombre_players,is_over,can_click
    if not can_click and nombre_players==1:
        return
    taille=height//3
    x,y=(event.x-(event.x%taille)),(event.y-(event.y%taille))
    if nombre_tours%2==0:
        color="blue"     
        char="X"
    else:
        color="red"
        char="O"
    if table[y//taille][x//taille]:
        return
    coche_case(y,x,char,color)
    can_click=False
    if nombre_players==1 and not is_over:
        time.sleep(0.5)     
        virtual_player(table)
def coche_case(y,x,char,color):
    global taille,nombre_tours
    table[y//taille][x//taille]=char
    canvas.create_text(x+taille//2,y+taille//2,text=char,font=("courrier",taille),fill=color)
    nombre_tours+=1
    window.update()
    game_over(table,x//taille,y//taille)
def game_over(table,x,y):
    global canvas,nombre_tours,button,label,scores,button_menu,is_over,strategie,len_lines,strategies,is_robot_first_player,nombre_players,n_l,strategies_robot
    strategie[table[y][x]].append(f"({y},{x})")
    time.sleep(0.5)
    is_full=True
    is_over=False
    for row in table:
        for case in row:
            if not case:
                is_full=False
    if table[y][0]==table[y][1]==table[y][2] or table[0][x]==table[1][x]==table[2][x] or table[0][0]==table[1][1]==table[2][2]==table[y][x]or table[0][2]==table[1][1]==table[2][0]==table[y][x] or is_full:
        canvas.destroy()
        X="X"
        O="O"
        if nombre_players==1 and is_robot_first_player:
            X="Robot"
            O="Player"
            is_robot_first_player=not is_robot_first_player
        elif nombre_players==1 :
            X="Player"
            O="Robot"
            is_robot_first_player=not is_robot_first_player
        if  table[y][0]==table[y][1]==table[y][2] or table[0][x]==table[1][x]==table[2][x] or table[0][0]==table[1][1]==table[2][2]==table[y][x]or table[0][2]==table[1][1]==table[2][0]==table[y][x]:
          if nombre_players==1:
              if table[y][x]=="X":
                  scores[X]+=1
              else:
                  scores[O]+=1
          else:
              scores[table[y][x]]+=1
          strategie[table[y][x]].pop()
          strategie[{"X":"O","O":"X"}[table[y][x]]].pop()
          empty_case=[]
          for x_1 in range(3):
              if len(strategie[table[y][x]])!=3:
                  break
              for x_2 in range(x_1+1,3):
                  pseudo_table=[[""]*3 for _ in range(3)]
                  pseudo_table[int(strategie[table[y][x]][x_1][1])][int(strategie[table[y][x]][x_1][3])]=table[y][x]
                  pseudo_table[int(strategie[table[y][x]][x_2][1])][int(strategie[table[y][x]][x_2][3])]=table[y][x]
                  to_add=virtual_player(pseudo_table,True)
                  if to_add!="(-1,-1)":
                      empty_case.append(to_add)
          if len(strategie[table[y][x]])==3 and not strategie[table[y][x]] in strategies[table[y][x]] and len(empty_case)==3:
              strategies[table[y][x]].append(strategie[table[y][x]])
              strategies_robot[table[y][x]].append((tpl_int(strategie[table[y][x]]),tpl_int(strategie[{"X":"O","O":"X"}[table[y][x]]])))
              file_strategies=open("strategies.txt","r+")
              if len_lines!=0:
                file_strategies.seek(len_lines+n_l)
              to_write=table[y][x]+",".join(strategie[table[y][x]])+f"|{','.join(strategie[{'O':'X','X':'O'}[table[y][x]]])}"+"\n"
              len_lines+=len(to_write)
              n_l+=1
              file_strategies.write(to_write)
              file_strategies.close()
        label=Label(window,text=f"JOUEUR {X} :{scores[X]} || JOUEUR {O} :{scores[O]}",font=("courrier",25),fg="yellow",bg="green")
        button=Button(window,text="replay",font=("courrier",25),fg="red",bg="yellow",command=create_table)
        button_menu=Button(window,text="menu",font=("courrier",25),fg="red",bg="yellow",command=menu)
        label.pack(pady=20)
        button.pack()
        button_menu.pack(pady=20)
        is_over=True
        strategie={"X":[],"O":[]}
def reading_line(line:list)->dict:
    cases={"X":0,"O":0,"":[]}
    for case in line:
        if case in ["X","O"]:
            cases[case]+=1
        else:
            cases[case].append(line.index(case))
    if cases[""]:
        cases[""]=cases[""][0]
    return cases
#--------------------------------------------  
def is_accepted(local_strategie:list,signe:str,anti_signe:str)->bool:
    global table,strategie
    resoult1,resoult2=True,True
    for index in range(len(strategie[signe])):
        if strategie[signe][index]!=local_strategie[0][index]:
            return False
    for index in range(len(strategie[anti_signe])):
        if strategie[anti_signe][index]!=local_strategie[1][index]:
            resoult1=False
            break
    empty_case=[]
    for x_1 in range(3):
        for x_2 in range(x_1+1,3):
            pseudo_table=[[""]*3 for _ in range(3)]
            pseudo_table[int(strategie[table[y][x]][x_1][1])][int(strategie[table[y][x]][x_1][3])]=table[y][x]
            pseudo_table[int(strategie[table[y][x]][x_2][1])][int(strategie[table[y][x]][x_2][3])]=table[y][x]
            to_add=virtual_player(pseudo_table,True)
            if to_add!="(-1,-1)":
                empty_case.append((int(to_add[1]),int(to_add[3])))
    for case in empty_case:
        if table[case[0]][case[1]]:
            resoult2=False
    if resoult1 or resoult2:
        return True
def best_strategies(signe):
    global strategies_robot
    anti_signe={"X":"O","O":"X"}[signe]
    result,anti_result=[],[]
    for local_strategie in strategies_robot[signe]:
        if is_accepted(local_strategie,signe,anti_signe):
            result.append(local_strategie[0])
    for local_strategie in strategies_robot[anti_signe]:
        if is_accepted(local_strategie,anti_signe,signe):
            anti_result.append(local_strategie)
    return result,anti_result

    
def virtual_player(table,return_case=False):
    global is_robot_first_player,can_click,strategie
    if not return_case and is_robot_first_player:
        signe_robot="X"
        signe_player="O"
    else:
        signe_robot="O"
        signe_player="X"
    x,y=-1,-1
    stat_1=reading_line([table[0][0],table[1][1],table[2][2]])
    stat_2=reading_line([table[2][0],table[1][1],table[0][2]])
    for i in range(3):
        stat_y=reading_line(table[i])
        stat_x=reading_line([table[0][i],table[1][i],table[2][i]])
        if stat_y[signe_player]==0 and stat_y[signe_robot]==2:
             y,x=i,stat_y[""]
             break
        elif stat_x[signe_player]==0 and stat_x[signe_robot]==2:
             y,x=stat_x[""],i
             break
        elif stat_1[signe_player]==0 and stat_1[signe_robot]==2:
            y,x=stat_1[""],stat_1[""]
            break
        elif stat_2[signe_player]==0 and stat_2[signe_robot]==2:
            y,x=2-stat_2[""],stat_2[""]
            break
        elif stat_1[signe_player]==2 and stat_1[signe_robot]==0:
            y,x=stat_1[""],stat_1[""]
        elif stat_2[signe_player]==2 and stat_2[signe_robot]==0:
            y,x=2-stat_2[""],stat_2[""]
        elif stat_y[signe_player]==2 and stat_y[signe_robot]==0:
            y,x=i,stat_y[""]
        elif stat_x[signe_player]==2 and stat_x[signe_robot]==0:
            y,x=stat_x[""],i   
    if return_case:
        return f"({y},{x})"
    if is_robot_first_player:
        char="X"
        color="blue"
    else:
        color="red"
        char="O"
    while x <0 or y<0 or table[y][x]:
        y,x=round(np.random.normal()*10**10)%3,round(np.random.normal()*10**10)%3
    coche_case(y*taille,x*taille,char,color)
    can_click=True
def one_player():
    global nombre_players,frame_start,scores
    scores={"Robot":0,"Player":0}
    nombre_players=1
    frame_start.destroy() 
    the_one_player()
def two_players():
    global nombre_players,frame_start,scores
    scores={"X":0,"O":0}
    nombre_players=2
    frame_start.destroy()  
    create_table()
window = Tk()
window.title("XO")
window.resizable(False,False)
width,height=720,720
width,height=width//3*3,height//3*3
window.geometry(f"{width}x{height}")
button=Button()
button_menu=Button()
label=Label()
menu()
window.mainloop()
