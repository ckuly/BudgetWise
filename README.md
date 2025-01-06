## BudgetWise

**BudgetWise** is a web application built with Django to help users manage their finances. Users can
track expenses, incomes, and savings goals while visualizing financial trends. The project emphasizes ease of use,
security, and data-driven insights into personal budgeting.

This project is licensed under the [MIT License](LICENSE).

---

### Core Features

- **Expense Management**: Add, edit, delete, and view expenses categorized by type (e.g., Food, Transport, Utilities).
- **Income Management**: Record multiple income sources such as salaries or side hustles.
- **Savings Goals**: Set and track progress toward savings goals with deadlines and targets.

### Additional Features

- **Dashboard**: Visual summaries of income, expenses, and savings via interactive charts.
- **Reports**: Export monthly or yearly financial reports as PDF/Excel files.
- **Authentication**: Secure login and registration system for user accounts.
- **Budget Alerts**: Notifications when expenses exceed predefined budgets.

---

### Backend

- **Django**: Web framework for scalable and secure application development.
- **SQLite**: Default database for development (PostgreSQL optional for production).

### Frontend

- **Bootstrap**: Responsive and modern design.
- **Chart.js**: Interactive data visualization for financial trends.

### Other Tools

- **Git**: Version control system.
- **Unit Tests**: Ensures stability and reliability.

---

## Installation

### Prerequisites

- Python 3.10+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PersonalFinanceTracker.git
   cd PersonalFinanceTracker
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the app in your browser at `http://127.0.0.1:8000/`.

---

## Usage

1. **Register/Login**: Create an account or log in to an existing one.
2. **Add Data**:
    - Use the dashboard to add expenses, incomes, and savings goals.
3. **View Trends**: Visualize spending patterns and savings progress.
4. **Export Reports**: Download financial summaries as needed.

---

## Contact

- **Developer**: Dom Paul
- **Email**: kyuakarago@gmail.com
- **GitHub**: [ckuly](https://github.com/ckuly)

