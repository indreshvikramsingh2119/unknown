
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib import colors
from datetime import datetime
import os
import serial.tools.list_ports
import serial
import threading
import time


baud_rates = ["9600", "19200", "38400", "57600", "115200"]
def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

serial_ports = get_serial_ports()

# --- Action Functions ---
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        frame.place_forget()
        canvas.pack_forget()
        show_main_page()

def show_main_page():
    root.geometry("1500x1000")
    main_frame.pack(fill="both", expand=True)

ser = None
running = False
latest_serial_values = ["", "", "", "", "", ""] 
serial_data_history = []

history_table_rows = []
history_table_frame = None



def start_serial():
    global ser, running
    selected_port = port_dropdown.get()
    selected_baud = baud_dropdown.get()

    try:
        ser = serial.Serial(selected_port, int(selected_baud), timeout=1)
        if ser.is_open:
            messagebox.showinfo("Connected", f"\ Connected to {selected_port}")
            running = True
            threading.Thread(target=read_serial_data, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f" Failed to connect:\n{e}")


def stop_serial():
    print("Stopped reading serial data...")

def stop_serial():
    global running
    running = False
    if ser.is_open:
        ser.close()
    messagebox.showinfo("Disconnected", "🔌 Serial connection closed.")



# def show_history_page():
#     main_frame.pack_forget()
#     history_frame.pack(fill="both", expand=True)


# def show_history_page():
#     global history_table_rows, history_table_frame
#     main_frame.pack_forget()
#     print_frame and print_frame.pack_forget()  # Hide print frame if it's active
#     history_frame.pack(fill="both", expand=True)

#     # Clear old table if it exists
#     if history_table_frame:
#         history_table_frame.destroy()
#         history_table_rows.clear()

#     # Create new table frame
#     history_table_frame = tk.Frame(history_frame, bg="white", bd=2, relief="ridge", highlightbackground="#ccc", highlightthickness=1)
#     history_table_frame.pack(padx=100, pady=20, fill="x")

#     # Header row
#     headers = ["[✓]", "Date", "Time", "Initial Temp", "Max Initial Temp", "Net Rise Temp", "Benzoic Acid CV", "Water Eq.", "Calo Val"]
#     for i, h in enumerate(headers):
#         label = tk.Label(history_table_frame, text=h, font=("Segoe UI", 13, "bold"), bg="white", fg="#37474f", anchor="center")
#         label.grid(row=0, column=i, padx=20, pady=12)

#     # Populate rows with data from serial_data_history
#     for row_num, row in enumerate(serial_data_history, start=1):
#         now = datetime.now()
#         date = now.strftime("%Y-%m-%d")
#         time_str = now.strftime("%I:%M %p")
#         full_row = [date, time_str] + row

#         var = tk.BooleanVar()
#         chk = tk.Checkbutton(history_table_frame, variable=var, bg="skyblue")
#         chk.grid(row=row_num, column=0, padx=10)

#         for col_num, value in enumerate(full_row):
#             data_label = tk.Label(history_table_frame, text=value, font=("Segoe UI", 11), bg="white", anchor="center")
#             data_label.grid(row=row_num, column=col_num + 1, padx=15, pady=8)

#         history_table_rows.append((chk, *full_row))




# def show_history_page():
#     global history_table_rows, history_table_frame
#     main_frame.pack_forget()
#     if print_frame:
#         print_frame.pack_forget()
#     history_frame.pack(fill="both", expand=True)

#     # Clear old widgets
#     for widget in history_frame.winfo_children():
#         widget.destroy()
#     history_table_rows.clear()

#     # --- Canvas + Scroll for Table Only ---
#     canvas_frame = tk.Frame(history_frame, bg="white")
#     canvas_frame.pack(fill="both", expand=True, padx=100, pady=(20, 0))

#     canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
#     scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
#     canvas.configure(yscrollcommand=scrollbar.set)

#     scrollbar.pack(side="right", fill="y")
#     canvas.pack(side="left", fill="both", expand=True)

#     scroll_inner_frame = tk.Frame(canvas, bg="white")
#     canvas.create_window((0, 0), window=scroll_inner_frame, anchor="nw")

#     def on_configure(event):
#         canvas.configure(scrollregion=canvas.bbox("all"))
#     scroll_inner_frame.bind("<Configure>", on_configure)

