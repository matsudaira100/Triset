# word_data.py

# ブロックの共通データ定義
BLOCK_SHAPES = {
    "1": [(1, 0)],
    "2": [(0, 1), (1, 1)],
    "3": [(0, 1), (1, 1), (2, 1)],
    "4": [(0, 1), (1, 1), (2, 1), (3, 1)],
    "L": [(1, 0), (1, 1), (1, 2), (2, 2)],
    "J": [(2, 0), (2, 1), (2, 2), (1, 2)],
    "T": [(1, 0), (2, 0), (3, 0), (2, 1)],
    "U": [(1, 1), (3,1), (1, 2), (2, 2), (3, 2)],
    "O": [(1, 1), (1, 2), (2, 1), (2, 2)],
    "S": [(2, 0), (3, 0), (1, 1), (2, 1)],
    "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],
    "V": [(0, 0), (1, 0), (1, 1)]
}

# ステージごとの単語データ
STAGE_WORDS = {
    "stage1": {  # 超初級：簡単な動詞と名詞
        "1": "go",      # 行く
        "2": "run",     # 走る
        "3": "fire",    # 火
        "4": "play",    # 遊ぶ
        "L": "like",    # 好き
        "J": "jet",     # ジェット
        "T": "top",     # 頂上
        "U": "user",    # 使用者
        "O": "own",     # 所有する
        "S": "set",     # セット
        "Z": "zoo",     # 動物園
        "V": "view"     # 見る 
    },
    "stage2": {  # 初級：動物名
        "1": "ant",     # アリ
        "2": "bee",     # ハチ
        "3": "monkey",  # サル
        "4": "elephant",# 象
        "L": "lion",    # ライオン
        "J": "rabbit",  # ウサギ
        "T": "tiger",   # トラ
        "U": "horse",   # 馬
        "O": "owl",     # フクロウ
        "S": "sheep",   # 羊
        "Z": "zebra",   # シマウマ
        "V": "bat"      # コウモリ
    },
    "stage3": {  # 初級：プログラミング基礎
        "1": "if",      # もし
        "2": "for",     # ために
        "3": "code",    # コード
        "4": "programing",# プログラミング
        "L": "list",    # リスト
        "J": "java",    # Java言語
        "T": "test",    # テスト
        "U": "unit",    # 単位
        "O": "open",    # 開く
        "S": "sort",    # 並び替え
        "Z": "zero",    # ゼロ
        "V": "void"     # 無効
    },
    "stage4": {  # 中級：一般単語
        "1": "dot",     # 点
        "2": "pair",    # 組
        "3": "delta",   # デルタ
        "4": "education",# 教育
        "L": "link",    # リンク
        "J": "jump",    # ジャンプ
        "T": "think",   # 考える
        "U": "union",   # 組合
        "O": "object",  # 物体
        "S": "shape",   # 形
        "Z": "zigzag",  # ジグザグ
        "V": "vital"    # 重要な
    },
    "stage5": {  # 中級：料理
        "1": "sushi",   # 寿司
        "2": "tempura", # 天ぷら
        "3": "curryrice",# カレーライス
        "4": "hamburger",# ハンバーガー
        "L": "lasagna", # ラザニア
        "J": "jelly",   # ゼリー
        "T": "tacos",   # タコス
        "U": "udon",    # うどん
        "O": "okonomiyaki",# お好み焼き
        "S": "kebab",   # ケバブ
        "Z": "pizza",   # ピザ
        "V": "vanilla"  # バニラ
    },
    "stage6": {  # 中級：宇宙
        "1": "star",    # 星
        "2": "meteor",  # 流星
        "3": "planet",  # 惑星
        "4": "supernova",# 超新星
        "L": "mars",    # 火星
        "J": "jupiter", # 木星
        "T": "mercury", # 水星
        "U": "uranus",  # 天王星
        "O": "earth",   # 地球
        "S": "saturn",  # 土星
        "Z": "neptune", # 海王星
        "V": "venus"    # 金星
    },
    "stage7": {  # 上級：スポーツ
        "1": "boxing",  # ボクシング
        "2": "baseball",# 野球
        "3": "volleyball",# バレーボール
        "4": "americanfootball",# アメフト
        "L": "wrestling",# レスリング
        "J": "basketball",# バスケットボール
        "T": "tabletennis",# 卓球
        "U": "marathon",# マラソン
        "O": "olympic", # オリンピック
        "S": "swimming",# 水泳
        "Z": "fencing", # フェンシング
        "V": "archery"  # アーチェリー
    },
    "stage8": {  # 上級：神々
        "1": "god",     # 神
        "2": "ebisu",   # 恵比寿
        "3": "athena",  # アテナ
        "4": "buddha",  # 仏陀
        "L": "allah",   # アッラー
        "J": "ganesha", # ガネーシャ
        "T": "tsukuyomi",# 月読
        "U": "nirvana", # 涅槃
        "O": "poseidon",# ポセイドン
        "S": "susanoo", # スサノオ
        "Z": "zeus",    # ゼウス
        "V": "hera"     # ヘラ
    },
    "stage9": {  # 超上級：神聖
        "1": "angel",   # 天使
        "2": "glory",   # 栄光
        "3": "sunshine",# 陽光
        "4": "gokurakujodo",# 極楽浄土
        "L": "luminary",# 光源
        "J": "justice", # 正義
        "T": "temple",  # 寺院
        "U": "utopia",  # 理想郷
        "O": "oracle",  # 神託
        "S": "sanctuary",# 聖域
        "Z": "zenith",  # 天頂
        "V": "vision"   # 幻視
    },
    "stage10": {  # エキスパート：専門用語
        "1": "algorithm",# アルゴリズム
        "2": "binarysearch",# 二分探索
        "3": "cryptography",# 暗号化
        "4": "quantumcomputing",# 量子コンピューティング
        "L": "deeplearning",# 深層学習
        "J": "javascript",# JavaScript
        "T": "turingmachine",# チューリングマシン
        "U": "userinterface",# ユーザーインターフェース
        "O": "optimizationtheory",# 最適化理論
        "S": "datastructure",# データ構造
        "Z": "zettabyte",# ゼタバイト
        "V": "virtualreality"# 仮想現実
    }
}


def get_stage_block_data(stage_name):
    #指定されたステージのブロックデータを生成する
    if stage_name not in STAGE_WORDS:
        raise ValueError(f"Stage {stage_name} not found")
    
    block_data = {}
    for shape, coords in BLOCK_SHAPES.items():
        word = STAGE_WORDS[stage_name][shape]
        block_data[shape] = (word, coords)
    
    return block_data