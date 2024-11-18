import os
import subprocess

def run_py(filename):
	file_path = os.path.join(os.path.dirname(__file__), filename)
	# subprocess.runでPythonファイルを実行
	subprocess.run(['python', file_path], check=True)
	print('実行：'+file_path)

# 別.pyを実行する
run_py('config.py')
run_py('mother.py')