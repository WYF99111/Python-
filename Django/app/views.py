#   coding:utf-8
from django.shortcuts import render  # 渲染模板
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import time
import random
import json
import csv
import os
from django.utils.encoding import escape_uri_path

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}  # 浏览器标识伪装


def updata_captcha(request):  # request参数为必须，不然报错
    mytuple = captcha()#接收captcha()的返回值
    if mytuple[0] == 'src':#若mytuple第一个元素为'src'
        name_dict = {#定义一个字典
            'src': mytuple[1],#src为验证码图片
            'webcookie': json.dumps(mytuple[2])#将head['cookie']对应的值转为字符串
        }
    else:
        name_dict = {'src': 'None'}
    return HttpResponse(json.dumps(name_dict), content_type='application/json')#将name_dict以字符串形式返回


def captcha():
    try:
        head['Cookie'] = ''
        head['Referer'] = 'http://bkjw.sxu.edu.cn/home.aspx'#告诉web服务器是从'http://bkjw.sxu.edu.cn/home.aspx'页面来的
        r = requests.get('http://bkjw.sxu.edu.cn/_data/login.aspx?', headers=head, timeout=10)#向网站发起请求，并获取响应对象
        if r.status_code == 200:#若连接成功
            cookiedict = requests.utils.dict_from_cookiejar(r.cookies)#利用request获取cookie
            head['Cookie'] = 'name=value; myCookie=; ASP.NET_SessionId=' + cookiedict[
                'ASP.NET_SessionId'] + '; name=value'#请求标头的Cookie: myCookie=; ASP.NET_SessionId=xdzbx1vudn2guhpwqfvejwsq
            head['Referer'] = 'http://bkjw.sxu.edu.cn/_data/login.aspx'#请求URL
            r = requests.get('http://bkjw.sxu.edu.cn/sys/ValidateCode.aspx', headers=head, timeout=10)#向网站发起请求，并获取响应对象，返回一个图片
            if r.status_code == 200:#若连接成功
                localtime = time.localtime(time.time())#获取当前时间
                _time = str(localtime[0]) + str(localtime[1]) + str(localtime[2]) + str(localtime[3])#将年月日小时组成字符串
                name = random.sample('zyxwvutsrqponmlkjihgfedcba', 10)# 多个字符中生成指定长度的随机字符
                _name = ''#定义空字符串用来存文件名
                for x in name:#遍历形成当前时间+随机10字符+'captcha.jpg'的指定格式
                    _name += x
                _time = _time + _name + 'captcha.jpg'
                with open('app/media/' + _time, 'wb') as fp:#写入
                    fp.write(r.content)
                return ('src', "/media/" + _time, head['Cookie'])
            else:#若请求失败则记录日志
                localtime = time.localtime(time.time())
                out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                           'a', newline='')
                csv_write = csv.writer(out, dialect='excel')
                data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                        'http://bkjw.sxu.edu.cn/sys/ValidateCode.aspx']
                csv_write.writerow(data)
                out.close()
        else:#若请求失败则记录日志
            localtime = time.localtime(time.time())
            out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                       newline='')
            csv_write = csv.writer(out, dialect='excel')
            data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                    'http://bkjw.sxu.edu.cn/_data/login.aspx']
            csv_write.writerow(data)
            out.close()
        return ('error', '服务器维护中，点击左上角X图标退出')#请求失败返回错误

    except requests.ConnectTimeout:#连接超时返回错误
        return ('error', '服务器维护中，点击左上角X图标退出')

    except Exception as e:#处理异常，并记录日志
        localtime = time.localtime(time.time())
        out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                   newline='')
        csv_write = csv.writer(out, dialect='excel')
        data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                '函数captcha()：未进行容错处理的情况：' + str(e)]
        csv_write.writerow(data)
        out.close()
        return ('error', '点击左上角X图标退出')#返回错误


