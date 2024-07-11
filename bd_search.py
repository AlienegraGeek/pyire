import urllib.request

response = urllib.request.urlopen("http://www.baidu.com")
# read是读取
# decode是解码成其他格式的编码，当我们爬取的数据包含中文的时候就需要这个
print(response.read().decode('utf-8'))
