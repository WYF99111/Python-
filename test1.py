mystring = "[{'category': '吃点素的', 'chirldren': [{'id': 1, 'menu_name': '韭菜炒鸡蛋', 'picture': 'website1', 'menu_price': 15, 'menu_integral': 15, 'valid': 1}]},{'category': '吃炖好的', 'chirldren': [{'id': 2, 'menu_name': '东北呼饼', 'picture': 'website2', 'menu_price': 45, 'menu_integral': 45, 'valid': 1}]}, {'category': '吃点素的', 'chirldren': [{'id': 3, 'menu_name': '包菜粉丝', 'picture': 'website3', 'menu_price': 15, 'menu_integral': 15, 'valid': 1}]}]"
mystring=eval(mystring)
mydict={}
for i in mystring:
    mydict[i["category"]]=[]
for i in mystring:
    mydict[i["category"]].append(i["chirldren"])
s = input("请输入想吃的菜：")
print(mydict[s])