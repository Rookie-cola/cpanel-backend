import sqlite3


# Connecting to the database
conn = sqlite3.connect('database.db')

# Creating a cursor object
cursor = conn.cursor()

# 创建一个users的表
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username VARCHAR(32) UNIQUE NOT NULL,
                 password VARCHAR(32) NOT NULL)''')
# 创建一个Token表
cursor.execute('''CREATE TABLE IF NOT EXISTS tokens
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 token VARCHAR(512) UNIQUE NOT NULL,
                 user_id INTEGER NOT NULL,
                 expires_at TIMESTAMP NOT NULL,
                 FOREIGN KEY (user_id) REFERENCES users(id))''')

# 插入数据
cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", ('admin', 'admin'))

# 提交事务
conn.commit()

# 关闭数据库连接
conn.close()