def login(request):
    try:
        head['Cookie'] = request.POST.get('webcookie', '')#接收从前端表单中传过来的webcookie
        form = {}
        form['Sel_Type'] = request.POST.get('Sel_Type', '')  # 身份标识
        if form['Sel_Type'] != 'STU' and form['Sel_Type'] != 'TEA':#若身份不为学生或教师则返回错误页面
            return render(request, 'error.html', {'error': '点击左上角X图标退出'})
        form['txt_asmcdefsddsd'] = request.POST.get('id', '')#接收从前端表单中传过来的id
        if (form['txt_asmcdefsddsd'] != ''):#若'txt_asmcdefsddsd'所对应的值不为空则记录日志
            localtime = time.localtime(time.time())
            out = open(
                'app/user_login/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                newline='')
            csv_write = csv.writer(out, dialect='excel')
            data = [str(localtime[0]) + '-' + str(localtime[1]) + '-' + str(localtime[2]) + ' ' + str(
                localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]), form['txt_asmcdefsddsd']]
            csv_write.writerow(data)
            out.close()
        form['dsdsdsdsdxcxdfgfg'] = request.POST.get('pwd', '')#接收从前端表单中传过来的pwd
        form['fgfggfdgtyuuyyuuckjg'] = request.POST.get('code', '')#接收从前端表单中传过来的code
        head['Referer'] = 'http://bkjw.sxu.edu.cn/_data/login.aspx'
        r = requests.post('http://bkjw.sxu.edu.cn/_data/login.aspx', headers=head, data=form, timeout=10)#向网站发起请求，并获取响应对象
        if r.status_code == 200:#若请求成功
            head['Referer'] = 'http://bkjw.sxu.edu.cn/_data/login.aspx'#让头部'Referer'所对应的值为'http://bkjw.sxu.edu.cn/_data/login.aspx'
            r = requests.get('http://bkjw.sxu.edu.cn/MAINFRM.aspx', headers=head, timeout=10)#向网站发起请求，并获取响应对象
            if r.status_code == 200:#若请求成功
                django_type = request.POST.get('django_type', '')#接收从前端表单传来的django_type
                if r.text[5] != 'h':  # 验证失败以h开头 成功以！开头   判断是否验证成功
                    if form['Sel_Type'] == 'STU':#登录身份为学生
                        # 学生已登录教务系统·····

                        # 学生查课表模块
                        if django_type == 'course':
                            mytuple = get_student_course(head['Cookie'], request.POST.get('randomstr', ''),
                                                         request.POST.get('hidsjyzm', ''))
                            if mytuple[0] == 'src':
                                return render(request, 'student_course.html', {'src': mytuple[1]})
                            else:
                                return render(request, 'error.html', {'error': mytuple[1]})

                                # 学生查成绩模块
                        if django_type == 'grade':#若django_type为'grade'则调用学生查成绩模块
                            mytuple = get_student_grade(head['Cookie'])
                            if mytuple[0] == 'src':#若mytuple第一个元素为'src'
                                return render(request, 'student_grade.html', {'src': mytuple[1]})#把get_student_grade()形成的成绩文件返回给'student_grade.html'
                            else:
                                return render(request, 'error.html', {'error': mytuple[1]})#失败则返回错误页面

                                # 学生查考试安排
                        if django_type == 'exame':
                            mytuple = get_student_exame(head['Cookie'])
                            if mytuple[0] == 'src':
                                return render(request, 'student_exame.html', {'src': mytuple[1]})
                            else:
                                return render(request, 'error.html', {'error': mytuple[1]})
                    else:
                        # 教师已登录教务系统·····
                        # 教师查课表模块
                        if django_type == 'course':
                            mytuple = get_teacher_course(head['Cookie'])
                            if mytuple[0] == 'value':
                                return render(request, 'teacher_course.html', {'value': mytuple[1]})
                            else:
                                return render(request, 'error.html', {'error': mytuple[1]})

                else:
                    if form['Sel_Type'] == 'STU':
                        if django_type == 'course':
                            return render(request, 'student_course_find_login_error.html')
                        if django_type == 'grade':
                            return render(request, 'student_grade_find_login_error.html')
                        if django_type == 'exame':
                            return render(request, 'student_exame_find_login_error.html')
                    else:
                        return render(request, 'teacher_course_find_login_error.html')
            else:
                localtime = time.localtime(time.time())
                out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                           'a', newline='')
                csv_write = csv.writer(out, dialect='excel')
                data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                        'http://bkjw.sxu.edu.cn/MAINFRM.aspx']
                csv_write.writerow(data)
                out.close()
        else:
            localtime = time.localtime(time.time())
            out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                       newline='')
            csv_write = csv.writer(out, dialect='excel')
            data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                    'http://bkjw.sxu.edu.cn/_data/login.aspx']
            csv_write.writerow(data)
            out.close()
        return render(request, 'error.html', {'error': '服务器维护中，点击左上角X图标退出'})

    except requests.ConnectTimeout:
        return render(request, 'error.html', {'error': '服务器维护中，点击左上角X图标退出'})

    except Exception as e:
        localtime = time.localtime(time.time())
        out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                   newline='')
        csv_write = csv.writer(out, dialect='excel')
        data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]), '函数login()：未进行容错处理的情况：' + str(e)]
        csv_write.writerow(data)
        out.close()
        return render(request, 'error.html', {'error': '点击左上角X图标退出'})


