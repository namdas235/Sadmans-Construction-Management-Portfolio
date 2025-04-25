### Project 2: Construction Data Analyzer with Automation (Unchanged)



# Construction Data Analyzer by Sadman Ali
import pandas as pd
import matplotlib.pyplot as plt
import os
import smtplib
from email.mime.text import MIMEText

def create_sample_data():
    """Create a sample CSV if none exists"""
    data = {
        "Material": ["Concrete", "Timber", "Bricks", "Steel"],
        "Quantity": [200, 50, 1000, 30],
        "Rate": [50, 30, 0.5, 100],
        "Task": ["Foundation", "Framing", "Walls", "Roofing"],
        "Duration": [5, 7, 3, 4]
    }
    df = pd.DataFrame(data)
    df["Cost"] = df["Quantity"] * df["Rate"]
    df.to_csv("[Your Name]_project_data.csv", index=False)  

def simulate_email_order(material, quantity):
    """Simulate sending an email to reorder materials"""
    msg = MIMEText(f"Order by [Your Name]: {quantity} units of {material} needed.")  
    msg["Subject"] = "Material Reorder by [Your Name]"
    msg["From"] = "[Your Name]@example.com"
    msg["To"] = "supplier@example.com"
    with open("reorder_log.txt", "a") as f:
        f.write(f"Simulated email sent: {msg.as_string()}\n")
    print(f"Simulated email order for {quantity} units of {material}")

def analyze_data():
    """Analyze construction data, generate visualizations, and automate reordering"""
    if not os.path.exists("[Your Name]_project_data.csv"):
        create_sample_data()
    
    df = pd.read_csv("[Your Name]_project_data.csv")
    
    total_cost = df["Cost"].sum()
    total_duration = df["Duration"].sum()
    
    print(f"Total Project Cost: ${total_cost:.2f}")
    print(f"Total Project Duration: {total_duration} days")
    print("\nCost Breakdown by Material:")
    for _, row in df.iterrows():
        print(f"{row['Material']}: ${row['Cost']:.2f}")
    
    print("\nChecking for low stock...")
    for _, row in df.iterrows():
        if row["Quantity"] < 100:
            simulate_email_order(row["Material"], 500 - row["Quantity"])
    
    plt.figure(figsize=(8, 5))
    plt.bar(df["Material"], df["Cost"], color="#4682b4")
    plt.title("[Your Name]'s Material Cost Analysis")  
    plt.xlabel("Material")
    plt.ylabel("Cost ($)")
    plt.grid(True)
    plt.close()
    
    plt.figure(figsize=(8, 5))
    plt.pie(df["Duration"], labels=df["Task"], autopct="%1.1f%%", colors=["#d4e4d4", "#4682b4", "#a9a9a9", "#f0e68c"])
    plt.title("[Your Name]'s Task Duration Distribution")  
    plt.savefig("[Your Name]_task_duration.png")  
    plt.close()

if __name__ == "__main__":
    analyze_data()
    print("Visualizations saved as '[Your Name]_material_costs.png' and '[Your Name]_task_duration.png'")
    print("Check 'reorder_log.txt' for simulated email orders")