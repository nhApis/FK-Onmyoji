'''
Project:FK-Onmyoji
Version:Beta 1.0.1

Powered By BluePlum Studio:lzycc234
https://github.com/BluePlumStudio/FK-Onmyoji
'''
#代码垃圾，不喜轻喷

import pyautogui as gui
import time
import datetime
import random
import threading
import os
import sys
import winsound
import cv2
import keyboard
import pathlib
import win32gui
import win32con
import win32clipboard

screenWidth,screenHeight=gui.size()
gui.PAUSE=0.0
#gui.FAILSAFE=False
mainLocker=threading.Lock()
feedbackerLocker=threading.Lock()
lastOperationTime=time.time()
isBossDetected=False

IMAGE_FAILED_PATH="./screenshots/failed.png"
IMAGE_SCREENSHOT_PATH="./screenshots/screenshot.png"
IMAGE_CONNECTING_PATH="./screenshots/connecting.png"
IMAGE_ASSISTANCE_PATH="./screenshots/assistance.png"
IMAGE_ACCEPT_PATH="./screenshots/accept.png"
IMAGE_OCCUPIED_PATH="./screenshots/occupied.png"

IMAGE_MITAMA_START_PATH="./screenshots/Mitama/start.png"
IMAGE_MITAMA_FINISHED1_PATH="./screenshots/Mitama/finished1.png"
IMAGE_MITAMA_FINISHED2_PATH="./screenshots/Mitama/finished2.png"

IMAGE_STROY_INVITE_PATH="./screenshots/Story/invite.png"
IMAGE_STROY_INVITATION_CONFIRMED_PATH="./screenshots/Story/invitationConfirmed.png"
IMAGE_STROY_START_PATH="./screenshots/Story/start.png"
IMAGE_STROY_FIGHT_PATH="./screenshots/Story/fight.png"
IMAGE_STROY_FIGHT_BOSS_PATH="./screenshots/Story/fightBoss.png"
IMAGE_STROY_FINISHED1_PATH="./screenshots/Story/finished1.png"
IMAGE_STROY_FINISHED2_PATH="./screenshots/Story/finished2.png"
IMAGE_STROY_ACCEPT_PATH="./screenshots/Story/accept.png"
IMAGE_STROY_BACK_PATH="./screenshots/Story/back.png"
IMAGE_STROY_GET_REWARD_PATH="./screenshots/Story/getReward.png"
IMAGE_STROY_REWARD_CONFIRMED_PATH="./screenshots/Story/rewardConfirmed.png"

IMAGE_MITAMA_X_START_PATH="./screenshots/MitamaX/start.png"
IMAGE_MITAMA_X_FINISHED1_PATH="./screenshots/MitamaX/finished1.png"
IMAGE_MITAMA_X_FINISHED2_PATH="./screenshots/MitamaX/finished2.png"

IMAGE_BREACH_START_PATH="./screenshots/Breach/start.png"
IMAGE_BREACH_SECTION_PATH="./screenshots/Breach/section.png"
IMAGE_BREACH_FINISHED1_PATH="./screenshots/Breach/finished1.png"
IMAGE_BREACH_FINISHED2_PATH="./screenshots/Breach/finished2.png"
IMAGE_BREACH_SHIKIGAMI_SELECTED_PATH="./screenshots/Breach/shikigamiSelected.png"
IMAGE_BREACH_SELECTION_MARK_PATH="./screenshots/Breach/selectionMark.png"


def getTimeFormatted():
    return time.strftime("[%Y-%m-%d %H:%M:%S]",time.localtime())

def printWithTime(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    print(getTimeFormatted()+":", sep=' ', end='')
    print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)

def inputWithTimePrompt(prompt):
    return input(getTimeFormatted()+":"+prompt)
    
def clickLeftButton():
    global lastOperationTime
    
    mainLocker.acquire()
    gui.click()
    lastOperationTime=time.time()
    mainLocker.release()

