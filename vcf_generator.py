import os


def escape_vcard(value):
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
    output_path,
    contacts,
    token,
    start_index
):
    """
    Create a single VCF file.

    Parameters:
        output_path  : Destination VCF file
        contacts     : List of contact tuples
        token        : Contact name prefix
        start_index  : Global starting contact index
    """

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
                f"{token}{global_index}"
            )

            second_name = contact_name

            escaped_first = escape_vcard(
                first_name
            )

            escaped_second = escape_vcard(
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


def split_contacts(
    contacts,
    number_of_files,
    token,
    output_directory
):
    """
    Split contacts evenly and create multiple VCF files.

    Returns:
        List of generated filenames.
    """

    total_contacts = len(contacts)

    # Calculate even distribution
    base_count = (
        total_contacts // number_of_files
    )

    remainder = (
        total_contacts % number_of_files
    )

    current_index = 0
    generated_files = []

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

        create_vcf(
            output_path,
            file_contacts,
            token,
            current_index + 1
        )

        generated_files.append(
            output_filename
        )

        current_index += contacts_in_file

    return generated_files
