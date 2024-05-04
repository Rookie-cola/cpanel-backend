import sqlite3


# Connecting to the database
conn = sqlite3.connect('database.db')

# Creating a cursor object
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username VARCHAR(32) UNIQUE NOT NULL,
                 password VARCHAR(32) NOT NULL)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS tokens
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 token VARCHAR(512) UNIQUE NOT NULL,
                 user_id INTEGER NOT NULL,
                 expires_at TIMESTAMP NOT NULL,
                 FOREIGN KEY (user_id) REFERENCES users(id))''')


cursor.execute('''CREATE TABLE IF NOT EXISTS ufw_ip
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ip VARCHAR(64) NOT NULL,
                 protocol VARCHAR(64) NOT NULL,
                 description VARCHAR(512),
                 is_allowed BOOLEAN NOT NULL)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS ufw_port
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 port VARCHAR(64) NOT NULL,
                 protocol VARCHAR(64) NOT NULL,
                 description VARCHAR(512),
                 is_allowed BOOLEAN NOT NULL)''')


# 插入用户数据
# cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", ('admin', 'admin'))

# 提交事务
conn.commit()

# 关闭数据库连接
conn.close()
