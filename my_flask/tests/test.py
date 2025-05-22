import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_path = os.path.join(project_root, 'templates', 'codes.html')

sys.path.append(project_root)

print(f"项目根目录: {project_root}")
print(f"模板完整路径: {template_path}")
print("文件存在:", os.path.exists(template_path))