def genPositionOffsets(position):
    offsetX=round(random.uniform(-1,1)*position.width/2,4)
    offsetY=round(random.uniform(-1,1)*position.height/2,4)
    return offsetX,offsetY

def resetMousePosition(startX,startY,windowWidth,windowHeight):
    mainLocker.acquire()
    gui.moveTo(startX+random.uniform(0.3,0.7)*windowWidth,
               startY+random.uniform(0.3,0.7)*windowHeight+30,
               0.2,
               gui.easeInElastic)
    mainLocker.release()

def clickMouseRandomly(startX,startY,windowWidth,windowHeight):
    global lastOperationTime
    
    mainLocker.acquire()
    gui.moveTo(startX+random.uniform(0.3,0.7)*windowWidth,
               startY+random.uniform(0.3,0.7)*windowHeight+30,
               0.2,
               gui.easeInElastic)
    gui.click()
    lastOperationTime=time.time()
    mainLocker.release()

def clickImageRandomly(path,clicks=1,duration=0.1,startX=0,startY=0,windowWidth=screenWidth,windowHeight=screenHeight,accuracy=0.9):
    global lastOperationTime

    ret=False
    mainLocker.acquire()
    position=gui.locateOnScreen(path,region=(startX,startY,windowWidth,windowHeight),confidence=accuracy)
    if position:
        x,y=gui.center(position)
        offsetX,offsetY=genPositionOffsets(position)
        printWithTime("账户:%s:"%(threading.current_thread().name)+"clickImageRandomly():"+path+"\tPosition:"+"X="+str(x)+" Y="+str(y))
        printWithTime("账户:%s:"%(threading.current_thread().name)+"clickImageRandomly():"+path+"\t"+"OffsetX="+str(offsetX)+" OffsetY="+str(offsetY))
        gui.moveTo(x+offsetX,y+offsetY,duration,gui.easeInElastic)
        gui.click(x+offsetX,y+offsetY,clicks,random.uniform(0.1,1))
        lastOperationTime=time.time()
        ret=True
    else:
        ret=False
        printWithTime("账户:%s:"%(threading.current_thread().name)+"clickImageRandomly():查找"+path+"失败")
    mainLocker.release()

    return ret

def dragMouseRandomly(directionX,directionY,windowWidth,windowHeight):
    global lastOperationTime
    
    moveX=round(directionX*random.uniform(0.1,0.5)*windowWidth,4)
    moveY=round(directionY*random.uniform(0.1,0.5)*windowHeight,4)

    mainLocker.acquire()
    printWithTime("账户:%s:dragMouseRandomly():MoveX=%s MoveY=%s"%(threading.current_thread().name,str(moveX),str(moveY)))
    gui.mouseDown()
    #gui.drag(moveX,moveY,button="left")
    gui.move(moveX,moveY,0.35,gui.easeInElastic)
    gui.mouseUp()
    lastOperationTime=time.time()
    mainLocker.release()

def waitImageDetected(path,startX=0,startY=0,windowWidth=screenWidth,windowHeight=screenHeight,accuracy=0.9):
    while gui.locateOnScreen(path,region=(startX,startY,windowWidth,windowHeight),confidence=accuracy)==None:
        continue
    printWithTime("账户:%s:"%(threading.current_thread().name)+"waitImageDetected():检测到:"+path)
    
def isImageDetected(path,startX=0,startY=0,windowWidth=screenWidth,windowHeight=screenHeight,accuracy=0.9):
    if gui.locateOnScreen(path,region=(startX,startY,windowWidth,windowHeight),confidence=accuracy)==None:
        return False
    else:
        return True

