import os
import customtkinter as ctk
import tkinter as tk
import json

ctk.set_appearance_mode("dark")

records = {}
if os.path.isfile("records.json"):
    with open("records.json", 'r') as file:
        try:
            records = json.load(file)
            if not records:
                records = {"name": [], "uid": [], "vote": []}
        except json.JSONDecodeError:
            records = {"name": [], "uid": [], "vote": []}
else:
    records = {"name": [], "uid": [], "vote": []}      

def write_records():
    with open('records.json', 'w') as file:
        json.dump(records, file, indent=4) 


def total_update():
    if not records["vote"]:
        for i in total:
            i.set(0)
    else:
        p, q, r, s = 0, 0, 0, 0
        for i in records["vote"]:
            if i == 1:
                p += 1
            elif i == 2:
                q += 1
            elif i == 3:
                r += 1
            elif i == 4:
                s += 1
        total[0].set(p)
        total[1].set(q)
        total[2].set(r)
        total[3].set(s)
    # print(f"total0 is {total[0].get()}")
    # print(f"total1 is {total[1].get()}")
    # print(f"total2 is {total[2].get()}")
    # print(f"total3 is {total[3].get()}")

    # print(len(records["vote"]))

def write_result(value_type, option_no):
    if value_type == 'percent':
        if len(records["vote"]) == 0:
            return "0%"
        else:
            return f"{round(total[option_no].get() / len(records["vote"]) * 100, 2)}%"
    elif value_type == 'bar':
        if len(records["vote"]) == 0:
            return 0
        else:
            return total[option_no].get() / len(records["vote"])
    elif value_type == 'total_votes':
        return f"{total[option_no].get()} votes"

def check_existence(x):
    if not records["uid"]:
        return 'no'
    else:    
        for i in records["uid"]:
            if i == x:
                return "yes"
            elif i != x:
                return 'no'


def frame_visible(s):
    for framek, framev in frames.items():
        framev["window"].pack_forget()

    frames[s]["window"].pack_propagate(False)
    frames[s]["window"].pack(fill='both', expand=True)


def frame_front():
    root = frames["front"]

    # Buttons
    for i in ["vote", "create", "result"]:
        temp = ctk.CTkButton(
            master=root["window"], 
            width=550,
            height=60,
            text="TEXT", 
            font=("Poppins Bold", 35),
            corner_radius=15,
            border_width=3,
            fg_color="#212121",
            hover_color="#a81bcc",
            border_color = "#d323ff"
        )
        root["buttons"][i] = temp
    i = None
    
    root["variables"]["choice var"] = tk.StringVar(value="Default Text")
    choice_var = root["variables"]["choice var"]

    root["buttons"]["vote"].configure(
        text="Vote ->", 
        command=lambda: (choice_var.set("button1"), frame_visible("form"))
    )
    root["buttons"]["create"].configure(
        text="Create ->", 
        command=lambda: (choice_var.set("button2"), frame_visible("create"))
    )
    root["buttons"]["result"].configure(
        text="Result ->", 
        command=lambda: (choice_var.set("button3"), frame_visible("result"), total_update())
    )

    root["buttons"]["vote"].place(relx=0.5, y=150, anchor=tk.N)
    root["buttons"]["create"].place(relx=0.5, y=150 + 100, anchor=tk.N)
    root["buttons"]["result"].place(relx=0.5, y=150 + 200, anchor=tk.N)
    # Binds
    def btn_binds_all(*args,**kwargs): 
        event = kwargs.get('event', None)
        btn_btn_type = kwargs.get('btn_btn_type', None)
        hover = kwargs.get('hover', None)

        if hover == None:
            pass
        elif hover == 'enter':
            root["buttons"][btn_btn_type].configure(border_color = "white")
        elif hover == 'leave':
            root["buttons"][btn_btn_type].configure(border_color = "#d323ff")


    root["buttons"]["vote"].bind("<Enter>", lambda ev: btn_binds_all(ev, btn_btn_type="vote", hover='enter'))
    root["buttons"]["vote"].bind("<Leave>", lambda ev: btn_binds_all(ev, btn_btn_type="vote", hover='leave'))
    root["buttons"]["create"].bind("<Enter>", lambda ev: btn_binds_all(ev, btn_btn_type="create", hover='enter'))
    root["buttons"]["create"].bind("<Leave>", lambda ev: btn_binds_all(ev, btn_btn_type="create", hover='leave'))
    root["buttons"]["result"].bind("<Enter>", lambda ev: btn_binds_all(ev, btn_btn_type="result", hover='enter'))
    root["buttons"]["result"].bind("<Leave>", lambda ev: btn_binds_all(ev, btn_btn_type="result", hover='leave'))

    
