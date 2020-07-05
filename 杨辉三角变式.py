# x = ord('a')
# x=x+1
# print(chr(x))
def yanghui():
    L = ['a']
    while(True):
       yield L
       L=[chr(ord(L[i])+1) for i in range(len(L))]+[chr(ord(L[0])+1)]

final = input("请输入行数：")
n = 0
result = []
for t in yanghui():#如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator，
                     # generator是可被遍历的所以这个函数就成了可被遍历的了
    result.append(t)
    n = n+1
    if n == eval(final):
        break
for t in result:
    print(t)


