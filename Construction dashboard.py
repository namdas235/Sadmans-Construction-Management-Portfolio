#Construction dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import openpyxl
import os

class ConstructionDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("[Your Name]'s Construction Project Dashboard")  # Personalize with your name
        self.root.geometry("900x700")
        self.root.configure(bg="#d4e4d4")  # Custom green shade
        
        # Data storage
        self.materials = []
        self.tasks = []
        
        # Setup GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Title Label
        ttk.Label(self.root, text="Developed by [Your Name] for WSU CM", font=("Helvetica", 16, "bold"), 
                 background="#d4e4d4").pack(pady=10)  # Personal welcome
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill="both")
        
        # Cost Estimation Tab
        self.cost_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.cost_frame, text="Cost Estimation")
        
        ttk.Label(self.cost_frame, text="Material:").grid(row=0, column=0, padx=5, pady=5)
        self.material_var = tk.StringVar()
        self.material_dropdown = ttk.Combobox(self.cost_frame, textvariable=self.material_var, 
                                            values=["Concrete", "Timber", "Bricks", "Steel"])
        self.material_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.cost_frame, text="Quantity (units):").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(self.cost_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.cost_frame, text="Rate ($/unit):").grid(row=2, column=0, padx=5, pady=5)
        self.rate_entry = ttk.Entry(self.cost_frame)
        self.rate_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(self.cost_frame, text="Add Cost", command=self.add_cost).grid(row=3, column=0, columnspan=2, pady=10)
        
        self.cost_tree = ttk.Treeview(self.cost_frame, columns=("Material", "Quantity", "Rate", "Cost"), show="headings")
        self.cost_tree.heading("Material", text="Material")
        self.cost_tree.heading("Quantity", text="Quantity")
        self.cost_tree.heading("Rate", text="Rate ($)")
        self.cost_tree.heading("Cost", text="Cost ($)")
        self.cost_tree.column("Material", width=150)
        self.cost_tree.column("Quantity", width=100)
        self.cost_tree.column("Rate", width=100)
        self.cost_tree.column("Cost", width=100)
        self.cost_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Inventory Tab
        self.inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_frame, text="Inventory Tracker")
        
        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=("Material", "Quantity", "Status"), show="headings")
        self.inventory_tree.heading("Material", text="Material")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.heading("Status", text="Status")
        self.inventory_tree.column("Material", width=150)
        self.inventory_tree.column("Quantity", width=100)
        self.inventory_tree.column("Status", width=100)
        self.inventory_tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        ttk.Button(self.inventory_frame, text="Update Inventory", command=self.update_inventory).grid(row=1, column=0, pady=10)
        
        # Schedule Tab
        self.schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.schedule_frame, text="Project Schedule")
        
        ttk.Label(self.schedule_frame, text="Task:").grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = ttk.Entry(self.schedule_frame)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.schedule_frame, text="Start Day:").grid(row=1, column=0, padx=5, pady=5)
        self.start_entry = ttk.Entry(self.schedule_frame)
        self.start_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.schedule_frame, text="Duration (days):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = ttk.Entry(self.schedule_frame)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(self.schedule_frame, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.schedule_frame)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        # Export Button
        ttk.Button(self.root, text="Export to Excel", command=self.export_to_excel, 
                  style="TButton").pack(pady=10)
    
    def add_cost(self):
        try:
            material = self.material_var.get()
            if not material:
                raise ValueError("Please select a material!")
            quantity = float(self.quantity_entry.get() or 0)
            rate = float(self.rate_entry.get() or 0)
            if quantity <= 0 or rate <= 0:
                raise ValueError("Quantity and rate must be positive!")
            
            cost = quantity * rate
            self.materials.append({"Material": material, "Quantity": quantity, "Rate": rate, "Cost": cost})
            self.cost_tree.insert("", "end", values=(material, f"{quantity:.2f}", f"{rate:.2f}", f"{cost:.2f}"))
            
            self.quantity_entry.delete(0, tk.END)
            self.rate_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def update_inventory(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        if not self.materials:
            messagebox.showinfo("Info", "No materials added yet!")
            return
        
        df = pd.DataFrame(self.materials)
        inventory = df.groupby("Material")["Quantity"].sum().reset_index()
        for _, row in inventory.iterrows():
            status = "Low" if row["Quantity"] < 100 else "Sufficient"
            self.inventory_tree.insert("", "end", values=(row["Material"], f"{row['Quantity']:.2f}", status))
    
    def add_task(self):
        try:
            task = self.task_entry.get()
            if not task:
                raise ValueError("Please enter a task!")
            start = float(self.start_entry.get() or 0)
            duration = float(self.duration_entry.get() or 0)
            if start < 0 or duration <= 0:
                raise ValueError("Start day must be non-negative and duration must be positive!")
            
            self.tasks.append({"Task": task, "Start_Day": start, "Duration": duration})
            self.plot_schedule()
            
            self.task_entry.delete(0, tk.END)
            self.start_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def plot_schedule(self):
        self.ax.clear()
        if self.tasks:
            df = pd.DataFrame(self.tasks)
            df["End_Day"] = df["Start_Day"] + df["Duration"]
            for i, task in df.iterrows():
                self.ax.barh(task["Task"], task["Duration"], left=task["Start_Day"], color="#4682b4")
            self.ax.set_xlabel("Days")
            self.ax.set_title("Project Schedule")
            self.ax.grid(True)
        else:
            self.ax.set_title("No Tasks Added")
        self.canvas.draw()
    
    def export_to_excel(self):
        try:
            excel_file = "[Your Name]_construction_report.xlsx"  # Personalize with your name
            writer = pd.ExcelWriter(excel_file, engine="openpyxl")
            
            # Cost Estimation Sheet
            if self.materials:
                df_cost = pd.DataFrame(self.materials)
                df_cost["Quantity"] = df_cost["Quantity"].map("{:.2f}".format)
                df_cost["Rate"] = df_cost["Rate"].map("{:.2f}".format)
                df_cost["Cost"] = df_cost["Cost"].map("{:.2f}".format)
                total_cost = df_cost["Cost"].astype(float).sum()
                df_cost.loc["Total"] = ["", "", "Total Cost", f"{total_cost:.2f}"]
                df_cost.to_excel(writer, sheet_name="Cost Estimation", index=False)
            else:
                pd.DataFrame({"Note": ["No cost data available"]}).to_excel(writer, sheet_name="Cost Estimation", index=False)
            
            # Inventory Sheet
            if self.materials:
                df = pd.DataFrame(self.materials)
                df_inventory = df.groupby("Material")["Quantity"].sum().reset_index()
                df_inventory["Status"] = df_inventory["Quantity"].apply(lambda x: "Low" if x < 100 else "Sufficient")
                df_inventory["Quantity"] = df_inventory["Quantity"].map("{:.2f}".format)
                df_inventory.to_excel(writer, sheet_name="Inventory", index=False)
            else:
                pd.DataFrame({"Note": ["No inventory data available"]}).to_excel(writer, sheet_name="Inventory", index=False)
            
            writer.close()
            messagebox.showinfo("Success", f"Excel report saved as {excel_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export Excel: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure("TButton", background="#4682b4", foreground="white")
    style.configure("TFrame", background="#d4e4d4")
    app = ConstructionDashboard(root)
    root.mainloop()