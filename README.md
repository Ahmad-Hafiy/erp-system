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
   git clone <YOUR_GITHUB_REPO_URL>
   cd <REPO_FOLDER_NAME>
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
   Open your browser at `http://127.0.0.1:8000/`.

---

## 3. Seed / Test Credentials

The database seeds with the following predefined roles for evaluation:

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `AdminPass2026!` | Accesses `/admin/` for master records and system management |
| **Manager** | `manager_dan` | `ErpTest2026!` | Assigned to Engineering Department; handles team approvals |
| **Staff** | `staff_alice` | `ErpTest2026!` | Submits leave, expense claims, and purchase orders |