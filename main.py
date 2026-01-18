import MySQL_connect as db
import Password as pw
import Create_Tables_script


# ================= DATABASE WRAPPER =================
class Database:
    def __init__(self, db):
        self.conn = db.conn
        self.cursor = db.cursor


database = Database(db)


# ================= BOOK =================
class Book:
    def __init__(self, db):
        self.db = db

    def add(self, title, author, copies):
        try:
            for _ in range(copies):
                self.db.cursor.execute(
                    "INSERT INTO BOOKS (BOOKTITLE, AUTHORNAME) VALUES (%s,%s)",
                    (title, author)
                )
            self.db.conn.commit()
            print("✅ Book(s) added successfully.")
        except self.db.mysql.connector.Error as err:
            self.db.conn.rollback()
            print("Error:", err)

    def is_available(self, book_id):
        self.db.cursor.execute(
            "SELECT BOOKID FROM BOOKS WHERE BOOKID=%s AND STATUS='AVAILABLE'",
            (book_id,)
        )
        return self.db.cursor.fetchone() is not None

    def mark_issued(self, book_id):
        self.db.cursor.execute(
            "UPDATE BOOKS SET STATUS='ISSUED' WHERE BOOKID=%s",
            (book_id,)
        )

    def mark_returned(self, book_id):
        self.db.cursor.execute(
            "UPDATE BOOKS SET STATUS='AVAILABLE' WHERE BOOKID=%s",
            (book_id,)
        )

    def view_all(self):
        self.db.cursor.execute("SELECT * FROM BOOKS")
        rows = self.db.cursor.fetchall()

        print("\nID  Title                     Author               Status       Added On            Updated On")
        print("-" * 115)
        for r in rows:
            print(f"{r[0]:<4} {r[1]:<25} {r[2]:<20} {r[3]:<12} {str(r[4])[:19]:<20} {str(r[5])[:19]}")


# ================= USER =================
class User:
    def __init__(self, db):
        self.db = db

    def add(self, name, email, phone, role, salary):
        self.db.cursor.execute(
            "INSERT INTO USERS (FULLNAME,EMAIL,PHONE,ROLE,SALARY) VALUES (%s,%s,%s,%s,%s)",
            (name, email, phone, role, salary)
        )
        self.db.conn.commit()
        print("✅ User added.")

    def exists(self, user_id):
        self.db.cursor.execute(
            "SELECT USERID FROM USERS WHERE USERID=%s",
            (user_id,)
        )
        return self.db.cursor.fetchone() is not None

    def view_all(self):
        self.db.cursor.execute("SELECT * FROM USERS")
        rows = self.db.cursor.fetchall()

        print("\nID  Name                 Email                    Phone          Role       Salary   Joined On           Updated On")
        print("-" * 140)
        for r in rows:
            print(f"{r[0]:<4} {r[1]:<20} {r[2]:<25} {r[3]:<15} {r[4]:<10} {float(r[5]):<8} {str(r[6])[:19]:<20} {str(r[7])[:19]}")


# ================= ISSUER =================
class Issuer:
    def __init__(self, db):
        self.db = db

    def add(self, name, email, phone):
        self.db.cursor.execute(
            "INSERT INTO ISSUERS (FULLNAME,EMAIL,PHONE) VALUES (%s,%s,%s)",
            (name, email, phone)
        )
        self.db.conn.commit()
        print("✅ Issuer added.")

    def exists(self, issuer_id):
        self.db.cursor.execute(
            "SELECT ISSUERID FROM ISSUERS WHERE ISSUERID=%s",
            (issuer_id,)
        )
        return self.db.cursor.fetchone() is not None

    def has_dues(self, issuer_id):
        self.db.cursor.execute(
            "SELECT SUM(FINE) FROM TRANSACTIONS WHERE ISSUEDBYID=%s AND STATUS='RETURNED AND FINE DUE'",
            (issuer_id,)
        )
        row = self.db.cursor.fetchone()
        return row and row[0] and row[0] > 0

    def view_all(self):
        self.db.cursor.execute("SELECT * FROM ISSUERS")
        rows = self.db.cursor.fetchall()

        print("\nID  Name                 Email                    Phone          Added On            Updated On")
        print("-" * 120)
        for r in rows:
            print(f"{r[0]:<4} {r[1]:<20} {r[2]:<25} {r[3]:<15} {str(r[4])[:19]:<20} {str(r[5])[:19]}")


