import tkinter as tk
import keyboard

HEIGH = 300
WIDTH = 500

# background colours
lred = "#bbddee"
lblue = "#ff8888"
red = "#8888ff"
blue = "#ff5555"
lred2 = "#aaccee"
lblue2 = "#ee7777"

players = {}

players["001"] = {"name": "John Cena",
                    "kills": 5,
                    "deaths": 15,
                    "outfit": "test outfit name",
                    "outfit_alias": "TON"}

root = tk.Tk()

frame1 = tk.Frame(root, bg=lred)

frame2 = tk.Frame(root, bg=lblue)

frame1.grid(row = 0, column = 0) 
frame2.grid(row = 0, column = 1) 

placeholder_team1 = tk.StringVar(root, "Tag1")
entry_team1 = tk.Entry(frame1, font="Helvetica 12 bold", bg=red, justify="center", textvariable=placeholder_team1)

placeholder_team2 = tk.StringVar(root, "Tag2")
entry_team2 = tk.Entry(frame2, font="Helvetica 12 bold", bg=blue, justify="center", textvariable=placeholder_team2)

entry_team1.grid(row = 0, column = 0, columnspan=3)
entry_team2.grid(row = 0, column = 3, columnspan=3)

def get_alias():
    alias1 = entry_team1.get()
    alias2 = entry_team2.get()
    print(alias1, alias2)

def display_player_stats(player_info, frame, row):
    print(str(frame))
    if str(frame) == ".!frame":
        bg = lred
        col = 0
    else:
        bg = lblue
        col = 3
    name = tk.Label(frame, text=player_info["name"], bg=bg)
    name.grid(row=row, column=col)
    k = tk.Label(frame, text=player_info["kills"], bg=bg)
    k.grid(row=row, column=col + 1)
    d = tk.Label(frame, text=player_info["deaths"], bg=bg)
    d.grid(row=row, column=col + 2)

# right side
player_name = tk.Label(frame1, text="Name", bg=lred, font="bold")
player_name.grid(row=2, column=0)
player_k = tk.Label(frame1, text="K", bg=lred, font="bold")
player_k.grid(row=2, column=1)
player_d = tk.Label(frame1, text="D", bg=lred, font="bold")
player_d.grid(row=2, column=2)

# left side
player_name = tk.Label(frame2, text="Name", bg=lblue, font="bold")
player_name.grid(row=2, column=3)
player_k = tk.Label(frame2, text="K", bg=lblue, font="bold")
player_k.grid(row=2, column=4)
player_d = tk.Label(frame2, text="D", bg=lblue, font="bold")
player_d.grid(row=2, column=5)

display_player_stats(players["001"], frame1, 3)
display_player_stats(players["001"], frame1, 4)
display_player_stats(players["001"], frame1, 5)
display_player_stats(players["001"], frame1, 6)
display_player_stats(players["001"], frame1, 7)
display_player_stats(players["001"], frame1, 8)

display_player_stats(players["001"], frame2, 3)
display_player_stats(players["001"], frame2, 4)
display_player_stats(players["001"], frame2, 5)
display_player_stats(players["001"], frame2, 6)
display_player_stats(players["001"], frame2, 7)
display_player_stats(players["001"], frame2, 8)

alias1 = ""
alias2 = ""
keyboard.add_hotkey("enter", get_alias)

root.mainloop()

#%%

text1=f"{'name':<30}{'K':>5}{'D':>15}"
text2=f"{'Edy':<30}{5:>5}{112312315:>15}"
text3=f"{'asd':<30}{1115:>5}{5:>15}"

print(text1)
print(text2)
print(text3)
