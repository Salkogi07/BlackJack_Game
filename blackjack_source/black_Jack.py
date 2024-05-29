import pygame
import time
import sys
import random

# 파이게임 초기화
pygame.init()

# FPS 설정
clock = pygame.time.Clock()
FPS = 15

# 현재 자금
coin = 1000

# 배팅 금액
dealcoin = 0

# 폰트 설정
myFont = pygame.font.SysFont("gillsansultra", 50, False)
font_small = pygame.font.SysFont("gillsansultra", 30, False)

# 화면 크기 설정
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# 덱 생성
suits = ["하트", "다이아몬드", "스페이드", "클로버"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

deck = [{"rank": rank, "suit": suit} for suit in suits for rank in ranks]

# 게임 상태
player_hand = []
dealer_hand = []
game_over = False
game_burst = False
pushCoin = False

# 카드 이미지 로드
card_images = {}
for suit in suits:
    for rank in ranks:
        card_image = pygame.image.load(f"images/cards/{suit}_{rank}.png")
        card_images[(rank, suit)] = pygame.transform.scale(card_image, (50, 70))

# 카드 위치
player_card_positions = [(350 + i * 60, 320) for i in range(10)]
dealer_card_positions = [(350 + i * 60, 60) for i in range(10)]

#카드 값
player_value = 0
dealer_value = 0

# 폰트 설정
font = pygame.font.Font(None, 36)

# 화면 생성
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 게임 이름 설정
pygame.display.set_caption("Jack Uli Uli")

# 아이콘 이미지 로드
widowicon = pygame.image.load("images/icon.png").convert_alpha()
pygame.display.set_icon(widowicon)

# 시작화면 배경 이미지 로드 및 크기 변경
bg = pygame.image.load("images/bg.png").convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
gameBackgroundImg1 = pygame.image.load("images/gameBackgroundImg1.png").convert()
gameBackgroundImg1 = pygame.transform.scale(gameBackgroundImg1, (SCREEN_WIDTH, SCREEN_HEIGHT))
gameBackgroundImg = pygame.image.load("images/gameBackgroundImg.png").convert()
gameBackgroundImg = pygame.transform.scale(gameBackgroundImg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 이미지 로드
Img = pygame.image.load("images/icon.png").convert()
# titleImg = pygame.image.load("images/title.png")
startImg = pygame.image.load("images/starticon.png").convert_alpha()
quitImg = pygame.image.load("images/quiticon.png").convert_alpha()
clickStartImg = pygame.image.load("images/clickedStartIcon.png").convert_alpha()
clickQuitImg = pygame.image.load("images/clickedQuitIcon.png").convert_alpha()
easyImg = pygame.image.load("images/EASY.png").convert_alpha()
hardImg = pygame.image.load("images/HARD.png").convert_alpha()
coin10 = pygame.image.load("images/10.png").convert_alpha()
coin20 = pygame.image.load("images/20.png").convert_alpha()
coin50 = pygame.image.load("images/50.png").convert_alpha()
coin100 = pygame.image.load("images/100.png").convert_alpha()
standImg = pygame.image.load("images/stand.png").convert_alpha()
dealImg = pygame.image.load("images/deal.png").convert_alpha()
hitImg = pygame.image.load("images/hit.png").convert_alpha()
backImg = pygame.image.load("images/back.png").convert_alpha()
allInButton = pygame.image.load("images/ALL IN.png").convert_alpha()
hidden_card = pygame.image.load("images/hidden_card.png").convert_alpha()
hidden_card = pygame.transform.scale(hidden_card, (50, 70))
playerBustText = pygame.image.load("images/playerBust.png").convert_alpha()
drawText = pygame.image.load("images/draw.png").convert_alpha()
playerWinDealerBustText = pygame.image.load("images/playerWinDealerBust.png").convert_alpha()
playerWinText = pygame.image.load("images/playerWin.png").convert_alpha()
dealerWinText = pygame.image.load("images/dealerWin.png").convert_alpha()
replay = pygame.image.load("images/replay.png").convert_alpha()


# 이미지의 Rect 정보를 저장
bg_Rect = bg.get_rect()

# 이미지가 가운데 올 수 있도록 좌표값 수정
bg_Rect.centerx = SCREEN_WIDTH / 2
bg_Rect.centery = SCREEN_HEIGHT / 2

# 폰트 설정
COLOR = (255, 255, 255)

myFont = pygame.font.SysFont("gillsansultra", 50, False)
text_Title = myFont.render("Jack Uli Uli", True, COLOR)
text_difficulty = myFont.render("Difficulty", True, COLOR)

# Rect 생성
text_Rect = text_Title.get_rect()

# 가로 가운데, 세로 50 위치
text_Rect.centerx = round(SCREEN_WIDTH / 2 - 15)
text_Rect.y = 100

# 게임 초기화
def init_game():
    global player_hand, dealer_hand, game_over, game_burst, pushCoin, deck
    deck = [{"rank": rank, "suit": suit} for suit in suits for rank in ranks]
    player_hand = []
    dealer_hand = []
    game_over = False
    game_burst = False
    pushCoin = False
    deal_card(player_hand)
    deal_card(player_hand)
    deal_card(dealer_hand)

# 카드 나눠주기
def deal_card(hand):
    if len(deck) > 0:  # 덱에 카드가 남아있는 경우에만 카드를 뽑음
        card = random.choice(deck)
        hand.append(card)
        deck.remove(card)

# 카드 합계 계산
def hand_value(hand):
    value = 0
    num_aces = 0

    for card in hand:
        rank = card["rank"]
        if rank in ["K", "Q", "J"]:
            value += 10
        elif rank == "A":
            value += 11
            num_aces += 1
        else:
            value += int(rank)

    while num_aces > 0 and value > 21:
        value -= 10
        num_aces -= 1

    return value

# 게임 결과 계산
def get_game_result(player_value, dealer_value):
    global coin, dealcoin, pushCoin
    if player_value > 21:
        return "P_b"
    elif dealer_value > 21:
        if pushCoin == False:
            coin += dealcoin*2
            pushCoin = True
        return "D_b"
    elif player_value == dealer_value:
        if pushCoin == False:
            coin += dealcoin
            pushCoin = True
        return "D_r"
    elif player_value > dealer_value:
        if pushCoin == False:
            coin += dealcoin*2
            pushCoin = True
        return "P_w"
    else:
        return "D_w"

def bettingCoin(bettingcoin):
    global dealcoin, coin
    if coin >= bettingcoin:
        dealcoin += bettingcoin
        coin -= bettingcoin

class Button:
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            screen.blit(img_act, (x_act, y_act))
            if click[0] and action is not None:
                time.sleep(0.3)
                action()
        else:
            screen.blit(img_in, (x, y))


def quitgame():
    pygame.quit()
    sys.exit()


def difficultyMenu():
    difficulty = True

    while difficulty:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 배경화면
        screen.blit(bg, bg_Rect)

        coin_text = font_small.render(f"coin: {coin}", True, (255, 255, 255))
        screen.blit(coin_text, (20, 10))

        # 텍스트 소환
        screen.blit(text_difficulty, (350,100))
        easyButton = Button(easyImg, 250, 250, 195, 120, easyImg, 250, 250, dealMenu)
        hardButton = Button(hardImg, 560, 230, 195, 140, hardImg, 560, 230, None)
        backButton = Button(backImg, 860, 10, 136, 91, backImg, 860, 10, title)
        pygame.display.update()
        clock.tick(FPS)


def dealMenu():
    deal = True
    global coin, dealcoin
    dealcoin = 0
    while deal:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 배경화면
        screen.blit(gameBackgroundImg1, bg_Rect)
        
        # coin 변수를 전역 변수로 사용
        coin_text = font_small.render(f"coin: {coin}", True, (255, 255, 255))
        screen.blit(coin_text, (20, 10))

        dealcoin_text = font_small.render(f"BET: {dealcoin}", True, (255, 255, 255))
        screen.blit(dealcoin_text, (20, 60))

        # 버튼 설정
        backTitleButton = Button(backImg, 860, 10, 136, 91, backImg, 860, 10, title)
        if dealcoin < 10:
            dealButton = Button(dealImg, 50, 470, 195, 105, dealImg, 50, 470, None)
        else:
            dealButton = Button(dealImg, 50, 470, 195, 105, dealImg, 50, 470, gameEasy)
        AllInButton = Button(allInButton, 795, 360, 195, 115, allInButton, 795, 360, lambda: bettingCoin(coin))
        deal10Button = Button(coin10, 375, 480, 150, 108, coin10, 375, 480, lambda: bettingCoin(10))
        deal20Button = Button(coin20, 530, 480, 150, 108, coin20, 530, 480, lambda: bettingCoin(20))
        deal50Button = Button(coin50, 685, 480, 150, 108, coin50, 685, 480, lambda: bettingCoin(50))
        deal100Button = Button(coin100, 840, 480, 150, 108, coin100, 840, 480, lambda: bettingCoin(100))

        pygame.display.update()
        clock.tick(FPS)

def dealerAI():
    global game_over, game_burst
    while hand_value(dealer_hand) < 17:
        deal_card(dealer_hand)
    game_over = True
    if hand_value(dealer_hand) > 21:
        game_burst = True

def gameEasy():
    global coin
    game = True
    global game_over, game_burst, dealer_value, player_value, pushCoin
    pushCoin = False
    game_end = False
    init_game()
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # 배경화면
        screen.blit(gameBackgroundImg, bg_Rect)

        for i, card in enumerate(player_hand):
            rank, suit = card["rank"], card["suit"]
            screen.blit(card_images[(rank, suit)], player_card_positions[i])

        for i, card in enumerate(dealer_hand):
            if not game_over or i > 0:
                rank, suit = card["rank"], card["suit"]
                screen.blit(card_images[(rank, suit)], dealer_card_positions[i])

        player_value = hand_value(player_hand)
        if(player_value > 21):
            game_burst = True
        dealer_value = hand_value(dealer_hand)

        player_text = font.render(f"Player Sum: {player_value}", True, (255, 255, 255))
        dealer_text = font.render(f"Dealer Sum: {dealer_value}", True, (255, 255, 255))
        screen.blit(player_text, (400, 400))
        screen.blit(dealer_text, (400, 20))

        coin_text = font_small.render(f"coin: {coin}", True, (255, 255, 255))
        screen.blit(coin_text, (20, 10))
        
        dealcoin_text = font_small.render(f"BET: {dealcoin}", True, (255, 255, 255))
        screen.blit(dealcoin_text, (20, 60))
        # 버튼 설정
        if game_end:
            standButton = Button(standImg, 50, 430, 195, 150, standImg, 50, 430,None)
            hitButton = Button(hitImg, 760, 480, 195, 95, hitImg, 760, 480,None)
            replayButton = Button(replay, 420, 450, 180, 112, replay, 420, 450, dealMenu)
        else:
            standButton = Button(standImg, 50, 430, 195, 150, standImg, 50, 430, dealerAI)
            hitButton = Button(hitImg, 760, 480, 195, 95, hitImg, 760, 480, lambda: deal_card(player_hand))
        if game_burst:
            game_end = True
            # 이미지의 Rect 정보를 저장
            text_Rect = playerBustText.get_rect()

            # 이미지가 가운데 올 수 있도록 좌표값 수정
            text_Rect.centerx = SCREEN_WIDTH / 2
            text_Rect.centery = SCREEN_HEIGHT / 2 -70

            if get_game_result(player_value, dealer_value) == "P_b":
               screen.blit(playerBustText, text_Rect)
            elif get_game_result(player_value, dealer_value) == "D_b":
                text_Rect.centerx = SCREEN_WIDTH / 2 -20
                text_Rect.centery = SCREEN_HEIGHT / 2 -70
                screen.blit(playerWinDealerBustText, text_Rect)
            elif get_game_result(player_value, dealer_value) == "D_r":
                text_Rect.centerx = SCREEN_WIDTH / 2 + 25
                text_Rect.centery = SCREEN_HEIGHT / 2 - 110
                screen.blit(drawText, text_Rect)
            elif get_game_result(player_value, dealer_value) == "P_w":
                text_Rect.centerx = SCREEN_WIDTH / 2 - 50
                text_Rect.centery = SCREEN_HEIGHT / 2 -70
                screen.blit(playerWinText, text_Rect)
            elif get_game_result(player_value, dealer_value) == "D_w":
                text_Rect.centerx = SCREEN_WIDTH / 2 - 50
                text_Rect.centery = SCREEN_HEIGHT / 2 -70
                screen.blit(dealerWinText, text_Rect)
        elif game_over:
            # 딜러가 17 이하일 때 카드를 계속 뽑음
            game_end = True
            while dealer_value < 17:
                deal_card(dealer_hand)
                dealer_value = hand_value(dealer_hand)
            # 이미지의 Rect 정보를 저장
            text_Rect = playerBustText.get_rect()

            # 이미지가 가운데 올 수 있도록 좌표값 수정
            text_Rect.centerx = SCREEN_WIDTH / 2
            text_Rect.centery = SCREEN_HEIGHT / 2 -70

            #결과 이미지 출력
            if get_game_result(player_value, dealer_value) == "P_b":
               screen.blit(playerBustText, text_Rect)
            elif get_game_result(player_value, dealer_value) == "D_b":
                text_Rect.centerx = SCREEN_WIDTH / 2 -20
                text_Rect.centery = SCREEN_HEIGHT / 2 -70
                screen.blit(playerWinDealerBustText, text_Rect)
            elif get_game_result(player_value, dealer_value) == "D_r":
                text_Rect.centerx = SCREEN_WIDTH / 2 + 25
                text_Rect.centery = SCREEN_HEIGHT / 2 - 110
                screen.blit(drawText, text_Rect)
            elif get_game_result(player_value, dealer_value) == "P_w":
                text_Rect.centerx = SCREEN_WIDTH / 2 - 50
                text_Rect.centery = SCREEN_HEIGHT / 2 -70
                screen.blit(playerWinText, text_Rect)
            elif get_game_result(player_value, dealer_value) == "D_w":
                text_Rect.centerx = SCREEN_WIDTH / 2 - 50
                text_Rect.centery = SCREEN_HEIGHT / 2 -70
                screen.blit(dealerWinText, text_Rect)

        pygame.display.update()
        clock.tick(FPS)

def title():
    title = True

    while title:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 배경화면
        screen.blit(bg, bg_Rect)
        # 텍스트 소환
        screen.blit(text_Title, text_Rect)
        coin_text = font_small.render(f"coin: {coin}", True, (255, 255, 255))
        screen.blit(coin_text, (20, 10))

        # titletext = screen.blit(titleImg, (220,150))
        startButton = Button(startImg, 230, 300, 220, 132, clickStartImg, 230, 300, difficultyMenu)
        quitButton = Button(quitImg, 550, 300, 220, 132, clickQuitImg, 550, 300, quitgame)
        pygame.display.update()
        clock.tick(FPS)

# 게임 시작
title()
