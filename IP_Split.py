from IPy import IP  # 需要安装
from IPy import IPint
import re
import os

source_filename = 'IP_range.txt'  # IP段输入文件
dest_filename = 'IP_range_result.txt'  # 拆分后IP输出文件
error_filename = 'IP_range_err.txt'  # 格式错误IP输出文件
enter = '\r'  # 换行符

def ipv4_mask_handle(ip):  # 将带掩码的IPv4地址处理为IPy库可处理的形式
    mask = ip.split('/')[-1]
    mask_int = int(mask)
    ip_return = ''
    '''
    ip_number = 0
    for i in range(0, 4):
        ip_number += int(ip.split('/')[-2].split('.')[-(4 - i)])
        if i < 3:
            ip_number = ip_number << 8
    '''
    ip_number = IPint(ip.split('/')[-2]).int()
    ip_number = (ip_number >> (32 - mask_int)) << (32 - mask_int)
    for i in range(0, 4):
        ip_return += str((ip_number >> ((3 - i) * 8)) & 255)
        if i < 3:
            ip_return += '.'
        else:
            ip_return += '/' + mask
            return ip_return


def ipv4_range_handle(ip, finput, ferror):  # 将IPv4地址范围拆分成单个IP
    start_ip = ''
    end_ip = ''
    for i in range(0, 4):
        ip_range_tmp = ip.split('.')[-(4 - i)]
        if ip_range_tmp == '*':
            start_ip += '0'
            end_ip += '255'
        elif re.search(r'\-', ip_range_tmp):
            start_ip += ip_range_tmp.split('-')[0]
            end_ip += ip_range_tmp.split('-')[1]
        else:
            start_ip += ip_range_tmp
            end_ip += ip_range_tmp

        if i < 3:
            start_ip += '.'
            end_ip += '.'

    start_ip_int = IPint(start_ip).int()
    end_ip_int = IPint(end_ip).int()
    for i in range(0, (end_ip_int - start_ip_int + 1)):
        try:
            fo.write(str(IP(start_ip_int + i)) + enter)
        except Exception as e:
            fe.write(ip + enter)


def ipv6_mask_handle(ip):  # 将带掩码的IPv6地址处理为IPy库可处理的形式
    mask = ip.split('/')[-1]
    mask_int = int(mask)
    ip_return = ''
    ip_number = IPint(ip.split('/')[-2]).int()
    ip_number = (ip_number >> (128 - mask_int)) << (128 - mask_int)
    for i in range(0, 8):
        ip_return += str(hex((ip_number >> ((7 - i) * 16)) & 0xFFFF))
        if i < 7:
            ip_return += ':'
        else:
            ip_return += '/' + mask
            return ip_return


if __name__ == '__main__':
    fi = open(source_filename, "r")
    fo = open(dest_filename, "w+")
    fe = open(error_filename, "w+")

    for line in fi:
        original_ip = line.strip()
        if re.match(r'^[0-9\.]+$', original_ip):  # 单一IPv4地址处理
            try:
                if IP(original_ip).version() == 4:
                    fo.write(original_ip + enter)
                else:
                    fe.write(original_ip + enter)
            except Exception as e:
                fe.write(original_ip + enter)

        elif re.match(r'^[0-9\.\/]+$', original_ip):  # 带掩码IPv4地址处理
            changed_ipv4 = ipv4_mask_handle(original_ip)
            try:
                for ip_tmp in IP(changed_ipv4):
                    fo.write(str(ip_tmp) + enter)
            except Exception as e:
                fe.write(original_ip + enter)

        elif re.match(r'^[0-9\.\-\*]+$', original_ip):  # 带'-'和'*'的IPv4地址处理
            ipv4_range_handle(original_ip, fo, fe);

        elif re.match(r'^[0-9a-eA-E\:]+$', original_ip):  # 单一IPv6地址处理
            try:
                if IP(original_ip).version() == 6:
                    fo.write(original_ip + enter)
                else:
                    fe.write(original_ip + enter)
            except Exception as e:
                fe.write(original_ip + enter)

        elif re.match(r'^[0-9a-eA-E\:\/]+$', original_ip):  # 带掩码IPv6地址处理
            changed_ipv6 = ipv6_mask_handle(original_ip)
            try:
                for ip_tmp in IP(changed_ipv6):
                    fo.write(str(ip_tmp) + enter)
            except Exception as e:
                fe.write(original_ip + enter)

    fi.close()
    fo.close()
    fe.close()
