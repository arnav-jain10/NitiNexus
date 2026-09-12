from sqlalchemy import inspect, text
from app.database import engine
from app import models  # noqa: F401


def main():
    inspector = inspect(engine)
    columns = {c["name"] for c in inspector.get_columns("schemes")}
    if "loan_min" not in columns:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE schemes ADD COLUMN loan_min FLOAT"))
        print("Added schemes.loan_min")
    else:
        print("schemes.loan_min already exists")


if __name__ == "__main__":
    main()