def gameTypeMitama(startX,startY,windowWidth,windowHeight,isCaptain):
    if isCaptain:
        time.sleep(3)
        printWithTime("消息:账户:%s:等待开始"%(threading.current_thread().name))
        waitImageDetected(IMAGE_MITAMA_START_PATH,startX,startY,windowWidth,windowHeight)
        clickImageRandomly(IMAGE_MITAMA_START_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
        while isImageDetected(IMAGE_MITAMA_START_PATH,startX,startY,windowWidth,windowHeight):
            clickImageRandomly(IMAGE_MITAMA_START_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
    ##########
    printWithTime("消息:账户:%s:等待结束界面1"%(threading.current_thread().name))
    waitImageDetected(IMAGE_MITAMA_FINISHED1_PATH,startX,startY,windowWidth,windowHeight)
    clickImageRandomly(IMAGE_MITAMA_FINISHED1_PATH,2,0.15,startX,startY,windowWidth,windowHeight)
    while isImageDetected(IMAGE_MITAMA_FINISHED1_PATH,startX,startY,windowWidth,windowHeight):
        clickImageRandomly(IMAGE_MITAMA_FINISHED1_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
    ##########
    time.sleep(0.5)
    printWithTime("消息:账户:%s:等待结束界面2"%(threading.current_thread().name))
    waitImageDetected(IMAGE_MITAMA_FINISHED2_PATH,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))
    clickImageRandomly(IMAGE_MITAMA_FINISHED2_PATH,2,0.15,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))
    while isImageDetected(IMAGE_MITAMA_FINISHED2_PATH,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3)):
        clickImageRandomly(IMAGE_MITAMA_FINISHED2_PATH,1,0.15,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))