def student_course_find(request):
    mytuple = captcha()
    if mytuple[0] == 'src':
        return render(request, 'student_course_find.html', {'src': mytuple[1], 'webcookie': json.dumps(mytuple[2])})
    else:
        return render(request, 'error.html', {'error': mytuple[1]})


def get_student_course(webcookie, randomstr, hidsjyzm):
    try:
        head['Cookie'] = webcookie
        head['Referer'] = 'http://bkjw.sxu.edu.cn/SYS/menu.aspx'
        r = requests.get('http://bkjw.sxu.edu.cn/znpk/Pri_StuSel.aspx', headers=head, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            form = {  # 这四个个缺一不可
                'Sel_XNXQ': '20191',
                'rad': '0',
                'hidyzm': soup.table.contents[5].input.attrs['value']  # 获取权限补充的‘类’cookice
            }
            form['hidsjyzm'] = hidsjyzm
            head['Referer'] = 'http://bkjw.sxu.edu.cn/znpk/Pri_StuSel.aspx'
            r = requests.post('http://bkjw.sxu.edu.cn/znpk/Pri_StuSel_rpt.aspx?m=' + randomstr, headers=head, data=form,
                              timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                head['Referer'] = 'http://bkjw.sxu.edu.cn/znpk/Pri_StuSel_rpt.aspx?m=' + randomstr
                r = requests.get(
                    'http://bkjw.sxu.edu.cn/znpk/' + soup.img.attrs['src'][:-29] + '&xnxq=20191&param_xh=' +
                    soup.img.attrs['src'][-12:], headers=head, timeout=10)
                if r.status_code == 200:
                    localtime = time.localtime(time.time())
                    _time = str(localtime[0]) + str(localtime[1]) + str(localtime[2]) + str(localtime[3])
                    name = random.sample('zyxwvutsrqponmlkjihgfedcba', 10)
                    _name = ''
                    for x in name:
                        _name += x
                    _time = _time + _name + 'student_course.jpg'
                    with open('app/media/' + _time, 'wb') as fp:
                        fp.write(r.content)
                    localtime = time.localtime(time.time())
                    out = open('app/user_all/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(
                        localtime[2]) + '.csv', 'a', newline='')
                    csv_write = csv.writer(out, dialect='excel')
                    data = [str(localtime[0]) + '-' + str(localtime[1]) + '-' + str(localtime[2]) + ' ' + str(
                        localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]), '使用了学生课表查询服务']
                    csv_write.writerow(data)
                    out.close()
                    return ('src', "/media/" + _time)
                else:
                    localtime = time.localtime(time.time())
                    out = open(
                        'app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                        'a', newline='')
                    csv_write = csv.writer(out, dialect='excel')
                    data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                            'http://bkjw.sxu.edu.cn/znpk/Pri_StuSel_Drawimg.aspx?type=1&' + soup.img.attrs['src'][
                                                                                            -41:-29] + '&xnxq=20191&param_xh=' +
                            soup.img.attrs['src'][-12:]]
                    csv_write.writerow(data)
                    out.close()
            else:
                localtime = time.localtime(time.time())
                out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                           'a', newline='')
                csv_write = csv.writer(out, dialect='excel')
                data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                        'http://bkjw.sxu.edu.cn/znpk/Pri_StuSel_rpt.aspx?m=' + randomstr]
                csv_write.writerow(data)
                out.close()
        else:
            localtime = time.localtime(time.time())
            out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                       newline='')
            csv_write = csv.writer(out, dialect='excel')
            data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                    'http://bkjw.sxu.edu.cn/znpk/Pri_StuSel.aspx']
            csv_write.writerow(data)
            out.close()
        return ('error', '服务器维护中，点击左上角X图标退出')
    except requests.ConnectTimeout:
        return ('error', '服务器维护中，点击左上角X图标退出')

    except Exception as e:
        localtime = time.localtime(time.time())
        out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                   newline='')
        csv_write = csv.writer(out, dialect='excel')
        data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                '函数get_student_course()：未进行容错处理的情况：' + str(e)]
        csv_write.writerow(data)
        out.close()
        return ('error', '点击左上角X图标退出')


def teacher_course_find(request):
    mytuple = captcha()
    if mytuple[0] == 'src':
        return render(request, 'teacher_course_find.html', {'src': mytuple[1], 'webcookie': json.dumps(mytuple[2])})
    else:
        return render(request, 'error.html', {'error': mytuple[1]})


def get_teacher_course(webcookie):
    try:
        head['Cookie'] = webcookie
        form = {
            'Sel_XNXQ': '20191',
            'rad': '0',
        }
        head['Referer'] = 'http://bkjw.sxu.edu.cn/znpk/Pri_TeacSel.aspx'
        r = requests.post('http://bkjw.sxu.edu.cn/znpk/Pri_TeacSel_rpt.aspx', headers=head, data=form, timeout=10)
        if r.status_code == 200:
            r.encoding = 'gbk'
            soup = BeautifulSoup(r.text, 'html.parser')
            localtime = time.localtime(time.time())
            out = open('app/user_all/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                       'a', newline='')
            csv_write = csv.writer(out, dialect='excel')
            data = [str(localtime[0]) + '-' + str(localtime[1]) + '-' + str(localtime[2]) + ' ' + str(
                localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]), '使用了教师课表查询服务']
            csv_write.writerow(data)
            out.close()
            return ('value', str(soup.div))
        else:
            localtime = time.localtime(time.time())
            out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                       newline='')
            csv_write = csv.writer(out, dialect='excel')
            data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                    'http://bkjw.sxu.edu.cn/znpk/Pri_TeacSel_rpt.aspx']
            csv_write.writerow(data)
            out.close()
        return ('error', '服务器维护中，点击左上角X图标退出')
    except requests.ConnectTimeout:
        return ('error', '服务器维护中，点击左上角X图标退出')

    except Exception as e:
        localtime = time.localtime(time.time())
        out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                   newline='')
        csv_write = csv.writer(out, dialect='excel')
        data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                '函数get_teacher_course()：未进行容错处理的情况：' + str(e)]
        csv_write.writerow(data)
        out.close()
        return ('error', '点击左上角X图标退出')


def student_grade_find(request):
    mytuple = captcha()#接收captcha()返回值
    if mytuple[0] == 'src':#若mytuple第一个元素为'src'
        return render(request, 'student_grade_find.html', {'src': mytuple[1], 'webcookie': json.dumps(mytuple[2])})#将验证码和head['cookie']返回给student_grade_find.html
    else:
        return render(request, 'error.html', {'error': mytuple[1]})#返回错误信息


