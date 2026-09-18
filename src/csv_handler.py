import csv


def read_contacts(csv_file):
    """
    Read contact names and phone numbers from a CSV file.
    """

    contacts = []

    with open(
        csv_file,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.reader(file)

        for row_number, row in enumerate(reader, start=1):

            if not row or all(
                not field.strip() for field in row
            ):
                continue

            if len(row) < 2:
                continue

            contact_name = row[0].strip()
            phone_number = row[1].strip()

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

            if not contact_name or not phone_number:
                continue

            contacts.append(
                (contact_name, phone_number)
            )

    return contacts
