import os

# 设置工作目录
directory = './'

# 要替换的旧URL和新URL
old_url = 'https://images.scan.work/test/'
new_url = 'https://fastly.jsdelivr.net/gh/hack-scan/Blog-pic/posts/'

# 遍历目录下的所有文件
for filename in os.listdir(directory):
    # 检查文件扩展名是否为.md
    if filename.endswith('.md'):
        # 构造完整的文件路径
        file_path = os.path.join(directory, filename)

        # 重命名文件，将.md改为.txt
        new_file_path = os.path.join(directory, filename[:-3] + 'txt')
        os.rename(file_path, new_file_path)

        # 读取文件内容
        with open(new_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 替换URL
        content = content.replace(old_url, new_url)

        # 将修改后的内容写回文件
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        # 将.txt文件重命名为.md文件
        os.rename(new_file_path, file_path)

print("所有文件已处理完毕。")