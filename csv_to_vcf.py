import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class CSVToVCFApp:
    def __init__(self, root):
        self.root = root

        self.root.title("CSV to VCF Converter")
        self.root.geometry("600x430")
        self.root.resizable(False, False)

        self.csv_path = tk.StringVar()
        self.token = tk.StringVar()
        self.number_of_files = tk.StringVar()

        self.setup_style()
        self.create_ui()

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

    def create_ui(self):
        main = ttk.Frame(self.root, padding=30)
        main.pack(fill="both", expand=True)

        # Title
        ttk.Label(
            main,
            text="CSV to VCF Converter",
            style="Title.TLabel"
        ).pack(anchor="w")

        # Subtitle
        ttk.Label(
            main,
            text="Convert CSV contacts into multiple VCF files.",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(4, 25))

        # CSV File
        ttk.Label(
            main,
            text="CSV File"
        ).pack(anchor="w")

        csv_frame = ttk.Frame(main)
        csv_frame.pack(fill="x", pady=(5, 18))

        ttk.Entry(
            csv_frame,
            textvariable=self.csv_path,
            state="readonly"
        ).pack(side="left", fill="x", expand=True)

        ttk.Button(
            csv_frame,
            text="Browse",
            command=self.select_csv
        ).pack(side="left", padx=(8, 0))

        # Token
        ttk.Label(
            main,
            text="Token"
        ).pack(anchor="w")

        ttk.Entry(
            main,
            textvariable=self.token
        ).pack(fill="x", pady=(5, 18))

        # Number of files
        ttk.Label(
            main,
            text="Number of VCF Files"
        ).pack(anchor="w")

        files_frame = ttk.Frame(main)
        files_frame.pack(fill="x", pady=(5, 18))

        ttk.Entry(
            files_frame,
            textvariable=self.number_of_files,
            width=15
        ).pack(side="left")

        ttk.Label(
            files_frame,
            text="Enter any positive integer"
        ).pack(side="left", padx=10)

        # Separator
        ttk.Separator(
            main,
            orient="horizontal"
        ).pack(fill="x", pady=(5, 20))

        # Convert button
        self.convert_button = ttk.Button(
            main,
            text="Convert to VCF",
            style="Convert.TButton",
            command=self.convert
        )
        self.convert_button.pack(fill="x")

        # Status
        self.status = tk.StringVar(
            value="Select a CSV file to begin."
        )

        ttk.Label(
            main,
            textvariable=self.status,
            wraplength=530
        ).pack(anchor="w", pady=(20, 0))

        # Footer
        ttk.Label(
            main,
            text="CSV → VCF",
            style="Subtitle.TLabel"
        ).pack(anchor="center", pady=(25, 0))

    def select_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            self.csv_path.set(file_path)
            self.status.set(
                f"Selected: {os.path.basename(file_path)}"
            )

    def read_contacts(self, csv_file):
        contacts = []

        with open(
            csv_file,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.reader(file)

            for row_number, row in enumerate(reader, start=1):

                # Ignore empty rows
                if not row or all(
                    not field.strip() for field in row
                ):
                    continue

                # At least two columns required
                if len(row) < 2:
                    continue

                contact_name = row[0].strip()
                phone_number = row[1].strip()

                # Detect common header formats
                if row_number == 1:
                    name_header = contact_name.lower()
                    phone_header = phone_number.lower()

                    if (
                        name_header in {
                            "contact name",
                            "name",
                            "contact_name"
                        }
                        or phone_header in {
                            "phone",
                            "phone number",
                            "phone_number",
                            "mobile",
                            "mobile number"
                        }
                    ):
                        continue

                # Ignore rows with missing data
                if not contact_name or not phone_number:
                    continue

                contacts.append(
                    (contact_name, phone_number)
                )

        return contacts

    def escape_vcard(self, value):
        """
        Escape characters required by the vCard format.
        """
        return (
            value
            .replace("\\", "\\\\")
            .replace("\n", "\\n")
            .replace(";", "\\;")
            .replace(",", "\\,")
        )

    def create_vcf(
        self,
        output_path,
        contacts,
        start_index
    ):
        with open(
            output_path,
            "w",
            encoding="utf-8",
            newline=""
        ) as vcf:

            for local_index, (
                contact_name,
                phone_number
            ) in enumerate(contacts):

                global_index = (
                    start_index + local_index
                )

                first_name = (
                    f"{self.token.get().strip()}"
                    f"{global_index}"
                )

                second_name = contact_name

                escaped_first = self.escape_vcard(
                    first_name
                )

                escaped_second = self.escape_vcard(
                    second_name
                )

                full_name = (
                    f"{escaped_first} "
                    f"{escaped_second}"
                )

                vcf.write("BEGIN:VCARD\r\n")
                vcf.write("VERSION:3.0\r\n")

                vcf.write(
                    f"N:{escaped_second};"
                    f"{escaped_first};;;\r\n"
                )

                vcf.write(
                    f"FN:{full_name}\r\n"
                )

                vcf.write(
                    f"TEL;TYPE=CELL:{phone_number}\r\n"
                )

                vcf.write("END:VCARD\r\n")

    def convert(self):
        csv_file = self.csv_path.get().strip()
        token = self.token.get().strip()

        # Validate CSV
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

        # Validate token
        if not token:
            messagebox.showwarning(
                "Token Required",
                "Please enter a token."
            )
            return

        # Validate number of files
        try:
            number_of_files = int(
                self.number_of_files.get().strip()
            )
        except ValueError:
            messagebox.showwarning(
                "Invalid Number",
                "Please enter a valid positive integer."
            )
            return

        # Number of files must be at least 1
        if number_of_files < 1:
            messagebox.showwarning(
                "Invalid Number",
                "The number of VCF files must be at least 1."
            )
            return

        # Read contacts
        try:
            contacts = self.read_contacts(csv_file)
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

        # More files than contacts
        if number_of_files > len(contacts):
            messagebox.showwarning(
                "Too Many Files",
                f"The CSV contains {len(contacts)} contacts.\n\n"
                f"You requested {number_of_files} files.\n\n"
                "The number of files cannot exceed the number "
                "of contacts."
            )
            return

        # Disable button during conversion
        self.convert_button.config(
            state="disabled"
        )

        try:
            total_contacts = len(contacts)

            # Even distribution
            base_count = (
                total_contacts // number_of_files
            )

            remainder = (
                total_contacts % number_of_files
            )

            output_directory = os.path.dirname(
                os.path.abspath(csv_file)
            )

            current_index = 0

            for file_number in range(
                1,
                number_of_files + 1
            ):

                contacts_in_file = base_count

                # Distribute remainder among
                # the first files
                if file_number <= remainder:
                    contacts_in_file += 1

                file_contacts = contacts[
                    current_index:
                    current_index + contacts_in_file
                ]

                output_filename = (
                    f"{token}{file_number}.vcf"
                )

                output_path = os.path.join(
                    output_directory,
                    output_filename
                )

                self.create_vcf(
                    output_path,
                    file_contacts,
                    current_index + 1
                )

                current_index += contacts_in_file

                self.status.set(
                    f"Created {output_filename} "
                    f"({contacts_in_file} contacts)"
                )

                self.root.update_idletasks()

            self.status.set(
                f"Completed: {total_contacts} contacts "
                f"converted into {number_of_files} files."
            )

            messagebox.showinfo(
                "Conversion Complete",
                f"Conversion completed successfully.\n\n"
                f"Contacts: {total_contacts}\n"
                f"VCF files: {number_of_files}\n\n"
                f"Output folder:\n{output_directory}"
            )

        except Exception as error:
            messagebox.showerror(
                "Conversion Error",
                f"An error occurred during conversion.\n\n{error}"
            )

        finally:
            self.convert_button.config(
                state="normal"
            )


def main():
    root = tk.Tk()

    app = CSVToVCFApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
