import sqlite3

c=None
def init():
    global c
    

    # 创建 Administrator 表
    createAdministratorTable = '''
    CREATE TABLE IF NOT EXISTS Administrator (
        AdminID INTEGER PRIMARY KEY,
        Password TEXT NOT NULL,
        Name TEXT NOT NULL
    );
    '''
    c.execute(createAdministratorTable)

    # 创建 Banquet 表
    createBanquetTable = '''
    CREATE TABLE IF NOT EXISTS Banquet (
        Bin INTEGER PRIMARY KEY,
        BanquetName TEXT NOT NULL,
        Date TEXT NOT NULL,
        Time TEXT NOT NULL,
        Address TEXT NOT NULL,
        Location TEXT NOT NULL,
        ContactStaffName TEXT NOT NULL,
        Available CHAR(1) NOT NULL,
        Quota INTEGER NOT NULL
    );
    '''
    c.execute(createBanquetTable)

    # 创建 Meal 表
    createMealTable = '''
    CREATE TABLE IF NOT EXISTS Meal (
        MealID INTEGER PRIMARY KEY,
        Bin INTEGER,
        DishName TEXT NOT NULL,
        MealType TEXT NOT NULL,
        Price REAL NOT NULL,
        SpecialCuisine TEXT,
        FOREIGN KEY (Bin) REFERENCES Banquet (Bin)
    );
    '''
    c.execute(createMealTable)

    # 创建 Attendee 表
    createAttendeeTable = '''
    CREATE TABLE IF NOT EXISTS Attendee (
        AttendeeID INTEGER PRIMARY KEY,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Address TEXT NOT NULL,
        AttendeeType TEXT NOT NULL,
        Email TEXT NOT NULL,
        Password TEXT NOT NULL,
        MobileNumber TEXT NOT NULL,
        AffiliatedOrganization TEXT
    );
    '''
    c.execute(createAttendeeTable)

    # 创建 Registration 表
    createRegistrationTable = '''
    CREATE TABLE IF NOT EXISTS Registration (
        RegistrationID INTEGER PRIMARY KEY,
        RegistrationTime TEXT NOT NULL,
        SeatNumber INTEGER NOT NULL,
        MealChoice TEXT,
        DrinkChoice TEXT,
        Remarks TEXT
    );
    '''
    c.execute(createRegistrationTable)

    # 创建 Report 表
    createReportTable = '''
    CREATE TABLE IF NOT EXISTS Report (
    ReportID INTEGER PRIMARY KEY AUTOINCREMENT,
    RegistrationStatus TEXT NOT NULL,
    PopularMeals TEXT,
    AttendanceBehavior TEXT
);

    '''
    c.execute(createReportTable)

    # 创建 Manages 表
    createManagesTable = '''
    CREATE TABLE IF NOT EXISTS Manages (
        AdminID INTEGER,
        Bin INTEGER,
        Time TEXT NOT NULL,
        FOREIGN KEY (AdminID) REFERENCES Administrator (AdminID),
        FOREIGN KEY (Bin) REFERENCES Banquet (Bin),
        PRIMARY KEY (AdminID, Bin)
    );
    '''
    c.execute(createManagesTable)

    # 创建 Inputs 表
    createInputsTable = '''
    CREATE TABLE IF NOT EXISTS Inputs (
        AdminID INTEGER,
        MealID INTEGER,
        FOREIGN KEY (AdminID) REFERENCES Administrator (AdminID),
        FOREIGN KEY (MealID) REFERENCES Meal (MealID),
        PRIMARY KEY (AdminID, MealID)
    );
    '''
    c.execute(createInputsTable)

    # 创建 Books 表
    createBooksTable = '''
    CREATE TABLE IF NOT EXISTS Books (
        AttendeeID INTEGER,
        Bin INTEGER,
        RegistrationID INTEGER,
        FOREIGN KEY (AttendeeID) REFERENCES Attendee (AttendeeID),
        FOREIGN KEY (Bin) REFERENCES Banquet (Bin),
        FOREIGN KEY (RegistrationID) REFERENCES Registration (RegistrationID),
        PRIMARY KEY (AttendeeID, Bin, RegistrationID)
    );
    '''
    c.execute(createBooksTable)

    # 创建 Provides 表
    createProvidesTable = '''
    CREATE TABLE IF NOT EXISTS Provides (
        MealID INTEGER,
        Bin INTEGER,
        FOREIGN KEY (MealID) REFERENCES Meal (MealID),
        FOREIGN KEY (Bin) REFERENCES Banquet (Bin),
        PRIMARY KEY (MealID, Bin)
    );
    '''
    c.execute(createProvidesTable)

    # 创建 Searches 表
    createSearchesTable = '''
    CREATE TABLE IF NOT EXISTS Searches (
        AttendeeID INTEGER,
        RegistrationID INTEGER,
        FOREIGN KEY (AttendeeID) REFERENCES Attendee (AttendeeID),
        FOREIGN KEY (RegistrationID) REFERENCES Registration (RegistrationID),
        PRIMARY KEY (AttendeeID, RegistrationID)
    );
    '''
    c.execute(createSearchesTable)

    # 创建 UpdatesRegistration 表
    createUpdatesRegistrationTable = '''
    CREATE TABLE IF NOT EXISTS UpdatesRegistration (
        AttendeeID INTEGER,
        RegistrationID INTEGER,
        FOREIGN KEY (AttendeeID) REFERENCES Attendee (AttendeeID),
        FOREIGN KEY (RegistrationID) REFERENCES Registration (RegistrationID),
        PRIMARY KEY (AttendeeID, RegistrationID)
    );
    '''
    c.execute(createUpdatesRegistrationTable)

    # 创建 Generates 表
    createGeneratesTable = '''
    CREATE TABLE IF NOT EXISTS Generates (
        AdminID INTEGER,
        ReportID INTEGER,
        FOREIGN KEY (AdminID) REFERENCES Administrator (AdminID),
        FOREIGN KEY (ReportID) REFERENCES Report (ReportID),
        PRIMARY KEY (AdminID, ReportID)
    );
    '''
    c.execute(createGeneratesTable)


    print("初始化成功")
    # 提交创建表的操作
    commit()

# 注意，空的会自动创建新的
def connect(path):
    global c, conn
    try:
        conn = sqlite3.connect(path)
        c = conn.cursor()
        print("数据库打开成功")
    except sqlite3.Error as e:
        print(f"数据库连接失败: {e}")


def commit():
    global conn
    try:
        conn.commit()
        print("提交成功")
    except sqlite3.Error as e:
        print(f"提交失败: {e}")


def close():
    global conn
    try:
        conn.close()
        print("数据库关闭成功")
    except sqlite3.Error as e:
        print(f"关闭数据库时出错: {e}")