def frame_form():
    root = frames["form"]
    # Entries
    for i in ["name", "uid"]:
        temp = ctk.CTkEntry(
        master=root["window"],
        width = 500,
        # height = 100,
        fg_color = "#212121",
        text_color = "white",
        # placeholder_text_color = "#00ccff",
        corner_radius = 20,
        placeholder_text = "Something", 
        font = ("Poppins Medium", 30),
        )
        root["entries"][i] = temp
    i = None

    root["entries"]["name"].configure(placeholder_text = "Name")
    root["entries"]["uid"].configure(placeholder_text = "Unique ID")

    root["entries"]["name"].place(relx=0.5, y=150, anchor=tk.N)
    root["entries"]["uid"].place(relx=0.5, y=150 + 100, anchor=tk.N)

    # Buttons
    def btn_fn(btn_type=None):
        if btn_type == 'c_btn':
            root["variables"]["name"] = root["entries"]["name"].get()
            root["variables"]["uid"] = root["entries"]["uid"].get()

            name = root["variables"]["name"]
            u_id = root["variables"]["uid"]
            
            

            if name != "" and u_id != "":
                if u_id.isdigit() or (u_id.startswith('-') and u_id[1:].isdigit()):   

                    # root["variables"]["name"] = root["variables"]["name"].strip()
                    # root["variables"]["uid"] = int(root["variables"]["uid"].strip())
                    # name = root["variables"]["name"]
                    # u_id = root["variables"]["uid"]

                    name = name.strip()
                    u_id = u_id.strip()

                    if check_existence(int(u_id)) == 'no':
                        print(f"name: {name}")
                        print(f"uid: {u_id}")

                        root["variables"]["name"] = name
                        root["variables"]["uid"] = u_id

                        frame_visible("vote")
                    elif check_existence(int(u_id)) == 'yes':
                        print("already_exist")
                        root["labels"]["invalid_info"].place_forget()
                        root["labels"]["invalid_existence"].place(relx=0.5, y=450, anchor=tk.CENTER)                   
                else:
                    print("Invalid_info")
                    root["labels"]["invalid_existence"].place_forget()
                    root["labels"]["invalid_info"].place(relx=0.5, y=450, anchor=tk.CENTER)  
            else:
                print("Invalid")
                root["labels"]["invalid_info"].place(relx=0.5, y=450, anchor=tk.CENTER)   

        elif btn_type == 'm_btn':
            root["labels"]["invalid_info"].place_forget()
            root["labels"]["invalid_existence"].place_forget()
            frame_visible("front")

        root["window"].focus_set()
        root["entries"]["name"].delete(0, ctk.END)
        root["entries"]["name"].insert(0, "") 
        root["entries"]["name"].configure(placeholder_text="Name")
        root["entries"]["uid"].delete(0, ctk.END)
        root["entries"]["uid"].insert(0, "") 
        root["entries"]["uid"].configure(placeholder_text="Unique ID")


    for i in ["confirm", "back_main"]:
        temp = ctk.CTkButton(
            master=root["window"], 
            width=550,
            height=60,
            text="TEXT", 
            font=("Poppins Bold", 25),
            corner_radius=15,
            border_width=3,
            fg_color="#d323ff",
            hover_color="#a81bcc",
            border_color = "#a81bcc"
        )
        root["buttons"][i] = temp
    
    # frames["front"]["variables"]["choice var"] = tk.StringVar(value="Default Text")

    root["buttons"]["confirm"].configure(
        text="Confirm",
        width=100,
        height=60, 
        command=lambda: btn_fn(btn_type = 'c_btn')
    )
    root["buttons"]["back_main"].configure(
        text="Go to Main Page",
        font=("Poppins Bold", 15),
        width=200,
        height=40, 
        border_width=2,
        fg_color="#212121",
        command=lambda: btn_fn(btn_type = 'm_btn')
    )

    root["buttons"]["confirm"].place(relx=0.5, y=350, anchor=tk.N)
    root["buttons"]["back_main"].place(relx=0.5, y=580, anchor=tk.S)

    # Binds


    # Labels

    for i in ["invalid_info", "invalid_existence", "txt"]:
        temp = ctk.CTkLabel(
            master=root["window"], 
            text="EMPTY", 
            font=("Poppins Medium", 20),
            fg_color="transparent",
            text_color="white"
        ) 
        root["labels"][i] = temp 

    root["labels"]["invalid_info"].configure(
        text="Invalid Input; Try Again", 
        font=("Poppins Medium", 20),
        fg_color="transparent",
        text_color="red"
    ) 

    root["labels"]["invalid_existence"].configure(
        text="You Have Already Given Vote", 
        font=("Poppins Medium", 20),
        text_color="red",
    ) 
                  
    # root["labels"]["invalid_info"].place_forget()


