from datetime import datetime

# 要解析的字符串
date_str = 'Feb'

# 使用 %b 进行解析
try:
    date_obj = datetime.strptime(date_str, '%b')
    print(date_obj)
except ValueError as e:
    print(f"解析错误: {e}")