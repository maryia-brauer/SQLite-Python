import sqlite3

conn = sqlite3.connect('C:\Program Files\Microsoft VS Code\SQL&Python\SQLite&Python_db.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS emailaddress(
   user_name TEXT,
   full_address TEXT,
   fk_domain int,
   fk_day int, 
   foreign key (fk_day) references weekday (day_id),
   foreign key (fk_domain) references domain (domain_id));
""")
cur.execute("""CREATE TABLE IF NOT EXISTS domain(
   name TEXT,
   domain_id int);
""")
cur.execute("""CREATE TABLE IF NOT EXISTS weekday(
   name TEXT,
   day_id int);
""")
conn.commit()

file = open("C:\Program Files\Microsoft VS Code\SQL&Python\mbox.txt", "r")

id_domains = 0
id_day = 0
domains = dict()
days = dict()
for line in file:
    line = line.rstrip()
    if not line.startswith('From ') : continue
    words = line.split()
    email = words[1]
    user = email.split("@")[0]
    dom = email.split("@")[1]
    if dom not in domains :
        id_domains = id_domains + 1 
        domains[dom] = id_domains
        cur.execute("INSERT INTO domain (name, domain_id) VALUES (?, ?)", (dom, id_domains))
        conn.commit()
    day = words[2]
    if day not in days : 
        id_day = id_day + 1 
        days[day] = id_day
        cur.execute("INSERT INTO weekday (name, day_id) VALUES (?, ?)", (day, id_day))
        conn.commit()
    cur.execute("INSERT INTO emailaddress (user_name, full_address, fk_domain, fk_day) VALUES (?, ?, ?, ?)", (user, email, domains[dom], days[day]))
    conn.commit()

#s = input("Insert domain: ")
#small_s = s.strip()
#lower_s = small_s.lower()
#if s in domains:
    cur.execute("SELECT emailaddress.full_address, domain.name, weekday.name FROM emailaddress JOIN domain JOIN weekday ON emailaddress.fk_domain = domain.domain_id AND emailaddress.fk_day = weekday.day_id ")
    for data in cur:
        if (data[1] == lower_s and (data[2] == 'Fri' or data[2] == 'Sat')):
            print(data)
            continue
else :
    print("There is no data with your input")    
cur.close()
