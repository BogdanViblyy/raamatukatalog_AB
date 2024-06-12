from tkinter import * 
import tkinter as tk
from sqlite3 import *
from sqlite3 import Error
from tkinter import ttk, messagebox
from os import path

def create_connect(db_path):
    connection = None
    try:
        connection = connect(db_path)
        print("Ühendus on olemas!")
    except Error as e:
                print(f"Tekkis viga: {e}")
    return connection

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Tabel on loodud või andmed on sisestatud")
    except Error as e:
        print(f"Tekkis viga: {e}")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Tekkis viga: {e}")


create_autorid_table = """
CREATE TABLE IF NOT EXISTS Autorid(
autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
autor_nimi TEXT NOT NULL
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
autor_id INTEGER,
zanr_id INTEGER,
FOREIGN KEY (autor_id) REFERENCES Autorid (autor_id),
FOREIGN KEY (zanr_id) REFERENCES Zanrid (zanr_id)
)
"""


insert_autorid = """
INSERT INTO Autorid (autor_nimi, sünnikuupäev)
VALUES 
("Fyodor Dostoevsky"),
("William Shakespeare"),
("Stephen King"),
("Arthur Conan Doyle")
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
(),
("Crime and punishment", 1, 3),
("Brothers karamazov, 1, 3),
("Kapten Bloodi odüsseia", "2023-07-23", 4, 5),
("Meister ja Margarita", "2024-02-12", 5, 2)
"""


def create_tables(conn):
    execute_query(conn, create_autorid_table)
    execute_query(conn, create_zanrid_table)
    execute_query(conn, create_raamatud_table)
    messagebox.showinfo("Tabelid on loodud!","Tabelid on loodud!")


def insert_tables(conn):
    execute_query(conn, insert_autorid)
    execute_query(conn, insert_zanrid)
    execute_query(conn, insert_raamatud)
    messagebox.showinfo("Tabelid on täidetud!","Tabelid on täidetud!")


filename = path.abspath(__file__)
dbdir=filename.rstrip('Andmebaasi_haldamine_raamatukataloogis2.py')
dbpath = path.join(dbdir, "data.db")
conn = create_connect(dbpath)


aken =tk.Tk()
aken.geometry("1000x1000")
aken.title("Raamatukataloog")
aken.configure(bg="#cfbaf0")


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


def add_raamat(conn, pealkiri, väljaandmise_kuupäev, autor_id, zanr_id):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Raamatud (pealkiri, väljaandmise_kuupäev, autor_id, zanr_id) VALUES (?, ?, ?, ?)",
                       (pealkiri, väljaandmise_kuupäev, autor_id, zanr_id))
        conn.commit()
        messagebox.showinfo("Raamat on lisatud", "Raamat on lisatud")
    except Error as e:
        messagebox.showerror("Viga", f"Viga tabeli sordimisel: {e}")


def add_raamat_aken():
    raamat_andmed_frame = tk.Toplevel(aken)
    raamat_andmed_frame.title("Lisa raamat")
    tk.Label(raamat_andmed_frame, text="Pealkiri:").grid(row=1, column=0)
    pealkiri_entry = tk.Entry(raamat_andmed_frame)
    pealkiri_entry.grid(row=1, column=1)
    tk.Label(raamat_andmed_frame, text="Väljaandmise kuupäev:").grid(row=2, column=0)
    väljaandmise_kuupäev_entry = tk.Entry(raamat_andmed_frame)
    väljaandmise_kuupäev_entry.grid(row=2, column=1)
    tk.Label(raamat_andmed_frame, text="Autor:").grid(row=3, column=0)
    autor_andmed = execute_read_query(conn, "SELECT autor_id, autor_nimi FROM Autorid")
    autor_ids = [row[0] for row in autor_andmed]
    autor_names = [row[1] for row in autor_andmed]
    valitud_autor_id = tk.StringVar()
    autor_id_combobox = ttk.Combobox(raamat_andmed_frame, textvariable=valitud_autor_id)
    autor_id_combobox['values'] = autor_names
    autor_id_combobox.grid(row=3, column=1)
    tk.Label(raamat_andmed_frame, text="Zanr:").grid(row=4, column=0)
    zanr_andmed = execute_read_query(conn, "SELECT zanr_id, zanri_nimi FROM Zanrid")
    zanr_ids = [row[0] for row in zanr_andmed]
    zanr_names = [row[1] for row in zanr_andmed]
    valitud_zanr_id = tk.StringVar()
    zanr_id_combobox = ttk.Combobox(raamat_andmed_frame, textvariable=valitud_zanr_id)
    zanr_id_combobox['values'] = zanr_names
    zanr_id_combobox.grid(row=4, column=1)

    def add_raamat_close():
        pealkiri = pealkiri_entry.get()
        väljaandmise_kuupäev = väljaandmise_kuupäev_entry.get()
        autor_id = autor_ids[autor_names.index(valitud_autor_id.get())]
        zanr_id = zanr_ids[zanr_names.index(valitud_zanr_id.get())]
        add_raamat(conn, pealkiri, väljaandmise_kuupäev, autor_id, zanr_id)
        raamat_andmed_frame.destroy()
    tk.Button(raamat_andmed_frame, text="Lisa raamat", command=add_raamat_close).grid(row=5, columnspan=2)


