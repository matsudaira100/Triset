#効果音https://soundeffect-lab.info/

import math
import pygame
import random
import time
from word_data import *

# Pygameの初期化
pygame.init()
pygame.mixer.init()

# 基本の設定
GRID_SIZE = 25
ROWS, COLS = 20, 10
SLOT_HEIGHT = 4 * GRID_SIZE
WINDOW_WIDTH = COLS * GRID_SIZE
WINDOW_HEIGHT = SLOT_HEIGHT + (ROWS * GRID_SIZE)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Triset!")
block_data = get_stage_block_data("stage10")
#音声ファイル読み込み
game_start_sound = pygame.mixer.Sound('game_start.mp3')
block_rotate_sound = pygame.mixer.Sound('block_rotate.mp3')
typing_mistake_sound = pygame.mixer.Sound('typing_mistake.mp3')
typing_success_sound = pygame.mixer.Sound('typing_success.mp3')
block_fall_sound = pygame.mixer.Sound('block_fall.mp3')
hard_drop_sound = pygame.mixer.Sound('hard_drop_sound.mp3')
line_clear_sound = pygame.mixer.Sound('line_clear.mp3')
game_clear_sound = pygame.mixer.Sound('game_clear_sound.mp3')
game_over_sound = pygame.mixer.Sound('game_over.mp3')

#タイマー設定
MAX_TIME = 7.0

# スコア点滅のための設定を追加
SCORE_FLASH_DURATION = 1  # 点滅の持続時間（秒）
score_flash_start = 0
score_is_flashing = False

# クリア条件のスコア
CLEAR_SCORE = 1500

# フォントサイズの調整
LARGE_FONT_SIZE = 48  
MEDIUM_FONT_SIZE = 32 
SMALL_FONT_SIZE = 24  

# スロットの余白設定
SLOT_MARGIN_LEFT = 10  # 左余白のピクセル数


COLORS = {
    "1": (255, 255, 255),     # 白
    "2": (190, 255, 90),      # 黄緑
    "3": (255, 182, 193),     # ピンク
    "4": (218, 112, 214),     # 紫
    "L": (255, 99, 71),       # 赤
    "J": (50, 205, 50),       # 緑 
    "T": (30, 144, 255),      # 青 
    "U": (255, 180, 70),      # オレンジ
    "O": (200, 200, 200),     # 灰色
    "S": (64, 224, 208),      # 水色
    "Z": (255, 255, 85),      # 黄色
    "V": (205, 133, 63)       # 茶
}

# スロットクラスの定義
class Slot:
    def __init__(self, shape):
        self.shape = shape
        self.word = block_data[shape][0]
        self.correct_count = 0

# 初期化関数
def init_game():
    global grid
    grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    slots = [Slot(random.choice(list(block_data.keys()))) for _ in range(2)]  # 3から2に変更
    return slots

# グリッド管理用の2次元リスト
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

# ライン消去のチェックと実行（位置関係継続の実装）
def check_and_clear_lines():
    lines_to_clear = []
    # 消去対象のライン探索
    for row in range(ROWS):
        if all(cell is not None for cell in grid[row]):
            lines_to_clear.append(row)
    
    if not lines_to_clear:
        return 0

    # 消去エフェクトの表示
    for _ in range(3):  # 点滅3回
        # 白く光らせる
        for row in lines_to_clear:
            for col in range(COLS):
                rect = pygame.Rect(
                    col * GRID_SIZE,
                    SLOT_HEIGHT + row * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE
                )
                pygame.draw.rect(screen, (255, 255, 255), rect)
        pygame.display.flip()
        time.sleep(0.1)

        # 元の色に戻す
        screen.fill((0, 0, 0))
        draw_grid()
        pygame.display.flip()
        time.sleep(0.1)

    # 位置関係を保ちながらライン消去と落下
    lines_to_clear.sort()  # 上から順にソート
    for clear_row in lines_to_clear:
        # clear_row より上の行を1つずつ下に移動
        for row in range(clear_row, 0, -1):
            grid[row] = [c for c in grid[row - 1]]
        # 最上段に空行を挿入
        grid[0] = [None for _ in range(COLS)]
    line_clear_sound.play()
    
    # 消したライン数に応じてスコアを計算
    lines = len(lines_to_clear)
    if lines == 1:
        return 100
    elif lines == 2:
        return 220
    elif lines == 3:
        return 330
    elif lines == 4:
        return 500
    return 0

