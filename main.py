import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics
import os

class CSVAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analyseur CSV")
        self.root.geometry("400x300")
        
        self.data = None
        self.file_path = None
        
        # Bouton pour sélectionner le fichier
        self.select_button = tk.Button(root, text="Sélectionner un fichier CSV", command=self.select_file)
        self.select_button.pack(pady=10)
        
        # Label pour afficher le fichier sélectionné
        self.file_label = tk.Label(root, text="Aucun fichier sélectionné")
        self.file_label.pack(pady=5)
        
        # Bouton pour calculer les statistiques
        self.calc_button = tk.Button(root, text="Calculer Moyenne, Min, Max, Médiane", command=self.calculate_stats, state=tk.DISABLED)
        self.calc_button.pack(pady=10)
        
        # Bouton pour afficher le graphique
        self.plot_button = tk.Button(root, text="Afficher Graphique", command=self.show_plot, state=tk.DISABLED)
        self.plot_button.pack(pady=10)
        
        # Bouton pour générer le rapport
        self.report_button = tk.Button(root, text="Générer Rapport", command=self.generate_report, state=tk.DISABLED)
        self.report_button.pack(pady=10)
        
        # Variables pour stocker les stats
        self.stats = {}
    
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            self.file_label.config(text=f"Fichier : {os.path.basename(self.file_path)}")
            try:
                self.data = pd.read_csv(self.file_path)
                # Assumer que la première colonne numérique est celle à analyser
                numeric_cols = self.data.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) == 0:
                    messagebox.showerror("Erreur", "Aucune colonne numérique trouvée dans le CSV.")
                    return
                self.column = numeric_cols[0]  # Utiliser la première colonne numérique
                self.calc_button.config(state=tk.NORMAL)
                self.plot_button.config(state=tk.NORMAL)
                self.report_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la lecture du fichier : {str(e)}")
    
    def calculate_stats(self):
        if self.data is None:
            return
        values = self.data[self.column].dropna()
        if len(values) == 0:
            messagebox.showerror("Erreur", "Aucune valeur numérique dans la colonne.")
            return
        self.stats = {
            'Moyenne': np.mean(values),
            'Min': np.min(values),
            'Max': np.max(values),
            'Médiane': statistics.median(values)
        }
        messagebox.showinfo("Statistiques", f"Colonne analysée : {self.column}\n" + "\n".join([f"{k}: {v:.2f}" for k, v in self.stats.items()]))
    
    def show_plot(self):
        if self.data is None or not self.stats:
            messagebox.showerror("Erreur", "Veuillez d'abord calculer les statistiques.")
            return
        values = self.data[self.column].dropna()
        plt.figure(figsize=(8, 6))
        plt.hist(values, bins=20, alpha=0.7, color='blue', edgecolor='black')
        plt.title(f"Histogramme de {self.column}")
        plt.xlabel(self.column)
        plt.ylabel("Fréquence")
        plt.grid(True)
        plt.show()
    
    def generate_report(self):
        if not self.stats:
            messagebox.showerror("Erreur", "Veuillez d'abord calculer les statistiques.")
            return
        report_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if report_path:
            with open(report_path, 'w') as f:
                f.write(f"Rapport d'analyse pour {os.path.basename(self.file_path)}\n")
                f.write(f"Colonne analysée : {self.column}\n\n")
                f.write("Statistiques :\n")
                for k, v in self.stats.items():
                    f.write(f"{k}: {v:.2f}\n")
                f.write("\nRapport généré avec succès.")
            messagebox.showinfo("Succès", f"Rapport sauvegardé dans {report_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVAnalyzer(root)
    root.mainloop()
