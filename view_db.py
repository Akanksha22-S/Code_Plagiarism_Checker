import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ================= USERS TABLE =================
print("\n================ USERS TABLE ================\n")
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

print("+------+---------+---------------+------------------------------+------------+")
print("| S.No | User_ID | Username      | Email                        | Password   |")
print("+------+---------+---------------+------------------------------+------------+")

for i, user in enumerate(users, start=1):
    print("| {:<4} | {:<7} | {:<13} | {:<28} | {:<10} |".format(
        i,
        user[0],
        user[1],
        user[2],
        user[3]
    ))

print("+------+---------+---------------+------------------------------+------------+")

# ================= REPORTS TABLE =================
print("\n================ REPORTS TABLE ================\n")
cursor.execute("SELECT * FROM reports")
reports = cursor.fetchall()

print("+------+-----------+---------+------------+----------------+")
print("| S.No | Report_ID | User_ID | Similarity | Language       |")
print("+------+-----------+---------+------------+----------------+")

for i, report in enumerate(reports, start=1):
    print("| {:<4} | {:<9} | {:<7} | {:<10} | {:<14} |".format(
        i,
        report[0],
        report[1],
        report[2],
        report[5]  # language column
    ))

print("+------+-----------+---------+------------+----------------+")

conn.close()
