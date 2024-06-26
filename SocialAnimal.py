from tkinter import *
from tkinter.font import Font 
from tkinter import filedialog
import pickle
import random

root=Tk()
root.title("Social Animal")
root.geometry("520x520")

label_display=Label(root, text="Social Animal Challenge",font=("American Typewriter", 24))
label_display.pack(pady=20)
#Define our Font
my_font = Font(
    family="American Typewriter",
    size=20,
    weight="bold")

#create frame
my_frame= Frame(root)
my_frame.pack(pady=10)

#create listbox
my_list= Listbox(my_frame,
    font=my_font,
    width=30,
    height=10,
    bg="SystemButtonFace",
    bd=0,
    fg="#464646",
    highlightthickness=0,
    selectbackground="#a6a6a6",
    activestyle="none")

my_list.pack(side=LEFT, fill=BOTH)

#Create default list
stuff=["Smile at a stranger","Say 'hello' to someone","Checkout with a cashier","Sit at at table with strangers","Go out to eat alone","Give someone a compliment","Take a selfie","Volunteer","Go to an event","Have a conversation with a stranger"]
#add default list to list box
for item in stuff:
    my_list.insert(END, item)

#Create scrollbar
my_scrollbar=Scrollbar(my_frame)
my_scrollbar.pack(side=RIGHT, fill=BOTH)

#Add scrollbar
my_list.config(yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_list.yview)

#Create entry box to add items to the list
my_entry= Entry(root, font=("American Typewriter", 24), fg="#000000", width=27, bg="#FFFFFF")
my_entry.pack(pady=20)

#Create a button frame
button_frame= Frame(root)
button_frame.pack(pady=20)

#FUNCTIONS
def delete_item():
    my_list.delete(ANCHOR)

def add_item():
    my_list.insert(END, my_entry.get())
    my_entry.delete(0, END)

accomplished=[]
def cross_off_item():
    #Cross off item
    my_list.itemconfig(
        my_list.curselection(),
        fg="#dedede",)
    #Get rid of selection bar
    my_list.selection_clear(0, END)
    #Add crossed off item to accomplished list
    accomplished.append(my_list.get(ANCHOR))
    #Delete crossed off item
    my_list.delete(ANCHOR)

def choose_random():
    #Choose a random task
    task= random.choice(my_list.get(0, END))
    #Update our entry box with the random task
    label_display["text"]=task
    

def accomplish_window():
    #Create a new window
    accomplishment_window=Toplevel(root)
    accomplishment_window.title("Accomplishments")
    accomplishment_window.geometry("500x500")

    #Create a listbox
    global my_accomplishment_list
    my_accomplishment_list=Listbox(accomplishment_window,
    font=my_font,
    width=30,
    height=10,
    bg="SystemButtonFace",
    bd=0,
    fg="#464646",
    highlightthickness=0,
    selectbackground="#a6a6a6",
    activestyle="none")
    my_accomplishment_list.pack(pady=20)
    
    for item in accomplished:
        my_accomplishment_list.insert(END, item)

def save_list():
    file_name=filedialog.asksaveasfilename(
        initialdir="C:/gui/data",
        title="Save File",
        filetypes=(
            ("Dat Files", "*.dat"),
            ("All Files", "*.*"))
        )
    if file_name:
        if file_name.endswith(".dat"):
            pass
        else:
            file_name=f"{file_name}.dat"
        
        #Delete crossed off items before saving
        count=0
        while count < my_list.size():
            if my_list.itemcget(count, "fg") =="#dedede":
                my_list.delete(my_list.index(count))
            else:
                count += 1
        #Grab all the stuff from the list
        stuff=my_list.get(0, END)

        #Open the file
        output_file=open(file_name, 'wb')

        #Add the stuff to the file
        pickle.dump(stuff, output_file)   
        #Add the accomplished items to the file
        pickle.dump(accomplished, output_file)   

def open_list():
    pass
    file_name=filedialog.askopenfilename(
        initialdir="C:/gui/data",
        title="Open File",
        filetypes=(
            ("Dat Files", "*.dat"),
            ("All Files", "*.*"))
    )
    if file_name:
        #Delete currently open list
        my_list.delete(0, END)

        #Open the file
        input_file=open(file_name, 'rb')

        #Load the data from the file
        stuff=pickle.load(input_file)
        #Load the data from the file
        accomplished=pickle.load(input_file)

        #Output stuff to the screen
        for item in stuff:
            my_list.insert(END, item)
        #Output accomplished to the screen
        for item in accomplished:
            my_accomplishment_list.insert(END, item)

def delete_list():
    my_list.delete(0, END)
    my_accomplishment_list.delete(0, END)


#create menu
my_menu=Menu(root)
root.config(menu=my_menu)

#Add items to the menu
file_menu=Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
#Add dropdown items
file_menu.add_command(label="Save List", command=save_list)
file_menu.add_command(label="Open List", command=open_list)
file_menu.add_separator()
file_menu.add_command(label="Clear List", command=delete_list)



#Add some buttons
delete_button=Button(button_frame, text="Delete Item",command=delete_item)
add_button=Button(button_frame, text="Add Item",command=add_item)
cross_off_button=Button(button_frame, text="Cross Off",command=cross_off_item)
accomp_button=Button(button_frame, text="Accomplishments",command=accomplish_window)
random_button=Button(button_frame, text="Random",command=choose_random)

accomp_button.grid(row=0, column=1)
delete_button.grid(row=0, column=2)
add_button.grid(row=0, column=3)
cross_off_button.grid(row=0, column=4)
random_button.grid(row=0, column=5)

root.mainloop()