#     # --- Table (white box look) ---
#     history_table_frame = tk.Frame(scroll_inner_frame, bg="white", bd=2, relief="ridge", highlightbackground="#ccc", highlightthickness=1)
#     history_table_frame.pack(fill="x")

#     headers = ["[✓]", "Date", "Time", "Initial Temp", "Max Initial Temp", "Net Rise Temp", "Benzoic Acid CV", "Water Eq.", "Calo Val"]
#     for i, h in enumerate(headers):
#         label = tk.Label(history_table_frame, text=h, font=("Segoe UI", 13, "bold"), bg="white", fg="#37474f", anchor="center")
#         label.grid(row=0, column=i, padx=20, pady=12)

#     for row_num, row in enumerate(serial_data_history, start=1):
#         now = datetime.now()
#         date = now.strftime("%Y-%m-%d")
#         time_str = now.strftime("%I:%M %p")
#         full_row = [date, time_str] + row

#         var = tk.BooleanVar()
#         chk = tk.Checkbutton(history_table_frame, variable=var, bg="skyblue")
#         chk.grid(row=row_num, column=0, padx=10)

#         for col_num, value in enumerate(full_row):
#             data_label = tk.Label(history_table_frame, text=value, font=("Segoe UI", 11), bg="white", anchor="center")
#             data_label.grid(row=row_num, column=col_num + 1, padx=15, pady=8)

#         history_table_rows.append((chk, *full_row))

#     # --- Separator below table ---
#     separator2 = tk.Frame(history_frame, bg="#90caf9", height=2)
#     separator2.pack(fill="x", padx=100, pady=(10, 0))
    
#     btn_frame = tk.Frame(history_frame, bg="#e3f2fd")
#     btn_frame.pack(pady=20)
    
#         # --- PDF Save Function ---
#     def save_selected_rows_as_pdf():
#         selected_data = []
#         for row in history_table_rows:
#             checkbox = row[0]
#             if checkbox.var.get():
#                 selected_data.append(row[1:])  # skip checkbox

#         if not selected_data:
#             messagebox.showinfo("No Selection", "Please select at least one row to save as PDF.")
#             return

#         file_name = f"Selected_History_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#         file_path = os.path.join(os.path.expanduser("~/Downloads"), file_name)

#         c = pdf_canvas.Canvas(file_path, pagesize=A4)
#         width, height = A4
#         y = height - 50

#         c.setFont("Helvetica-Bold", 16)
#         c.drawString(50, y, "Selected History Data")
#         y -= 30

#         c.setFont("Helvetica", 12)
#         col_headers = headers[1:]  # skip checkbox header
#         col_widths = [75] * len(col_headers)  # set equal column width

#         # Draw table header
#         for i, h in enumerate(col_headers):
#             c.drawString(50 + i * 75, y, h)
#         y -= 20

#         # Draw selected rows
#         for row in selected_data:
#             for i, val in enumerate(row):
#                 c.drawString(50 + i * 75, y, str(val))
#             y -= 20
#             if y < 50:
#                 c.showPage()
#                 y = height - 50
#                 c.setFont("Helvetica", 12)

#         c.save()

#         messagebox.showinfo("PDF Saved", f"PDF saved to:\n{file_path}")

#     # --- Save PDF Button ---
#     save_pdf_btn = tk.Button(btn_frame, text="📄 Save as PDF", 
#                              font=("Segoe UI", 12, "bold"), bg="#6a1b9a", fg="white",
#                              command=save_selected_rows_as_pdf, cursor="hand2", bd=0, relief="flat")
#     save_pdf_btn.pack(side="left", padx=10, ipadx=15, ipady=7)

    
    

    # # --- Back to Dashboard Button ---
    # back_btn = tk.Button(history_frame, text="⬅ Back to Dashboard", 
    #                      font=("Segoe UI", 12, "bold"), bg="#4a4e69", fg="white",
    #                      command=back_to_main, cursor="hand2", bd=0, relief="flat")
    # back_btn.pack(pady=20, ipadx=15, ipady=7)





