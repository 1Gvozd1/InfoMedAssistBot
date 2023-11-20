import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('users.db')
    cur = base.cursor()
    if base:
        print("Data base connected OK!")
    base.execute('CREATE TABLE IF NOT EXISTS user(id TEXT PRIMARY KEY, chat_id TEXT, substation TEXT, teamNumber TEXT, cardNumber TEXT)')
    # base.execute('CREATE TABLE IF NOT EXIST user(id TEXT PRIMARY KEY, chat_id TEXT, substation TEXT, teamNumber TEXT, cardNumber TEXT, address TEXT, genderAndAge TEXT, diagnosis TEXT, overallConditionSeverity TEXT, levelOfConsciousness TEXT, heartRate TEXT, bloodPressure TEXT, respiratoryRate TEXT, oxygenSaturation TEXT, bodyTemperature TEXT, crewPhone TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        # cur.execute('INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        cur.execute('INSERT INTO user VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit