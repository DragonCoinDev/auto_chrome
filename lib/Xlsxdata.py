import os
import xlrd
import xlsxwriter


class Xlsxdata():
    def __init__(self,data_path):   #传入环境目录
        self.data = {}
        self.data_path = data_path
        self.key_translate = {
            '浏览器ID':'browserId',
            '分组':'group',
            '应用网址':'siteUrl',
            '用户名':'username',
            '密码':'password',
            '邮箱地址':'email',
            '邮箱密码':'email_passwd',
            '手机号码':'phone',
            '打开页面':'startUrl',
            'cookie':'cookie',
        }

    def read(self,filename):
        res = {}
        data = xlrd.open_workbook(filename)
        table = data.sheet_by_index(0)
        nrows = table.nrows #获取行数
        headings = table.row_values(0, start_colx=0, end_colx=None) # 获取表头
        #定位表头 关键参数位置
        key_index = {
            '浏览器ID':0,
            '分组':0,
            '应用网址':0,
            '代理地址':0,
            '代理类型':0,
            '用户名':0,
            '密码':0,
            '邮箱地址':0,
            '邮箱密码':0,
            '手机号码':0,
            '打开页面':0,
            'cookie':0,
            '钱包地址':0,
            '钱包密码':0,
        }
        for key in key_index.keys():
            key_index[key] = headings.index(key)
        for row_num in range(1,nrows):
            row_data =  table.row_values(row_num)
            browserId = int(row_data[key_index['浏览器ID']])
            group = row_data[key_index['分组']]
            siteUrl = row_data[key_index['应用网址']]
            username = row_data[key_index['用户名']]
            password = row_data[key_index['密码']]
            email = row_data[key_index['邮箱地址']]
            email_passwd = row_data[key_index['邮箱密码']]
            phone = row_data[key_index['手机号码']]
            startUrl = row_data[key_index['打开页面']]
            cookie = row_data[key_index['cookie']]
            proxys_ip = row_data[key_index['代理地址']]
            proxy_type = row_data[key_index['代理类型']]
            wallet_addres = row_data[key_index['钱包地址']]
            wallet_passwd = row_data[key_index['钱包密码']]
            name = group + '_' + str(browserId)
            user_path = os.sep + 'user_data' + os.sep + name
            proxys = proxy_type + "://" + proxys_ip
            res[name] = {
                    "id": browserId,
                    "name": name,
                    "group": group,
                    "startUrl": startUrl,
                    "browserId": browserId,
                    "user_path": user_path,
                    "account": {
                        "username": username,
                        "password": password,
                        "email": email,
                        "email_passwd":email_passwd,
                        "phone": phone,
                        "cookie": cookie,
                        "siteUrl": siteUrl,
                        "proxys":proxys,
                        "wallet_passwd":wallet_passwd,
                        "wallet_addres":wallet_addres
                    }
            }
        return res

    def write(self):
        pass