def frame_vote():
    root = frames["vote"]

    root["variables"]["selected_vote_no"] = None

    # Buttons
    def btn_fn(btn_type=None):

        if btn_type in ['1', '2', '3', '4']:
            for k, v in root["buttons"].items():
                root["buttons"][k].configure(
                    border_color = "#d323ff"
                )

            root["buttons"][f"vote_{btn_type}"].configure(
                border_color = "#00ccff"
            )
            root["variables"]["selected_vote_no"] = btn_type
            
        elif btn_type == 'c_btn':
            if root["variables"]["selected_vote_no"] != None:
                root["labels"]["txt"].place(relx=0.5, y=25, anchor=tk.N)

                name = frames["form"]["variables"]["name"]
                uid = int(frames["form"]["variables"]["uid"])
                vote = int(root["variables"]["selected_vote_no"])

                records["name"].append(name) 
                records["uid"].append(uid) 
                records["vote"].append(vote)
                write_records()


            else:
                root["labels"]["invalid_selection"].place(relx=0.5, y=500, anchor=tk.N)
        elif btn_type == 'm_btn':
            root["labels"]["invalid_selection"].place_forget()
            root["labels"]["invalid_existence"].place_forget()
            root["labels"]["txt"].place_forget()

            for k, v in root["buttons"].items():
                root["buttons"][k].configure(
                    border_color = "#d323ff"
                )
            frame_visible("front")

        root["window"].focus_set()

    for i in ["vote_1", "vote_2", "vote_3", "vote_4", "confirm", "back_main"]:
        temp = ctk.CTkButton(
            master=root["window"], 
            width=550,
            height=60,
            text="TEXT", 
            font=("Poppins Bold", 35),
            corner_radius=15,
            border_width=3,
            fg_color="#d323ff",
            hover_color="#a81bcc",
            border_color = "#d323ff"
        )
        root["buttons"][i] = temp 

    root["variables"]["choice var"] = tk.StringVar(value="Default Text")

    root["buttons"]["vote_1"].configure(
        text=options[0].get(),
        command=lambda: btn_fn(btn_type = '1')
    )
    root["buttons"]["vote_2"].configure(
        text=options[1].get(),
        command=lambda: btn_fn(btn_type = '2')
    )
    root["buttons"]["vote_3"].configure(
        text=options[2].get(),
        command=lambda: btn_fn(btn_type = '3')
    )
    root["buttons"]["vote_4"].configure(
        text=options[3].get(),
        command=lambda: btn_fn(btn_type = '4')
    )
    root["buttons"]["confirm"].configure(
        text="Confirm",
        font=("Poppins Bold", 15),
        width=100,
        height=40, 
        command=lambda: btn_fn(btn_type = 'c_btn'),
    )
    root["buttons"]["back_main"].configure(
        text="Go to Main Page",
        font=("Poppins Bold", 15),
        width=200,
        height=40, 
        border_width=2,
        fg_color="#212121",
        command=lambda: btn_fn(btn_type = 'm_btn')
    )

    root["buttons"]["vote_1"].place(relx=0.5, y=50, anchor=tk.N)
    root["buttons"]["vote_2"].place(relx=0.5, y=50+100, anchor=tk.N)
    root["buttons"]["vote_3"].place(relx=0.5, y=50+100+100, anchor=tk.N)
    root["buttons"]["vote_4"].place(relx=0.5, y=50+100+100+100, anchor=tk.N)
    root["buttons"]["confirm"].place(relx=0.5, y=475, anchor=tk.CENTER)
    root["buttons"]["back_main"].place(relx=0.5, y=580, anchor=tk.S)

    # Labels
    for i in ["invalid_selection", "invalid_existence", "txt"]:
        temp = ctk.CTkLabel(
            master=root["window"], 
            text="EMPTY", 
            font=("Poppins Medium", 20),
            fg_color="transparent",
            text_color="white"
        ) 
        root["labels"][i] = temp  
    
    root["labels"]["invalid_selection"].configure(
        text="Invalid; Select Something", 
        font=("Poppins Medium", 20),
        text_color="red",
    )

    root["labels"]["txt"].configure(
        text="Thanks For Voting", 
        font=("Poppins Medium", 50),
        width=600,
        height = 510,
        text_color="#d323ff",
    )


