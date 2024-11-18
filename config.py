import os
from module.mod_read_ini import read_ini  # mod_read_ini.py の read_ini 関数をインポート

# iniファイルのパスを構築
ini_file_path = os.path.join(os.path.dirname(__file__), 'ini', 'system.ini')
# iniを読み、値を保管
ini = read_ini(ini_file_path)

# INIクラスの内容を全て出力する方法
def print_ini(ini):
    # INIオブジェクトの属性をリスト化
    sections = [
        ("database", vars(ini.database)),
        ("server", vars(ini.server)),
        ("rate", vars(ini.rate)),
        ("bless", vars(ini.bless)),
        ("curse", vars(ini.curse)),
        ("start_channel", vars(ini.start_channel)),
        ("bank",vars(ini.bank))
    ]
    # 各セクションの内容を表示
    for section_name, section_data in sections:
        print(f"--- {section_name} ---")
        for key, value in section_data.items():
            print(f"{key}: {value}")
        print()  # セクションごとに空行を入れる
