# Library Management System (Python + SQL)

A fully object-oriented **Library Management System** implemented using **Python and MySQL**, designed to demonstrate backend development concepts such as relational database design, SQL query handling, transaction management, and clean OOP architecture.

This project is a **menu-driven CLI application** with persistent database storage.

---

## 🚀 Features

- 📚 Add and manage books with availability tracking
- 👤 Add and manage library users
- 🧑‍💼 Add and manage issuers (library staff)
- 🔄 Issue and return books with rule enforcement
- 💰 Automatic fine calculation for late returns
- 📊 View complete transaction history
- 📜 View transaction history of a specific issuer
- 🔐 Password-protected system access
- 🧠 Object-Oriented Design (separation of concerns)

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Database:** MySQL  
- **Architecture:** Object-Oriented Programming (OOP)  
- **Interface:** Command Line Interface (CLI)  

---

## 🧩 Project Architecture

The system is structured using **independent classes**, each responsible for a single concern:

- `Database` – database connection wrapper
- `Book` – book operations and availability handling
- `User` – library user management
- `Issuer` – issuer management and dues tracking
- `Transaction` – issue, return, fine calculation, history
- `LibrarySystem` – main controller and menu handler

This design ensures:
- modularity
- readability
- easy maintenance
- clear responsibility boundaries

---

## 🗄️ Database Schema Overview

### BOOKS
- Book ID
- Title
- Author
- Status
- Added On
- Updated On

### USERS
- User ID
- Name
- Email
- Phone
- Role
- Salary
- Joined On
- Updated On

### ISSUERS
- Issuer ID
- Name
- Email
- Phone
- Timestamps

### TRANSACTIONS
- Transaction ID
- Book ID (FK)
- Issued To (FK)
- Issued By (FK)
- Issue Date
- Return Date
- Status
- Fine

All relationships are enforced using **foreign keys**.

---

## ⚙️ How to Run the Project

### 1️⃣ Clone the repository
```bash
git clone <repo-url>
cd library-management-system
