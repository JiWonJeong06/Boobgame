import pygame
import os
import random

# 게임초기화
pygame.init()
# 게임 창 옵션
size = [540, 960]
screen = pygame.display.set_mode(size)
#제목
title = '똥 피하기'
pygame.display.set_caption(title)
# Fps
clock = pygame.time.Clock()
#색
white = (255,255,255)
black = (0,0,0)
#최고 점수 설정
cscore = []
choiscorer = open("choiscore.txt", 'r')
line = choiscorer.readline()
cscore.append(line)
choiscorer.close
#오브젝트 설정
class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    def put_img(self, address):
        current_path = os.path.dirname(__file__)
        self.img = pygame.image.load(os.path.join(current_path,address)).convert_alpha()
        self.sx, self.sy = self.img.get_size()
    def change_size(self, sx,sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()
    def show(self):
        screen.blit(self.img, (self.x, self.y))
#크래쉬
def crash(a,b):
    if (a.x-b.sx <= b.x) and (b.x <= a.x+a.sx):
        if (a.y-b.sy <= b.y) and (b.y <= a.y+a.sy):
            return True
        else:
            return False
    else: 
        return False
#메인 캐릭터 설정
ob1 = obj()
ob1.put_img('object1.png')
ob1.change_size(50, 50)
ob1.x = round(size[0]/2)
ob1.y = size[1] -ob1.y -160
ob1.move = 5
left_go = False
right_go = False

# 4-0 대기 화면
current_path = os.path.dirname(__file__)
bg = pygame.image.load(os.path.join(current_path, 'background.png'))
run = True
while run == True:
    clock.tick(60) 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run =  False
    screen.blit(bg, (0, 0))
    font = pygame.font.Font("Maplestory Bold.ttf",25)
    text = font.render('스페이스바를 누르세요 ', True,white)
    screen.blit(text,(170, round(size[1]/2-50)))
    pygame.display.update()



# 4. 메인 이벤트
run = True
# 배경화면
current_path = os.path.dirname(__file__)
bg =pygame.image.load(os.path.join(current_path, 'background.png'))
ob3_list = []
ob2_list = []

score = 0
while run:

    # 4-1 FPS설정----------------------------------------------------
    clock.tick(60)
    # 4-2 각종 입력감지    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:#왼
                left_go = True    
            elif event.key == pygame.K_RIGHT:#오
                right_go = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
    # 오른쪽, 왼쪽 움직이기
    if left_go == True:
        ob1.x -= ob1.move
        if ob1.x <= 0: #벽나가기 금지
            ob1.x = 0
    elif right_go == True: 
        ob1.x += ob1.move
        if ob1.x >= size[0] -ob1.sx: #벽나가기 금지
            ob1.x = size[0] -ob1.sx

    #똥 떨어짐    
    if random.random() > 0.985:
        ob2 = obj()
        ob2.put_img('object2.png')
        random_size = random.randint(30,60)
        ob2.change_size(random_size, random_size)
        ob2.x = random.randrange(0,size[0]-ob2.sx-round(ob1.sx/2))
        ob2.y = 10
        speed = random.randint(3, 20)
        ob2.move = speed
        ob2_list.append(ob2) 
    d_list = []
    for i in range(len(ob2_list)):
        o2 = ob2_list[i]
        o2.y += o2.move
        if o2.y >= size[1]:
            d_list.append(i)
    for d in d_list:
        del ob2_list[d]
        #점수 받는 곳
        score += 1
    d_list = []
    #충돌
    for i in range(len(ob2_list)):
        a = ob2_list[i]
        if crash(a, ob1) == True:
            run = False
            GAME_OVER = False
    
    #그리기
    screen.blit(bg, (0, 0))

    ob1.show() #메인 캐릭터
    
    for o2 in ob2_list: #똥
        o2.show()

    font = pygame.font.Font("Maplestory Bold.ttf",20)
    font2 = pygame.font.Font("Maplestory Bold.ttf",65)
    
    text = font2.render(f'{score}', True,white)
    text2 = font.render(f'최고점수: {cscore[0]}', True,white)
    
    screen.blit(text,(round(size[0]/2-45), 60))
    screen.blit(text2,(10,5))
    # 업데이트
    pygame.display.update() 


cscore = []
choiscorer = open("choiscore.txt", 'r')

line = choiscorer.readline()
cscore.append(line)
if int(line) >= int(score):
        choiscorer.close
       
if int(line) < int(score):
        choiscorew = open("choiscore.txt", 'w')
        choiscorew.write(str(score))
        choiscorew.close()    

# 5. 게임 종료 --------------------------------------------------------
current_path = os.path.dirname(__file__)
bg = pygame.image.load(os.path.join(current_path, 'background.png'))
run = True
cscore = []
choiscorer = open("choiscore.txt", 'r')
line = choiscorer.readline()
cscore.append(line)
choiscorer.close
while GAME_OVER == False:
    clock.tick(60) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                GAME_OVER = True
    screen.blit(bg, (0, 0))
    font = pygame.font.Font("Maplestory Bold.ttf",25)

    text1 = font.render(f'    점수: {score} 점 ', True,white)
    text2 = font.render(f'최고점수: {cscore[0]} 점 ', True,white)
    
    screen.blit(text2,(160, round(size[1]/2-130)))
    screen.blit(text1,(160, round(size[1]/2-80)))
    
    pygame.display.update()
pygame.quit()