def show_history_page():
    global history_table_rows, history_table_frame
    main_frame.pack_forget()
    if print_frame:
        print_frame.pack_forget()
    history_frame.pack(fill="both", expand=True)

    # Clear old widgets
    for widget in history_frame.winfo_children():
        widget.destroy()
    history_table_rows.clear()

    # --- Canvas + Scroll for Table Only ---
    canvas_frame = tk.Frame(history_frame, bg="white")
    canvas_frame.pack(fill="both", expand=True, padx=100, pady=(20, 0))

    canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scroll_inner_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=scroll_inner_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scroll_inner_frame.bind("<Configure>", on_configure)

    # --- Table ---
    history_table_frame = tk.Frame(scroll_inner_frame, bg="white", bd=2, relief="ridge", highlightbackground="#ccc", highlightthickness=1)
    history_table_frame.pack(fill="x")

    headers = ["[✓]", "Date", "Time", "Initial Temp", "Max Initial Temp", "Net Rise Temp", "Benzoic Acid CV", "Water Eq.", "Calo Val"]
    for i, h in enumerate(headers):
        label = tk.Label(history_table_frame, text=h, font=("Segoe UI", 13, "bold"), bg="white", fg="#37474f", anchor="center")
        label.grid(row=0, column=i, padx=20, pady=12)

    for row_num, row in enumerate(serial_data_history, start=1):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%I:%M %p")
        full_row = [date, time_str] + row

        var = tk.BooleanVar()
        chk = tk.Checkbutton(history_table_frame, variable=var, bg="skyblue")
        chk.var = var  # attach variable for later access
        chk.grid(row=row_num, column=0, padx=10)

        for col_num, value in enumerate(full_row):
            data_label = tk.Label(history_table_frame, text=value, font=("Segoe UI", 11), bg="white", anchor="center")
            data_label.grid(row=row_num, column=col_num + 1, padx=15, pady=8)

        history_table_rows.append((chk, *full_row))

    # --- Separator ---
    separator2 = tk.Frame(history_frame, bg="#90caf9", height=2)
    separator2.pack(fill="x", padx=100, pady=(10, 0))

    # --- Button Frame ---
    btn_frame = tk.Frame(history_frame, bg="#e3f2fd")
    btn_frame.pack(pady=20)

    # --- Save PDF Function ---
    def save_selected_rows_as_pdf():
        selected_data = []
        for row in history_table_rows:
            checkbox = row[0]
            if checkbox.var.get():  # if checkbox is selected
                selected_data.append(row[1:])  # skip checkbox

        if not selected_data:
            messagebox.showinfo("No Selection", "Please select at least one row to save as PDF.")
            return

        file_name = f"Selected_History_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = os.path.join(os.path.expanduser("~/Downloads"), file_name)

        c = pdf_canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y = height - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "( History Data")
        y -= 30

        c.setFont("Helvetica-Bold", 12)
        headers_to_print = ["Date", "Time", "Initial Temp", "Max Initial Temp", "Net Rise Temp", "Benzoic Acid CV", "Water Eq.", "Calo Val"]
        for i, h in enumerate(headers_to_print):
            c.drawString(50 + i * 65, y, h)
        y -= 20

        c.setFont("Helvetica", 11)
        for row in selected_data:
            for i, val in enumerate(row):
                c.drawString(50 + i * 65, y, str(val))
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 11)

        c.save()
        messagebox.showinfo("PDF Saved", f"PDF saved to:\n{file_path}")

    # --- Save Button ---
    save_pdf_btn = tk.Button(btn_frame, text=" print Pdf", font=("Segoe UI", 12, "bold"), bg="#6a1b9a", fg="white",
                             command=save_selected_rows_as_pdf, cursor="hand2", bd=0, relief="flat")
    save_pdf_btn.pack(side="left", padx=10, ipadx=15, ipady=7)

    # --- Back to Dashboard Button ---
    back_btn = tk.Button(btn_frame, text="🔙 ", font=("Segoe UI", 12, "bold"), bg="#0288d1", fg="white",
                         command=back_to_main, cursor="hand2", bd=0, relief="flat")
    back_btn.pack(side="left", padx=10, ipadx=15, ipady=7)


print_frame = None

