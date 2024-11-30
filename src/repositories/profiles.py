from psycopg2.extensions import connection as DbConnection

from models import Profile


class ProfileRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def add_profile(self, profile: Profile) -> Profile:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO locations (country, city) "
                "VALUES (%s, %s) "
                "RETURNING id;",
                (profile.country, profile.city),
            )
            location_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO profiles (first_name, last_name, age, "
                "photo_url, hobbies, occupation, description, location_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                (
                    profile.first_name,
                    profile.last_name,
                    profile.age,
                    profile.photo_url,
                    profile.hobbies,
                    profile.occupation,
                    profile.description,
                    location_id,
                ),
            )

            profile.id = cursor.fetchone()[0]
            return profile
