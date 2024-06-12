from tkinter import *
import tkinter as tk
from sqlite3 import *
from sqlite3 import Error
from tkinter import ttk, messagebox
from os import path

# Function to establish connection to SQLite database
def create_connect(db_path):
    connection = None
    try:
        connection = connect(db_path)
        print("Ühendus on olemas!")  # Connection is established!
    except Error as e:
        print(f"Tekkis viga: {e}")  # Error occurred
    return connection

# Function to execute queries that modify data (CREATE, INSERT, UPDATE, DELETE)
def execute_query(connection, query, params=()):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        print("Tabel on loodud või andmed on sisestatud")  # Table created or data inserted
    except Error as e:
        print(f"Tekkis viga: {e}")  # Error occurred

# Function to execute queries that read data (SELECT)
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Tekkis viga: {e}")  # Error occurred

# SQL queries to create tables if they don't exist
create_autorid_table = """
CREATE TABLE IF NOT EXISTS Autorid(
autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
autor_nimi TEXT NOT NULL,
sünnikuupäev DATE
)
"""

create_zanrid_table = """
CREATE TABLE IF NOT EXISTS Zanrid(
zanr_id INTEGER PRIMARY KEY AUTOINCREMENT,
zanri_nimi TEXT NOT NULL
)
"""

create_raamatud_table = """
CREATE TABLE IF NOT EXISTS Raamatud(
raamat_id INTEGER PRIMARY KEY AUTOINCREMENT,
pealkiri TEXT NOT NULL,
väljaandmise_kuupäev DATE,
autor_id INTEGER,
zanr_id INTEGER,
FOREIGN KEY (autor_id) REFERENCES Autorid (autor_id),
FOREIGN KEY (zanr_id) REFERENCES Zanrid (zanr_id)
)
"""

# SQL queries to insert initial data into tables
insert_autorid = """
INSERT INTO Autorid (autor_nimi, sünnikuupäev)
VALUES 
("Fyodor Dostoevsky", NULL),
("William Shakespeare", NULL),
("Stephen King", NULL),
("Arthur Conan Doyle", NULL)
"""

insert_zanrid = """
INSERT INTO Zanrid (zanri_nimi)
VALUES 
("Lugu"),
("Detektiv"),
("Romaanid"),
("Fantastiline"),
("Horror novels")
"""

insert_raamatud = """
INSERT INTO Raamatud (pealkiri, väljaandmise_kuupäev, autor_id, zanr_id)
VALUES 
("Crime and Punishment", '1866-01-01', 1, 3),
("Brothers Karamazov", '1880-01-01', 1, 3),
("Captain Blood's Odyssey", '1922-01-01', 4, 5),
("The Master and Margarita", '1967-01-01', 2, 2)
"""

# Function to create tables in the database
def create_tables(conn):
    execute_query(conn, create_autorid_table)
    execute_query(conn, create_zanrid_table)
    execute_query(conn, create_raamatud_table)
    messagebox.showinfo("Tabelid on loodud!","Tabelid on loodud!")  # Tables have been created!

# Function to insert initial data into tables
def insert_tables(conn):
    execute_query(conn, insert_autorid)
    execute_query(conn, insert_zanrid)
    execute_query(conn, insert_raamatud)
    messagebox.showinfo("Tabelid on täidetud!","Tabelid on täidetud!")  # Tables have been filled with data!

# Get the absolute path of the current script and construct the database path
filename = path.abspath(__file__)
dbpath = path.join(path.dirname(filename), "data.db")

# Create connection to SQLite database
conn = create_connect(dbpath)

# Tkinter GUI code
aken = tk.Tk()
aken.geometry("1000x1000")
aken.title("Raamatukataloog")
aken.configure(bg="#cfbaf0")

# Function to display authors in a separate window
def table_autorid(conn):
    aken_autorid = tk.Toplevel(aken)
    aken_autorid.title("Autorite tabel")
    tree = ttk.Treeview(aken_autorid, columns=("autor_id", "autor_nimi", "sünnikuupäev"), show="headings")
    tree.column("autor_id", anchor=tk.CENTER)
    tree.heading("autor_id", text="autor_id")
    tree.column("autor_nimi", anchor=tk.CENTER)
    tree.heading("autor_nimi", text="autor_nimi")
    tree.column("sünnikuupäev", anchor=tk.CENTER)
    tree.heading("sünnikuupäev", text="sünnikuupäev")
    try:
        read = execute_read_query(conn, "SELECT * FROM Autorid")
        for row in read:
            tree.insert("", END, values=row)
    except Error as e:
        print("Viga", f"Viga tabelis autorid: {e}")
    tree.pack()
    aken_autorid.mainloop()

# Function to display genres in a separate window
def table_zanr(conn):
    aken_zanr = tk.Toplevel(aken)
    aken_zanr.title("Zanrite tabel")
    tree = ttk.Treeview(aken_zanr, columns=("zanr_id", "zanri_nimi"), show="headings")
    tree.column("zanr_id", anchor=tk.CENTER)
    tree.heading("zanr_id", text="zanr_id")
    tree.column("zanri_nimi", anchor=tk.CENTER)
    tree.heading("zanri_nimi", text="zanri_nimi")
    try:
        read = execute_read_query(conn, "SELECT * FROM Zanrid")
        for row in read:
            tree.insert("", END, values=row) 
    except Error as e:
        print("Viga", f"Viga tabelis zanrid: {e}")
    tree.pack()
    aken_zanr.mainloop()

