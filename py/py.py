import requests
import datetime
import pytz

# GitHub 仓库的信息
repository_owner = 'png-dot'
repository_name = 'pngpng'
access_token = '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'

# 构建API请求的URL
url = f'https://api.github.com/repos/{repository_owner}/{repository_name}/contents/'

# 构建HTTP请求头，包括授权令牌
headers = {
    'Authorization': f'token {access_token}'
}

# 获取当前北京时间
beijing_tz = pytz.timezone('Asia/Shanghai')
current_time = datetime.datetime.now(beijing_tz)
# 90天的时间差
ninety_days = datetime.timedelta(days=90)

# 获取仓库内容
response = requests.get(url, headers=headers)

# 检查响应是否成功
if response.status_code == 200:
    # 解析JSON响应
    data = response.json()
    
    # 初始化一个提交信息
    commit_message = "删除过期文件"
    
    # 用于标记是否删除了文件
    deleted_files = False
    
    # 用于记录删除的文件数量
    deleted_file_count = 0
    
    # 遍历文件
    for item in data:
        if item['type'] == 'file':
            # 解析文件名中的日期
            file_name = item['name']
            file_date_str = file_name[:8]
            file_date = beijing_tz.localize(datetime.datetime.strptime(file_date_str, '%Y%m%d'))
            
            # 计算日期差异
            delta = current_time - file_date
            
            # 如果日期差异大于90天，删除文件
            if delta > ninety_days:
                delete_url = f'https://api.github.com/repos/{repository_owner}/{repository_name}/contents/{file_name}'
                
                # 构建包含提交信息的请求体
                data = {
                    "message": commit_message,
                    "committer": {
                        "name": "你的名字",
                        "email": "你的电子邮件@example.com"
                    },
                    "content": "",
                    "sha": item['sha']
                }
                
                # 发送删除文件的请求
                delete_response = requests.delete(delete_url, headers=headers, json=data)
                
                if delete_response.status_code == 200:
                    print(f'已删除文件: {file_name}')
                    deleted_files = True
                    deleted_file_count += 1
                else:
                    print(f'无法删除文件: {file_name}. 状态码: {delete_response.status_code}')
    
    # 输出删除的文件数量和时间
    if not deleted_files:
        print(f'没有符合条件的文件\n{current_time.strftime("%Y-%m-%d %H:%M:%S")}\n')
    else:
        print('删除文件为：')
        print(f'共删除 {deleted_file_count} 个文件')
        print(f'{current_time.strftime("%Y-%m-%d %H:%M:%S")}\n')
else:
    print(f'获取仓库内容失败。状态码: {response.status_code}')
