#Create Mini project: To-do list app
import os
import time
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
import json

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Data storage
        self.tasks = []
        self.completed_tasks = []
        self.task_file = "tasks.json"
        
        # Load existing tasks
        self.load_tasks()
        
        # Create GUI
        self.create_widgets()
        
        # Refresh task display
        self.update_task_list()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="My To-Do List", 
            font=("Arial", 20, "bold"),
            bg="#4A90E2",
            fg="white",
            pady=10
        )
        title_label.pack(fill=tk.X)
        
        # Frame for input
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(fill=tk.X)
        
        # Task input field
        self.task_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            width=40
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Add button
        add_btn = tk.Button(
            input_frame,
            text="Add Task",
            command=self.add_task,
            bg="#50C878",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5,
            cursor="hand2"
        )
        add_btn.pack(side=tk.LEFT)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, padx=10, pady=5)
        buttons_frame.pack(fill=tk.X)
        
        # Action buttons
        complete_btn = tk.Button(
            buttons_frame,
            text="Mark Complete",
            command=self.mark_complete,
            bg="#FFA500",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5,
            cursor="hand2"
        )
        complete_btn.pack(side=tk.LEFT, padx=2)
        
        delete_btn = tk.Button(
            buttons_frame,
            text="Delete Task",
            command=self.delete_task,
            bg="#FF4444",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5,
            cursor="hand2"
        )
        delete_btn.pack(side=tk.LEFT, padx=2)
        
        clear_completed_btn = tk.Button(
            buttons_frame,
            text="Clear Completed",
            command=self.clear_completed,
            bg="#9B59B6",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5,
            cursor="hand2"
        )
        clear_completed_btn.pack(side=tk.LEFT, padx=2)
        
        save_btn = tk.Button(
            buttons_frame,
            text="Save Tasks",
            command=self.save_tasks,
            bg="#3498DB",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=2)
        
        load_btn = tk.Button(
            buttons_frame,
            text="Load Tasks",
            command=self.load_tasks_from_file,
            bg="#3498DB",
            fg="white",
            font=("Arial", 10),
            padx=10,
            pady=5,
            cursor="hand2"
        )
        load_btn.pack(side=tk.LEFT, padx=2)
        
        # Listbox with scrollbar
        list_frame = tk.Frame(self.root, padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 11),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            bg="#F5F5F5",
            selectbackground="#ADD8E6"
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padx=10,
            pady=5,
            bg="#E0E0E0"
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind double-click to mark complete
        self.task_listbox.bind("<Double-Button-1>", lambda e: self.mark_complete())
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task = {
                "text": task_text,
                "completed": False,
                "created": timestamp
            }
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.update_task_list()
            self.status_label.config(text=f"Task added: {task_text}")
        else:
            messagebox.showwarning("Warning", "Please enter a task!")
    
    def mark_complete(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.tasks):
                task = self.tasks[index]
                if not task["completed"]:
                    task["completed"] = True
                    task["completed_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.completed_tasks.append(task)
                    self.update_task_list()
                    self.status_label.config(text=f"Task marked as complete: {task['text']}")
                else:
                    messagebox.showinfo("Info", "This task is already completed!")
            else:
                messagebox.showwarning("Warning", "Invalid selection!")
        else:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.tasks):
                task = self.tasks[index]
                confirm = messagebox.askyesno("Confirm", f"Delete task: {task['text']}?")
                if confirm:
                    if task["completed"]:
                        self.completed_tasks.remove(task)
                    self.tasks.remove(task)
                    self.update_task_list()
                    self.status_label.config(text="Task deleted")
            else:
                messagebox.showwarning("Warning", "Invalid selection!")
        else:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def clear_completed(self):
        completed_count = len([t for t in self.tasks if t["completed"]])
        if completed_count > 0:
            confirm = messagebox.askyesno("Confirm", f"Clear all {completed_count} completed tasks?")
            if confirm:
                self.tasks = [t for t in self.tasks if not t["completed"]]
                self.completed_tasks.clear()
                self.update_task_list()
                self.status_label.config(text="All completed tasks cleared")
        else:
            messagebox.showinfo("Info", "No completed tasks to clear!")
    
    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task["completed"] else "○"
            task_display = f"{status} {task['text']}"
            if task["completed"]:
                self.task_listbox.insert(tk.END, task_display)
                # Gray out completed tasks
                last_index = self.task_listbox.size() - 1
                self.task_listbox.itemconfig(last_index, {'fg': 'gray'})
            else:
                self.task_listbox.insert(tk.END, task_display)
        
        # Update status with task count
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["completed"]])
        pending = total - completed
        self.status_label.config(text=f"Total: {total} | Completed: {completed} | Pending: {pending}")
    
    def save_tasks(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=self.task_file
            )
            if file_path:
                data = {
                    "tasks": self.tasks,
                    "saved_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                self.task_file = file_path
                self.status_label.config(text=f"Tasks saved to {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Tasks saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
    
    def load_tasks(self):
        # Try to load from default file
        if os.path.exists(self.task_file):
            try:
                with open(self.task_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.completed_tasks = [t for t in self.tasks if t.get("completed", False)]
            except Exception as e:
                self.status_label.config(text=f"Error loading default file: {str(e)}")
    
    def load_tasks_from_file(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=self.task_file
            )
            if file_path:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.completed_tasks = [t for t in self.tasks if t.get("completed", False)]
                    self.task_file = file_path
                    self.update_task_list()
                    self.status_label.config(text=f"Tasks loaded from {os.path.basename(file_path)}")
                    messagebox.showinfo("Success", "Tasks loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")


def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
