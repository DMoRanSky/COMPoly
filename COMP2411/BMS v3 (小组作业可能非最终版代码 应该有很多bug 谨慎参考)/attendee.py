import sqlite3

AID = None  # 全局变量，用于存储当前登录的与会者 ID

def newAccount(account):
    # 注册用户
    if not check(account):
        return False

    from database import c
    c.execute("INSERT INTO Attendee (AttendeeID, FirstName, LastName, Address, AttendeeType, Email, Password, MobileNumber, AffiliatedOrganization) VALUES (?,?,?,?,?,?,?,?,?)",
              (account['AttendeeID'], account['FirstName'], account['LastName'], account['Address'], account['AttendeeType'], 
               account['Email'], account['Password'], account['MobileNumber'], account['AffiliatedOrganization']))
    print("Account successfully created.")
    return True

def check(account):
    # 系统检查所有必填字段以正确格式填写
    if '@' not in account['Email']:
        print("Invalid email format.")
        return False
    if len(account['MobileNumber']) != 8 or not account['MobileNumber'].isdigit():
        print("Mobile number must be an 8-digit number.")
        return False
    if not account['FirstName'].isalpha() or not account['LastName'].isalpha():
        print("First and last names must contain only alphabetic characters.")
        return False
    return True

def updateAccount(type, newValue):
    # 更新账户数据
    if not isLoggedIn():
        print("You must be logged in to update the account.")
        return False

    from database import c

    if type == 'Email' and '@' not in newValue:
        print("Invalid email format.")
        return False
    if type == 'Mobile' and (len(newValue) != 8 or not newValue.isdigit()):
        print("Mobile number must be an 8-digit number.")
        return False
    if type in ['FirstName', 'LastName'] and not newValue.isalpha():
        print("Names must contain only alphabetic characters.")
        return False

    # 更新数据库
    c.execute(f"UPDATE Attendee SET {type} = ? WHERE AttendeeID = ?", (newValue, AID))
    print(f"Account updated: {type} set to {newValue}.") 
    return True

def test():
    from database import c
    c.execute("SELECT * FROM Attendee WHERE AttendeeID = ?", (AID,))
    user = c.fetchone()
    print(user)

def login(email, password):
    global AID  # 使用全局变量 AID
    from database import c

    c.execute("SELECT * FROM Attendee WHERE Email = ? AND Password = ?", (email, password))
    user = c.fetchone()

    if user:
        AID = user[0]  # 设置 AID 为当前登录用户的 AttendeeID
        print("Login successful.")
        return AID
    else:
        print("Invalid email or password.")
        return None

def isLoggedIn():
    """检查用户是否已登录."""
    return AID is not None

def getNextRegistrationId():
    from database import c

    # 查询当前 Registration 表中的行数
    c.execute("SELECT COUNT(*) FROM Registration")
    rowCount = c.fetchone()[0]

    # 返回下一个可用的 RegistrationID
    return rowCount + 1

def registration(registrationTime, binNumber, mealChoice, drinkChoice, remarks):
    if not isLoggedIn():
        print("You must be logged in to register.")
        return False

    from database import c

    # 检查宴会的座位配额
    c.execute("SELECT Quota, Available FROM Banquet WHERE Bin = ?", (binNumber,))
    banquet = c.fetchone()

    if not banquet:
        print("Banquet not found.")
        return False

    quota, available = banquet

    # 确保可用座位大于 0，并且不超过名额
    if available != 'Y':
        print("Not enough seats available.")
        return False

    # 获取下一个 RegistrationID
    rid = getNextRegistrationId()

    # 更新注册信息
    c.execute('''
        INSERT INTO Registration (RegistrationID, RegistrationTime, SeatNumber, MealChoice, DrinkChoice, Remarks) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (rid, registrationTime, available, mealChoice, drinkChoice, remarks))

    # 更新宴会的可用座位
    newquota = quota - 1  # 假设每次注册占用一个座位
    c.execute("UPDATE Banquet SET Quota = ? WHERE Bin = ?", (newquota, binNumber))
    if(quota==0):
        c.execute("UPDATE Banquet SET Available = ? WHERE Bin = ?", ('N', binNumber))

    # 在 Books 表中插入预订信息
    c.execute('''
        INSERT INTO Books (AttendeeID, Bin, RegistrationID) 
        VALUES (?, ?, ?)
    ''', (AID, binNumber, rid))

    print("Registration successful.")
    return True


def search(searchCriteria):
    """
    Registration Search: An attendee shall search for his/her registered banquets based on various criteria
    such as date, a part of banquet name, attendee type, etc.

    :param searchCriteria: A dictionary containing the search criteria. The keys can include:
        - 'date': The date of the banquet (string).
        - 'banquetName': A part of the banquet name (string).
        - 'attendeeType': The type of attendee (string).
        
    :return: A list of dictionaries, each representing a banquet with the following attributes:
        - 'name': The name of the banquet.
        - 'date': The date of the banquet.
        - 'time': The time of the banquet.
        - 'address': The address of the banquet.
        - 'location': The location of the banquet.
        - 'contact_staff': The name of the contact staff for the banquet.
        - 'available': The number of available seats for the banquet.
        - 'quota': The total quota of seats for the banquet.
    """
    if not isLoggedIn():
        print("You must be logged in to search for registrations.")
        return []

    from database import c

    # Initialize the base query for searching registrations
    query = """
    SELECT B.BanquetName, B.Date, B.Time, B.Address, B.Location, B.ContactStaffName, B.Available, B.Quota
    FROM Books AS Bk
    JOIN Registration AS R ON Bk.RegistrationID = R.RegistrationID
    JOIN Banquet AS B ON Bk.Bin = B.BIN  -- 使用全大写的 BIN
    WHERE Bk.AttendeeID = ?
    """
    params = [AID]  # 使用全局变量 AID

    # Add criteria based on the provided search criteria
    if searchCriteria.get('date'):
        query += " AND B.Date LIKE ?"
        params.append(f"%{searchCriteria['date']}%")
    
    if searchCriteria.get('banquetName'):
        query += " AND B.BanquetName LIKE ?"
        params.append(f"%{searchCriteria['banquetName']}%")
    
    if searchCriteria.get('attendeeType'):
        query += " AND R.AttendeeType = ?"
        params.append(searchCriteria['attendeeType'])
    
    if searchCriteria.get('available'):
        query += " AND B.Available = ?"
        params.append(searchCriteria['available'])

    # Execute the query with the parameters
    c.execute(query, params)
    results = c.fetchall()
    print(results)

    # Convert results into a list of dictionaries for easy access
    banquetList = []
    for row in results:
        banquetList.append({
            'name': row[0],
            'date': row[1],
            'time': row[2],
            'address': row[3],
            'location': row[4],
            'contact_staff': row[5],
            'available': row[6],
            'quota': row[7]
        })

    return banquetList

def updateRegistration(registrationId, key, value):
    if not isLoggedIn():
        print("You must be logged in to update the registration.")
        return False

    from database import c

    # 更新注册信息
    c.execute(f"UPDATE Registration SET {key} = ? WHERE RegistrationID = ?", (value, registrationId))

    # 在 UpdatesRegistration 表中插入更新信息
    c.execute('''
        INSERT INTO UpdatesRegistration (AttendeeID, RegistrationID) 
        VALUES (?, ?)
    ''', (AID, registrationId))

    print("Registration information updated.")
    return True