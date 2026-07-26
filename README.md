# Workout Application Backend

A Flask-based REST API backend for workout application management.

## Project Structure

```
Workout-Application-Backend/
├── .gitignore
├── Pipfile
├── README.md
└── server/
    ├── app.py              # Flask app + all API routes
    ├── models.py           # SQLAlchemy models, relationships, constraints, validations
    ├── schemas.py          # Marshmallow schemas + schema-level validations
    ├── seed.py             # Seed data script
    ├── app.db              # SQLite database
    └── migrations/         # Flask-Migrate migration scripts
```

## Setup

1. **Install dependencies:**
   ```bash
   pipenv install
   ```

2. **Activate the environment:**
   ```bash
   pipenv shell
   ```

3. **Initialize the database:**
   ```bash
   cd server
   flask db upgrade
   ```

4. **Seed the database (optional):**
   ```bash
   python seed.py
   ```

5. **Run the development server:**
   ```bash
   python app.py
   ```

## Development

### Create a new migration

```bash
flask db migrate -m "description of changes"
flask db upgrade
```

### Running tests

```bash
pytest
```
