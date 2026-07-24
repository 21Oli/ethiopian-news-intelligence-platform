from sqlalchemy import text

from database.database import engine


print("=" * 60)
print("TESTING POSTGRESQL CONNECTION")
print("=" * 60)


try:

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT 1")
        )

        print(
            "\nPostgreSQL connection successful!"
        )

        print(
            f"Test result: {result.scalar()}"
        )


except Exception as e:

    print(
        "\nPostgreSQL connection failed."
    )

    print(
        f"Error: {e}"
    )