def get_student_grade(webcookie):
    try:
        head['Cookie'] = webcookie#将前端传的webcookie传到head['Cookie']中
        form = {#模拟网页表单数据
            'sel_xn': '2019',
            'sel_xq': '1',
            'SJ': '0',
            'SelXNXQ': '2',
            'zfx_flag': '0'
        }
        head['Referer'] = 'http://bkjw.sxu.edu.cn/xscj/Stu_MyScore.aspx'#告诉web服务器网页是从'http://bkjw.sxu.edu.cn/xscj/Stu_MyScore.aspx'过来的
        r = requests.post('http://bkjw.sxu.edu.cn/xscj/Stu_MyScore_rpt.aspx', headers=head, data=form, timeout=10)#向该网页发出请求
        if r.status_code == 200:#若请求成功
            r.encoding = 'gbk'#网页内容编码转为‘gbk’
            soup = BeautifulSoup(r.text, 'html.parser')#对网页进行爬取
            head['Referer'] = 'http://bkjw.sxu.edu.cn/xscj/Stu_MyScore_rpt.aspx'#告诉web服务器网页是从'http://bkjw.sxu.edu.cn/xscj/Stu_MyScore_rpt.aspx'过来的
            r = requests.get(
                'http://bkjw.sxu.edu.cn/xscj/' + soup.img.attrs['src'][:-18] + "&param_xh=" + soup.img.attrs['src'][
                                                                                              -12:], headers=head,
                timeout=10)#从img标签中提取src属性的后18个字符和后12个字符拼到网址链接中，对该网页发送请求
            if r.status_code == 200:#若请求成功，将学生成绩写入xxxstudent_grade.jpg文件中并记录日志
                localtime = time.localtime(time.time())
                _time = str(localtime[0]) + str(localtime[1]) + str(localtime[2]) + str(localtime[3])
                name = random.sample('zyxwvutsrqponmlkjihgfedcba', 10)
                _name = ''
                for x in name:
                    _name += x
                _time = _time + _name + 'student_grade.jpg'
                with open('app/media/' + _time, 'wb') as fp:
                    fp.write(r.content)
                localtime = time.localtime(time.time())
                out = open(
                    'app/user_all/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                    'a', newline='')
                csv_write = csv.writer(out, dialect='excel')
                data = [str(localtime[0]) + '-' + str(localtime[1]) + '-' + str(localtime[2]) + ' ' + str(
                    localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]), '使用了学生成绩查询服务']
                csv_write.writerow(data)
                out.close()
                return ('src', "/media/" + _time)
            else:#请求失败则记录访问失败日志
                localtime = time.localtime(time.time())
                out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                           'a', newline='')
                csv_write = csv.writer(out, dialect='excel')
                data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                        'http://bkjw.sxu.edu.cn/xscj/' + soup.img.attrs['src'][:-18] + "&param_xh=" + soup.img.attrs[
                                                                                                          'src'][-12:]]
                csv_write.writerow(data)
                out.close()
                return ('error', '服务器维护中，点击左上角X图标退出')
        else:#请求失败则记录访问失败日志
            localtime = time.localtime(time.time())
            out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                       newline='')
            csv_write = csv.writer(out, dialect='excel')
            data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                    'http://bkjw.sxu.edu.cn/xscj/Stu_MyScore_rpt.aspx']
            csv_write.writerow(data)
            out.close()
        return ('error', '服务器维护中，点击左上角X图标退出')
    except requests.ConnectTimeout:
        return ('error', '服务器维护中，点击左上角X图标退出')

    except Exception as e:
        localtime = time.localtime(time.time())
        out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                   newline='')
        csv_write = csv.writer(out, dialect='excel')
        data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                '函数get_student_grade()：未进行容错处理的情况：' + str(e)]
        csv_write.writerow(data)
        out.close()
        return ('error', '点击左上角X图标退出')


def student_exame_find(request):
    mytuple = captcha()
    if mytuple[0] == 'src':
        return render(request, 'student_exame_find.html', {'src': mytuple[1], 'webcookie': json.dumps(mytuple[2])})
    else:
        return render(request, 'error.html', {'error': mytuple[1]})