def add_zanr(conn, zanri_nimi):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Zanrid (zanri_nimi) VALUES (?)", (zanri_nimi,))
        conn.commit()
        messagebox.showinfo("Zanr on lisatud","Zanr on lisatud")
    except Error as e:
        messagebox.showerror("Viga", f"Viga {e}") 


def add_autor(conn, autor_nimi, sünnikuupäev):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Autorid (autor_nimi, sünnikuupäev) VALUES (?, ?)", (autor_nimi, sünnikuupäev))
        conn.commit()
        messagebox.showinfo("Autor on lisatud","Autor on lisatud")
    except Error as e:
        messagebox.showerror("Viga", f"Viga {e}")


def delete_raamat_autor_nimi(conn, autor_nimi):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Raamatud WHERE autor_id = (SELECT autor_id FROM Autorid WHERE autor_nimi = ?)", (autor_nimi,))
        conn.commit()
        messagebox.showinfo("Autor nimi raamatud on kustutatud","Autor nimi raamatud on kustutatud")
    except Error as e:
        messagebox.showerror("Viga", f"Viga {e}")

def delete_raamat_autor_nimi_aken():
    raamat_kustuta_autor_frame = tk.Toplevel(aken)
    raamat_kustuta_autor_frame.title("Raamatute kustutamine autori nime järgi")
    tk.Label(raamat_kustuta_autor_frame, text="Autor_nimi:").grid(row=1, column=0)
    autor_andmed = execute_read_query(conn, "SELECT autor_nimi FROM Autorid")
    autor_names = [row[0] for row in autor_andmed]
    valitud_autor_nimi = tk.StringVar()
    autor_nimi_combobox = ttk.Combobox(raamat_kustuta_autor_frame, textvariable=valitud_autor_nimi)
    autor_nimi_combobox['values'] = autor_names
    autor_nimi_combobox.grid(row=1, column=1)

    def delete_raamat_autor_nimi_close():
        delete_raamat_autor_nimi(conn, valitud_autor_nimi.get())
        raamat_kustuta_autor_frame.destroy()

    tk.Button(raamat_kustuta_autor_frame, text="Kustuta", command=delete_raamat_autor_nimi_close).grid(row=2, columnspan=2)

def delete_raamat_pealkiri(conn, pealkiri):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Raamatud WHERE pealkiri = ?", (pealkiri,))
        conn.commit()
        messagebox.showinfo("Pealkiri raamatud on kustutatud","Pealkiri raamatud on kustutatud")
    except Error as e:
        messagebox.showerror("Viga", f"Viga {e}")

def delete_raamat_pealkiri_aken():
    raamat_kustuta_pealkiri_frame = tk.Toplevel(aken)
    raamat_kustuta_pealkiri_frame.title("Pealkirjaraamatute kustutamine ")
    tk.Label(raamat_kustuta_pealkiri_frame, text="Pealkiri: ").grid(row=1, column=0)
    pealkiri_entry = tk.Entry(raamat_kustuta_pealkiri_frame)
    pealkiri_entry.grid(row=1, column=1)

    def delete_raamat_pealkiri_close():
        delete_raamat_pealkiri(conn, pealkiri_entry.get())
        raamat_kustuta_pealkiri_frame.destroy()

    tk.Button(raamat_kustuta_pealkiri_frame, text="Kustuta", command=delete_raamat_pealkiri_close).grid(row=2, columnspan=2)



def add_autor_aken():
    autor_andmed_frame = tk.Toplevel(aken)
    autor_andmed_frame.title("Autorite lisamine") 
    tk.Label(autor_andmed_frame, text="Autor nimi:").grid(row=1, column=0)
    autor_nimi_entry = tk.Entry(autor_andmed_frame)
    autor_nimi_entry.grid(row=1, column=1)
    tk.Label(autor_andmed_frame, text="Sünnikuupäev: ").grid(row=2, column=0)
    sünnikuupäev_entry = tk.Entry(autor_andmed_frame)
    sünnikuupäev_entry.grid(row=2, column=1)

    def add_autor_close():
        autor_nimi = autor_nimi_entry.get()
        sünnikuupäev = sünnikuupäev_entry.get()
        add_autor(conn, autor_nimi, sünnikuupäev)
        autor_andmed_frame.destroy()

    tk.Button(autor_andmed_frame, text="Autor lisatud", command=add_autor_close).grid(row=3, columnspan=2)



