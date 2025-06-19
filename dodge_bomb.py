import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向，縦方向の画面内外判定結果
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True  # 初期値：画面内
    if rct.left < 0 or WIDTH < rct.right:  # 横方向の画面外判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向の画面外判定
        tate = False
    return yoko, tate  


def g_o(screen: pg.Surface):
    """
    ゲームオーバー画面を表示する関数
    引数:
        screen: Pygameの描画Surface
    """
    #go gameover関数
    go_surface = pg.Surface((WIDTH, HEIGHT))
    go_surface.fill((0, 0, 0)) # 黒で塗りつぶし
    go_surface.set_alpha(150)
    screen.blit(go_surface, (0, 0))
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
    screen.blit(text, text_rect)
    #ckk crying koukaton
    ckk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    ckk_rct_left = ckk_img.get_rect()
    ckk_rct_left.right = text_rect.left - 20
    ckk_rct_left.centery = text_rect.centery
    screen.blit(ckk_img, ckk_rct_left)
    ckk_rct_right = ckk_img.get_rect()
    ckk_rct_right.left = text_rect.right + 20
    ckk_rct_right.centery = text_rect.centery
    screen.blit(ckk_img, ckk_rct_right)

    pg.display.update()
    pg.time.wait(5000) # 5秒
    
def make_bomb() -> tuple[list, list]:
    sbb_accs = [a for a in range(1, 11)] #bombspeed
    ex_bb_imgs = [] 

    for r in range(1, 11): # 10size
        bomb_size = 20 * r
        bb_img = pg.Surface((bomb_size, bomb_size))
        pg.draw.circle(bb_img, (255, 0, 0), (bomb_size // 2, bomb_size // 2), bomb_size // 2)
        bb_img.set_colorkey((0, 0, 0)) 
        ex_bb_imgs.append(bb_img)
    
    return sbb_accs, ex_bb_imgs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    # 爆弾の拡大・加速リストを生成
    sbb_accs, ex_bb_imgs = make_bomb()

    # 爆弾Rectの初期位置をランダムに設定
    # 最初は最小サイズの爆弾Rectを使用
    bb_rct = ex_bb_imgs[0].get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    
    vx, vy = +5, +5  #firstspeed
    
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        # こうかとんRectと爆弾Rectの衝突判定
        if kk_rct.colliderect(bb_rct):
            g_o(screen) # collgo
            return 

        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        
        # tmrの値に応じて、爆弾の拡大率と加速度を選択
        idx = min(tmr // 500, len(sbb_accs) - 8) 
        
        current_bb_img = ex_bb_imgs[idx]
        acceleration_factor = sbb_accs[idx]

        # 爆弾の移動
        bb_rct.move_ip(vx * acceleration_factor, vy * acceleration_factor)
        
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(current_bb_img, bb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50) # 50


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()