# ================= TRANSACTION =================
class Transaction:
    def __init__(self, db, book):
        self.db = db
        self.book = book

    def issue(self, book_id, user_id, issuer_id):
        try:
            self.db.cursor.execute(
                "INSERT INTO TRANSACTIONS (BOOKID,ISSUEDTOID,ISSUEDBYID) VALUES (%s,%s,%s)",
                (book_id, user_id, issuer_id)
            )
            self.book.mark_issued(book_id)
            self.db.conn.commit()
            print("✅ Book issued.")
        except self.db.mysql.connector.Error as err:
            self.db.conn.rollback()
            print("Issue failed:", err)

    def return_book(self, book_id):
        self.db.cursor.execute(
            "SELECT DATEDIFF(CURRENT_TIMESTAMP,ISSUEDON) FROM TRANSACTIONS WHERE BOOKID=%s AND STATUS='ISSUED'",
            (book_id,)
        )
        row = self.db.cursor.fetchone()
        overdue = max(0, row[0] - 14) if row else 0
        fine = overdue * 2

        self.db.cursor.execute(
            "UPDATE TRANSACTIONS SET RETURNEDON=CURRENT_TIMESTAMP, STATUS=%s, FINE=%s WHERE BOOKID=%s AND STATUS='ISSUED'",
            ("RETURNED AND FINE DUE" if fine else "RETURNED", fine, book_id)
        )
        self.book.mark_returned(book_id)
        self.db.conn.commit()
        print("✅ Book returned.")

    def view_all(self):
        self.db.cursor.execute("SELECT * FROM TRANSACTIONS")
        rows = self.db.cursor.fetchall()

        print("\nTID  BID  UID  IID  Issued On           Returned On         Status                   Fine")
        print("-" * 120)
        for r in rows:
            print(f"{r[0]:<4} {r[1]:<4} {r[2]:<4} {r[3]:<4} {str(r[4])[:19]:<20} {str(r[5])[:19] if r[5] else '—':<20} {r[6]:<24} {float(r[7])}")

    def view_issuer_history(self, issuer_id):
        self.db.cursor.execute(
            "SELECT * FROM TRANSACTIONS WHERE ISSUEDBYID=%s",
            (issuer_id,)
        )
        rows = self.db.cursor.fetchall()

        print("\nTID  BID  UID  IID  Issued On           Returned On         Status                   Fine")
        print("-" * 120)
        for r in rows:
            print(f"{r[0]:<4} {r[1]:<4} {r[2]:<4} {r[3]:<4} {str(r[4])[:19]:<20} {str(r[5])[:19] if r[5] else '—':<20} {r[6]:<24} {float(r[7])}")


# ================= MAIN SYSTEM =================
class LibrarySystem:
    def __init__(self):
        self.book = Book(database)
        self.user = User(database)
        self.issuer = Issuer(database)
        self.transaction = Transaction(database, self.book)

    def menu(self):
        print("""
1. Add User
2. Add Issuer
3. Add Book
4. Issue Book
5. Return Book
6. Pay Dues
7. View Books
8. View Users
9. View Issuers
10. View All Transactions
11. View Issuer Transaction History
0. Exit
""")

    def run(self):
        if input("Enter Password: ") != pw.pswd:
            print("❌ Access Denied")
            return

        while True:
            self.menu()
            choice = int(input("Choice: "))

            if choice == 1:
                self.user.add(input("Name: "), input("Email: "), input("Phone: "), input("Role: "), float(input("Salary: ")))

            elif choice == 2:
                self.issuer.add(input("Name: "), input("Email: "), input("Phone: "))

            elif choice == 3:
                self.book.add(input("Title: "), input("Author: "), int(input("Copies: ")))

            elif choice == 4:
                b, u, i = int(input("Book ID: ")), int(input("User ID: ")), int(input("Issuer ID: "))
                if self.user.exists(u) and self.issuer.exists(i) and self.book.is_available(b) and not self.issuer.has_dues(i):
                    self.transaction.issue(b, u, i)
                else:
                    print("❌ Issue conditions failed.")

            elif choice == 5:
                self.transaction.return_book(int(input("Book ID: ")))

            elif choice == 6:
                iid = int(input("Issuer ID: "))
                database.cursor.execute(
                    "UPDATE TRANSACTIONS SET FINE=0, STATUS='RETURNED' WHERE ISSUEDBYID=%s AND STATUS='RETURNED AND FINE DUE'",
                    (iid,)
                )
                database.conn.commit()
                print("✅ Dues cleared.")

            elif choice == 7:
                self.book.view_all()

            elif choice == 8:
                self.user.view_all()

            elif choice == 9:
                self.issuer.view_all()

            elif choice == 10:
                self.transaction.view_all()

            elif choice == 11:
                self.transaction.view_issuer_history(int(input("Issuer ID: ")))

            elif choice == 0:
                print("Goodbye!")
                break


# ================= RUN =================
LibrarySystem().run()