def get_student_exame(webcookie):
    try:
        head['Cookie'] = webcookie
        form = {
            'sel_xnxq': '20190',
            'sel_lcxz': '2',
            'sel_lc': '2019004'
        }
        head['Referer'] = 'http://bkjw.sxu.edu.cn/KSSW/stu_ksap.aspx'
        r = requests.post('http://bkjw.sxu.edu.cn/KSSW/stu_ksap_rpt.aspx', headers=head, data=form, timeout=10)
        if r.status_code == 200:
            r.encoding = 'gbk'
            soup = BeautifulSoup(r.text, 'html.parser')
            head['Referer'] = 'http://bkjw.sxu.edu.cn/KSSW/stu_ksap_rpt.aspx'
            r = requests.get(
                'http://bkjw.sxu.edu.cn/KSSW/' + soup.img.attrs['src'][:-18] + "&param_xh=" + soup.img.attrs['src'][
                                                                                              -12:], headers=head,
                timeout=10)
            if r.status_code == 200:
                localtime = time.localtime(time.time())
                _time = str(localtime[0]) + str(localtime[1]) + str(localtime[2]) + str(localtime[3])
                name = random.sample('zyxwvutsrqponmlkjihgfedcba', 10)
                _name = ''
                for x in name:
                    _name += x
                _time = _time + _name + 'student_exame.jpg'
                with open('app/media/' + _time, 'wb') as fp:
                    fp.write(r.content)
                localtime = time.localtime(time.time())
                out = open(
                    'app/user_all/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                    'a', newline='')
                csv_write = csv.writer(out, dialect='excel')
                data = [str(localtime[0]) + '-' + str(localtime[1]) + '-' + str(localtime[2]) + ' ' + str(
                    localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]), '使用了学生考试安排查询服务']
                csv_write.writerow(data)
                out.close()
                return ('src', "/media/" + _time)
            else:
                localtime = time.localtime(time.time())
                out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                           'a', newline='')
                csv_write = csv.writer(out, dialect='excel')
                data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                        'http://bkjw.sxu.edu.cn/KSSW/' + soup.img.attrs['src'][:-18] + "&param_xh=" + soup.img.attrs[
                                                                                                          'src'][-12:]]
                csv_write.writerow(data)
                out.close()
                return ('error', '服务器维护中，点击左上角X图标退出')
        else:
            localtime = time.localtime(time.time())
            out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                       newline='')
            csv_write = csv.writer(out, dialect='excel')
            data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                    'http://bkjw.sxu.edu.cn/KSSW/stu_ksap_rpt.aspx']
            csv_write.writerow(data)
            out.close()
        return ('error', '服务器维护中，点击左上角X图标退出')
    except requests.ConnectTimeout:
        return ('error', '服务器维护中，点击左上角X图标退出')

    except Exception as e:
        localtime = time.localtime(time.time())
        out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                   newline='')
        csv_write = csv.writer(out, dialect='excel')
        data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                '函数get_student_exame()：未进行容错处理的情况：' + str(e)]
        csv_write.writerow(data)
        out.close()
        return ('error', '点击左上角X图标退出')


def section_course_find(request):
    mytuple = captcha()
    if mytuple[0] == 'src':
        return render(request, 'section_course_find.html', {'src': mytuple[1], 'webcookie': json.dumps(mytuple[2])})
    else:
        return render(request, 'error.html', {'error': mytuple[1]})


def get_section_course(request):
    try:
        head['Cookie'] = request.POST.get('webcookie', '')
        if head['Cookie'] == '':
            return render(request, 'error.html', {'error': '点击左上角X图标退出'})
        else:
            form = {
                'Sel_XNXQ': '20191',
                'rad': '3',
            }
            form['Sel_XZBJ2_YX'] = request.POST.get('belong', '')
            form['Sel_ZC'] = request.POST.get('week', '')
            form['selxqs'] = request.POST.get('day', '')
            form['Sel_JC'] = request.POST.get('section', '')
            form['txt_yzm'] = request.POST.get('code', '')
            head['Referer'] = 'http://bkjw.sxu.edu.cn/ZNPK/KBFB_DayJCSel.aspx'
            # 学生节次课表数据
            r = requests.post('http://bkjw.sxu.edu.cn/ZNPK/KBFB_DayJCSel_rpt.aspx', headers=head, data=form, timeout=10)
            if r.status_code == 200:
                r.encoding = 'gbk'
                mystr = r.text
                if mystr[1] == 't':
                    soup = BeautifulSoup(mystr[671:len(mystr) - 440], 'html.parser')
                    mytd = soup.find_all('td')
                    mytd_len = len(mytd)
                    mydict = {}
                    i = 0
                    while i < mytd_len:
                        mykey = ''
                        myvalue = ''
                        i += 1;
                        mynum = 1
                        while mynum < 8:
                            myvalue += str(mytd[i])
                            if mynum == 6:
                                mykey = str(mytd[i])
                            mynum += 1
                            i += 1
                        mydict[mykey] = myvalue

                    # 获取教师节次课表
                    form['Sel_XZBJ2_YX'] = ''
                    form['sel_bm'] = request.POST.get('belong', '')
                    r = requests.post('http://bkjw.sxu.edu.cn/ZNPK/KBFB_DayJCSel_rpt.aspx', headers=head, data=form,
                                      timeout=10)
                    if r.status_code == 200:
                        r.encoding = 'gbk'
                        mystr = r.text
                        soup = BeautifulSoup(mystr[671:len(mystr) - 440], 'html.parser')
                        mytd = soup.find_all('td')
                        mytd_len = len(mytd)
                        i = 0
                        while i < mytd_len:
                            mykey = ''
                            myvalue = ''
                            i += 1;
                            mynum = 1
                            while mynum < 8:
                                myvalue += str(mytd[i])
                                if mynum == 6:
                                    mykey = str(mytd[i])
                                mynum += 1
                                i += 1
                            mydict[mykey] = myvalue
                        i = 0
                        mystr = ''
                        for x in mydict:
                            i += 1
                            mystr += "<td width='5%' align='center' >" + str(i) + "<br></td>" + str(mydict[x]) + "</tr>"
                        localtime = time.localtime(time.time())
                        out = open('app/user_all/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(
                            localtime[2]) + '.csv', 'a', newline='')
                        csv_write = csv.writer(out, dialect='excel')
                        data = [str(localtime[0]) + '-' + str(localtime[1]) + '-' + str(localtime[2]) + ' ' + str(
                            localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]), '使用了节次课表查询服务']
                        csv_write.writerow(data)
                        out.close()
                        return render(request, 'section_course.html', {'value': mystr})
                    else:
                        localtime = time.localtime(time.time())
                        out = open(
                            'app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                            'a', newline='')
                        csv_write = csv.writer(out, dialect='excel')
                        data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                                'http://bkjw.sxu.edu.cn/ZNPK/KBFB_DayJCSel_rpt.aspx']
                        csv_write.writerow(data)
                        out.close()
                else:
                    return render(request, 'section_find_login_error.html')
            else:
                localtime = time.localtime(time.time())
                out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                           'a', newline='')
                csv_write = csv.writer(out, dialect='excel')
                data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                        'http://bkjw.sxu.edu.cn/ZNPK/KBFB_DayJCSel_rpt.aspx']
                csv_write.writerow(data)
                out.close()
        return render(request, 'error.html', {'error': '服务器维护中，点击左上角X图标退出'})
    except requests.ConnectTimeout:
        return render(request, 'error.html', {'error': '服务器维护中，点击左上角X图标退出'})

    except Exception as e:
        localtime = time.localtime(time.time())
        out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                   newline='')
        csv_write = csv.writer(out, dialect='excel')
        data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                '函数section_find_login()：未进行容错处理的情况：' + str(e)]
        csv_write.writerow(data)
        out.close()
        return render(request, 'error.html', {'error': '点击左上角X图标退出'})