def add_zanr_aken():
    zanr_andmed_frame = tk.Toplevel(aken)
    zanr_andmed_frame.title("Zanrite lisamine")
    tk.Label(zanr_andmed_frame, text="Zanri_nimi: ").grid(row=1, column=0)
    zanri_nimi_entry = tk.Entry(zanr_andmed_frame)
    zanri_nimi_entry.grid(row=1, column=1)

    def add_zanr_close():
        zanri_nimi = zanri_nimi_entry.get()
        add_zanr(conn, zanri_nimi)
        zanr_andmed_frame.destroy()

    tk.Button(zanr_andmed_frame, text="Lisa zanr", command=add_zanr_close).grid(row=2, columnspan=2)

def drop_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Autorid")
        cursor.execute("DROP TABLE IF EXISTS Zanrid")
        cursor.execute("DROP TABLE IF EXISTS Raamatud")
        conn.commit()
        messagebox.showinfo("Viga", "Tabelid on kustutatud!")
    except Error as e:
        messagebox.showerror("Viga", f"Tekkis väga: {e}")

btn_drop_tables = tk.Button(aken,
                            text="Tabeli kustutamine",
                            bg="#ffc4d6",
                            fg="#d1495b",
                            font=("Forte 25"),
                            width=30,
                            command=lambda: drop_tables(conn))
btn_drop_tables.pack()

btn_create_tables = tk.Button(aken,
                              text="Tabelite loomine",
                              bg="#8eecf5",
                              fg="#27187e",
                              font=("Forte 25"),
                              width=25,
                              command=lambda: create_tables(conn))
btn_create_tables.pack()

btn_insert_data = tk.Button(aken,
                            text="Tabeli täitmine",
                            bg="#8eecf5",
                            fg="#27187e",
                            font=("Forte 25"),
                            width=25,
                            command=lambda: insert_tables(conn))
btn_insert_data.pack()

btn_autorid = tk.Button(aken,
                        text="Autorite tabel",
                        bg="#fbf8cc",
                        fg="#ff7d00",
                        font=("Forte 25"),
                        width=22,
                        command=lambda: table_autorid(conn))
btn_autorid.pack()

btn_zanrid = tk.Button(aken,
                       text="Zanrite tabel",
                       bg="#fbf8cc",
                       fg="#ff7d00",
                       font=("Forte 25"),
                       width=22,
                       command=lambda: table_zanr(conn))
btn_zanrid.pack()

btn_raamatud = tk.Button(aken,
                         text="Raamatute tabel",
                         bg="#fbf8cc",
                         fg="#ff7d00",
                         font=("Forte 25"),
                         width=22,
                         command=lambda: table_raamatud(conn))
btn_raamatud.pack()

btn_add_autor = tk.Button(aken,
                          text="Autoride lisamine",
                          bg="#b9fbc0",
                          fg="#0a9396",
                          font=("Forte 25"),
                          width=20,
                          command=add_autor_aken)
btn_add_autor.pack()

btn_add_zanr = tk.Button(aken,
                         text="Žanrite lisamine",
                         bg="#b9fbc0",
                         fg="#0a9396",
                         font=("Forte 25"),
                         width=20,
                         command=add_zanr_aken)
btn_add_zanr.pack()

btn_add_raamat = tk.Button(aken,
                           text="Raamatute lisamine",
                           bg="#b9fbc0",
                           fg="#0a9396",
                           font=("Forte 25"),
                           width=20,
                           command=add_raamat_aken)
btn_add_raamat.pack()

btn_delete_raamat_autor_nimi = tk.Button(aken,
                                    text="Raamatute kustutamine autori nime järgi",
                                    bg="#f7d1cd",
                                    fg="#b56576",
                                    font=("Forte 25"),
                                    width=38,
                                    command=delete_raamat_autor_nimi_aken)
btn_delete_raamat_autor_nimi.pack()

btn_delete_raamat_pealkiri = tk.Button(aken,
                                       text="Pealkirjaraamatute kustutamine",
                                       bg="#f7d1cd",
                                       fg="#b56576",
                                       font=("Forte 25"),
                                       width=35,
                                       command=delete_raamat_pealkiri_aken)
btn_delete_raamat_pealkiri.pack()



aken.mainloop()
