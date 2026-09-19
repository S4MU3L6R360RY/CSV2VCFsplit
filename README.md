## How to Use

### 1. Add a CSV File

Click **Browse** next to **CSV File** and select the CSV file containing your contacts.

The CSV file must contain:

* **Contact Name** in the first column
* **Phone Number** in the second column
* One contact per row

Example:

```csv
Contact Name,Phone Number
John Doe,+919876543210
Jane Smith,+919876543211
Robert,+919876543212
```

The CSV file can have a header row, but it is not required.

---

### 2. Enter a Token

The **Token** is a text value that is added to the beginning of every generated contact name.

For example, if the token is:

```text
ISHA
```

the generated contacts will start with:

```text
ISHA1
ISHA2
ISHA3
```

The original contact name is added after the token and index.

For example:

```text
ISHA1 John Doe
ISHA2 Jane Smith
ISHA3 Robert
```

---

### 3. Contact Index

Each contact in the CSV is automatically assigned a sequential **index number**, starting from `1`.

For example:

| Index | Contact Name |
| ----: | ------------ |
|     1 | John Doe     |
|     2 | Jane Smith   |
|     3 | Robert       |
|     4 | David        |

The index is combined with the Token to create the first name of the generated contact.

If the Token is `ISHA`:

```text
ISHA1 John Doe
ISHA2 Jane Smith
ISHA3 Robert
ISHA4 David
```

The index is assigned automatically. **You do not need to enter it manually.**

---

### 4. Number of VCF Files

Enter the number of VCF files you want to create.

For example:

```text
5
```

will create **5 VCF files**, with the contacts distributed as evenly as possible between them.

---

### 5. Select Output Folder

Click **Browse** next to **Output Folder** and select where you want the generated VCF files to be saved.

---

### 6. Convert

After selecting the CSV file and filling in the required fields, click **Convert to VCF**.

The generated VCF files will be saved in the selected output folder.