def frame_result():
    root = frames["result"]
    # Labels
    for i in ["o1", "o2", "o3", "o4"]:
        temp = ctk.CTkLabel(
            master=root["window"], 
            text="O's", 
            font=("Poppins", 30),
            fg_color="transparent",
            text_color="white"
        ) 
        root["labels"][i] = temp 


    root["labels"]["o1"].configure(text=options[0].get())
    root["labels"]["o2"].configure(text=options[1].get())
    root["labels"]["o3"].configure(text=options[2].get())
    root["labels"]["o4"].configure(text=options[3].get())


    root["labels"]["o1"].place(x=200, y=110, anchor=tk.SW)
    root["labels"]["o2"].place(x=200, y=110+125, anchor=tk.SW)
    root["labels"]["o3"].place(x=200, y=110+125+125, anchor=tk.SW)
    root["labels"]["o4"].place(x=200, y=110+125+125+125, anchor=tk.SW)
   

    for i in ["p1", "p2", "p3", "p4"]:
        temp = ctk.CTkLabel(
            master=root["window"], 
            text="percentage", 
            font=("Poppins Medium", 40),
            fg_color="transparent",
            text_color="white"
        ) 
        root["labels"][i] = temp 

    root["labels"]["p1"].configure(text=( write_result('percent', 0) ))
    root["labels"]["p2"].configure(text=( write_result('percent', 1) ))
    root["labels"]["p3"].configure(text=( write_result('percent', 2) ))
    root["labels"]["p4"].configure(text=( write_result('percent', 3) ))

    root["labels"]["p1"].place(x=850, y=50, anchor=tk.NE)
    root["labels"]["p2"].place(x=850, y=50+125, anchor=tk.NE)
    root["labels"]["p3"].place(x=850, y=50+125+125, anchor=tk.NE)
    root["labels"]["p4"].place(x=850, y=50+125+125+125, anchor=tk.NE)


    for i in ["t1", "t2", "t3", "t4"]:
        temp = ctk.CTkLabel(
            master=root["window"], 
            text="Option 1", 
            font=("Poppins", 15, "italic"),
            fg_color="transparent",
            text_color="white"
        ) 
        root["labels"][i] = temp 

    root["labels"]["t1"].configure(text= write_result('total_votes', 0) )
    root["labels"]["t2"].configure(text= write_result('total_votes', 1) )
    root["labels"]["t3"].configure(text= write_result('total_votes', 2) )
    root["labels"]["t4"].configure(text= write_result('total_votes', 3) )


    root["labels"]["t1"].place(x=850, y=105, anchor=tk.NE)
    root["labels"]["t2"].place(x=850, y=105+125, anchor=tk.NE)
    root["labels"]["t3"].place(x=850, y=105+125+125, anchor=tk.NE)
    root["labels"]["t4"].place(x=850, y=105+125+125+125, anchor=tk.NE)

    # Bars
    for i in range(0, 5):
        temp = ctk.CTkProgressBar(
            master=root["window"], 
            width=500,
            height=30,
            fg_color='#2c2c2c',
            progress_color='#3d2b41',
            corner_radius=20,
            border_color="#802895",
            border_width=2
        )
        root["bar"][f"bar_{i+1}"] = temp
    
    root["bar"]["bar_1"].set( write_result('bar', 0) )
    root["bar"]["bar_2"].set( write_result('bar', 1) )
    root["bar"]["bar_3"].set( write_result('bar', 2) )
    root["bar"]["bar_4"].set( write_result('bar', 3) )

    # Place progress bars
    root["bar"]["bar_1"].place(relx=0.5, y=100, anchor=tk.N)
    root["bar"]["bar_2"].place(relx=0.5, y=100 + 125, anchor=tk.N)
    root["bar"]["bar_3"].place(relx=0.5, y=100 + 125 + 125, anchor=tk.N)
    root["bar"]["bar_4"].place(relx=0.5, y=100 + 125 + 125 + 125, anchor=tk.N)
    
    # Buttons   
    def btn_fn(btn_type=None):
        if btn_type == 'm_btn':
            frame_visible("front")
            print("yellow")

    for i in ["back_main"]:
        temp = ctk.CTkButton(
            master=root["window"], 
            width=550,
            height=60,
            text="TEXT", 
            font=("Poppins Bold", 25),
            corner_radius=15,
            border_width=3,
            fg_color="#d323ff",
            hover_color="#a81bcc",
            border_color = "#a81bcc"
        )
        root["buttons"][i] = temp

    root["buttons"]["back_main"].configure(
        text="Go to Main Page",
        font=("Poppins Bold", 15),
        width=200,
        height=40, 
        border_width=2,
        fg_color="#212121",
        command=lambda: btn_fn(btn_type = 'm_btn')
    )
    root["buttons"]["back_main"].place(relx=0.5, y=580, anchor=tk.S)