def show_print_page():
    global print_frame
    main_frame.pack_forget()
    history_frame.pack_forget()

    if print_frame:
        print_frame.destroy()

    print_frame = tk.Frame(root, bg="#f8f9fa")
    print_frame.pack(fill="both", expand=True)

    heading = tk.Label(print_frame, text=" Fill Report Details",
                       font=("Segoe UI", 16, "bold"), bg="#f8f9fa", fg="#1a1a1a")
    heading.pack(pady=(20, 10))

    form = tk.Frame(print_frame, bg="#e8f5e9", bd=2, relief="groove", width=500)
    form.pack(padx=30, pady=20, fill="both", expand=True)
    # form.place(relx=0.5, rely=0.5, anchor="center")


    fields = [
        ("Company Name:", ""),
        ("Company Address:", ""),
        ("Customer ID:", ""),
        ("Mobile No:", ""),
        # ("Initial Temp:", ""),
        # ("Max Initial Temp:", ""),
        # ("Net Rise Temp:", ""),
        # ("Benzioc Acid CV:", ""),
        # ("Water Equivalent:", ""),
        # ("Caloric Value:", ""),
        
        ("Initial Temp:", latest_serial_values[0]),
        ("Max Initial Temp:", latest_serial_values[1]),
        ("Net Rise Temp:", latest_serial_values[2]),
        ("Benzioc Acid CV:", latest_serial_values[3]),
        ("Water Equivalent:", latest_serial_values[4]),
        ("Caloric Value:", latest_serial_values[5]),
        ]
    
    
    
    
    def validate_mobile(P):
     return P == "" or (P.isdigit() and len(P) <= 10)

    
    vcmd = (root.register(validate_mobile), '%P')
    
    
    unit_labels = {
        "Initial Temp:": "°C",
        "Max Initial Temp:": "°C",
        "Net Rise Temp:": "°C",
        "Benzioc Acid CV:": "cal/gram",
        "Water Equivalent:": "cal/°C",
        "Caloric Value:": "cal/gram"
    }
    
        
    entries = {}
    for i, (label_text, default) in enumerate(fields):
        tk.Label(form, text=label_text, font=("Segoe UI", 11, "bold"),
                 bg="white").grid(row=i, column=0, padx=15, pady=8, sticky="e")

        if label_text == "Mobile No:":
            e = tk.Entry(form, font=("Segoe UI", 11), width=30,
                         validate="key", validatecommand=vcmd)
        else:
            e = tk.Entry(form, font=("Segoe UI", 11), width=30)

        e.insert(0, default)
        e.grid(row=i, column=1, padx=15, pady=8, sticky="w")
        entries[label_text] = e
        
        
        unit = unit_labels.get(label_text)
        if unit:
            tk.Label(form, text=unit, font=("Segoe UI", 11,"bold"),
                     bg="white", fg="#555").grid(row=i, column=2, padx=(5, 10), sticky="w")

    
    
    # Button Row
    button_row = tk.Frame(print_frame, bg="#f8f9fa")
    button_row.pack(pady=(10, 20))

    back_btn = tk.Button(button_row, text="⬅ Back", font=("Segoe UI", 12, "bold"),
                         bg="#694a54", fg="white", bd=0, cursor="hand2",
                         command=back_to_main, width=18)
    back_btn.grid(row=0, column=0, padx=10, ipadx=5, ipady=6)

    # -------- PDF REPORT GENERATION -------- #
    def generate_report():
        file_name = f"Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = os.path.join(os.path.expanduser("~/Downloads"), file_name)

        c = pdf_canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y = height - 50

        # === Title Bar ===
        # c.setFillColorRGB(224/255, 247/255, 250/255)  # Light cyan blue
        # c.rect(0, 0, width, height, fill=1)
        c.setFillColorRGB(0.95, 0.95, 0.95)  
        c.rect(0, height -70,width ,30,stroke=0,fill=1)

        # Title Text
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.HexColor("#1a237e"))
        c.drawCentredString(width / 2, y, " PATIENT REPORT")
        y -= 35

        # Line
        c.setStrokeColor(colors.lightgrey)
        c.line(40, y, width - 40, y)
        y -= 20

        # Helper Function
        def draw_section(title, lines):
            nonlocal y
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(colors.HexColor("#3f51b5"))
            c.drawString(50, y, title)
            y -= 20

            c.setFont("Courier", 11)
            c.setFillColor(colors.black)
            for line in lines:
                c.drawString(60, y, line)
                y -= 16
                if y < 50:
                    c.showPage()
                    y = height - 50

        # Content Sections
        draw_section(" Company Details", [
            f"Company Name     : {entries['Company Name:'].get()}",
            f"Company Address  : {entries['Company Address:'].get()}",
            f"Customer ID      : {entries['Customer ID:'].get()}",
            f"Mobile No        : {entries['Mobile No:'].get()}",
        ])

        draw_section(" Temperature Analysis", [
            f"Initial Temp     : {entries['Initial Temp:'].get()} °C",
            f"Max Initial Temp : {entries['Max Initial Temp:'].get()} °C",
            f"Net Rise Temp    : {entries['Net Rise Temp:'].get()} °C",
        ])

        draw_section(" Code Readings", [
            f"Benzoic Acid CV                : {entries['Benzoic Acid CV:'].get()}",
            f"Water Equivalent               : {entries['Water Equivalent:'].get()}",
            f"Caloric Value                : {entries['Caloric Value:'].get()}",
        ])

        # Footer
        y -= 10
        c.setFillColor(colors.gray)
        c.drawString(50, y, "-" * 70)
        y -= 16
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(50, y, "-- End of Report --")

        c.save()
        messagebox.showinfo("PDF Saved", f"Report saved to:\n{file_path}")

    generate_btn = tk.Button(button_row, text=" Generate PDF Report", font=("Segoe UI", 12, "bold"),
                              bg="#1a759f", fg="white", bd=0, cursor="hand2",
                              command=generate_report, width=18)
    generate_btn.grid(row=0, column=1, padx=10, ipadx=5, ipady=6)


def back_to_main():
    global print_frame
    if print_frame:
        print_frame.destroy()
        print_frame = None
    history_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)





# --- Main Window ---
root = tk.Tk()
root.title("Serial Plotter Login")
root.geometry("500x500")
root.configure(bg="#4a4e69")

# ---------------- LOGIN PAGE ----------------
window_width = root.winfo_screenwidth()     
window_height = root.winfo_screenheight()   

# Load and resize image to window
bg_image = Image.open("images/ram.jpg")
bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)  
bg_photo = ImageTk.PhotoImage(bg_image)

# Create canvas and place background image
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")





# Create modern-style login frame on top of canvas
frame = tk.Frame(canvas, bg="white", bd=2, relief="ridge", highlightbackground="#ccc", highlightthickness=2)
frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=300)

heading = tk.Label(frame, text="Serial Data Plotter", font=("Segoe UI", 18, "bold"), bg="white", fg="#22223b")
heading.pack(pady=(20, 10))

username_label = tk.Label(frame, text="Username", font=("Segoe UI", 11,"bold"), bg="white", anchor="w")
username_label.pack(fill="x", padx=40)
# username_entry = tk.Entry(frame, font=("Segoe UI", 11), bd=1, relief=tk.SOLID)
# username_entry.pack(padx=40, pady=(5, 10), ipady=5, fill="x")

username_canvas = tk.Canvas(frame, width=220, height=35, bg="white", bd=0, highlightthickness=0)
username_canvas.pack(padx=40, pady=(5, 10))
username_canvas.create_oval(0, 0, 35, 35, fill="#f0f0f0", outline="#ccc")
username_canvas.create_oval(185, 0, 220, 35, fill="#f0f0f0", outline="#ccc")
username_canvas.create_rectangle(17, 0, 203, 35, fill="#f0f0f0", outline="#ccc")
username_entry = tk.Entry(username_canvas, font=("Segoe UI", 11), bd=0, relief=tk.FLAT, bg="#f0f0f0", highlightthickness=0)
username_entry.place(x=10, y=5, width=200, height=25)

password_label = tk.Label(frame, text="Password", font=("Segoe UI", 11,"bold") ,bg="white", anchor="w")
password_label.pack(fill="x", padx=40)
# password_entry = tk.Entry(frame, font=("Segoe UI", 11), show="*", bd=1, relief=tk.SOLID)
# password_entry.pack(padx=40, pady=(5, 15), ipady=5, fill="x")
password_canvas = tk.Canvas(frame, width=220, height=35, bg="white", bd=0, highlightthickness=0)
password_canvas.pack(padx=40, pady=(5, 15))
password_canvas.create_oval(0, 0, 35, 35, fill="#f0f0f0", outline="#ccc")
password_canvas.create_oval(185, 0, 220, 35, fill="#f0f0f0", outline="#ccc")
password_canvas.create_rectangle(17, 0, 203, 35, fill="#f0f0f0", outline="#ccc")
password_entry = tk.Entry(password_canvas, font=("Segoe UI", 11), show="*", bd=0, relief=tk.FLAT, bg="#f0f0f0", highlightthickness=0)
password_entry.place(x=10, y=5, width=200, height=25)

