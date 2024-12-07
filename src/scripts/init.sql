CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    address VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    photo_url VARCHAR(255) NOT NULL,
    hobbies VARCHAR(255),
    occupation VARCHAR(100),
    description VARCHAR(255),

    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_banned BOOLEAN DEFAULT FALSE,

    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    profile_id UUID NULL REFERENCES profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS actions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS complaints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content VARCHAR(255) NOT NULL,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    name VARCHAR(100) NOT NULL,
    image_url VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS chat_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    CONSTRAINT unique_chat_user UNIQUE (chat_id, user_id)
);

CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    content VARCHAR(255) NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS meetings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    name VARCHAR(100) NOT NULL,
    held_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    location_id UUID NOT NULL REFERENCES locations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS meeting_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    meeting_id UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    CONSTRAINT unique_meeting_user UNIQUE (meeting_id, user_id)
);

CREATE OR REPLACE FUNCTION delete_location_on_meeting_delete()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM locations
    WHERE id = OLD.location_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_delete_location
AFTER DELETE ON meetings
FOR EACH ROW
EXECUTE FUNCTION delete_location_on_meeting_delete();

INSERT INTO roles (id, name)
VALUES
    ('eb808052-1d0a-42a9-9273-b374ec789adf', 'admin'),
    ('88a14eaf-5a82-41e7-9224-48e86da7d9f0', 'user')
ON CONFLICT (id) DO NOTHING;

INSERT INTO users (username, password, role_id)
VALUES
    ('admin', 'admin', 'eb808052-1d0a-42a9-9273-b374ec789adf')
ON CONFLICT (username) DO NOTHING;
