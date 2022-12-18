import subprocess


def upload(data):
    # 使用 rclone 的 copy 命令将文件复制到目标位置
    subprocess.run(['rclone', 'copy', data['SourceFile'], data['Destination']])
