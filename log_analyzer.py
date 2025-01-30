import sys
import pandas as pd
import matplotlib.pyplot as plt
import re

# Verifica se Tkinter está disponível
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ImportError:
    print("Erro: Tkinter não está disponível neste ambiente.")
    sys.exit(1)

class LogAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador de Logs")
        self.root.geometry("800x600")

        self.create_widgets()
        self.log_data = []
    
    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        btn_open = tk.Button(frame, text="Abrir Arquivo de Log", command=self.load_log)
        btn_open.pack(side=tk.LEFT, padx=5)
        
        btn_filter = tk.Button(frame, text="Filtrar Erros", command=self.filter_errors)
        btn_filter.pack(side=tk.LEFT, padx=5)
        
        btn_export = tk.Button(frame, text="Exportar CSV", command=self.export_csv)
        btn_export.pack(side=tk.LEFT, padx=5)
        
        btn_graph = tk.Button(frame, text="Gerar Gráfico", command=self.show_graph)
        btn_graph.pack(side=tk.LEFT, padx=5)
        
        self.tree = ttk.Treeview(self.root, columns=("Data", "Tipo", "Mensagem"), show="headings")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Mensagem", text="Mensagem")
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    def load_log(self):
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos de Log", "*.log *.txt")])
        if not file_path:
            return
        
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()
        
        pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (ERROR|WARNING|INFO) (.*)")
        
        self.log_data.clear()
        for line in lines:
            match = pattern.search(line)
            if match:
                self.log_data.append(match.groups())
        
        self.update_treeview()
    
    def update_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for entry in self.log_data:
            self.tree.insert("", "end", values=entry)
    
    def filter_errors(self):
        if not self.log_data:
            messagebox.showerror("Erro", "Nenhum log carregado!")
            return
        
        self.log_data = [entry for entry in self.log_data if entry[1] == "ERROR"]
        self.update_treeview()
    
    def export_csv(self):
        if not self.log_data:
            messagebox.showerror("Erro", "Nenhum log disponível para exportar!")
            return
        
        try:
            df = pd.DataFrame(self.log_data, columns=["Data", "Tipo", "Mensagem"])
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
            if file_path:
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Sucesso", "Arquivo exportado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar CSV: {e}")
    
    def show_graph(self):
        if not self.log_data:
            messagebox.showerror("Erro", "Nenhum log carregado!")
            return
        
        try:
            df = pd.DataFrame(self.log_data, columns=["Data", "Tipo", "Mensagem"])
            error_count = df["Tipo"].value_counts()
            error_count.plot(kind="bar", color=["red", "orange", "blue"], alpha=0.7)
            plt.xlabel("Tipo de Log")
            plt.ylabel("Quantidade")
            plt.title("Distribuição dos Tipos de Logs")
            plt.show()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar gráfico: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LogAnalyzer(root)
    root.mainloop()