def frame_create():
    root = frames["create"]

    # vars
    # frames["front"]["variables"]["choice var"] = tk.StringVar(value="Default Text")


    # Entries
    for i in ["o1", "o2", "o3", "o4"]:
        temp = ctk.CTkEntry(
        master=root["window"],
        width = 500,
        # height = 100,
        fg_color = "#212121",
        text_color = "white",
        # placeholder_text_color = "#00ccff",
        corner_radius = 20,
        placeholder_text = "Something", 
        font = ("Poppins Medium", 30),
        )
        root["entries"][i] = temp

    root["entries"]["o1"].configure(placeholder_text = "Option1")
    root["entries"]["o2"].configure(placeholder_text = "Option2")
    root["entries"]["o3"].configure(placeholder_text = "Option3")
    root["entries"]["o4"].configure(placeholder_text = "Option4")

    root["entries"]["o1"].place(relx=0.5, y=25, anchor=tk.N)
    root["entries"]["o2"].place(relx=0.5, y=25+100, anchor=tk.N)
    root["entries"]["o3"].place(relx=0.5, y=25+100+100, anchor=tk.N)
    root["entries"]["o4"].place(relx=0.5, y=25+100+100+100, anchor=tk.N)

    # Buttons
    def btn_fn(btn_type=None):
        if btn_type == 'c_btn':
            root["variables"]["o1"] = root["entries"]["o1"].get()
            root["variables"]["o2"] = root["entries"]["o2"].get()
            root["variables"]["o3"] = root["entries"]["o3"].get()
            root["variables"]["o4"] = root["entries"]["o4"].get()

            o1 = root["variables"]["o1"]
            o2 = root["variables"]["o2"]
            o3 = root["variables"]["o3"]
            o4 = root["variables"]["o4"]

            if o1 != "" and o2 != "" and o3 != "" and o4 != "":
                o1 = o1.strip()
                o2 = o2.strip()
                o3 = o3.strip()
                o4 = o4.strip()

                options[0].set(o1) 
                options[1].set(o2) 
                options[2].set(o3)
                options[3].set(o4) 

                root["labels"]["invalid"].place_forget()
                frame_visible("front")
            else:
                print("Invalid")
                root["labels"]["invalid"].place(relx=0.5, y=420, anchor=tk.CENTER)
        elif btn_type == 'm_btn':
            root["labels"]["invalid"].place_forget()
            frame_visible("front")

        root["window"].focus_set()

        root["entries"]["o1"].delete(0, ctk.END)
        root["entries"]["o1"].insert(0, "") 
        root["entries"]["o1"].configure(placeholder_text="Option1")
        root["entries"]["o2"].delete(0, ctk.END)
        root["entries"]["o2"].insert(0, "") 
        root["entries"]["o2"].configure(placeholder_text="Option2")
        root["entries"]["o3"].delete(0, ctk.END)
        root["entries"]["o3"].insert(0, "") 
        root["entries"]["o3"].configure(placeholder_text="Option3")
        root["entries"]["o4"].delete(0, ctk.END)
        root["entries"]["o4"].insert(0, "") 
        root["entries"]["o4"].configure(placeholder_text="Option4")

    for i in ["confirm", "back_main"]:
        temp = ctk.CTkButton(
            master=root["window"], 
            width=550,
            height=60,
            text="TEXT", 
            font=("Poppins Bold", 25),
            corner_radius=15,
            border_width=3,
            fg_color="#d323ff",
            hover_color="#a81bcc",
            border_color = "#a81bcc"
        )
        root["buttons"][i] = temp
    
    frames["front"]["variables"]["choice var"] = tk.StringVar(value="Default Text")

    root["buttons"]["confirm"].configure(
        text="Confirm",
        width=100,
        height=60, 
        command=lambda: btn_fn(btn_type = 'c_btn')
    )
    root["buttons"]["back_main"].configure(
        text="Go to Main Page",
        font=("Poppins Bold", 15),
        width=200,
        height=40, 
        border_width=2,
        fg_color="#212121",
        command=lambda: btn_fn(btn_type = 'm_btn')
    )

    root["buttons"]["confirm"].place(relx=0.5, y=460, anchor=tk.N)
    root["buttons"]["back_main"].place(relx=0.5, y=580, anchor=tk.S) 

    # Labels
    for i in ["invalid"]:
        temp = ctk.CTkLabel(
            master=root["window"], 
            text="EMPTY", 
            font=("Poppins Medium", 20),
            fg_color="transparent",
            text_color="white"
        ) 
        root["labels"][i] = temp 

    root["labels"]["invalid"].configure(
        text="Invalid Input; Try Again", 
        font=("Poppins Medium", 20),
        fg_color="transparent",
        text_color="red"
    ) 
        