# login_button = tk.Button(frame, text="Login", font=("Segoe UI", 11, "bold"),
#                          bg="#694a54", fg="white", bd=0, command=login,
#                          cursor="hand2", activebackground="#22223b")
# login_button.pack(pady=(10, 0), ipadx=10, ipady=5)
# --- Rounded Login Button using Canvas ---
def on_login_hover(event):
    login_canvas.itemconfig(login_button_rect, fill="#22223b")

def on_login_leave(event):
    login_canvas.itemconfig(login_button_rect, fill="#694a54")

def on_login_click(event):
    login()

login_canvas = tk.Canvas(frame, width=180, height=40, bg="white", bd=0, highlightthickness=0)
login_canvas.pack(pady=(10, 0))

def create_rounded_rect(canvas, x1, y1, x2, y2, r=20, **kwargs):
    points = [x1+r, y1,
              x2-r, y1,
              x2, y1,
              x2, y1+r,
              x2, y2-r,
              x2, y2,
              x2-r, y2,
              x1+r, y2,
              x1, y2,
              x1, y2-r,
              x1, y1+r,
              x1, y1]
    return canvas.create_polygon(points, smooth=True, **kwargs)

login_button_rect = create_rounded_rect(login_canvas, 0, 0, 180, 40, r=20, fill="#694a54")
login_text = login_canvas.create_text(90, 20, text="Login", fill="white", font=("Segoe UI", 11, "bold"))

login_canvas.bind("<Enter>", on_login_hover)
login_canvas.bind("<Leave>", on_login_leave)
login_canvas.bind("<Button-1>", on_login_click)


# ---------------- MAIN PAGE AFTER LOGIN ----------------
main_frame = tk.Frame(root, bg="#bebebe")
inner_page = tk.Frame(main_frame, bg="#f5f5f5", bd=2, relief="groove")


inner_page.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=700)

main_heading = tk.Label(inner_page, text="Serial Data Monitor", font=("Segoe UI", 22, "bold"), bg="white", fg="#1a1a1a")
main_heading.pack(pady=(40, 20))

# --- Dropdowns ---
dropdown_frame = tk.Frame(inner_page, bg="white")
dropdown_frame.pack(pady=20)

baud_label = tk.Label(dropdown_frame, text="Baud Rate:", font=("Segoe UI", 12), bg="white")
baud_label.pack(side="left", padx=(0, 5))
baud_dropdown = ttk.Combobox(dropdown_frame, values=baud_rates, font=("Segoe UI", 11), state="readonly", width=12)
baud_dropdown.set("9600")
baud_dropdown.pack(side="left", padx=(0, 20))

port_label = tk.Label(dropdown_frame, text="Serial Port:", font=("Segoe UI", 12), bg="white")
port_label.pack(side="left", padx=(0, 5))


port_dropdown = ttk.Combobox(dropdown_frame, values=serial_ports, font=("Segoe UI", 11), state="readonly", width=12)
if serial_ports:
    port_dropdown.set(serial_ports[0])
else:
    port_dropdown.set("No Ports Found")
port_dropdown.pack(side="left")




graph_container = tk.Frame(inner_page, bg="black", width=1500, height=1200, relief="sunken", bd=2)
graph_container.pack(pady=30)

#  DATA TABLE will come here
data_table = tk.Frame(graph_container, bg="black")
data_table.pack(fill="both", expand=True, padx=0, pady=0)

row_widgets = []  # 🔄 For tracking and removing old rows

# Placeholder label (optional, can remove if table is showing)
graph_placeholder = tk.Label(graph_container, fg="white", bg="black", font=("Segoe UI", 11))
graph_placeholder.place(relx=0.5, rely=0.5, anchor="center")






# def update_table(values):
#     row = tk.Frame(data_table, bg="black")
#     row.pack(fill="x", pady=1)

