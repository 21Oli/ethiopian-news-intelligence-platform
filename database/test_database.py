from sqlalchemy import text

from database.database import engine


def test_database():

    print("=" * 60)
    print("POSTGRESQL DATABASE VERIFICATION")
    print("=" * 60)

    try:
        with engine.connect() as connection:

            # 1. Test connection
            result = connection.execute(
                text("SELECT 1")
            )

            print("\nDatabase connection: SUCCESS")
            print("Connection test result:", result.scalar())

            # 2. Count articles
            result = connection.execute(
                text("SELECT COUNT(*) FROM articles")
            )

            article_count = result.scalar()

            print(
                f"\nTotal articles in database: {article_count}"
            )

            # 3. Get sample articles
            result = connection.execute(
                text("""
                    SELECT
                        id,
                        title,
                        author,
                        published_date
                    FROM articles
                    ORDER BY id
                    LIMIT 5
                """)
            )

            rows = result.fetchall()

            print("\nSample articles:")
            print("-" * 60)

            for row in rows:

                print(
                    f"ID: {row.id}"
                )

                print(
                    f"Title: {row.title}"
                )

                print(
                    f"Author: {row.author}"
                )

                print(
                    f"Published: {row.published_date}"
                )

                print("-" * 60)

            # 4. Check duplicate URLs
            result = connection.execute(
                text("""
                    SELECT COUNT(*) 
                    FROM (
                        SELECT article_url
                        FROM articles
                        GROUP BY article_url
                        HAVING COUNT(*) > 1
                    ) duplicates
                """)
            )

            duplicate_urls = result.scalar()

            print(
                f"\nDuplicate URL groups: {duplicate_urls}"
            )

            # 5. Check empty content
            result = connection.execute(
                text("""
                    SELECT COUNT(*)
                    FROM articles
                    WHERE content IS NULL
                       OR TRIM(content) = ''
                """)
            )

            empty_content = result.scalar()

            print(
                f"Articles with empty content: {empty_content}"
            )

            print("\n" + "=" * 60)
            print("DATABASE VERIFICATION COMPLETE")
            print("=" * 60)

    except Exception as e:

        print("\nDatabase verification failed.")

        print(
            f"Error: {e}"
        )


if __name__ == "__main__":
    test_database()