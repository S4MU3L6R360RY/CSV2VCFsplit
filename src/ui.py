import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.csv_handler import read_contacts
from src.vcf_generator import split_contacts


class CSVToVCFApp:

    def __init__(self, root):
        self.root = root

        self.root.title("CSV to VCF Converter")
        self.root.geometry("620x470")
        self.root.resizable(False, False)

        self.csv_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.token = tk.StringVar()
        self.number_of_files = tk.StringVar()

        self.status = tk.StringVar(
            value="Select a CSV file to get started."
        )

        self.setup_style()
        self.create_ui()

    # -------------------------------------------------
    # Styling
    # -------------------------------------------------

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("vista")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 21, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 9)
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 9, "bold")
        )

        # Dedicated status style
        style.configure(
            "Status.TLabel",
            font=("Segoe UI", 9),
            padding=(0, 4)
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 9),
            padding=(10, 6)
        )

        style.configure(
            "TEntry",
            padding=6
        )

        # Highlighted convert button
        style.configure(
            "Convert.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 9)
        )

    # -------------------------------------------------
    # User Interface
    # -------------------------------------------------

    def create_ui(self):

        main = ttk.Frame(
            self.root,
            padding=(32, 24, 32, 20)
        )

        main.pack(
            fill="both",
            expand=True
        )

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        ttk.Label(
            main,
            text="CSV to VCF",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            main,
            text="Convert your contacts into VCF files.",
            style="Subtitle.TLabel"
        ).pack(
            anchor="w",
            pady=(2, 18)
        )

        # -------------------------------------------------
        # CSV File
        # -------------------------------------------------

        ttk.Label(
            main,
            text="CSV file",
            style="Section.TLabel"
        ).pack(anchor="w")

        csv_frame = ttk.Frame(main)

        csv_frame.pack(
            fill="x",
            pady=(5, 12)
        )

        ttk.Entry(
            csv_frame,
            textvariable=self.csv_path,
            state="readonly"
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Button(
            csv_frame,
            text="Browse",
            command=self.select_csv
        ).pack(
            side="left",
            padx=(7, 0)
        )

        # -------------------------------------------------
        # Token
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Contact token",
            style="Section.TLabel"
        ).pack(anchor="w")

        ttk.Entry(
            main,
            textvariable=self.token
        ).pack(
            fill="x",
            pady=(5, 12)
        )

        # -------------------------------------------------
        # Number of Files
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Number of VCF files",
            style="Section.TLabel"
        ).pack(anchor="w")

        ttk.Entry(
            main,
            textvariable=self.number_of_files
        ).pack(
            fill="x",
            pady=(5, 12)
        )

        # -------------------------------------------------
        # Output Folder
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Output folder",
            style="Section.TLabel"
        ).pack(anchor="w")

        output_frame = ttk.Frame(main)

        output_frame.pack(
            fill="x",
            pady=(5, 16)
        )

        ttk.Entry(
            output_frame,
            textvariable=self.output_folder,
            state="readonly"
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Button(
            output_frame,
            text="Browse",
            command=self.select_output_folder
        ).pack(
            side="left",
            padx=(7, 0)
        )

        # -------------------------------------------------
        # Convert Button
        # -------------------------------------------------

        self.convert_button = ttk.Button(
            main,
            text="Convert to VCF",
            style="Convert.TButton",
            command=self.convert
        )

        self.convert_button.pack(
            fill="x",
            pady=(0, 10)
        )

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        ttk.Label(
            main,
            textvariable=self.status,
            style="Status.TLabel"
        ).pack(
            anchor="w",
            fill="x"
        )

    # -------------------------------------------------
    # CSV Selection
    # -------------------------------------------------

    def select_csv(self):

        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        self.csv_path.set(file_path)

        self.status.set(
            f"Selected: {os.path.basename(file_path)}"
        )

        # Automatically use the CSV directory
        # as the output folder if none is selected.
        if not self.output_folder.get():

            self.output_folder.set(
                os.path.dirname(file_path)
            )

    # -------------------------------------------------
    # Output Folder Selection
    # -------------------------------------------------

    def select_output_folder(self):

        folder_path = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if not folder_path:
            return

        self.output_folder.set(folder_path)

        self.status.set(
            "Output folder selected."
        )

    # -------------------------------------------------
    # Conversion
    # -------------------------------------------------

    def convert(self):

        csv_file = self.csv_path.get().strip()
        output_folder = self.output_folder.get().strip()
        token = self.token.get().strip()

        # -------------------------------------------------
        # Validate CSV
        # -------------------------------------------------

        if not csv_file:

            messagebox.showwarning(
                "CSV File Required",
                "Please select a CSV file."
            )

            return

        if not os.path.isfile(csv_file):

            messagebox.showerror(
                "File Error",
                "The selected CSV file does not exist."
            )

            return

        # -------------------------------------------------
        # Validate Token
        # -------------------------------------------------

        if not token:

            messagebox.showwarning(
                "Token Required",
                "Please enter a contact token."
            )

            return

        # -------------------------------------------------
        # Validate Number of Files
        # -------------------------------------------------

        try:

            number_of_files = int(
                self.number_of_files.get().strip()
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Number",
                "Please enter a positive integer."
            )

            return

        if number_of_files < 1:

            messagebox.showwarning(
                "Invalid Number",
                "The number of VCF files must be at least 1."
            )

            return

        # -------------------------------------------------
        # Validate Output Folder
        # -------------------------------------------------

        if not output_folder:

            messagebox.showwarning(
                "Output Folder Required",
                "Please select an output folder."
            )

            return

        if not os.path.isdir(output_folder):

            messagebox.showerror(
                "Output Folder Error",
                "The selected output folder does not exist."
            )

            return

        # -------------------------------------------------
        # Read Contacts
        # -------------------------------------------------

        try:

            contacts = read_contacts(csv_file)

        except Exception as error:

            messagebox.showerror(
                "CSV Error",
                f"Unable to read the CSV file.\n\n{error}"
            )

            return

        if not contacts:

            messagebox.showwarning(
                "No Contacts",
                "No valid contacts were found in the CSV file."
            )

            return

        # -------------------------------------------------
        # Validate Number of Files
        # -------------------------------------------------

        if number_of_files > len(contacts):

            messagebox.showwarning(
                "Too Many Files",
                f"The CSV contains {len(contacts)} contacts.\n\n"
                f"You requested {number_of_files} files.\n\n"
                "The number of files cannot exceed "
                "the number of contacts."
            )

            return

        # -------------------------------------------------
        # Start Conversion
        # -------------------------------------------------

        self.convert_button.config(
            state="disabled"
        )

        self.status.set(
            "Converting contacts..."
        )

        self.root.update_idletasks()

        try:

            generated_files = split_contacts(
                contacts,
                number_of_files,
                token,
                output_folder
            )

            self.status.set(
                f"Completed: {len(contacts)} contacts "
                f"→ {len(generated_files)} VCF files."
            )

            messagebox.showinfo(
                "Conversion Complete",
                "Conversion completed successfully.\n\n"
                f"Contacts: {len(contacts)}\n"
                f"VCF files: {len(generated_files)}\n\n"
                f"Saved to:\n{output_folder}"
            )

        except Exception as error:

            self.status.set(
                "Conversion failed."
            )

            messagebox.showerror(
                "Conversion Error",
                f"An error occurred during conversion.\n\n"
                f"{error}"
            )

        finally:

            self.convert_button.config(
                state="normal"
            )
