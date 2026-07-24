from database.database import engine
from database.models import Base


print("=" * 60)
print("CREATING DATABASE TABLES")
print("=" * 60)


try:

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "\nDatabase tables created successfully."
    )

except Exception as e:

    print(
        "\nDatabase connection failed."
    )

    print(
        f"Error: {e}"
    )