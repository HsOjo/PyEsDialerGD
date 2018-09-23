import hashlib
import time


def md5(data: bytes):
    return hashlib.md5(data).hexdigest()


def md5_str(data: str):
    return md5(data.encode('utf8'))


def now_str():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def str_extract(data_str: str, start_str: str, end_str: str):
    result = ''
    offset_start = data_str.find(start_str)
    if offset_start != -1:
        offset_end = data_str.find(end_str, offset_start)
        if offset_end != -1:
            result = data_str[offset_start + len(start_str):offset_end]

    return result


def get_tag_content(data_str: str, tag: str):
    result = str_extract(data_str, '<%s>' % tag, '</%s>' % tag)
    if result[:9] == '<![CDATA[' and result[-3:] == ']]>':
        result = result[9:-3]
    return result