#     for val in values:
#         cell = tk.Label(row, text=val, width=10, fg="white", borderwidth=1,
#                         relief="solid", bg="gray20", font=("Segoe UI", 10))
#         cell.pack(side="left", padx=1)

#     row_widgets.append(row)

#     if len(row_widgets) > 20:
#         oldest = row_widgets.pop(0)
#         oldest.destroy()

# def update_table(values):
#     global current_index

#     row_data = "   ".join(values)

#     if len(table_rows) < max_rows:
#         label = tk.Label(graph_container, text=row_data, fg="white", bg="black", anchor="w", font=("Segoe UI", 11))
#         label.pack(fill="x")
#         table_rows.append(label)
#     else:
#         table_rows[current_index].config(text=row_data)
#         current_index = (current_index + 1) % max_rows  # circular overwrite

def update_table(values):
    global current_index, latest_serial_values
    latest_serial_values = values  
    
    serial_data_history.append(values)


    row_data = "   ".join(values)

    if len(table_rows) < max_rows:
        label = tk.Label(graph_container, text=row_data, fg="white", bg="black", anchor="w", font=("Segoe UI", 11))
        label.pack(fill="x", anchor="w", padx=10, pady=2)
        table_rows.append(label)
    else:
        table_rows[current_index].config(text=row_data)
        current_index = (current_index + 1) % max_rows



table_rows = []        # stores Label rows
max_rows = 10          # max 10 rows visible
current_index = 0      # points to row to overwrite next
graph_placeholder.place(relx=0.5, rely=0.5, anchor="center")


def read_serial_data():
    global ser
    while running:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                values = line.split(',')
                if len(values) == 6:
                    update_table(values)
        except Exception as e:
            print("Serial Read Error:", e)
        time.sleep(0.1)



style = ttk.Style()
style.theme_use('default')

style.configure("Rounded.TButton",
    font=("Segoe UI", 12, "bold"),
    foreground="white",
    background="#4a4e69",  # default background (can override per button)
    padding=10,
    borderwidth=0
)
style.map("Rounded.TButton",
    background=[("active", "#22223b")],
    foreground=[("pressed", "white")],
    relief=[("pressed", "flat")]
)

style.configure("Start.TButton", background="#4361ee")
style.map("Start.TButton", background=[("active", "#364fc7")])

style.configure("Stop.TButton", background="#ef476f")
style.map("Stop.TButton", background=[("active", "#d6336c")])

style.configure("Print.TButton", background="#06d6a0")
style.map("Print.TButton", background=[("active", "#38b000")])

style.configure("History.TButton", background="#adb5bd")
style.map("History.TButton", background=[("active", "#6c757d")])

bottom_button_frame = tk.Frame(inner_page, bg="#f5f5f5")
bottom_button_frame.pack(side="bottom", pady=20)



# Start Button - Indigo Blue
start_btn = ttk.Button(bottom_button_frame, text="Start", style="Rounded.TButton", command=start_serial)
start_btn.pack(side="left", padx=10, ipadx=10, ipady=6)
start_btn.configure(style="Start.TButton")

# Stop Button - Coral Red
stop_btn = ttk.Button(bottom_button_frame, text="Stop", style="Rounded.TButton", command=stop_serial)
stop_btn.pack(side="left", padx=10, ipadx=10, ipady=6)
stop_btn.configure(style="Stop.TButton")

# Print Button - Mint Green
print_btn = ttk.Button(bottom_button_frame, text="Print", style="Rounded.TButton", command=show_print_page)
print_btn.pack(side="left", padx=10, ipadx=10, ipady=6)
print_btn.configure(style="Print.TButton")

# History Button - Soft Gray
history_btn = ttk.Button(bottom_button_frame, text="History", style="Rounded.TButton", command=show_history_page)
history_btn.pack(side="left", padx=10, ipadx=10, ipady=6)
history_btn.configure(style="History.TButton")





# --- History Page ---
history_frame = tk.Frame(root, bg="#e3f2fd")  # soft blue background

# 1. Header Section
history_heading = tk.Label(history_frame, text="📊 History Overview", 
                           font=("Segoe UI", 24, "bold"), bg="#e3f2fd", fg="#0d47a1")
history_heading.pack(pady=(30, 10))

separator1 = tk.Frame(history_frame, bg="#90caf9", height=2)
separator1.pack(fill="x", padx=100)



root.mainloop()