def class_course_find(request):
    mytuple = captcha()
    if mytuple[0] == 'src':
        return render(request, 'class_course_find.html', {'src': mytuple[1], 'webcookie': json.dumps(mytuple[2])})
    else:
        return render(request, 'error.html', {'error': mytuple[1]})


def get_class_course(request):
    try:
        head['Cookie'] = request.POST.get('webcookie', '')
        if head['Cookie'] == '':
            return render(request, 'error.html', {'error': '点击左上角X图标退出'})
        else:
            form = {
                'Sel_XNXQ': '20191',
                'type': '1'
            }
            form['Sel_XZBJ'] = request.POST.get('class', '')
            form['txt_yzm'] = request.POST.get('code', '')
            head['Referer'] = 'http://bkjw.sxu.edu.cn/ZNPK/KBFB_ClassSel.aspx'
            r = requests.post('http://bkjw.sxu.edu.cn/ZNPK/KBFB_ClassSel_rpt.aspx', headers=head, data=form, timeout=10)
            if r.status_code == 200:
                if (r.text[0] == '<'):
                    return render(request, 'class_course_find_login_error.html')
                else:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    head['Referer'] = 'http://bkjw.sxu.edu.cn/ZNPK/KBFB_ClassSel_rpt.aspx'
                    r = requests.get('http://bkjw.sxu.edu.cn/ZNPK/' + soup.img.attrs['src'], headers=head, timeout=10)
                    if r.status_code == 200:
                        localtime = time.localtime(time.time())
                        _time = str(localtime[0]) + str(localtime[1]) + str(localtime[2]) + str(localtime[3])
                        name = random.sample('zyxwvutsrqponmlkjihgfedcba', 10)
                        _name = ''
                        for x in name:
                            _name += x
                        _time = _time + _name + 'class_course.jpg'
                        with open('app/media/' + _time, 'wb') as fp:
                            fp.write(r.content)
                        localtime = time.localtime(time.time())
                        out = open('app/user_all/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(
                            localtime[2]) + '.csv', 'a', newline='')
                        csv_write = csv.writer(out, dialect='excel')
                        data = [str(localtime[0]) + '-' + str(localtime[1]) + '-' + str(localtime[2]) + ' ' + str(
                            localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]), '使用了班级课表查询服务']
                        csv_write.writerow(data)
                        out.close()
                        return render(request, 'class_course.html', {'src': "/media/" + _time})
                    else:
                        localtime = time.localtime(time.time())
                        out = open(
                            'app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                            'a', newline='')
                        csv_write = csv.writer(out, dialect='excel')
                        data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                                'http://bkjw.sxu.edu.cn/ZNPK/' + soup.img.attrs['src']]
                        csv_write.writerow(data)
                        out.close()

            else:
                localtime = time.localtime(time.time())
                out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv',
                           'a', newline='')
                csv_write = csv.writer(out, dialect='excel')
                data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                        'http://bkjw.sxu.edu.cn/ZNPK/KBFB_ClassSel_rpt.aspx']
                csv_write.writerow(data)
                out.close()
        return render(request, 'error.html', {'error': '服务器维护中，点击左上角X图标退出'})

    except requests.ConnectTimeout:
        return render(request, 'error.html', {'error': '服务器维护中，点击左上角X图标退出'})

    except Exception as e:
        localtime = time.localtime(time.time())
        out = open('app/log/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
                   newline='')
        csv_write = csv.writer(out, dialect='excel')
        data = [str(localtime[3]) + ':' + str(localtime[4]) + ':' + str(localtime[5]),
                '函数class_find_login()：未进行容错处理的情况：' + str(e)]
        csv_write.writerow(data)
        out.close()
        return render(request, 'error.html', {'error': '点击左上角X图标退出'})


