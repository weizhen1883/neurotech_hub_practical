
import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from datetime import datetime

class Record:
    def __init__(self, path):
        self.path = path
        self.meta_path = os.path.join(path, "meta.json")
        self.load()

    def load(self):
        if os.path.exists(self.meta_path):
            with open(self.meta_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"title": "", "date": "", "report": "", "logs": []}
        self.title = data.get("title", "")
        self.date = data.get("date", "")
        self.report = data.get("report", "")
        self.logs = data.get("logs", [])

    def save(self):
        data = {
            "title": self.title,
            "date": self.date,
            "report": self.report,
            "logs": self.logs
        }
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

class Project:
    def __init__(self, folder):
        self.folder = folder
        self.records = []
        self.index_path = os.path.join(folder, "records.json")
        self.load()

    def load(self):
        if os.path.exists(self.index_path):
            with open(self.index_path, "r", encoding="utf-8") as f:
                record_dirs = json.load(f)
        else:
            record_dirs = []

        self.records = []
        for name in record_dirs:
            path = os.path.join(self.folder, name)
            if os.path.isdir(path):
                self.records.append(Record(path))

    def save(self):
        record_names = [os.path.basename(r.path) for r in self.records]
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(record_names, f)

def enable_drag_and_drop(widget, log_list, log_cache, record_logs):
    def drop(event):
        files = widget.tk.splitlist(event.data)
        for file_path in files:
            if os.path.isfile(file_path):
                fname = os.path.basename(file_path)
                if fname in record_logs:
                    continue
                record_logs.append(fname)
                log_list.insert(tk.END, fname)
                log_cache[fname] = file_path
    widget.drop_target_register(DND_FILES)
    widget.dnd_bind('<<Drop>>', drop)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Post-mortem Tool")
        self.project = None
        self.selected_record = None
        self.build_ui()

    def build_ui(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        tk.Button(toolbar, text="New", command=self.new_project).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Open", command=self.open_project).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Close", command=self.close_project).pack(side=tk.LEFT)

        main = tk.PanedWindow(self.root, sashrelief=tk.RAISED)
        main.pack(fill=tk.BOTH, expand=1)

        # 左侧记录列表
        left = tk.Frame(main)
        self.record_list = tk.Listbox(left)
        self.record_list.pack(fill=tk.BOTH, expand=True)
        self.record_list.bind("<<ListboxSelect>>", self.on_select_record)
        tk.Button(left, text="Add Record", command=self.add_record).pack(fill=tk.X)
        main.add(left)

        # 右侧记录详情（只读）
        self.right = tk.Frame(main)
        self.details = tk.Text(self.right, height=15, state=tk.DISABLED)
        self.details.pack(fill=tk.BOTH, expand=True)
        self.log_list = tk.Listbox(self.right)
        self.log_list.pack(fill=tk.X)
        tk.Button(self.right, text="Edit Record", command=self.edit_record).pack()
        main.add(self.right)

    def new_project(self):
        path = filedialog.askdirectory(title="Select Project Folder")
        if not path: return
        os.makedirs(path, exist_ok=True)
        self.project = Project(path)
        self.root.title(f"Post-mortem Tool - {os.path.basename(path)}")
        self.project.save()
        self.refresh_record_list()

    def open_project(self):
        self.root.title("Post-mortem Tool")  # Reset title
        path = filedialog.askdirectory(title="Open Project Folder")
        if not path: return
        self.project = Project(path)
        self.root.title(f"Post-mortem Tool - {os.path.basename(path)}")
        self.refresh_record_list()

    def close_project(self):
        self.project = None
        self.record_list.delete(0, tk.END)
        self.details.config(state=tk.NORMAL)
        self.details.delete(1.0, tk.END)
        self.details.config(state=tk.DISABLED)
        self.log_list.delete(0, tk.END)

    def refresh_record_list(self):
        self.record_list.delete(0, tk.END)
        if self.project:
            for record in self.project.records:
                self.record_list.insert(tk.END, record.title)

    def on_select_record(self, event):
        if not self.project: return
        idx = self.record_list.curselection()
        if not idx: return
        self.selected_record = self.project.records[idx[0]]
        self.show_record()

    def show_record(self):
        r = self.selected_record
        self.details.config(state=tk.NORMAL)
        self.details.delete(1.0, tk.END)
        self.details.insert(tk.END, f"Title: {r.title}\nDate: {r.date}\nReport:\n{r.report}\n")
        self.details.config(state=tk.DISABLED)

        self.log_list.delete(0, tk.END)
        for log_file in r.logs:
            self.log_list.insert(tk.END, log_file)

    def add_record(self):
        if not self.project:
            messagebox.showwarning("No Project Selested", "Please open a new project first!")
            return

        record_logs = []

        def upload():
            file_path = filedialog.askopenfilename(title="Select log file")
            if not file_path:
                return
            fname = os.path.basename(file_path)
            if fname in record_logs:
                messagebox.showinfo("Warning", "File alredy added!")
                return
            record_logs.append(fname)
            log_list.insert(tk.END, fname)
            log_cache[fname] = file_path

        def delete_selected():
            idx = log_list.curselection()
            if not idx:
                return
            fname = log_list.get(idx[0])
            record_logs.remove(fname)
            log_list.delete(idx[0])
            log_cache.pop(fname, None)

        def save():
            title = e_title.get()
            report = e_report.get("1.0", tk.END).strip()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record_id = f"record_{int(datetime.now().timestamp())}"
            record_path = os.path.join(self.project.folder, record_id)
            os.makedirs(record_path)

            for fname in record_logs:
                src = log_cache[fname]
                dest = os.path.join(record_path, fname)
                shutil.copy(src, dest)

            new_record = Record(record_path)
            new_record.title = title
            new_record.date = date
            new_record.report = report
            new_record.logs = record_logs
            new_record.save()

            self.project.records.append(new_record)
            self.project.save()
            self.refresh_record_list()
            win.destroy()

        win = tk.Toplevel(self.root)
        win.title("New Record")
        tk.Label(win, text="Title:").pack()
        e_title = tk.Entry(win)
        e_title.pack(fill=tk.X)
        tk.Label(win, text="Report:").pack()
        e_report = tk.Text(win, height=10)
        e_report.pack(fill=tk.BOTH)

        tk.Label(win, text="Log Files(Drag and place supported):").pack()
        log_list = tk.Listbox(win, height=5)
        log_list.pack(fill=tk.X)
        log_cache = {}
        enable_drag_and_drop(log_list, log_list, log_cache, record_logs)

        tk.Button(win, text="Upload", command=upload).pack()
        tk.Button(win, text="Delect Selected", command=delete_selected).pack()

        btn_frame = tk.Frame(win)
        tk.Button(btn_frame, text="Save", command=save).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Cancel", command=win.destroy).pack(side=tk.RIGHT)
        btn_frame.pack(fill=tk.X)

    def edit_record(self):
        if not self.selected_record:
            messagebox.showinfo("Warning", "Please select a record.")
            return

        r = self.selected_record
        record_logs = r.logs.copy()

        def upload():
            file_path = filedialog.askopenfilename(title="Select log file")
            if not file_path:
                return
            fname = os.path.basename(file_path)
            if fname in record_logs:
                messagebox.showinfo("Warning", "File Already Added!")
                return
            dest = os.path.join(r.path, fname)
            shutil.copy(file_path, dest)
            record_logs.append(fname)
            log_list.insert(tk.END, fname)

        def delete_selected():
            idx = log_list.curselection()
            if not idx:
                return
            fname = log_list.get(idx[0])
            record_logs.remove(fname)
            log_list.delete(idx[0])
            path = os.path.join(r.path, fname)
            if os.path.exists(path):
                os.remove(path)

        def save():
            r.title = e_title.get()
            r.report = e_report.get("1.0", tk.END).strip()
            r.logs = record_logs
            r.save()
            self.project.save()
            self.refresh_record_list()
            self.show_record()
            win.destroy()

        win = tk.Toplevel(self.root)
        win.title("Edit Record")
        tk.Label(win, text="Title:").pack()
        e_title = tk.Entry(win)
        e_title.insert(0, r.title)
        e_title.pack(fill=tk.X)
        tk.Label(win, text="Report:").pack()
        e_report = tk.Text(win, height=10)
        e_report.insert(tk.END, r.report)
        e_report.pack(fill=tk.BOTH)

        tk.Label(win, text="Log Files(Drag and place supported}:").pack()
        log_list = tk.Listbox(win, height=5)
        log_list.pack(fill=tk.X)
        for f in record_logs:
            log_list.insert(tk.END, f)
        enable_drag_and_drop(log_list, log_list, {}, record_logs)

        tk.Button(win, text="Upload", command=upload).pack()
        tk.Button(win, text="Delete Selected", command=delete_selected).pack()

        btn_frame = tk.Frame(win)
        tk.Button(btn_frame, text="Save", command=save).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Cancel", command=win.destroy).pack(side=tk.RIGHT)
        btn_frame.pack(fill=tk.X)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = App(root)
    root.mainloop()
