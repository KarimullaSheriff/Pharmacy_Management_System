from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pymysql
from PIL import Image, ImageTk

# Database Connection
database_Connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Sheriff@1515',
    database='pharmacy_management_system'
)
my_Database = database_Connection.cursor()
print("The Database Has Been Connected Successfully.....")

# Reusable label function
def partLabel(frame, headingText, valueRow, valueColumn):
    name_label = tk.Label(frame, text=headingText, font=('Times New Roman', 15, 'bold'), bg="skyblue")
    name_label.grid(row=valueRow, column=valueColumn, sticky='w', padx=30, pady=15)

# Main Application Function
def pharmacyManagementSystem():
    root = tk.Tk()
    root.title('Pharmacy Management System Software')
    root.geometry('1200x800')

    # Set Background Image And Cover The Window
    try:
        image = Image.open(r"C:\Users\sheri\OneDrive\Desktop\Python_Project\pms.png")
        bg_image = ImageTk.PhotoImage(image)
        bg_label = Label(root, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)
    except:
        print("Error. The Image File Is Not Found. Kindly Check The File Path.")

    # Title Label
    title_label = tk.Label(
        root,
        text='Pharmacy Management System Software',
        font=('Times New Roman', 24, 'bold'),
        bg="navyblue",
        fg="white"
    )
    title_label.place(x=0, y=0, relwidth=1)

    # Frame for Entry Widgets
    frame = tk.Frame(root, bg="navyblue")
    frame.place(x=50, y=100, width=800, height=600)

    # Drug Name
    partLabel(frame, 'Drug Name:', 0, 0)
    drugName_entry = tk.Entry(frame, font=('Times New Roman', 15), width=36, bd=4, relief='solid')
    drugName_entry.grid(row=0, column=1, padx=30, pady=15)

    # Manufacturer
    partLabel(frame, 'Manufacturer:', 1, 0)
    manufacturer_entry = tk.Entry(frame, font=('Times New Roman', 15), width=36, bd=4, relief='solid')
    manufacturer_entry.grid(row=1, column=1, padx=30, pady=15)

    # Category
    partLabel(frame, 'Category:', 2, 0)
    category_entry = tk.Entry(frame, font=('Times New Roman', 15), width=36, bd=4, relief='solid')
    category_entry.grid(row=2, column=1, padx=30, pady=15)

    # Manufacturing Date
    partLabel(frame, 'Manufacturing Date:', 3, 0)
    manufacturingDate_entry = tk.Entry(frame, font=('Times New Roman', 15), width=36, bd=4, relief='solid')
    manufacturingDate_entry.grid(row=3, column=1, padx=30, pady=15)

    # Expiration Date
    partLabel(frame, 'Expiration Date:', 4, 0)
    expirationDate_entry = tk.Entry(frame, font=('Times New Roman', 15), width=36, bd=4, relief='solid')
    expirationDate_entry.grid(row=4, column=1, padx=30, pady=15)

    # Availability Status
    partLabel(frame, 'Availability Status:', 5, 0)
    availabilityStatus_entry = tk.Entry(frame, font=('Times New Roman', 15), width=36, bd=4, relief='solid')
    availabilityStatus_entry.grid(row=5, column=1, padx=30, pady=15)

    # Functions for Buttons
    def delete_record():
        selected_record = record_listbox.curselection()
        if not selected_record:
            messagebox.showwarning('Warning', 'Please Select A Record To Delete.')
            return
        record_name = record_listbox.get(selected_record).split(' - ')[0]
        sqlStatement = f'DELETE FROM pharmacy_system_records WHERE drugname="{record_name}"'
        my_Database.execute(sqlStatement)
        database_Connection.commit()
        messagebox.showinfo("Deleted", "Record Deleted Successfully.")
        update_record_list()

    def add_record():
        drugName = drugName_entry.get().strip()
        manufacturer = manufacturer_entry.get().strip()
        category = category_entry.get().strip()
        manufacturingDate = manufacturingDate_entry.get().strip()
        expirationDate = expirationDate_entry.get().strip()
        availabilityStatus = availabilityStatus_entry.get().strip()
        if not all([drugName, manufacturer, category, manufacturingDate, expirationDate, availabilityStatus]):
            messagebox.showerror("Error", "All Fields Are Required.")
            return
        sqlStatement = "INSERT INTO pharmacy_system_records(drugname, manufacturer, category, manufacturingdate, expirationdate, availabilitystatus) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (drugName, manufacturer, category, manufacturingDate, expirationDate, availabilityStatus)
        my_Database.execute(sqlStatement, values)
        database_Connection.commit()
        messagebox.showinfo("Success", "Record Added Successfully.")
        update_record_list()

    def update_record():
        selected_record = record_listbox.curselection()
        if not selected_record:
            messagebox.showwarning("Warning", "Please Select A Record To Update.")
            return
        # Get the drug name of the selected record
        record_name = record_listbox.get(selected_record).split(' - ')[0]
        # Fetch the updated values from the entry fields
        drugName = drugName_entry.get().strip()
        manufacturer = manufacturer_entry.get().strip()
        category = category_entry.get().strip()
        manufacturingDate = manufacturingDate_entry.get().strip()
        expirationDate = expirationDate_entry.get().strip()
        availabilityStatus = availabilityStatus_entry.get().strip()

        # Ensure all fields are filled
        if not all([drugName, manufacturer, category, manufacturingDate, expirationDate, availabilityStatus]):
            messagebox.showerror("Error", "All Fields Are Required.")
            return
        try:
            # Update the record in the database
            sqlStatement = """
UPDATE pharmacy_system_records
        SET drugname=%s, manufacturer=%s, category=%s, manufacturingdate=%s, expirationdate=%s, availabilitystatus=%s
        WHERE drugname=%s
        """
            values = (drugName, manufacturer, category, manufacturingDate, expirationDate, availabilityStatus, record_name)
            my_Database.execute(sqlStatement, values)
            database_Connection.commit()
            # Show a success message
            messagebox.showinfo("Success", "Record Updated Successfully.")
            # Refresh the listbox to display the updated records
            update_record_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed To Update The Record. Error: {e}")
        
    def on_record_select(event):
        selected_record = record_listbox.curselection()
        if selected_record:
            record_name = record_listbox.get(selected_record).split(' - ')[0]
            sqlStatement = "SELECT * FROM pharmacy_system_records WHERE drugname=%s"
            my_Database.execute(sqlStatement, (record_name,))
            record = my_Database.fetchone()
            if record:
                drugName_entry.delete(0, tk.END)
                drugName_entry.insert(0, record[0])
                manufacturer_entry.delete(0, tk.END)
                manufacturer_entry.insert(0, record[1])
                category_entry.delete(0, tk.END)
                category_entry.insert(0, record[2])
                manufacturingDate_entry.delete(0, tk.END)
                manufacturingDate_entry.insert(0, record[3])
                expirationDate_entry.delete(0, tk.END)
                expirationDate_entry.insert(0, record[4])
                availabilityStatus_entry.delete(0, tk.END)
                availabilityStatus_entry.insert(0, record[5])

    


    def update_record_list():
        record_listbox.delete(0, tk.END)
        my_Database.execute("SELECT * FROM pharmacy_system_records")
        for record in my_Database.fetchall():
            drugname, _, _, _, _, availabilitystatus = record
            record_listbox.insert(tk.END, f"{drugname} - {availabilitystatus}")

    def clear_fields():
        drugName_entry.delete(0, tk.END)
        manufacturer_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        manufacturingDate_entry.delete(0, tk.END)
        expirationDate_entry.delete(0, tk.END)
        availabilityStatus_entry.delete(0, tk.END)

    # Display All Records in Treeview
    def view_all_records():
        all_records_window = tk.Toplevel(root)
        all_records_window.title("All Records")
        all_records_window.geometry("400x400")
        
        tree = ttk.Treeview(all_records_window, columns=("Drug Name", "Manufacturer", "Category", 
                                                         "Manufacturing Date", "Expiration Date", "Availability Status"),
                            show="headings")
        tree.heading("Drug Name", text="Drug Name")
        tree.heading("Manufacturer", text="Manufacturer")
        tree.heading("Category", text="Category")
        tree.heading("Manufacturing Date", text="Manufacturing Date")
        tree.heading("Expiration Date", text="Expiration Date")
        tree.heading("Availability Status", text="Availability Status")

        tree.pack(fill=tk.BOTH, expand=True)

        # Populate the Treeview
        my_Database.execute("SELECT * FROM pharmacy_system_records")
        records = my_Database.fetchall()
        for record in records:
            tree.insert("", tk.END, values=record)

    # Buttons
    tk.Button(frame, text='Add', command=add_record, font=('Times New Roman', 15, 'bold'), bg="blue", fg="white").grid(row=6, columnspan=1, pady=10)
    tk.Button(frame, text='Delete', command=delete_record, font=('Times New Roman', 15, 'bold'), bg="skyblue", fg="white").grid(row=6, columnspan=5, pady=10)
    tk.Button(frame, text='Update', command=update_record, font=('Times New Roman', 15, 'bold'), bg="orange", fg="white").grid(row=7, columnspan=1, pady=10)
    tk.Button(frame, text='Clear', command=clear_fields, font=('Times New Roman', 15, 'bold'), bg="red", fg="white").grid(row=7, columnspan=5, pady=10)
    tk.Button(frame, text='View All', command=view_all_records, font=('Times New Roman', 15, 'bold'), bg="purple", fg="white").grid(row=8, columnspan=3, pady=10)

    # Record Listbox
    record_listbox = tk.Listbox(root, font=("Times New Roman", 15), height=2, width=80, relief="solid", bd=3)
    record_listbox.place(x=45, y=650)
    # Bind the event
    record_listbox.bind("<<ListboxSelect>>", on_record_select)

    update_record_list()
    root.mainloop()

pharmacyManagementSystem()