def school_calendar(request):
    localtime = time.localtime(time.time())
    out = open('app/user_all/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
               newline='')
    csv_write = csv.writer(out, dialect='excel')
    data = [str(localtime[0]) + '-' + str(localtime[1]) + '-' + str(localtime[2]) + ' ' + str(localtime[3]) + ':' + str(
        localtime[4]) + ':' + str(localtime[5]), '使用了校历服务']
    csv_write.writerow(data)
    out.close()
    return render(request, 'school_calendar.html')


def school_car(request):
    localtime = time.localtime(time.time())
    out = open('app/user_all/' + str(localtime[0]) + '_' + str(localtime[1]) + '_' + str(localtime[2]) + '.csv', 'a',
               newline='')
    csv_write = csv.writer(out, dialect='excel')
    data = [str(localtime[0]) + '-' + str(localtime[1]) + '-' + str(localtime[2]) + ' ' + str(localtime[3]) + ':' + str(
        localtime[4]) + ':' + str(localtime[5]), '使用了校车时间表服务']
    csv_write.writerow(data)
    out.close()
    return render(request, 'school_car.html')


def trip(request):
    return render(request, 'trip.html')


def file(request):
    all_file = os.listdir('app/static/file')
    for i in range(0, len(all_file)):
        all_file[i] = [all_file[i], time.strftime("%Y--%m--%d %H:%M:%S",
                                                  time.localtime(os.path.getmtime('app/static/file/' + all_file[i])))]
    return render(request, 'file.html', {'all_file': all_file})


def need_file(request):
    file = open('app/static/file/' + request.GET['name'], 'rb')
    response = HttpResponse(file)
    print(response)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f"attachment; filename={escape_uri_path(request.GET['name'])};"
    return response


def upload(request):
    obj = request.FILES.get('upload')
    f = open('app/static/file/' + obj.name, 'wb')
    for line in obj.chunks():
        f.write(line)
    f.close()
    return HttpResponse("<script>alert('提交成功');parent.location.reload(); </script>")


def app(request):
    if request.GET.get("code", -1) == -1:
        return render(request, 'app.html')
    else:
        kv = {
            "appkey": "ding0jl1mpugprhidpz0",
            "appsecret": "lQMnf7XSezk5IgkcaVaNeVKfgMGZ9mPc7rNSYk7ZuBMM1m4RH4-aehGMS-lLcmyG"
        }
        r = requests.get("https://oapi.dingtalk.com/gettoken", params=kv)
        kv = {
            "access_token": eval(r.text)["access_token"],
            "code": request.GET["code"]
        }
        r = requests.get("https://oapi.dingtalk.com/user/getuserinfo", params=kv)
        print(r.text)
        return HttpResponse("成功")
