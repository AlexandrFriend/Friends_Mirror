import sqlite3
import sys

import os
DB = os.getenv("DATABASE_PATH", "/app/data/bot_database.db")

def clear_fakes():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    for fid in (900000001, 900000002, 900000003):
        cur.execute('DELETE FROM answers WHERE telegram_id = ?', (fid,))
        cur.execute('DELETE FROM users WHERE telegram_id = ?', (fid,))
    conn.commit()
    conn.close()
    print("Удалено 3 тестовых пользователя.")

def seed_fakes():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    fakes = [
        (900000001, 'TestUser_All0', 25, 'М', lambda i: 0, lambda i: 0),
        (900000002, 'TestUser_All1', 30, 'Ж', lambda i: 1, lambda i: 1),
        (900000003, 'TestUser_Alt', 22, 'Ж', lambda i: i % 2, lambda i: i % 2),
    ]
    for tid, nick, age, gender, q_fn, l_fn in fakes:
        cur.execute(
            'INSERT OR REPLACE INTO users (telegram_id, nickname, age, gender, consent) VALUES (?, ?, ?, ?, 1)',
            (tid, nick, age, gender)
        )
        cur.execute('DELETE FROM answers WHERE telegram_id = ?', (tid,))
        for i in range(1, 25):
            cur.execute(
                'INSERT OR REPLACE INTO answers (telegram_id, q_key, answer_index) VALUES (?, ?, ?)',
                (tid, f'q{i}', q_fn(i))
            )
        for i in range(1, 12):
            cur.execute(
                'INSERT OR REPLACE INTO answers (telegram_id, q_key, answer_index) VALUES (?, ?, ?)',
                (tid, f'l{i}', l_fn(i))
            )
    conn.commit()
    conn.close()
    print("Добавлено 3 тестовых пользователя: TestUser_All0, TestUser_All1, TestUser_Alt.")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'clear':
        clear_fakes()
    else:
        seed_fakes()
