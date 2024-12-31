import sqlite3

AID = None

def newAID():
    from database import c
    c.execute("SELECT COUNT(*) FROM Administrator")
    count = c.fetchone()[0]  # 获取查询结果
    return count + 1

def adminExists(name):
    from database import c
    # 执行 SQL 查询，判断 Administrator 表中是否存在 Name 为指定值的记录
    c.execute("SELECT COUNT(*) FROM Administrator WHERE Name = ?", (name,))
    count = c.fetchone()[0]  # 获取查询结果
    return count > 0  # 如果 count 大于 0，则表示存在

# ----

def reg(name, pw):
    from database import c
    if (adminExists(name)):
        print(f"Admin {name} is already exist")
        return False
    id = newAID()
    c.execute("INSERT INTO Administrator VALUES (?, ?, ?);", (id, pw, name))
    print("Successfully reg!")
    return True

def login(name, pw):
    from database import c
    if not adminExists(name):
        print(f"Admin {name} is not exist")
        return False
    # 检查密码是否匹配
    c.execute("SELECT AdminID FROM Administrator WHERE Name = ? AND Password = ?", (name, pw))
    result = c.fetchone()  # 获取匹配的结果

    if result:
        global AID
        AID = result[0]  # 获取 AdminID
        print(f"Login successful for Admin {name}.")
        return True
    else:
        print(f"Incorrect password for Admin {name}.")
        return False


def newBanquet(banquet, meals):
    if AID is None:
        print("You need to login")
        return False

    from database import c

    # Insert the new banquet record
    c.execute('''
        INSERT INTO Banquet (BanquetName, Date, Time, Address, Location, ContactStaffName, Available, Quota)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (banquet['name'], banquet['date'], banquet['time'], banquet['address'],
          banquet['location'], banquet['contact_staff'], banquet['available'], banquet['quota']))

    # Get the newly inserted banquet's BIN (Banquet ID)
    banquetId = c.lastrowid

    print(f"New banquet created with BIN: {banquetId}")  # Debug print to verify the BIN number

    # Insert meal information and record the "Provides" relationship
    for meal in meals:
        c.execute('''
            INSERT INTO Meal (Bin, DishName, MealType, Price, SpecialCuisine)
            VALUES (?, ?, ?, ?, ?)
        ''', (banquetId, meal['dish_name'], meal['meal_type'], meal['price'], meal['special_cuisine']))

        # Get the newly inserted meal's MealID
        mealId = c.lastrowid

        # Insert the relationship between the meal and banquet into "Provides" table
        c.execute('''
            INSERT INTO Provides (MealID, Bin)
            VALUES (?, ?)
        ''', (mealId, banquetId))

    # Record the administrator's management of the banquet in the "Manages" table
    c.execute('''
        INSERT INTO Manages (AdminID, Bin, Time)
        VALUES (?, ?, ?)
    ''', (AID, banquetId, banquet['date'] + ' ' + banquet['time']))

    # Commit changes to the database
    print(f"Banquet with BIN {banquetId} created successfully with {len(meals)} meals.")
    return banquetId  # Return the actual BIN number


def updBanquet(BIN, key, value):
    if AID is None:
        print("You need to login")
        return False
    
    from database import c

    # 确保 key 是有效的
    valid_keys = ['BanquetName', 'Date', 'Time', 'Address', 'Location', 'ContactStaffName', 'Available', 'Quota']
    
    if key not in valid_keys:
        print(f"Invalid key: {key}. Must be one of {valid_keys}.")
        return False
    
    # 创建 SQL 更新语句
    query = f"UPDATE Banquet SET {key} = ? WHERE Bin = ?"
    
    # 执行更新操作
    c.execute(query, (value, BIN))
    
    # 提交更改
    print(f"Banquet with BIN {BIN} updated: {key} set to {value}.")
    return True

def report():
    if AID is None:
        print("You need to login")
        return False
    from database import c
    from datetime import datetime

    # Analyze registration count
    c.execute("SELECT COUNT(*) FROM Registration")
    registrationCount = c.fetchone()[0]

    # Analyze the most popular meal
    c.execute("SELECT MealChoice, COUNT(*) as Count FROM Registration GROUP BY MealChoice ORDER BY Count DESC LIMIT 1")
    popularMeal = c.fetchone()
    popularMealName = popularMeal[0] if popularMeal else "No meal selected"

    # Analyze attendee count
    c.execute("SELECT COUNT(*) as AttendeeCount FROM Attendee")
    attendeeCount = c.fetchone()[0]

    # Report generation time
    generatedTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    c.execute("SELECT COUNT(*) FROM Report")
    reportID = c.fetchone()[0] + 1

    # # Check if a report for this AdminID already exists
    # c.execute('''
    #     SELECT COUNT(*) FROM Generates WHERE AdminID = ? AND ReportID = ?
    # ''', (AID, registrationCount))  # Assuming ReportID is based on registrationCount

    # # If the report already exists, we skip inserting it
    # if c.fetchone()[0] > 0:
    #     print(f"Report for Admin {AID} with ReportID {registrationCount} already exists.")
    #     return False  # Return False to indicate that the report wasn't generated

    # Insert the report into the Generates table if not already present
    #print(AID, reportID, "??inss")
    c.execute('''
        INSERT INTO Generates (AdminID, ReportID)
        VALUES (?, ?)
    ''', (AID, reportID))

    # Print the report details (for debugging purposes)
    print("Report generated successfully.")
    print(f"Registration Count: {registrationCount}")
    print(f"Popular Meal: {popularMealName}")
    print(f"Attendee Count: {attendeeCount}")
    print(f"Report Generated Time: {generatedTime}")


    c.execute('''
        INSERT INTO Report (ReportID, RegistrationStatus, PopularMeals, AttendanceBehavior)
        VALUES (?, ?, ?, ?)
    ''', (reportID, registrationCount, popularMealName, attendeeCount))

    return True


def get_report_content():
    if AID is None:
        print("You need to login")
        return "You need to login"

    from database import c
    from datetime import datetime

    # 分析注册状态
    c.execute("SELECT COUNT(*) FROM Registration")
    registrationCount = c.fetchone()[0]

    # 分析流行餐点
    c.execute("SELECT MealChoice, COUNT(*) as Count FROM Registration GROUP BY MealChoice ORDER BY Count DESC LIMIT 1")
    popularMeal = c.fetchone()
    popularMealName = popularMeal[0] if popularMeal else "No meal selected"

    # 分析出席行为
    c.execute("SELECT COUNT(*) as AttendeeCount FROM Attendee")
    attendeeCount = c.fetchone()[0]

    # 生成时间
    generatedTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format the report content as a string
    report_content = f"""
    Registration Count: {registrationCount}
    Popular Meal: {popularMealName}
    Attendee Count: {attendeeCount}
    Report Generated Time: {generatedTime}
    """
    return report_content
