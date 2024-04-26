import tkinter as tk
from tkinter import messagebox
import ctypes
from tkinter import PhotoImage
import hamming_code
from tkinter import filedialog
from tkinter import scrolledtext


encoded_result = None


def_values_m1 = -1
check1 = 0
check2 = 0
encode_page_open = False  
encode_page = None  
decode_page_open = False
decode_page = None

decode_page1_open = False
decode_page1 = None
error_page_open = False
error_page = None
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def open_encode_page():
    global encode_page, encode_page_open
    encode_page = tk.Toplevel(root)
    encode_page.title("Encode Page")
    encode_page.geometry("400x150")
    center_window(encode_page, 700, 300)
    encode_page_open = True  
    canvas = tk.Canvas(encode_page)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(encode_page, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)



    def encode_message():
        message = encode_entry.get()

        if extra_bit_var.get() == 1:
            encoded_message = hamming_code.encoder(message, extra_bit=1)
            check = True
        else:
            encoded_message = hamming_code.encoder(message, extra_bit=False)
            check = False
        encoded_result.config(text="Encoded Message: "+encoded_message)

        if(error_page_open):
            error_entry.delete(0, 'end')
            error_entry.insert(0 , encoded_message)
        if (decode_page_open):
            decode_entry.delete(0, 'end')
            decode_entry.insert(0,encoded_message)
        global def_values_m1
        def_values_m1 = encoded_message
    extra_bit_var = tk.IntVar()
    extra_bit_var.set(1)

    include_extra_bit = tk.Radiobutton(frame, text="Include extra bit", variable=extra_bit_var, value=1, height=2, width=35, font=("Helvetica", 12))
    include_extra_bit.grid(row=0, column=0)

    dont_include_extra_bit = tk.Radiobutton(frame, text="Don't include extra bit", variable=extra_bit_var, value=0, height=2, width=35, font=("Helvetica", 12))
    dont_include_extra_bit.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame, text="Enter input message or upload text file:", font=("Helvetica", 12)).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    global encode_entry
    encode_entry = tk.Entry(frame, font=("Helvetica", 12))
    encode_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10)



    def upload_file():
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'r') as file:
                content = file.read()
                content = content.replace('\n' , '')
                encode_entry.delete(0, tk.END)
                encode_entry.insert(0, content)

    # Create Button to upload file
    upload_button = tk.Button(frame, text="Upload File", command=upload_file)
    upload_button.grid(row = 2,column=1, padx=5, pady=10)

    encode_button = tk.Button(frame, text="Encode", command=encode_message, width=20, height=2, font=("Helvetica", 12))
    encode_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    global encoded_result
    encoded_result = tk.Label(frame, text="", font=("Helvetica", 12), wraplength=350)
    encoded_result.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)
    encode_page.protocol("WM_DELETE_WINDOW", close_encode_page)

def close_encode_page():
    global encode_page_open
    encode_page_open = False
    encode_page.destroy()


def error_simulation():
    global error_page, error_page_open
    error_page = tk.Toplevel(root)
    error_page.title("Error generator Page")
    error_page.geometry("400x150")
    center_window(error_page, 700, 300)
    error_page_open = True
    def error_message():
        message = error_entry.get()
        error_simulation_result = hamming_code.error_simulation(message)
        # print(error_simulation_result)
        error_result.config(text="After Error Simulation Message: "+error_simulation_result,fg="red")
        if (decode_page_open):
            decode_entry.delete(0, 'end')
            decode_entry.insert(0,error_simulation_result)

    tk.Label(error_page, text="Enter input message:", font=("Helvetica", 12)).grid(row=1, column=0, columnspan=2, padx=100, pady=10)


    global error_entry
    error_entry = tk.Entry(error_page, font=("Helvetica", 12))
    error_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    if (def_values_m1 != -1 ):
        error_entry.delete(0, 'end')
        error_entry.insert(0, def_values_m1)
    def upload_file():
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'r') as file:
                content = file.read()
                content = content.replace('\n' , '')
                error_entry.delete(0, tk.END)
                error_entry.insert(0, content)
    upload_button1 = tk.Button(error_page, text="Upload File", command=upload_file)
    upload_button1.grid(row = 2,column=2, padx=5, pady=10)
    error_sim_button = tk.Button(error_page, text="Generate Error", command=error_message, width=20, height=2, font=("Helvetica", 12))
    error_sim_button.grid(row=3, column=0, columnspan=2, padx=100, pady=10)

    global error_result
    error_result = tk.Label(error_page, text="", font=("Helvetica", 12), wraplength=350)
    error_result.grid(row=4, column=0, columnspan=2, padx=100, pady=10)

    error_page.protocol("WM_DELETE_WINDOW", close_error_page)