def gameTypeStory(startX,startY,windowWidth,windowHeight,isCaptain):
    global isBossDetected
    isBossDetected=False
    
    if isCaptain:
        printWithTime("消息:账户:%s:等待开始"%(threading.current_thread().name))
        while (isImageDetected(IMAGE_STROY_INVITE_PATH,startX,startY,windowWidth,windowHeight)==False
               or isImageDetected(IMAGE_STROY_INVITATION_CONFIRMED_PATH,startX,startY,windowWidth,windowHeight)==False
               or isImageDetected(IMAGE_STROY_START_PATH,startX,startY,windowWidth,windowHeight))==False:
            continue
            
        while (isImageDetected(IMAGE_STROY_INVITE_PATH,startX,startY,windowWidth,windowHeight)
               or isImageDetected(IMAGE_STROY_INVITATION_CONFIRMED_PATH,startX,startY,windowWidth,windowHeight)
               or isImageDetected(IMAGE_STROY_START_PATH,startX,startY,windowWidth,windowHeight)):
            if isImageDetected(IMAGE_STROY_INVITE_PATH,startX,startY,windowWidth,windowHeight):
                clickImageRandomly(IMAGE_STROY_INVITE_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
                while isImageDetected(IMAGE_STROY_INVITE_PATH,startX,startY,windowWidth,windowHeight):
                    clickImageRandomly(IMAGE_STROY_INVITE_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
                break
            elif isImageDetected(IMAGE_STROY_INVITATION_CONFIRMED_PATH,startX,startY,windowWidth,windowHeight):
                clickImageRandomly(IMAGE_STROY_INVITATION_CONFIRMED_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
                while isImageDetected(IMAGE_STROY_INVITATION_CONFIRMED_PATH,startX,startY,windowWidth,windowHeight):
                    clickImageRandomly(IMAGE_STROY_INVITATION_CONFIRMED_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
                break
            elif isImageDetected(IMAGE_STROY_START_PATH,startX,startY,windowWidth,windowHeight):
                clickImageRandomly(IMAGE_STROY_START_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
                while isImageDetected(IMAGE_STROY_START_PATH,startX,startY,windowWidth,windowHeight):
                    clickImageRandomly(IMAGE_STROY_START_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
                break

        time.sleep(5.0)
        while True:
            printWithTime("消息:账户:%s:等待开战"%(threading.current_thread().name))
            detectCount=15
            xDirection=-1.0
            while detectCount:
                detectCount-=1
                if (isImageDetected(IMAGE_STROY_FIGHT_PATH,startX,startY,windowWidth-30,windowHeight)==False
                       and isImageDetected(IMAGE_STROY_FIGHT_BOSS_PATH,startX,startY,windowWidth-30,windowHeight)==False):
                    resetMousePosition(startX,startY,windowWidth,windowHeight)
                    dragMouseRandomly(xDirection,random.uniform(0.01,0.1),windowWidth,windowHeight)
                    printWithTime("账户:%s:第%s次检测:%s"
                                  %(threading.current_thread().name,str(15-detectCount),IMAGE_STROY_FIGHT_PATH))
                    printWithTime("账户:%s:第%s次检测:%s"
                                  %(threading.current_thread().name,str(15-detectCount),IMAGE_STROY_FIGHT_BOSS_PATH))
                elif detectCount==0:
                    detectCount=15
                    xDirection=-xDirection
                else:
                    break
                
            if isImageDetected(IMAGE_STROY_FIGHT_PATH,startX,startY,windowWidth,windowHeight):
                clickImageRandomly(IMAGE_STROY_FIGHT_PATH,1,0.1,startX,startY,windowWidth,windowHeight)
                while isImageDetected(IMAGE_STROY_FIGHT_PATH,startX,startY,windowWidth,windowHeight):
                    clickImageRandomly(IMAGE_STROY_FIGHT_PATH,1,0.1,startX,startY,windowWidth,windowHeight)
            elif isImageDetected(IMAGE_STROY_FIGHT_BOSS_PATH,startX,startY,windowWidth,windowHeight):
                clickImageRandomly(IMAGE_STROY_FIGHT_BOSS_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
                while isImageDetected(IMAGE_STROY_FIGHT_BOSS_PATH,startX,startY,windowWidth,windowHeight):
                    clickImageRandomly(IMAGE_STROY_FIGHT_BOSS_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
                mainLocker.acquire()
                isBossDetected=True
                mainLocker.release()

            time.sleep(3.0)
            printWithTime("消息:账户:%s:等待结束界面1"%(threading.current_thread().name))
            waitImageDetected(IMAGE_STROY_FINISHED1_PATH,startX,startY,windowWidth,windowHeight)
            clickImageRandomly(IMAGE_STROY_FINISHED1_PATH,2,0.15,startX,startY,windowWidth,windowHeight)
            while isImageDetected(IMAGE_STROY_FINISHED1_PATH,startX,startY,windowWidth,windowHeight):
                clickImageRandomly(IMAGE_STROY_FINISHED1_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
            ##########
            time.sleep(0.4)
            printWithTime("消息:账户:%s:等待结束界面2"%(threading.current_thread().name))
            waitImageDetected(IMAGE_STROY_FINISHED2_PATH,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))
            clickImageRandomly(IMAGE_STROY_FINISHED2_PATH,2,0.15,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))
            while isImageDetected(IMAGE_STROY_FINISHED2_PATH,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3)):
                clickImageRandomly(IMAGE_STROY_FINISHED2_PATH,1,0.15,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))

            if isBossDetected:
                break
        
    else:
        printWithTime("消息:账户:%s:等待开始"%(threading.current_thread().name))
        waitImageDetected(IMAGE_STROY_ACCEPT_PATH,startX,startY,windowWidth,windowHeight)
        clickImageRandomly(IMAGE_STROY_ACCEPT_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
        while isImageDetected(IMAGE_STROY_ACCEPT_PATH,startX,startY,windowWidth,windowHeight):
            clickImageRandomly(IMAGE_STROY_ACCEPT_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
            
        time.sleep(1.0)
        while True:
            time.sleep(3.0)
            printWithTime("消息:账户:%s:等待结束界面1"%(threading.current_thread().name))
            waitImageDetected(IMAGE_STROY_FINISHED1_PATH,startX,startY,windowWidth,windowHeight)
            clickImageRandomly(IMAGE_STROY_FINISHED1_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
            while isImageDetected(IMAGE_STROY_FINISHED1_PATH,startX,startY,windowWidth,windowHeight):
                clickImageRandomly(IMAGE_STROY_FINISHED1_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
            ##########
            time.sleep(0.5)
            printWithTime("消息:账户:%s:等待结束界面2"%(threading.current_thread().name))
            waitImageDetected(IMAGE_STROY_FINISHED2_PATH,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))
            clickImageRandomly(IMAGE_STROY_FINISHED2_PATH,2,0.15,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))
            while isImageDetected(IMAGE_STROY_FINISHED2_PATH,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3)):
                clickImageRandomly(IMAGE_STROY_FINISHED2_PATH,1,0.15,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))

            if isBossDetected:
                break
    #waitImageDetected(IMAGE_STROY_GET_REWARD_PATH,startX,startY,windowWidth,windowHeight)
    '''不稳定'''
    waitImageDetected(IMAGE_STROY_BACK_PATH,startX,startY,windowWidth,windowHeight)
    
    while isImageDetected(IMAGE_STROY_BACK_PATH,startX,startY,windowWidth,windowHeight):
        while isImageDetected(IMAGE_STROY_GET_REWARD_PATH,startX,startY,windowWidth,windowHeight):
            clickImageRandomly(IMAGE_STROY_GET_REWARD_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
            while (isImageDetected(IMAGE_STROY_GET_REWARD_PATH,startX,startY,windowWidth,windowHeight)
                   and isImageDetected(IMAGE_STROY_REWARD_CONFIRMED_PATH,startX,startY,windowWidth,windowHeight)==False):
                clickImageRandomly(IMAGE_STROY_GET_REWARD_PATH,1,0.15,startX+30,startY,windowWidth,windowHeight)
            waitImageDetected(IMAGE_STROY_REWARD_CONFIRMED_PATH,startX,startY,windowWidth,windowHeight)
            clickMouseRandomly(startX,startY,windowWidth/4,windowHeight/8)
            while isImageDetected(IMAGE_STROY_REWARD_CONFIRMED_PATH,startX,startY,windowWidth,windowHeight):
                clickMouseRandomly(startX+30,startY,windowWidth/4,windowHeight/8)
    
    #winsound.Beep(800,1000)

def gameTypeMitamaX(startX,startY,windowWidth,windowHeight,isCaptain):
    printWithTime("消息:账户:%s:等待开始"%(threading.current_thread().name))
    waitImageDetected(IMAGE_MITAMA_X_START_PATH,startX,startY,windowWidth,windowHeight)
    clickImageRandomly(IMAGE_MITAMA_X_START_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
    while isImageDetected(IMAGE_MITAMA_X_START_PATH,startX,startY,windowWidth,windowHeight):
        clickImageRandomly(IMAGE_MITAMA_X_START_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
    ##########
    printWithTime("消息:账户:%s:等待结束界面1"%(threading.current_thread().name))
    waitImageDetected(IMAGE_MITAMA_X_FINISHED1_PATH,startX,startY,windowWidth,windowHeight)
    clickImageRandomly(IMAGE_MITAMA_X_FINISHED1_PATH,2,0.15,startX,startY,windowWidth,windowHeight)
    while isImageDetected(IMAGE_MITAMA_X_FINISHED1_PATH,startX,startY,windowWidth,windowHeight):
        clickImageRandomly(IMAGE_MITAMA_X_FINISHED1_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
    ##########
    time.sleep(0.5)
    printWithTime("消息:账户:%s:等待结束界面2"%(threading.current_thread().name))
    waitImageDetected(IMAGE_MITAMA_X_FINISHED2_PATH,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))
    clickImageRandomly(IMAGE_MITAMA_X_FINISHED2_PATH,2,0.15,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))
    while isImageDetected(IMAGE_MITAMA_X_FINISHED2_PATH,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3)):
        clickImageRandomly(IMAGE_MITAMA_X_FINISHED2_PATH,1,0.15,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))

def gameTypeBreach(startX,startY,windowWidth,windowHeight,isCaptain):
    printWithTime("消息:账户:%s:等待开始"%(threading.current_thread().name))
    waitImageDetected(IMAGE_BREACH_SECTION_PATH,startX,startY,windowWidth,windowHeight)
    clickImageRandomly(IMAGE_BREACH_SECTION_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
    while (isImageDetected(IMAGE_BREACH_SECTION_PATH,startX,startY,windowWidth,windowHeight)
           and isImageDetected(IMAGE_BREACH_START_PATH,startX,startY,windowWidth,windowHeight)==False):
        clickImageRandomly(IMAGE_BREACH_SECTION_PATH,1,0.15,startX,startY,windowWidth,windowHeight)

    waitImageDetected(IMAGE_BREACH_START_PATH,startX,startY,windowWidth,windowHeight)
    clickImageRandomly(IMAGE_BREACH_START_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
    while isImageDetected(IMAGE_BREACH_START_PATH,startX,startY,windowWidth,windowHeight):
        clickImageRandomly(IMAGE_BREACH_START_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
    ##########
    if pathlib.Path(IMAGE_BREACH_SHIKIGAMI_SELECTED_PATH).exists():
        printWithTime("账户:%s:检测到被选式神"%(threading.current_thread().name))
        while (isImageDetected(IMAGE_BREACH_SELECTION_MARK_PATH,startX,startY,windowWidth,windowHeight)==False
               and isImageDetected(IMAGE_BREACH_FINISHED1_PATH,startX,startY,windowWidth,windowHeight)==False):
            clickImageRandomly(IMAGE_BREACH_SHIKIGAMI_SELECTED_PATH,1,0.25,startX,startY,windowWidth,windowHeight)
    ##########
    printWithTime("消息:账户:%s:等待结束界面1"%(threading.current_thread().name))
    waitImageDetected(IMAGE_BREACH_FINISHED1_PATH,startX,startY,windowWidth,windowHeight)
    clickImageRandomly(IMAGE_BREACH_FINISHED1_PATH,2,0.15,startX,startY,windowWidth,windowHeight)
    while isImageDetected(IMAGE_BREACH_FINISHED1_PATH,startX,startY,windowWidth,windowHeight):
        clickImageRandomly(IMAGE_BREACH_FINISHED1_PATH,1,0.15,startX,startY,windowWidth,windowHeight)
    ##########
    time.sleep(0.5)
    printWithTime("消息:账户:%s:等待结束界面2"%(threading.current_thread().name))
    waitImageDetected(IMAGE_BREACH_FINISHED2_PATH,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))
    clickImageRandomly(IMAGE_BREACH_FINISHED2_PATH,2,0.15,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))
    while isImageDetected(IMAGE_BREACH_FINISHED2_PATH,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3)):
        clickImageRandomly(IMAGE_BREACH_FINISHED2_PATH,1,0.15,startX,int(startY+windowHeight*2/3),windowWidth,int(windowHeight/3))

def account(number,gameType,limit,startX,startY,windowWidth,windowHeight,isCaptain,feedbackerName):
    threads=[];
    
    failureDetector=threading.Thread(None,detectFailure,
                                     "account:"+str(number),args=(threading.current_thread(),startX,startY,windowWidth,windowHeight))
    disconnectionDetector=threading.Thread(None,detectDisconnection,
                                           "account:"+str(number),args=(threading.current_thread(),startX,startY,windowWidth,windowHeight))
    interceptionDetector=threading.Thread(None,detectInterception,
                                           "account:"+str(number),args=(startX,startY,windowWidth,windowHeight))
    assistanceDetector=threading.Thread(None,detectAssistance,
                                           "account:"+str(number),args=(startX,startY,windowWidth,windowHeight))
    if gameType!=4:
        threads.append(failureDetector)
    threads.append(disconnectionDetector)
    threads.append(interceptionDetector)
    threads.append(assistanceDetector)
    for thread in threads:
        thread.start()
    
    printWithTime("账户:%s"%(threading.current_thread().name))
    count=0
    while count<limit:
        seconds=4
        while seconds:
            printWithTime("账户:%s:"%(threading.current_thread().name)+str(seconds)+"s后开始")
            time.sleep(1)
            seconds-=1
        mainLocker.acquire()
        printWithTime("账户:%s:"%(threading.current_thread().name)+"开始")
        printWithTime("账户:%s:"%(threading.current_thread().name)+"\n"
              +"\t局数:"+str(limit)+"\n"
              +"\t窗口起始位置X:"+str(startX)+"\n"
              +"\t窗口起始位置Y:"+str(startY)+"\n"
              +"\t窗口宽度:"+str(windowWidth)+"\n"
              +"\t窗口高度:"+str(windowHeight)+"\n"
              +"\t是否为房主(Y/N):"+str(isCaptain))
        mainLocker.release()

        if gameType==1:
            gameTypeMitama(startX,startY,windowWidth,windowHeight,isCaptain)
        elif gameType==2:
            gameTypeStory(startX,startY,windowWidth,windowHeight,isCaptain)
        elif gameType==3:
            gameTypeMitamaX(startX,startY,windowWidth,windowHeight,isCaptain)
        elif gameType==4:
            gameTypeBreach(startX,startY,windowWidth,windowHeight,isCaptain)
            
        count+=1
        printWithTime("账户:%s:游戏类型:%s,已完成%s局"%(threading.current_thread().name,str(gameType),str(count)))
        message="%s:账户:%s:游戏类型:%s,已完成%s局"%(getTimeFormatted(),threading.current_thread().name,str(gameType),str(count))
        threading.Thread(None,feedbacker,"account:"+str(number),args=(threading.current_thread().name,feedbackerName,message)).start()
    print("==============================")
    printWithTime("账户:%s:游戏类型:%s,已完成"%(threading.current_thread().name,str(gameType)))
    message="%s:账户:%s:游戏类型:%s,已完成"%(getTimeFormatted(),threading.current_thread().name,str(gameType))
    threading.Thread(None,feedbacker,"account:"+str(number),args=(threading.current_thread().name,feedbackerName,message)).start()
    winsound.Beep(1200,10000)
    os.system("taskkill /IM onmyoji.exe /F")

def detectFailure(accountThread,startX,startY,windowWidth,windowHeight):
    global lastOperationTime
    
    waitImageDetected(IMAGE_FAILED_PATH,startX,startY,windowWidth,windowHeight)
    message="账户:%s:失败，请重新运行!"%(accountThread.name)
    gui.screenshot(IMAGE_SCREENSHOT_PATH)
    printWithTime(message)
    def inner():
        mainLocker.acquire()
        lastOperationTime=time.time()
        mainLocker.release()
        winsound.Beep(800,60000)
        os.system("taskkill /IM onmyoji.exe /F")
        winsound.Beep(800,10000)
    threading.Thread(None,inner,"account:"+str(accountThread.name)).start()
    mainLocker.acquire()
    gui.alert(message,"错误",button="确定")

def detectDisconnection(accountThread,startX,startY,windowWidth,windowHeight):
    global lastOperationTime

    while (True):
        waitImageDetected(IMAGE_CONNECTING_PATH,startX,startY,windowWidth,windowHeight)
        message="账户:%s:正在重新连接。。。。。。"%(accountThread.name)
        printWithTime(message)
        winsound.Beep(1000,10000)
	
def detectInterception(startX,startY,windowWidth,windowHeight):
    global lastOperationTime
    
    while (True):
        time.sleep(301)
        
        currentTime=time.time()
        if (time.time()-lastOperationTime)>=300.0:
            printWithTime("警告:已检查到超过5分钟未执行任何操作!\tCurrent Time:%s Last Operation Time:%s"%(currentTime,lastOperationTime))
            clickMouseRandomly(startX,startY,windowWidth,windowHeight)
            clickMouseRandomly(startX,startY,windowWidth,windowHeight)
            winsound.Beep(1000,3000)
        

def detectAssistance(startX,startY,windowWidth,windowHeight):
    while (True):
        waitImageDetected(IMAGE_ASSISTANCE_PATH,startX,startY,windowWidth,windowHeight)
        printWithTime("账户:%s:检测到悬赏封印邀请"%(threading.current_thread().name))
        winsound.Beep(1000,500)
        waitImageDetected(IMAGE_ACCEPT_PATH,startX,startY,windowWidth,windowHeight)
        clickImageRandomly(IMAGE_ACCEPT_PATH,2,0.15,startX,startY,windowWidth,windowHeight)
        while isImageDetected(IMAGE_ACCEPT_PATH,startX,startY,windowWidth,windowHeight):
            clickImageRandomly(IMAGE_ACCEPT_PATH,1,0.1,startX,startY,windowWidth,windowHeight)
        printWithTime("账户:%s:已尝试接受悬赏封印邀请"%(threading.current_thread().name))

def detectOccupation():
    global lastOperationTime
    
    waitImageDetected(IMAGE_OCCUPIED_PATH,0,0,screenWidth,screenHeight)
    message="错误:检测到账户在其他设备登录!"
    printWithTime(message)
    def inner():
        mainLocker.acquire()
        lastOperationTime=time.time()
        mainLocker.release()
        winsound.Beep(1000,30000)
        os.system("taskkill /IM onmyoji.exe /F")
        winsound.Beep(1000,10000)
    threading.Thread(None,inner).start()
    mainLocker.acquire()
    gui.alert(message,"错误",button="确定")

def detectPause():
    isPaused=False
    while (True):
        keyboard.wait('p')
        if isPaused==False:
            printWithTime("警告:脚本已暂停!")
            isPaused=True
            mainLocker.acquire()
        elif isPaused:
            printWithTime("警告:脚本已启动!")
            isPaused=False
            mainLocker.release()

def feedbacker(accountName,feedbackerName,message):
    printWithTime("账户:%s:反馈者:%s"%(accountName,feedbackerName))
    qqWindow = win32gui.FindWindow(None, feedbackerName)
    if qqWindow==0:
        printWithTime("账户:%s:无法定位到反馈者:%s"%(accountName,feedbackerName))
        return
    feedbackerLocker.acquire()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, message)
    win32clipboard.CloseClipboard()

    qqWindow = win32gui.FindWindow(None, feedbackerName)

    win32gui.SendMessage(qqWindow, 258, 22, 2080193)
    win32gui.SendMessage(qqWindow, 770, 0, 0)

    win32gui.SendMessage(qqWindow, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(qqWindow, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    feedbackerLocker.release()

def main():
    winsound.Beep(500,100)
    printWithTime("警告:请务必使用'管理员权限'运行!")
    threading.Thread(None,detectPause).start()
    accountCount=int(inputWithTimePrompt("账户数:"))
    threads=[];
    while accountCount:
        accountCount-=1

        gameType=int(inputWithTimePrompt("游戏类型(1.御魂/觉醒 2.章节探索 3.业原火 4.结界突破):"))
        limit=int(inputWithTimePrompt("局数:"))
        startX=int(inputWithTimePrompt("窗口起始位置X:"))
        startY=int(inputWithTimePrompt("窗口起始位置Y:"))
        windowWidth=int(inputWithTimePrompt("窗口宽度:"))
        windowHeight=int(inputWithTimePrompt("窗口高度:"))
        isCaptainChar=inputWithTimePrompt("是否为房主(Y/N):")
        feedbackerName=inputWithTimePrompt("QQ反馈者名称:")
        isCaptain=False
        if isCaptainChar=='y' or isCaptainChar=="Y":
            isCaptain=True
        else:
            isCaptain=False

        newAccount=threading.Thread(None,account,
                                    "account:"+str(accountCount),
                                    args=(accountCount,gameType,limit,startX,startY,windowWidth,windowHeight,isCaptain,feedbackerName))
        threads.append(newAccount)
    
    for thread in threads:
        thread.start()
    threading.Thread(None,detectOccupation).start()
##########
    #os.system("pause")

main()
