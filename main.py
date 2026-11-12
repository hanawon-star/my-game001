import sys
import random
import pygame

# 초기화 및 설정
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge & Collect Game")
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
RED = (235, 60, 60)
BLUE = (50, 150, 255)
GOLD = (255, 215, 0)

# 플레이어 설정
player_size = 40
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 80
player_speed = 7

# 장애물 및 아이템 설정
obstacles = []
coins = []
obstacle_speed = 5
spawn_counter = 0

# 점수 및 상태
score = 0
game_over = False
font = pygame.font.SysFont("malgungothic", 30)


def reset_game():
    global player_x, player_y, obstacles, coins, score, game_over, obstacle_speed
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - 80
    obstacles.clear()
    coins.clear()
    score = 0
    obstacle_speed = 5
    game_over = False


# 메인 게임 루프
running = True
while running:
    clock.tick(60)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_game()

    if not game_over:
        # 키 입력
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (
            keys[pygame.K_RIGHT] or keys[pygame.K_d]
        ) and player_x < WIDTH - player_size:
            player_x += player_speed

        # 장애물 및 코인 생성
        spawn_counter += 1
        if spawn_counter >= 30:
            spawn_counter = 0
            # 장애물 생성
            obs_x = random.randint(0, WIDTH - 30)
            obstacles.append(pygame.Rect(obs_x, -30, 30, 30))

            # 확률적으로 코인 생성
            if random.random() < 0.4:
                coin_x = random.randint(0, WIDTH - 25)
                coins.append(pygame.Rect(coin_x, -25, 25, 25))

        # 플레이어 히트박스
        player_rect = pygame.Rect(
            player_x, player_y, player_size, player_size
        )

        # 장애물 이동 및 충돌 검사
        for obs in obstacles[:]:
            obs.y += obstacle_speed
            if obs.colliderect(player_rect):
                game_over = True
            if obs.y > HEIGHT:
                obstacles.remove(obs)

        # 코인 이동 및 획득 검사
        for coin in coins[:]:
            coin.y += obstacle_speed
            if coin.colliderect(player_rect):
                score += 10
                coins.remove(coin)
                # 점수에 따라 난이도 상승
                if score % 50 == 0:
                    obstacle_speed += 0.5
            elif coin.y > HEIGHT:
                coins.remove(coin)

    # 화면 그리기
    screen.fill(BLACK)

    if not game_over:
        # 플레이어 (파란색 사각형)
        pygame.draw.rect(screen, BLUE, player_rect, border_radius=8)

        # 장애물 (빨간색 사각형)
        for obs in obstacles:
            pygame.draw.rect(screen, RED, obs, border_radius=5)

        # 코인 (노란색 원)
        for coin in coins:
            pygame.draw.circle(screen, GOLD, coin.center, 12)

        # 점수 표시
        score_text = font.render(f"SCORE: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    else:
        # 게임 오버 화면
        over_text = font.render("GAME OVER", True, RED)
        restart_text = font.render(
            "Press 'R' to Restart", True, WHITE
        )
        final_score_text = font.render(
            f"Final Score: {score}", True, GOLD
        )

        screen.blit(
            over_text,
            (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 60),
        )
        screen.blit(
            final_score_text,
            (
                WIDTH // 2 - final_score_text.get_width() // 2,
                HEIGHT // 2,
            ),
        )
        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                HEIGHT // 2 + 60,
            ),
        )

    pygame.display.flip()

pygame.quit()
sys.exit()