# Function to display books in a separate window
def table_raamatud(conn):
    aken_raamatud = tk.Toplevel(aken)
    aken_raamatud.title("Raamatute tabel")
    tree = ttk.Treeview(aken_raamatud, columns=("raamat_id", "pealkiri", "väljaandmise_kuupäev", "autor_nimi", "zanri_nimi"), show="headings")
    tree.column("raamat_id", anchor=tk.CENTER)
    tree.heading("raamat_id", text="raamat_id")
    tree.column("pealkiri", anchor=tk.CENTER)
    tree.heading("pealkiri", text="pealkiri")
    tree.column("väljaandmise_kuupäev", anchor=tk.CENTER)
    tree.heading("väljaandmise_kuupäev", text="väljaandmise_kuupäev")
    tree.column("autor_nimi", anchor=tk.CENTER)
    tree.heading("autor_nimi", text="autor_nimi")
    tree.column("zanri_nimi", anchor=tk.CENTER)
    tree.heading("zanri_nimi", text="zanri_nimi")
    try:
        read = execute_read_query(conn, """
            SELECT r.raamat_id, r.pealkiri, r.väljaandmise_kuupäev, a.autor_nimi, z.zanri_nimi
            FROM Raamatud r
            INNER JOIN Autorid a ON r.autor_id = a.autor_id
            INNER JOIN Zanrid z ON r.zanr_id = z.zanr_id
        """)
        for row in read:
            tree.insert("", END, values=row)    
    except Error as e:
        print(f"Viga raamatu tabelis: {e}") 
    tree.pack()
    aken_raamatud.mainloop()

# Function to add a book to the database
def add_raamat(conn, pealkiri, väljaandmise_kuupäev, autor_id, zanr_id):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Raamatud (pealkiri, väljaandmise_kuupäev, autor_id, zanr_id) VALUES (?, ?, ?, ?)",
                       (pealkiri, väljaandmise_kuupäev, autor_id, zanr_id))
        conn.commit()
        messagebox.showinfo("Raamat on lisatud", "Raamat on lisatud")
    except Error as e:
        messagebox.showerror("Viga", f"Viga tabeli sordimisel: {e}")

# Function to open a window to add a book
def add_raamat_aken():
    raamat_andmed_frame = tk.Toplevel(aken)
    raamat_andmed_frame.title("Lisa raamat")
    tk.Label(raamat_andmed_frame, text="Pealkiri:").grid(row=1, column=0)
    pealkiri_entry = tk.Entry(raamat_andmed_frame)
    pealkiri_entry.grid(row=1, column=1)
    tk.Label(raamat_andmed_frame, text="Väljaandmise kuupäev (YYYY-MM-DD):").grid(row=2, column=0)
    väljaandmise_kuupäev_entry = tk.Entry(raamat_andmed_frame)
    väljaandmise_kuupäev_entry.grid(row=2, column=1)
    
    # Fetching author names from database to populate dropdown
    autorid_query = "SELECT autor_id, autor_nimi FROM Autorid"
    autorid_results = execute_read_query(conn, autorid_query)
    autorid_options = {autor[1]: autor[0] for autor in autorid_results}

    tk.Label(raamat_andmed_frame, text="Autor:").grid(row=3, column=0)
    autor_var = tk.StringVar()
    autor_dropdown = tk.OptionMenu(raamat_andmed_frame, autor_var, *autorid_options.keys())
    autor_dropdown.grid(row=3, column=1)

    # Fetching genre names from database to populate dropdown
    zanrid_query = "SELECT zanr_id, zanri_nimi FROM Zanrid"
    zanrid_results = execute_read_query(conn, zanrid_query)
    zanrid_options = {zanr[1]: zanr[0] for zanr in zanrid_results}

    tk.Label(raamat_andmed_frame, text="Žanr:").grid(row=4, column=0)
    zanr_var = tk.StringVar()
    zanr_dropdown = tk.OptionMenu(raamat_andmed_frame, zanr_var, *zanrid_options.keys())
    zanr_dropdown.grid(row=4, column=1)

    def save_raamat():
        pealkiri = pealkiri_entry.get()
        väljaandmise_kuupäev = väljaandmise_kuupäev_entry.get()
        autor_id = autorid_options[autor_var.get()]
        zanr_id = zanrid_options[zanr_var.get()]
        add_raamat(conn, pealkiri, väljaandmise_kuupäev, autor_id, zanr_id)
        raamat_andmed_frame.destroy()

    tk.Button(raamat_andmed_frame, text="Salvesta raamat", command=save_raamat).grid(row=5, columnspan=2)

    raamat_andmed_frame.mainloop()

# Buttons for displaying tables and adding books
Button(aken, text="Näita autoreid", command=lambda: table_autorid(conn)).pack(pady=10)
Button(aken, text="Näita žanreid", command=lambda: table_zanr(conn)).pack(pady=10)
Button(aken, text="Näita raamatuid", command=lambda: table_raamatud(conn)).pack(pady=10)
Button(aken, text="Lisa raamat", command=add_raamat_aken).pack(pady=10)

# Create tables and insert initial data if they don't exist
create_tables(conn)
insert_tables(conn)

# Start Tkinter main loop
aken.mainloop()

