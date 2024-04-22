import os
import time

from werkzeug.utils import secure_filename


class FileManager:
    def __init__(self, path):
        self.path = os.path.abspath(path)

    @staticmethod
    def _change_mode_format(mode):
        mode_dict = {
            '7': 'rwx',
            '6': 'rw-',
            '5': 'r-x',
            '4': 'r--',
            '3': '-wx',
            '2': '-w-',
            '1': '--x',
            '0': '---'
        }
        return ''.join([mode_dict[x] for x in mode])

    def get_file_list(self):
        try:
            # 使用os.listdir获取路径下的目录和文件
            items = os.listdir(self.path)
            items.sort(key=lambda x: os.path.isdir(os.path.join(self.path, x)), reverse=True)  # 按目录在前，文件在后排序
            if not items:
                return {'error': 'No files or directories found'}
        except OSError as e:
            return {'error': str(e)}

        file_list = []
        for item in items:
            item_path = os.path.join(self.path, item)
            if os.path.isdir(item_path):
                file_type = 'dir'
            elif item.lower().endswith('.html'):
                file_type = 'html'
            elif item.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_type = 'pic'
            else:
                file_type = "file"

            try:
                mode = os.stat(item_path).st_mode
                owner = os.stat(item_path).st_uid
                if owner == 0:
                    owner = 'root'

                else:
                    owner = 'user'
            except OSError as e:
                continue  # 如果无法获取文件信息，则跳过此项
            created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(item_path)))
            modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(item_path)))
            file_list.append({
                'file_type': file_type,
                'mode': FileManager._change_mode_format(oct(mode)[-3:]),
                'mode_oct': oct(mode)[-3:],
                'created_time': created_time,
                'modified_time': modified_time,
                'owner': owner,
                'name': item
            })
        return file_list

    def delete_file(self, path):
        # 只删除指定的文件或目录，而不是整个路径
        try:
            if os.path.isfile(path) or os.path.isdir(path):
                os.remove(path) if os.path.isfile(path) else os.rmdir(path)
                return {"status": "success", "message": f"Deleted {path}"}
            else:
                return {"status": "error", "message": "File not found"}
        except OSError as e:
            return {"status": "error", "message": str(e)}

    def upload(self, file, path):
        # 使用secure_filename确保文件名安全
        filename = secure_filename(file.filename)
        if filename:
            try:
                file_path = os.path.join(path, filename)
                file.save(file_path)
                return {"status": "success", "message": f"Uploaded {filename}", "filename": file_path}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        else:
            return {"status": "error", "message": "Invalid file name"}