app = ctk.CTk()
app.title("Progress Bar Example")

screen_dimensions = (app.winfo_screenwidth(), app.winfo_screenheight())
window_dimensions = (900, 600)
window_coordinations = (
    (screen_dimensions[0] // 2) - (window_dimensions[0] // 2),
    (screen_dimensions[1] // 2) - (window_dimensions[1] // 2)
)
app.geometry(f"{window_dimensions[0]}x{window_dimensions[1]}+{window_coordinations[0]}+{window_coordinations[1]}")
app.resizable(False, False)

frames = {
    "front": {
        "window": None,
        "labels": {},
        "buttons": {},
        "entries": {},
        "bar": {},
        "variables": {}
    },
    "form": {
        "window": None,
        "labels": {},
        "buttons": {},
        "entries": {},
        "bar": {},
        "variables": {}
    },
    "vote": {
        "window": None,
        "labels": {},
        "buttons": {},
        "entries": {},
        "bar": {},
        "variables": {}
    },
    "result": {
        "window": None,
        "labels": {},
        "buttons": {},
        "entries": {},
        "bar": {},
        "variables": {}
    },
    "create": {
        "window": None,
        "labels": {},
        "buttons": {},
        "entries": {},
        "bar": {},
        "variables": {}
    },
}

for i in frames.keys():
    frames[i]["window"] = ctk.CTkFrame(
    app, 
    fg_color="#212121",
    border_width=2,
    border_color="#c720f2"
)

options = [
    ctk.StringVar(value="Option1"), 
    ctk.StringVar(value="Option2"), 
    ctk.StringVar(value="Option3"), 
    ctk.StringVar(value="Option4"), 
]

total = [ctk.IntVar(), ctk.IntVar(), ctk.IntVar(), ctk.IntVar()]
# for i in total:
#     i.set(0)

def update_button_text(*args):
    frames["vote"]["buttons"]["vote_1"].configure(text=options[0].get())
    frames["vote"]["buttons"]["vote_2"].configure(text=options[1].get())
    frames["vote"]["buttons"]["vote_3"].configure(text=options[2].get())
    frames["vote"]["buttons"]["vote_4"].configure(text=options[3].get())

    frames["result"]["labels"]["o1"].configure(text=options[0].get())
    frames["result"]["labels"]["o2"].configure(text=options[1].get())
    frames["result"]["labels"]["o3"].configure(text=options[2].get())
    frames["result"]["labels"]["o4"].configure(text=options[3].get())

def update_total(*args):
    frames["result"]["labels"]["p1"].configure(text=( write_result('percent', 0) ))
    frames["result"]["labels"]["p2"].configure(text=( write_result('percent', 1) ))
    frames["result"]["labels"]["p3"].configure(text=( write_result('percent', 2) ))
    frames["result"]["labels"]["p4"].configure(text=( write_result('percent', 3) ))

    frames["result"]["labels"]["t1"].configure(text= write_result('total_votes', 0) )
    frames["result"]["labels"]["t2"].configure(text= write_result('total_votes', 1) )
    frames["result"]["labels"]["t3"].configure(text= write_result('total_votes', 2) )
    frames["result"]["labels"]["t4"].configure(text= write_result('total_votes', 3) )

    frames["result"]["bar"]["bar_1"].set( write_result('bar', 0) )
    frames["result"]["bar"]["bar_2"].set( write_result('bar', 1) )
    frames["result"]["bar"]["bar_3"].set( write_result('bar', 2) )
    frames["result"]["bar"]["bar_4"].set( write_result('bar', 3) )

    print(f"total0 is {total[0].get()}")
    print(f"total1 is {total[1].get()}")
    print(f"total2 is {total[2].get()}")
    print(f"total3 is {total[3].get()}")

options[0].trace_add("write", update_button_text)
options[1].trace_add("write", update_button_text)
options[2].trace_add("write", update_button_text)
options[3].trace_add("write", update_button_text)

total[0].trace_add("write", update_total)
total[1].trace_add("write", update_total)
total[2].trace_add("write", update_total)
total[3].trace_add("write", update_total)

frame_front()
frame_result()
frame_form()
frame_vote()
frame_create()

frame_visible("front")

app.bind("<Escape>", lambda ev: app.quit())

app.mainloop()


