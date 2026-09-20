# Multi-Module Company ERP System

A role-based ERP web application built with Python and Django. The system manages core enterprise workflows including Leave Requests, Expense Claims (with receipt file verification), and Procurement Purchase Orders, backed by strict server-side validation and access control.

---

## 1. Key Features & Hardening

* **Role-Based Access Control (RBAC)**: Distinct interfaces and permissions for Staff, Managers, and System Administrators.
* **State & Workflow Integrity**: State modifications (approvals and rejections) are strictly handled over CSRF-protected `POST` requests.
* **Self-Approval Prevention**: Managers cannot review or approve their own leave or procurement submissions.
* **Departmental Isolation**: Managers can only review submissions originating from staff within their assigned department.
* **Concurrency Protection**: Automated leave balance deductions run inside atomic database transactions (`@transaction.atomic`) to eliminate race conditions.
* **Input & Media Validation**: Server-side checks enforce chronological date ordering, positive item costs, receipt file extensions (`.pdf`, `.png`, `.jpg`), and upload size limits (5 MB).

---

## 2. Quickstart & Local Setup

### Prerequisites
* Python 3.10+
* Git

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Ahmad-Hafiy/erp-system.git
   cd erp-system
   ```

2. **Set Up a Virtual Environment**
   * **Windows**:
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   * **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations & Seed Test Data**
   ```bash
   python manage.py migrate
   python manage.py seed_data
   ```

5. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

---

## 3. Application Access & Portal Navigation

The application provides two separate portals depending on administrative needs:

* **Main ERP Portal**: Navigate to `http://127.0.0.1:8000/` (or `http://127.0.0.1:8000/login/`).
  * Used by **Staff** to create leave requests, expense claims, and purchase orders.
  * Used by **Managers** to submit their own requests and review team submissions in their department approval queue.
* **Admin Portal**: Navigate to `http://127.0.0.1:8000/admin/`.
  * Used by **Administrators** for system management, configuring departments, managing user roles, and adjusting global leave balances. 
  * If logged in as an Admin on the main portal, you can also access this via the **Admin Portal** button on the dashboard.

---

## 4. Seed / Test Credentials

The database seeds automatically with the following predefined accounts for evaluation:

| Role | Username | Password | Portal Entry Point | Purpose / Scope |
| :--- | :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `AdminPass2026!` | `http://127.0.0.1:8000/admin/` | System configuration, user management, and department records |
| **Manager** | `manager_dan` | `ErpTest2026!` | `http://127.0.0.1:8000/` | Engineering Department manager; evaluates pending team requests |
| **Staff** | `staff_alice` | `ErpTest2026!` | `http://127.0.0.1:8000/` | Engineering Department employee; submits leave, claims, and purchases |