# グリッドを描画する関数
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            # グリッドの線を描画
            pygame.draw.rect(screen, (128, 128, 128), 
                           (col * GRID_SIZE, SLOT_HEIGHT + row * GRID_SIZE, 
                            GRID_SIZE, GRID_SIZE), 1)
            # 固定されたブロックを描画
            if grid[row][col] is not None:
                color = COLORS[grid[row][col]]
                rect = pygame.Rect(col * GRID_SIZE, SLOT_HEIGHT + row * GRID_SIZE,
                                 GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (128, 128, 128), rect, 1)


def draw_slots(slots, remaining_time):
    font = pygame.font.SysFont(None, SMALL_FONT_SIZE)
    mini_grid_size = GRID_SIZE // 2

    # タイマーゲージの描画
    gauge_width = WINDOW_WIDTH // 3
    gauge_height = 5
    gauge_x = WINDOW_WIDTH - gauge_width - 20
    gauge_y = 5
    
    # ゲージの背景
    pygame.draw.rect(screen, (64, 64, 64), (gauge_x, gauge_y, gauge_width, gauge_height))
    
    # 残り時間のゲージ
    remaining_ratio = remaining_time / MAX_TIME
    current_width = int(gauge_width * remaining_ratio)
    gauge_color = (255, 0, 0) if remaining_time <= 3 else (0, 255, 0)
    pygame.draw.rect(screen, gauge_color, (gauge_x, gauge_y, current_width, gauge_height))

    # スロットごとに描画
    for i, slot in enumerate(slots):
        # スロットの基本位置
        x_offset = (i + 1) * (WINDOW_WIDTH // (len(slots) + 1)) - (mini_grid_size * 2)
        y_offset = GRID_SIZE

        # ブロックの描画（高さは固定）
        color = COLORS[slot.shape]
        for dx, dy in block_data[slot.shape][1]:
            rect = pygame.Rect(
                x_offset + dx * mini_grid_size,
                y_offset + dy * mini_grid_size,
                mini_grid_size, mini_grid_size
            )
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (128, 128, 128), rect, 1)

        # 単語の描画（高さをスロットごとにずらす）
        height_offset = GRID_SIZE if i % 2 != 0 else GRID_SIZE // 2  # 偶数・奇数で高さを調整
        completed_text = font.render(slot.word[:slot.correct_count], True, (0, 255, 0))
        remaining_text = font.render(slot.word[slot.correct_count:], True, (255, 255, 255))

        # 単語全体の幅を計算
        total_text_width = completed_text.get_width() + remaining_text.get_width()

        # テキストの描画位置を計算
        text_x = x_offset + (len(block_data[slot.shape][1]) * mini_grid_size) // 2 - total_text_width // 2
        text_y = y_offset + 1.3 * GRID_SIZE + height_offset

        screen.blit(completed_text, (text_x, text_y))
        screen.blit(remaining_text, (text_x + completed_text.get_width(), text_y))

# ブロックの描画関数
def draw_block(x, y, shape):
    color = COLORS[shape]
    for dx, dy in block_data[shape][1]:
        rect = pygame.Rect(
            (x + dx) * GRID_SIZE,
            SLOT_HEIGHT + (y + dy) * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (128, 128, 128), rect, 1)

def draw_score(score, current_time, score_flash_start, score_is_flashing):
    font = pygame.font.SysFont(None, SMALL_FONT_SIZE)
    score_color = (255, 255, 255)

    # スコアが点滅中の場合
    if score_is_flashing:
        elapsed_time = current_time - score_flash_start
        if elapsed_time < SCORE_FLASH_DURATION:
            # 点滅エフェクト（sin波を使用してなめらかな点滅を実現）
            flash_intensity = abs(math.sin(elapsed_time * 100))
            score_color = (
                255,
                int(255 * (1 - flash_intensity)),
                int(255 * (1 - flash_intensity)),
            )

    score_text = font.render(f"Score: {score}/{CLEAR_SCORE}", True, score_color)
    screen.blit(score_text, (10, 5))  # タイマーゲージの下に表示位置を調整

