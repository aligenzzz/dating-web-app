from psycopg2.extensions import connection as DbConnection
from psycopg2.extras import RealDictCursor

from models import Profile


class ProfileRepository:
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def get_profiles(self) -> list[Profile]:
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT profiles.*, locations.country, locations.city "
                "FROM profiles JOIN locations "
                "ON location_id = locations.id;",
                (id,),
            )
            profiles_data = cursor.fetchall()

            profiles = []
            for profile_data in profiles_data:
                profiles.append(Profile(**profile_data))

            return profiles

    def get_profiles_exclude_one(self, id: str) -> list[Profile]:
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT profiles.*, locations.country, locations.city "
                "FROM profiles JOIN locations "
                "ON location_id = locations.id WHERE "
                "profiles.id != %s;",
                (id,),
            )
            profiles_data = cursor.fetchall()

            profiles = []
            for profile_data in profiles_data:
                profiles.append(Profile(**profile_data))

            return profiles

    def get_profile(self, id: str) -> Profile | None:
        if not id or id.isspace():
            return None

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM profiles WHERE id = %s;",
                (id,),
            )
            profile_data = cursor.fetchone()

            if not profile_data:
                return None
            else:
                return Profile(**profile_data)

    def get_profile_by_user_id(self, user_id: str) -> Profile | None:
        if not user_id or user_id.isspace():
            return None

        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT profiles.* FROM users "
                "JOIN profiles ON profile_id = profiles.id "
                "WHERE users.id = %s;",
                (user_id,),
            )
            profile_data = cursor.fetchone()

            if not profile_data:
                return None
            else:
                return Profile(**profile_data)

    def add_profile(self, profile: Profile) -> Profile:
        with self._connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO locations (country, city) "
                "VALUES (%s, %s) RETURNING id;",
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