def close_error_page():

    global error_page_open
    error_page_open = False
    error_page.destroy()

def open_decode_page():
    global decode_page, decode_page_open
    decode_page = tk.Toplevel(root)
    decode_page.title("decode Page")
    decode_page.geometry("400x150")
    center_window(decode_page, 700, 400)
    decode_page_open = True
    canvas = tk.Canvas(decode_page)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(decode_page, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)
    def decode_message():
        message = decode_entry.get()
        if extra_bit_var.get() == 1:
            decoded_message = hamming_code.decoder(message, extra_bit=1)


        else:
            decoded_message = hamming_code.decoder(message, extra_bit=False)
            check = False
        error = 1
        # print(decoded_message)
        if (decoded_message[1] == 0) :
            error =0
            decoded_result1.config(text="No error",fg="green")
            decoded_result.config(text="Decoded Message: "+decoded_message[0],fg="green", wraplength=350)
        if (error == 1) :
            decoded_result.config(text="error detected",fg="red")
            if (decoded_message[1] == 1) :
                decoded_result1.config(text="Single bit error at index : " + str(decoded_message[2]),fg="red")
                decoded_result.config(text="correct decoded Message: "+decoded_message[0],fg="green", wraplength=350)
            else:
                decoded_result1.config(text="")
                decoded_result.config(text=""+ decoded_message[0], wraplength=350)


    def save_to_file(decoded_message):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w') as file:
                file.write(decoded_message)

    extra_bit_var = tk.IntVar()
    extra_bit_var.set(1)

    include_extra_bit = tk.Radiobutton(frame, text="Include extra bit", variable=extra_bit_var, value=1, height=2, width=35, font=("Helvetica", 12))
    include_extra_bit.grid(row=0, column=0)

    dont_include_extra_bit = tk.Radiobutton(frame, text="Don't include extra bit", variable=extra_bit_var, value=0, height=2, width=35, font=("Helvetica", 12))
    dont_include_extra_bit.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame, text="Enter input message:", font=("Helvetica", 12)).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    global decode_entry
    decode_entry = tk.Entry(frame, font=("Helvetica", 12))
    decode_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    if (def_values_m1 != -1 ):
        decode_entry.delete(0, 'end')
        decode_entry.insert(0, def_values_m1)
    def upload_file():
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'r') as file:
                content = file.read()
                # Display only the first line of the file content in the Entry widget
                content = content.replace('\n' , '')
                decode_entry.delete(0, tk.END)
                decode_entry.insert(0, content)
    # Create Button to upload file
    upload_button1 = tk.Button(frame, text="Upload File", command=upload_file)
    upload_button1.grid(row = 2,column=1, padx=5, pady=10)
    decode_button = tk.Button(frame, text="decode", command=decode_message, width=20, height=2, font=("Helvetica", 12))
    decode_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    global decoded_result
    decoded_result = tk.Label(frame, text="", font=("Helvetica", 12))
    decoded_result.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    global decoded_result1
    decoded_result1 = tk.Label(frame, text="", font=("Helvetica", 12), wraplength=350)
    decoded_result1.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    save_button = tk.Button(frame, text="Save Decoded Message", command=lambda: save_to_file(decoded_result.cget("text")), width=20, height=2, font=("Helvetica", 12))
    save_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)
    decode_page.protocol("WM_DELETE_WINDOW", close_decode_page)


def close_decode_page():

    global decode_page_open
    decode_page_open = False
    decode_page.destroy()

root = tk.Tk()
root.title("Hamming Code Encoder/Decoder")
root.geometry("400x200")
center_window(root, 700, 500)
root.configure(bg="lightblue")  



tk.Label(root, text="Hamming Code Encoder/Decoder", font=("Helvetica", 21), bg="lightblue").pack(pady=30)

encode_button = tk.Button(root, text="Encode", command=open_encode_page, width=20, height=3, font=("Helvetica", 12), bg="#f7723d", fg="black")
encode_button.pack(pady=10)

error_simulator = tk.Button(root, text="Error Simulation", command=error_simulation, width=20, height=3, font=("Helvetica", 12), bg="yellow", fg="black")
error_simulator.pack(pady=10)

decode_button = tk.Button(root, text="Decode", command=open_decode_page, width=20, height=3, font=("Helvetica", 12), bg="#53f424", fg="black")
decode_button.pack(pady=10)

root.mainloop()
