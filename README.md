**BudgetWise** is a Django-powered web application designed to simplify personal finance management. Users can track
expenses, incomes, and savings goals while visualizing trends and generating financial insights.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ckuly/BudgetWise.git
   cd BudgetWise
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```
6. Open the app in your browser at `http://127.0.0.1:8000/`.

## Usage

1. **Register or Log In**: Create an account or access an existing one.
2. **Manage Finances**: Add expenses, incomes, and savings goals.
3. **Visualize Trends**: Use the dashboard to track financial progress.

## Contact

- **Developer**: Dom Paul
- **Email**: kyukarago@gmail.com
- **GitHub**: [ckuly](https://github.com/ckuly)

This project is licensed under the [MIT License](LICENSE).
