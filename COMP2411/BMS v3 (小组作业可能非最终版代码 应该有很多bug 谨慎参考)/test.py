import database as d
import administrator as ad
import attendee as at

# 连接数据库
d.connect('test.db')

# 初始化数据库
d.init()

# 管理员注册并登录
ad.reg("Yan", 318)
ad.reg("L", 0)
ad.login("Yan", 318)
ad.login("L", 0)

# 创建宴会
b = {
    'name': 'Gala Dinner',
    'date': '2023-12-31',
    'time': '19:00',
    'address': '456 Celebration Ave.',
    'location': 'Crystal Hall',
    'contact_staff': 'Jane Smith',
    'available': 'Y',  # 1 表示可用
    'quota': 150  # 宴会的名额
}
c = {
    'name': 'Gala Dinner',
    'date': '2024-12-30',
    'time': '19:00',
    'address': '456 Celebration Ave.',
    'location': 'Crystal Hall',
    'contact_staff': 'Jane Smith',
    'available': 'Y',  # 1 表示可用
    'quota': 150  # 宴会的名额
}
m = [
    {'dish_name': 'Grilled Salmon', 'meal_type': 'Main Course', 'price': 25.00, 'special_cuisine': 'Mediterranean'},
    {'dish_name': 'Vegetable Spring Rolls', 'meal_type': 'Appetizer', 'price': 8.00, 'special_cuisine': 'Asian'},
    {'dish_name': 'Chocolate Mousse', 'meal_type': 'Dessert', 'price': 6.50, 'special_cuisine': 'French'},
    {'dish_name': 'Caesar Salad', 'meal_type': 'Appetizer', 'price': 7.50, 'special_cuisine': 'Italian'}
]

# 添加宴会
ad.newBanquet(b, m)
# 更新宴会名称
bin_number = 1
update_key = 'BanquetName'
update_value = 'New Year Gala'
ad.updBanquet(bin_number, update_key, update_value)

# 注册与会者
a = {
    'AttendeeID': 2,
    'FirstName': "ZhangYang",
    'LastName': 'Yan',
    'Address': 'p',
    'AttendeeType': 'a',
    'Email': 'zhangyang@example.com',  # 这里换成有效的邮箱格式
    'Password': '12345678',
    'MobileNumber': '12345678',
    'AffiliatedOrganization': 'a'
}

# 创建新帐户
if at.newAccount(a):
    # 登录与会者
    attendeeId = at.login(a['Email'], a['Password'])
    
    # 报名宴会
    meal_choice = 'Grilled Salmon'  # 假设选择的餐点
    drink_choice = 'Tea'  # 假设选择的饮料
    remarks = 'Window seat preferred'  # 备注
    at.updateAccount('FirstName',"Yufan")
    at.test()
    if attendeeId:
        at.registration("2024/11/12", bin_number, meal_choice, drink_choice, remarks)
        print(at.search({'date':2023}))
        print(at.search({'available':'Y'}))

# 生成报告
ad.report()

# 提交更改并关闭数据库
d.commit()
d.close()