import sqlite3
import json

# Załóżmy, że 'data' to Twój JSON
data = json.loads('./Threads.json'
                  )  # Załaduj JSON jako słownik Pythona

print(data)

# # Połączenie z bazą danych SQLite
# conn = sqlite3.connect('SQLite_Python.db')
# c = conn.cursor()

# # Utworzenie tabeli
# c.execute('''CREATE TABLE IF NOT EXISTS threads (
#     id TEXT PRIMARY KEY,
#     read BOOLEAN,
#     lastMessageDateTime TEXT,
#     interlocutor_login TEXT,
#     interlocutor_avatarUrl TEXT
# )''')

# # Wstawianie danych do tabeli
# for item in data['messages']:
#     # Zakładając, że struktura każdego elementu jest taka sama jak podana w przykładzie
#     thread = item['thread']
#     author = item['author']
#     c.execute("INSERT INTO threads (id, read, lastMessageDateTime, interlocutor_login, interlocutor_avatarUrl) VALUES (?, ?, ?, ?, ?)",
#               (thread['id'], item['status'] == 'DELIVERED', item['createdAt'], author['login'], author.get('avatarUrl')))

# # Zatwierdzenie zmian i zamknięcie połączenia
# conn.commit()
# conn.close()