def draw_game_status(game_over, game_clear, score, clear_time=None):
    if game_clear:
        # CLEARの表示
        font_clear = pygame.font.SysFont(None, LARGE_FONT_SIZE)
        result_text = font_clear.render("GAME CLEAR!", True, (0, 255, 0))
        text_rect = result_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        screen.blit(result_text, text_rect)

        # クリアタイムの表示（大きめに）
        if clear_time is not None:
            font_time = pygame.font.SysFont(None, MEDIUM_FONT_SIZE)
            clear_time_text = font_time.render(f"Clear Time: {clear_time:.2f}s", True, (255, 255, 255))
            clear_time_rect = clear_time_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            screen.blit(clear_time_text, clear_time_rect)

    elif game_over:
        # GAME OVERの表示
        font_over = pygame.font.SysFont(None, LARGE_FONT_SIZE)
        result_text = font_over.render("GAME OVER", True, (255, 0, 0))
        text_rect = result_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        screen.blit(result_text, text_rect)

    # Press ESCの表示
    font_esc = pygame.font.SysFont(None, SMALL_FONT_SIZE)
    press_esc_text = font_esc.render("Press ESC to restart", True, (255, 255, 255))
    esc_rect = press_esc_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
    screen.blit(press_esc_text, esc_rect)

# ブロックを固定
def fix_block(x, y, shape):
    for dx, dy in block_data[shape][1]:
        grid[y + dy][x + dx] = shape

# 衝突判定関数
def check_collision(x, y, shape):
    for dx, dy in block_data[shape][1]:
        if y + dy >= ROWS or x + dx < 0 or x + dx >= COLS or grid[y + dy][x + dx] is not None:
            return True
    return False

# ゲームオーバー判定関数
def check_game_over():
    # 積みすぎ判定
    for col in range(COLS):
        if grid[0][col] is not None:
            game_over = True
            game_over_sound.play()
            return "stack"
    return None

# ゲームクリア判定関数
def check_game_clear(score):
    return score >= CLEAR_SCORE

# 回転関数
def rotate_block(shape):
    """ブロックの座標を時計回りに90度回転"""
    coords = block_data[shape][1]
    # 座標の回転処理
    new_coords = []
    for x, y in coords:
        # 時計回りの90度回転 (x, y) -> (-y, x)
        new_coords.append((-y, x))
    
    # 回転後の座標を正の値に調整
    min_x = min(x for x, y in new_coords)
    min_y = min(y for x, y in new_coords)
    new_coords = [(x - min_x, y - min_y) for x, y in new_coords]
    
    return new_coords

# 回転後の位置が有効かチェックする関数
def check_rotation_valid(x, y, new_coords):
    for dx, dy in new_coords:
        new_x = x + dx
        new_y = y + dy
        if (new_y >= ROWS or new_x < 0 or new_x >= COLS or
            new_y < 0 or  # 上端のチェックを追加
            (new_y < ROWS and new_x >= 0 and new_x < COLS and grid[new_y][new_x] is not None)):
            return False
    return True

# ハードドロップの位置を計算する関数
def get_hard_drop_position(x, y, shape):
    while not check_collision(x, y + 1, shape):
        y += 1
    return y
