# IP_Split
IP地址拆分(支持IPv6)
## 需要的依赖：
Python 3

IPy库
## 支持以下格式的IP拆分：
192.168.0.1

192.168.1.1-254

192.168.18.255/24

192.168.1.*

192.168.1-10.*

2001:0DB8:0000:0000:0000:0000:1428:07ab

2001:0DB8:0:0:0:0:1428:07ab

2001:128::1428:732

2001:DB8::1428:7ab/120
## 使用方式：
1. 将IP地址(段)按行放入"IP_range.txt"文件中
2. 运行"IP_Split.py“文件
3. 拆分结果将保存在"IP_range_result.txt"中
4. 错误的IP地址将保存在"IP_range_err.txt"中


mail_acc  = 123456@chinatelecom.cn
mail_pass = 123456
