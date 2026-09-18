import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.csv_handler import read_contacts
from src.vcf_generator import split_contacts


class CSVToVCFApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "CSV to VCF Converter"
        )

        self.root.geometry(
            "650x500"
        )

        self.root.resizable(
            False,
            False
        )

        self.csv_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.token = tk.StringVar()
        self.number_of_files = tk.StringVar()

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
            font=("Segoe UI", 20, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 10)
        )

        style.configure(
            "TLabel",
            font=("Segoe UI", 10)
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=7
        )

        style.configure(
            "Convert.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def create_ui(self):

        main = ttk.Frame(
            self.root,
            padding=30
        )

        main.pack(
            fill="both",
            expand=True
        )

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        ttk.Label(
            main,
            text="CSV to VCF Converter",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            main,
            text=(
                "Convert CSV contacts into "
                "multiple VCF files."
            ),
            style="Subtitle.TLabel"
        ).pack(
            anchor="w",
            pady=(4, 25)
        )

        # -------------------------------------------------
        # CSV File
        # -------------------------------------------------

        ttk.Label(
            main,
            text="CSV File"
        ).pack(anchor="w")

        csv_frame = ttk.Frame(main)

        csv_frame.pack(
            fill="x",
            pady=(5, 18)
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
            padx=(8, 0)
        )

        # -------------------------------------------------
        # Token
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Token"
        ).pack(anchor="w")

        ttk.Entry(
            main,
            textvariable=self.token
        ).pack(
            fill="x",
            pady=(5, 18)
        )

        # -------------------------------------------------
        # Number of VCF Files
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Number of VCF Files"
        ).pack(anchor="w")

        files_frame = ttk.Frame(main)

        files_frame.pack(
            fill="x",
            pady=(5, 18)
        )

        ttk.Entry(
            files_frame,
            textvariable=self.number_of_files,
            width=15
        ).pack(side="left")

        ttk.Label(
            files_frame,
            text="Enter a positive integer"
        ).pack(
            side="left",
            padx=10
        )

        # -------------------------------------------------
        # Output Folder
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Output Folder"
        ).pack(anchor="w")

        output_frame = ttk.Frame(main)

        output_frame.pack(
            fill="x",
            pady=(5, 18)
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
            padx=(8, 0)
        )

        # -------------------------------------------------
        # Separator
        # -------------------------------------------------

        ttk.Separator(
            main,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=(5, 20)
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
            fill="x"
        )

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        self.status = tk.StringVar(
            value="Select a CSV file to begin."
        )

        ttk.Label(
            main,
            textvariable=self.status,
            wraplength=580
        ).pack(
            anchor="w",
            pady=(20, 0)
        )

        # -------------------------------------------------
        # Footer
        # -------------------------------------------------

        ttk.Label(
            main,
            text="CSV → VCF",
            style="Subtitle.TLabel"
        ).pack(
            anchor="center",
            pady=(20, 0)
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

        if file_path:

            self.csv_path.set(
                file_path
            )

            self.status.set(
                f"Selected: "
                f"{os.path.basename(file_path)}"
            )

            # Automatically suggest the CSV's
            # directory as the output folder
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

        if folder_path:

            self.output_folder.set(
                folder_path
            )

            self.status.set(
                f"Output folder: {folder_path}"
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
                "Please enter a token."
            )

            return

        # -------------------------------------------------
        # Validate Number of Files
        # -------------------------------------------------

        try:

            number_of_files = int(
                self.number_of_files
                .get()
                .strip()
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Number",
                "Please enter a valid positive integer."
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

            contacts = read_contacts(
                csv_file
            )

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
                f"The CSV contains "
                f"{len(contacts)} contacts.\n\n"
                f"You requested "
                f"{number_of_files} files.\n\n"
                "The number of files cannot exceed "
                "the number of contacts."
            )

            return

        # -------------------------------------------------
        # Disable Button
        # -------------------------------------------------

        self.convert_button.config(
            state="disabled"
        )

        try:

            # -------------------------------------------------
            # Generate VCF Files
            # -------------------------------------------------

            generated_files = split_contacts(
                contacts,
                number_of_files,
                token,
                output_folder
            )

            self.status.set(
                f"Completed: "
                f"{len(contacts)} contacts "
                f"converted into "
                f"{len(generated_files)} files."
            )

            # -------------------------------------------------
            # Success Message
            # -------------------------------------------------

            messagebox.showinfo(
                "Conversion Complete",
                "Conversion completed successfully.\n\n"
                f"Contacts: {len(contacts)}\n"
                f"VCF files: {len(generated_files)}\n\n"
                f"Output folder:\n"
                f"{output_folder}"
            )

        except Exception as error:

            messagebox.showerror(
                "Conversion Error",
                "An error occurred during conversion.\n\n"
                f"{error}"
            )

        finally:

            self.convert_button.config(
                state="normal"
            )