# メインゲームループ
def main():
    clock = pygame.time.Clock()
    running = True
    game_over = False
    game_clear = False
    score = 0

    # スロットの初期化
    slots = init_game()
    
    #ゲーム開始音
    game_start_sound.play()

    # ゲームの状態
    active_block = None
    block_x, block_y = 4, 0
    normal_fall_speed = 500
    fast_fall_speed = 50
    fall_speed = normal_fall_speed
    last_fall_time = pygame.time.get_ticks()
    last_move_time = pygame.time.get_ticks()
    MOVE_DELAY = 100  

    # タイマー関連
    remaining_time = MAX_TIME
    last_time = time.time()
    start_time = time.time()  # ゲーム開始時間を記録
    clear_time = 0  # クリアタイム
    score_is_flashing = False
    score_flash_start = 0

    while running:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        # タイマー更新（アクティブブロックがない時のみ）
        if not active_block and not game_over and not game_clear:
            remaining_time -= dt
            if remaining_time <= 0:
                game_over = True
                game_clear = False
                remaining_time = 0
                game_over_sound.play()

        screen.fill((0, 0, 0))
        draw_slots(slots, remaining_time)
        pygame.draw.line(screen, (255, 0, 0), 
                        (0, SLOT_HEIGHT), (WINDOW_WIDTH, SLOT_HEIGHT), 3)
        draw_grid()

        # スコア表示
        draw_score(score, current_time, score_flash_start, score_is_flashing)

        if game_over or game_clear:
            draw_game_status(game_over, game_clear, score, 
                           clear_time if game_clear else None)

        if active_block and not game_over and not game_clear:
            draw_block(block_x, block_y, active_block)

            # キー入力による移動と落下速度の制御
            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()

            if current_time - last_move_time > MOVE_DELAY:
                if keys[pygame.K_LEFT] and not check_collision(block_x - 1, block_y, active_block):
                    block_x -= 1
                    last_move_time = current_time
                if keys[pygame.K_RIGHT] and not check_collision(block_x + 1, block_y, active_block):
                    block_x += 1
                    last_move_time = current_time

            fall_speed = fast_fall_speed if keys[pygame.K_DOWN] else normal_fall_speed

            if current_time - last_fall_time > fall_speed:
                if not check_collision(block_x, block_y + 1, active_block):
                    block_y += 1
                else:
                    fix_block(block_x, block_y, active_block)
                    block_fall_sound.play()
                    lines_score = check_and_clear_lines()
                    score += lines_score

                    # クリア判定
                    if not game_clear and check_game_clear(score):
                        game_clear = True
                        game_clear_sound.play()
                        clear_time = time.time() - start_time

                    # ゲームオーバー判定
                    if check_game_over() == "stack":
                        game_over = True
                        game_over_sound.play()

                    active_block = None
                    block_x, block_y = 4, 0
                    remaining_time = MAX_TIME
                last_fall_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and (game_over or game_clear):
                    # ゲームリセット
                    game_over = False
                    game_clear = False
                    score = 0
                    slots = init_game()
                    active_block = None
                    block_x, block_y = 4, 0
                    remaining_time = MAX_TIME
                    start_time = time.time()
                    game_start_sound.play()
                elif event.key == pygame.K_UP and active_block and not game_over and not game_clear:
                    if active_block != "O":
                        temp_coords = block_data[active_block][1]
                        new_coords = rotate_block(active_block)
                        if check_rotation_valid(block_x, block_y, new_coords):
                            block_data[active_block] = (block_data[active_block][0], new_coords)
                            block_rotate_sound.play()
                        else:
                            block_data[active_block] = (block_data[active_block][0], temp_coords)
                elif event.key == pygame.K_SPACE and active_block and not game_over and not game_clear:
                    block_y = get_hard_drop_position(block_x, block_y, active_block)
                    hard_drop_sound.play()
                    fix_block(block_x, block_y, active_block)
                    block_score = len(block_data[active_block][1])
                    score += block_score
                    lines_score = check_and_clear_lines()
                    score += lines_score

                    if not game_clear and check_game_clear(score):
                        game_clear = True
                        game_clear_sound.play()
                        clear_time = time.time() - start_time

                    if check_game_over() == "stack":
                        game_over = True

                    active_block = None
                    block_x, block_y = 4, 0
                    remaining_time = MAX_TIME
                elif not game_over and not game_clear and not active_block and event.unicode.isalpha():
                    # タイピング判定
                    any_match = False
                    for slot in slots:
                        if slot.correct_count < len(slot.word) and \
                           event.unicode.lower() == slot.word[slot.correct_count].lower():
                            slot.correct_count += 1
                            typing_success_sound.play()
                            any_match = True
                            if slot.correct_count == len(slot.word):
                                active_block = slot.shape
                                score += len(slot.word)
                                index = slots.index(slot)
                                slots[index] = Slot(random.choice(list(block_data.keys())))
                                for other_slot in slots:
                                    if other_slot != slot:
                                        other_slot.correct_count = 0
                                remaining_time = MAX_TIME
                                break
                    #タイプミス処理
                    if not any_match:
                        score = max(0, score - 10)
                        score_is_flashing = True
                        score_flash_start = current_time
                        typing_mistake_sound.play()
                        if score == 0:
                            game_over = True
                            game_over_sound.play()
                       

        if score_is_flashing and (current_time - score_flash_start) >= SCORE_FLASH_DURATION:
            score_is_flashing = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()