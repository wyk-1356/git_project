-- Этот файл инициализации будет выполнен при создании контейнера PostgreSQL
-- Все команды выполняются от имени пользователя postgres

-- Создание базы данных auth_db (если она не существует)
-- В среде Docker обычно база данных создается автоматически через переменную окружения POSTGRES_DB
-- Эта команда для дополнительной гарантии
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'auth_db') THEN
        CREATE DATABASE auth_db;
    END IF;
END
$$;

-- Подключение к базе данных auth_db не требуется в этом скрипте,
-- так как контейнер PostgreSQL автоматически подключается к правильной базе данных

-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы истории входов
CREATE TABLE IF NOT EXISTS login_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_agent TEXT,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Создание индексов для ускорения запросов
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_login_history_user_id ON login_history(user_id);

-- Добавление комментариев к таблицам
COMMENT ON TABLE users IS 'Таблица для хранения информации о пользователях системы аутентификации';
COMMENT ON TABLE login_history IS 'Таблица для хранения истории входов пользователей в систему';

-- Добавление комментариев к столбцам таблицы users
COMMENT ON COLUMN users.id IS 'Уникальный идентификатор пользователя (автоинкремент)';
COMMENT ON COLUMN users.email IS 'Электронная почта пользователя, используется для входа в систему';
COMMENT ON COLUMN users.hashed_password IS 'Хэшированный пароль пользователя (bcrypt)';
COMMENT ON COLUMN users.created_at IS 'Дата и время регистрации пользователя';
COMMENT ON COLUMN users.updated_at IS 'Дата и время последнего обновления данных пользователя';

-- Добавление комментариев к столбцам таблицы login_history
COMMENT ON COLUMN login_history.id IS 'Уникальный идентификатор записи о входе';
COMMENT ON COLUMN login_history.user_id IS 'Идентификатор пользователя, который выполнил вход';
COMMENT ON COLUMN login_history.user_agent IS 'Информация о браузере или клиенте, с которого выполнен вход';
COMMENT ON COLUMN login_history.login_time IS 'Дата и время успешного входа пользователя';

-- Создание пользователя базы данных (если используется отдельный пользователь)
-- Это уже настроено через переменные окружения в docker-compose.yml
-- CREATE USER auth_user WITH PASSWORD 'auth_password';
-- GRANT ALL PRIVILEGES ON DATABASE auth_db TO auth_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO auth_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO auth_user;