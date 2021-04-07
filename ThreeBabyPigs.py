import cs1graphics
import cs1media
import time, math, sys

class Scene:
    def __init__(self):
        self.canvas = Canvas(1600,900)
        self.canvas.setBackgroundColor((55,0,180))
        self.canvas.setTitle("3 baby pigs")
        self.canvas.wait()

        self.group = Layer()
        self.ground = Ground(self.group)
        self.sun = Sun(self.group)
        self.cloud = Cloud(self.group)
        self.stars = Stars(self.group)
        self.canvas.add(self.group)

        self.message = Text()
        self.message.setFontColor("black")
        self.message.setFontSize(50)
        self.message.moveTo(self.canvas.getWidth()/2, self.canvas.getHeight()- 60) 
        self.canvas.add(self.message)

        self.question = Text()
        self.question.setFontColor('white')
        self.question.setFontSize(50)
        self.question.moveTo(self.canvas.getWidth()/2, self.canvas.getHeight()-40)
        self.canvas.add(self.question)

    # take responese    
    def ask_response(self, prompt):
        self.question.setMessage(prompt)
        while True:
            event = self.canvas.wait()
            response = event.getDescription()
            if response == "canvas close":
                sys.exit(1)
            if response == "keyboard":
                key = event.getKey()
                self.question.setMessage("")
                if key == "y":
                    return True
                if key == "n":
                    return False
            self.question.setMessage("둘 중에 하나만 골라 ~♪ y or n ~♬")
    # 태양의 위치를 변화시키면서 동시에 배경색도 변경시킵니다.
    def move_sun(self, angle, order):
        rad = (math.pi/116.0) * angle
        self.sun.image.move(28,0)
        if order == 1:
            sky_colors = self.interpolate_colors(math.sin(rad), (55,0,180), (85, 171, 244))
            self.canvas.setBackgroundColor(sky_colors)
        elif order == 2:
            sky_colors = self.interpolate_colors(math.sin(rad), (85, 171, 244), (89, 195, 253))
            self.canvas.setBackgroundColor(sky_colors)
        elif order == 3:
            sky_colors = self.interpolate_colors(math.sin(rad), (89, 195, 253), (55,0,180))
            self.canvas.setBackgroundColor(sky_colors)
    # 변화되는 삼원색의 값을 받아오기 위한 함수입니다.
    def interpolate_colors(self, t, color1, color2):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return(int((1-t) *r1 + t * r2), int((1-t) * g1 + t * g2), int((1-t) * b1 + t*b2)) 

    def print_msg(self,msg):
        self.message.setMessage(msg)
        
class Ground:
    def __init__(self, group):
        self.shape = Rectangle(4800,300)
        self.shape.setFillColor("forest green")
        self.shape.setBorderColor("darkgreen")
        self.shape.setBorderWidth(15)
        self.shape.setDepth(79)
        self.shape.move(2200, 800)
        group.add(self.shape)

class Sun:
    def __init__(self,group):
        self.image = gg.Image("./img/sun.png")
        self.image.move(5,25)
        self.image.setDepth(20)
        group.add(self.image)

class Cloud(object):
    def __init__(self, group):
        self.image1 = Image("./img/Cloud1.png")
        self.image2 = Image("./img/Cloud2.png")
        self.image3 = Image("./img/Cloud3.png")
        self.image1.move(1765, 200)
        self.image2.move(2300, 200)
        self.image3.move(3200, 200)
        group.add(self.image1)
        group.add(self.image2)
        group.add(self.image3)

class Stars(object):
    def __init__(self, group):
        self.image = Image("./img/stars.png")
        self.image.move(4500,345)
        self.image.setDepth(80)
        group.add(self.image)
        
class Wind:
    def __init__(self):
        self.wind = Image("./img/wind.png")

    def display(self, scene, x, y):
        self.wind.move(x,y)
        scene.canvas.add(self.wind)
    def blow(self):
        for i in range(80):
            self.wind.move(4,0)
            for i in range(5):
                self.wind.move(0,5)
            for i in range(5):
                self.wind.move(0,-5)
# 이미지를 선언한 변수를 한번 canvas에 add하고 remove 했다가, 다시 add하는 것이 불가능한 것을 확인했습니다.
# 그래서 동일 이미지에 대해, 위치를 변화시키 화면상에 안보이게 했다가 다시 위치변화를 통해 등장시키는 방법을 택했습니다.
# 그것을 위한 함수입니다
    def teleport(self, x, y):
        self.wind.move(x,y)


class House(object):
    def __init__(self, intact= True): 
        self.intact = True
        self.houses = []
    
    def clear(self, sence):
        for house in self.houses:
            sence.group.remove(house)
        self.houses = []
# house를 display 시킬 때 어떤 이미지를 불러올지 intact란 parameter 값을 조정해 선택할 수 있게 만들었습니다.
    def update_state(self, intact):
        self.intact = intact
    def Hay_House(self, intact=True):
        if self.intact:
            image = Image("./img/hay_house.png")
        else:
            image = Image("./img/broken_hay_house.png")
        return image
    def Wooden_House(self, intact):
        if self.intact:
            image = Image("./img/wooden_house.png")
        else:
            image = Image("./img/broken_wooden_house.png")
        return image
    def Brick_House(self, intact):
        if self.intact:
            image = Image("./img/brick_house.png")
        else:
            image = Image("./img/open_brick_house.png")
        return image
# n 값을 이용해서 어떤 집이 나타날지 선택하는 기능입니다.
    def display(self, scene, n, x, y):
        if n == 1:
            image = self.Hay_House(self.intact)
        elif n == 2:
            image = self.Wooden_House(self.intact)
        elif n == 3:
            image = self.Brick_House(self.intact)
        image.move(x,y)
        scene.group.add(image)
        self.houses.append(image)  
# 무너진 집이 나타나도록 하는 함수입니다. hay 값을 통해서 어떤 집인지 결정합니다.
    def pull_down(self,scene, x, y, hay=True):
        if hay:
            self.update_state(False)
            self.broken_house = self.Hay_House(self.intact)
            self.broken_house.move(x, y)
            scene.group.add(self.broken_house)
        else:
            self.update_state(False)
            self.broken_house = self.Wooden_House(self.intact)
            self.broken_house.move(x, y)
            scene.group.add(self.broken_house)
# 문이 열린 집을 canvas 함수입니다.
    def open_door(self, scene, x, y):
        self.update_state(False)
        self.open_house = self.Brick_House(self.intact)
        self.open_house.move(x, y)
        self.open_house.setDepth(70)
        scene.group.add(self.open_house)        
    
class Wolf:
    def __init__(self):
        self.layer = Layer()
        self.head = Wolf_Head(self.layer)
        self.body = Wolf_Body(self.layer)
        self.arm = Wolf_Arm(self.layer)
        self.leg = Wolf_Leg(self.layer)
        self.layer.setDepth(30)
        self.wolfs = []

    def display(self, scene, x, y):
        self.layer.move(x,y)
        scene.group.add(self.layer)
    def clear(self, sence):
        for wolf in self.wolfs:
            sence.group.remove(wolf)
        self.wolfs = []
# 장면 전환시 늑대가 빨리 나타나도록 만든 함수입니다.
    def teleport(self, x, y):
        self.layer.move(x,y)
    def move(self):
        for i in range(55):
            self.layer.move(8, 0)
            for j in range(5):
                self.leg.legL.move(-5,0)
                self.leg.legR.move(5,-0)
                self.arm.armL.move(-0,2)
                self.arm.armR.move(0,-2)
                time.sleep(0.01)
            for j in range(5):
                self.leg.legR.move(-5,0)
                self.leg.legL.move(5,-0)
                self.arm.armR.move(-0,2)
                self.arm.armL.move(0,-2)      
    def blow_wind(self):
        for i in range(10):
            self.head.head.move(-2,0)
        time.sleep(1)
        for i in range(10):
            self.head.head.move(4,0)
        time.sleep(.5)
        for i in range(10):
            self.head.head.move(-2,0)
    def hurray(self):
        for i in range(3):
            self.layer.move(0, -21)
            for j in range(5):
                self.arm.armL.move(0,-2)
                self.arm.armR.move(0,2)
            for j in range(5):
                self.arm.armR.move(0,-2)
                self.arm.armL.move(0,2)
                time.sleep(0.01)
        for i in range(3):
            self.layer.move(0, 21)
            for j in range(5):
                self.arm.armL.move(0,-2)
                self.arm.armR.move(0,2)
            for j in range(5):
                self.arm.armR.move(0,-2)
                self.arm.armL.move(0,2)
                time.sleep(0.01)   
    def fall_down(self, scene, n):
        self.wolf = Image("./img/wolf"+ str(n) +".png")
        self.wolfs.append(self.wolf)
        self.wolf.move(3400-n*40, 530+n*20)
        scene.group.add(self.wolf)
        time.sleep(0.4)
    def worn_out(self):
        for i in range(5):
            self.head.head.move(8,8)
            self.arm.armL.move(0,10)
            self.arm.armR.move(0,10)
            time.sleep(0.3)
            self.head.head.move(-8,-8)
            self.arm.armL.move(0,-10)
            self.arm.armR.move(0,-10)
            time.sleep(0.3)
        
class Wolf_Head:
    def __init__(self, layer):
        self.head = Image("./img/wolf_head.png")
        self.head.move(0,-50)
        self.head.adjustReference(-5, -5)
        layer.add(self.head)


class Wolf_Body:
    def __init__(self, layer):
        self.body = Image("./img/wolf_body.png")
        self.body.move(-25,90)
        layer.add(self.body)

class Wolf_Arm:
    def __init__(self, layer):
        self.armL = Image("./img/wolf_Larm.png")
        self.armR = Image("./img/wolf_Rarm.png")
        self.armL.move(60, 50)
        self.armR.move(-75, 25)
        layer.add(self.armL)
        layer.add(self.armR)


class Wolf_Leg:
    def __init__(self, layer):
        self.legL = Image("./img/wolf_Lleg.png")
        self.legR = Image("./img/wolf_Rleg.png")
        self.legL.move(35, 180)
        self.legR.move(-60, 175)
        layer.add(self.legL)
        layer.add(self.legR)

class Pig1:
    def __init__(self):
        self.layer = Layer()
        self.face = Pig1_Face(self.layer)
        self.body = Pig1_Body(self.layer)
        self.arm = Pig1_Arm(self.layer)
        self.leg = Pig1_Leg(self.layer)
        self.layer.setDepth(51)

    def display(self, scene, x, y):
        self.layer.move(x,y)
        scene.group.add(self.layer)
    def clear(self, scene):
        scene.group.remove(self.layer)
    def teleport(self, x, y):
        self.layer.move(x,y)
    def jump(self):
        for j in range(10):
            self.layer.move(15,-25)
            self.leg.legL.move(-2,0)
            self.leg.legR.move(2,-0)
            time.sleep(0.01)
        for j in range(10):
            self.layer.move(15,25)
            self.leg.legR.move(-2,0)
            self.leg.legL.move(2,-0)
            time.sleep(0.01)
        time.sleep(0.5)
    def move(self):
        for i in range(50):
            self.layer.move(-10, 0)
            for j in range(5):
                self.leg.legL.move(-2,0)
                self.leg.legR.move(2,-0)
            for j in range(5):
                self.leg.legR.move(-2,0)
                self.leg.legL.move(2,-0)              
    def hurray(self):
        for i in range(3):
            self.layer.move(0, -21)
            for j in range(5):
                self.arm.armL.move(0,-2)
                self.arm.armR.move(0,2)
            for j in range(5):
                self.arm.armR.move(0,-2)
                self.arm.armL.move(0,2)
                time.sleep(0.01)
        for i in range(3):
            self.layer.move(0, 21)
            for j in range(5):
                self.arm.armL.move(0,-2)
                self.arm.armR.move(0,2)
            for j in range(5):
                self.arm.armR.move(0,-2)
                self.arm.armL.move(0,2)
                time.sleep(0.01)        
  
class Pig1_Face:
    def __init__(self,layer):
         self.face = Image("./img/pig1_face.png")
         self.face.move(0,0)
         layer.add(self.face)

class Pig1_Body:
    def __init__(self,layer):
         self.body=Image("./img/pig1_body.png")
         self.body.move(0,100)
         layer.add(self.body)

class Pig1_Arm:
    def __init__(self,layer):
         self.armL = Image("./img/pig1_Larm.png")
         self.armR = Image("./img/pig1_Rarm.png")
         self.armL.move(-45,65)
         self.armR.move(50,75)
         layer.add(self.armL)
         layer.add(self.armR)

class Pig1_Leg:
    def __init__(self,layer):
         self.legL = Image("./img/pig1_Lleg.png")
         self.legR = Image("./img/pig1_Rleg.png")
         self.legL.move(-10,150)
         self.legR.move(20,150)
         self.legL.setDepth(60)
         self.legR.setDepth(60)
         layer.add(self.legL)
         layer.add(self.legR)

class Pig2:
    def __init__(self):
        self.layer = Layer()
        self.face = Pig2_Face(self.layer)
        self.body = Pig2_Body(self.layer)
        self.arm = Pig2_Arm(self.layer)
        self.leg = Pig2_Leg(self.layer)
        self.layer.setDepth(51)
        
    def display(self, scene, x, y):
        self.layer.move(x,y)
        scene.group.add(self.layer)
    def clear(self, scene):
        scene.group.remove(self.layer)
    def teleport(self, x, y):
        self.layer.move(x,y)
    def jump(self):
        for j in range(10):
            self.layer.move(15,-25)
            self.leg.legL.move(-2,0)
            self.leg.legR.move(2,-0)
            time.sleep(0.01)
        for j in range(10):
            self.layer.move(15,25)
            self.leg.legR.move(-2,0)
            self.leg.legL.move(2,-0)
            time.sleep(0.01)
        time.sleep(0.5)    
    def move(self):
        for i in range(70):
            self.layer.move(-5, 0)
            for j in range(5):
                self.leg.legL.move(-2,0)
                self.leg.legR.move(2,-0)
            for j in range(5):
                self.leg.legR.move(-2,0)
                self.leg.legL.move(2,-0)
    def hurray(self):
        for i in range(3):
            self.layer.move(0, -21)
            for j in range(5):
                self.arm.armL.move(0,-2)
                self.arm.armR.move(0,2)
            for j in range(5):
                self.arm.armR.move(0,-2)
                self.arm.armL.move(0,2)
                time.sleep(0.01)
        for i in range(3):
            self.layer.move(0, 21)
            for j in range(5):
                self.arm.armL.move(0,-2)
                self.arm.armR.move(0,2)
            for j in range(5):
                self.arm.armR.move(0,-2)
                self.arm.armL.move(0,2)
                time.sleep(0.01)     

class Pig2_Face:
    def __init__(self,layer):
         self.face = Image("./img/pig2_face.png")
         self.face.move(0,0)
         layer.add(self.face)

class Pig2_Body:
    def __init__(self,layer):
         self.body=Image("./img/pig2_body.png")
         self.body.move(0,100)
         layer.add(self.body)

class Pig2_Arm:
    def __init__(self,layer):
         self.armL = Image("./img/pig2_Larm.png")
         self.armR = Image("./img/pig2_Rarm.png")
         self.armL.move(-30,100)
         self.armR.move(55,75)
         layer.add(self.armL)
         layer.add(self.armR)

class Pig2_Leg:
    def __init__(self,layer):
         self.legL = Image("./img/pig2_Lleg.png")
         self.legR = Image("./img/pig2_Rleg.png")
         self.legL.move(-10,150)
         self.legR.move(20,150)
         self.legL.setDepth(60)
         self.legR.setDepth(60)
         layer.add(self.legL)
         layer.add(self.legR)

class Pig3:
    def __init__(self):
        self.layer = Layer()
        self.body = Pig3_Body(self.layer)
        self.leg = Pig3_Leg(self.layer)
        self.layer.setDepth(51)
        
    def display(self, scene, x, y):
        self.layer.move(x,y)
        scene.group.add(self.layer)
    def clear(self, scene):
        scene.group.remove(self.layer)
    def teleport(self, x, y):
        self.layer.move(x,y)
    def jump(self):
        for i in range(3):
            for j in range(10):
                self.layer.move(15,-25)
                time.sleep(0.01)
            for j in range(10):
                self.layer.move(15,25)
                time.sleep(0.01)
            time.sleep(0.5)
    def move(self):
        for i in range(60):
            self.layer.move(-5, 0)
            for j in range(5):
                self.leg.legL.move(-2,0)
                self.leg.legR.move(2,-0)
            for j in range(5):
                self.leg.legR.move(-2,0)
                self.leg.legL.move(2,-0)
    def hurray(self):
        for i in range(3):
            self.layer.move(0, -21)
            for j in range(5):
                self.leg.legL.move(-2,0)
                self.leg.legR.move(2,-0)
            for j in range(5):
                self.leg.legR.move(-2,0)
                self.leg.legL.move(2,-0)
                time.sleep(0.01)
        for i in range(3):
            self.layer.move(0, 21)
            for j in range(5):
                self.leg.legL.move(-2,0)
                self.leg.legR.move(2,-0)
            for j in range(5):
                self.leg.legR.move(-2,0)
                self.leg.legL.move(2,-0)
                time.sleep(0.01)  
                
class Pig3_Body:
    def __init__(self,layer):
        self.body=Image("./img/pig3_body.png")
        self.body.move(0,45)
        layer.add(self.body)

class Pig3_Leg:
    def __init__(self,layer):
        self.legL = Image("./img/pig3_Lleg.png")
        self.legR = Image("./img/pig3_Rleg.png")
        self.legL.move(-25,138)
        self.legR.move(10,138)
        self.legL.setDepth(60)
        self.legR.setDepth(60)
        layer.add(self.legL)
        layer.add(self.legR)
        
# Slam Dunk parody 장면입니다. 늑대와 돼지가 손을 잡는 것을 표현한 것입니다.
class Next_page1(object):
    def __init__(self):
        self.page = Canvas(1600,900)
        self.page.setBackgroundColor("white")
        self.page.setTitle("Slam Dunk Parody")
        
    def display(self, n, x, y):
        self.image = Image("./img/slamdunk"+ str(n) +".png")
        image = self.image
        image.move(x,y)
        self.page.add(image)
        time.sleep(1)

# 돼지들이 프로그래밍 과제를 하는 장면입니다.
class Next_page2(object):
    def __init__(self):
        self.page = Canvas(1600,900)
        self.page.setBackgroundColor("white")
        self.page.setTitle("Programming assignment")
        self.back = Image("./img/programming.png")
        self.back.move(800,450)
        self.page.add(self.back)
        self.message = Text()
        self.message.setFontColor("black")
        self.message.setFontSize(50)
        self.message.moveTo(self.page.getWidth()/2, self.page.getHeight()- 60) 
        self.page.add(self.message)

    def display(self, n):
        self.image = Image("./img/python"+ str(n) +".png")
        image = self.image
        image.move(350+n*50,200+n*10)
        self.page.add(image)
        time.sleep(1)
        
    def print_msg(self,msg):
        self.message.setMessage(msg)
        
def animation(scene):
    house = House()
    wind = Wind()
    wolf = Wolf()
    pig1 = Pig1()
    pig2 = Pig2()
    pig3 = Pig3()
    
    scene.print_msg("프밍마을에 늑대와 아기돼지 삼형제가 살고 있었어요")
    time.sleep(2)
    scene.print_msg("늑대는 아주 짖궃게 장난을 치는 친구였어요.")
    time.sleep(2)
    scene.print_msg("최근에 아기 돼지 삼형제는 독립하여 직접 집을 지었어요.")
    time.sleep(2)
    scene.print_msg("앗, 저기 늑대가 오네요!")
    time.sleep(2)       
    scene.print_msg("")
    wolf.display(scene,-115,500)
    wolf.move()
    scene.print_msg("늑대 : 아 배고프고 심심하다~")
    time.sleep(2)
    scene.print_msg("늑대 : 맞다! 아기돼지 삼형제가 집을 지었다고 했지.")
    time.sleep(2)
    scene.print_msg("늑대 : 돼지나 잡아먹어볼까~?")
    time.sleep(2)
    scene.print_msg("")
    hay_house = house.display(scene, 1, 2000, 500)
    pig1.display(scene, 1855, 530)
    time.sleep(1)
    for i in range(60):
        scene.group.move(-16,0)
        scene.move_sun(i,1)
        scene.cloud.image1.move(-5,0)
        scene.cloud.image2.move(-3,0)
    time.sleep(1)
    wolf.teleport(550,0) 
    wolf.move()
    scene.print_msg("늑대 : 돼지야, 문 좀 열어봐ㅎ")
    time.sleep(2)
    scene.print_msg("돼지1 : 싫은데~")
    time.sleep(2)
    scene.print_msg("늑대 : 그렇다면 어쩔 수 없지!")
    time.sleep(1)
    scene.print_msg("늑대 : 후~")
    time.sleep(1)
    wolf.blow_wind()
    wind.display(scene, 430, 500)
    time.sleep(0.5)
    wind.blow()
    time.sleep(0.5)
    wind.teleport(0, 600)
    time.sleep(0.5)
    house.clear(scene)
    house.pull_down(scene, 2000, 600)
    time.sleep(0.5)
    scene.print_msg("늑대가 바람을 불자 건초더미 집은 와장창! 무너졌어요.")
    time.sleep(2)
    for i in range (3):
        pig1.jump()
        if i == 0:
            scene.print_msg("돼지1 : 꺄악~엄마야ㅠㅠ")
            time.sleep(1)
        if i == 1:
            scene.print_msg("늑대 : 그러게 좋은 말로 할 때 문을 열었어야지!")
            time.sleep(1)
        if i == 2:
            scene.print_msg("어디가~!")
            time.sleep(1)
            scene.print_msg("")  
    pig1.teleport(385,0)
    house.update_state(True)
    wooden_house = house.display(scene, 2, 3000, 500)
    pig2.display(scene ,2855, 530)
    for i in range(60):
        scene.group.move(-16,0)
        scene.move_sun(i,2)
        scene.cloud.image1.move(2,0)
        scene.cloud.image2.move(3,0)
    wolf.teleport(550,0)
    wolf.move()
    scene.print_msg("첫째돼지는 둘째돼지 집으로 들어갔어요.")
    time.sleep(2)
    scene.print_msg("늑대 : 돼지야~도망가면 어떡해. 문열어~또 무너뜨린다~")
    time.sleep(2)
    scene.print_msg("돼지2 : 하! 웃기셔, 그냥 가라")
    time.sleep(2)
    scene.print_msg("늑대 : 그렇단 말이지.")
    time.sleep(2)
    scene.print_msg("늑대 : 후~")
    time.sleep(2)
    wolf.blow_wind()
    wind.teleport(-290, -600)
    wind.blow()
    wind.teleport(0,600)
    house.clear(scene)
    house.pull_down(scene, 3000, 600, False)
    scene.print_msg("이번에도 늑대가 바람을 불자 나무집은 우당탕! 무너졌어요.")
    time.sleep(2)
    scene.print_msg("늑대 : 내가 못 무너뜨릴 줄 알고!")
    for i in range(3):
        pig2.jump()
        pig1.jump()
        if i == 0:
            scene.print_msg("돼지1,2 : 으앗!!! 돼지살려!!")
            time.sleep(1)
        elif i == 1:
            scene.print_msg("늑대 : 너희는 뛰어봤자 벼룩이야~")
            time.sleep(1)
    scene.print_msg("")
    pig2.teleport(100,0)
    house.update_state(True)
    brick_house = house.display(scene, 3, 4000, 500)
    pig3.display(scene ,4160, 560)
    for i in range(60):
        scene.group.move(-16,0)
        scene.move_sun(i,3)
        scene.cloud.image3.move(-10,0)
        scene.stars.image.move(-13,0)
    wolf.teleport(580, 0)
    wolf.move()
    scene.print_msg("첫째돼지와 둘째돼지는 세심한 막내돼지 집으로 들어갔어요.")
    time.sleep(2)
    scene.print_msg("늑대 : 얘들아 한참 찾았잖아~어서나와! 배고프단 말이야T.T")
    time.sleep(2)
    scene.print_msg("돼지3 : 이번엔 정말이다!")
    time.sleep(2)
    scene.print_msg("이건 벽돌로 지은 튼튼한 집이라구! 한번 해보시지!")
    time.sleep(2)
    scene.print_msg("돼지1,2 : 벽돌집이라구!!")
    time.sleep(2)
    scene.print_msg("늑대 : 그렇단 말이지. 이 늑대를 뭘로 보고!")
    time.sleep(2)
    scene.print_msg("바이, 후~")
    time.sleep(2)
    for i in range(3):
         wolf.blow_wind()
         wind.teleport(-290,-600)
         wind.blow()
         wind.teleport(0,600)
         if i == 0:
             scene.print_msg("? 후~")
             time.sleep(2)
         elif i == 1:
             scene.print_msg("?? 후~~")
    time.sleep(1)
    wolf.worn_out()
    scene.print_msg("왜 안되지?! 늑대의 수치다..! ㅠㅠ")
    time.sleep(2)
    wolf.teleport(0,600)       
    for i in range(4):
        wolf.fall_down(scene, i)
        wolf.clear(scene)
    wolf.fall_down(scene, 4)
    scene.print_msg("꽈당!!")
    time.sleep(1)
    scene.print_msg("늑대는 꼬리뼈가 부러져 혼자 일어날 수가 없었어요.")
    time.sleep(2)
    scene.print_msg("")
    if scene.ask_response("애들아ㅜㅜ 내 손 좀 잡아줄래?ㅜㅜ (y/n)"):
        scene.print_msg("돼지1 : 너 우리 잡아먹을꺼야?")
        time.sleep(2)
        scene.print_msg("늑대 : 아니야ㅠㅠ 살려줘ㅠㅠ")
        time.sleep(2)
        scene.print_msg("늑대 : 살려주면 프밍과제 도와줄게ㅠㅠ")
        time.sleep(2)
        scene.print_msg("돼지1,2,3 : 오 아직 과제 다 못했는데..!")
        time.sleep(2)
        scene.print_msg("")
        house.clear(scene)
        house.open_door(scene, 4000, 500)
        pig1.teleport(0,20)
        pig2.teleport(130,40)
        pig3.teleport(-130,40)
        pig1.move()
        pig2.move()
        pig3.move()
        wolf.clear(scene)
        parody()
        wolf.teleport(0,-600)
        scene.print_msg("와아~~~~~")
        for i in range (4):
            pig1.hurray()
            pig2.hurray()
            pig3.hurray()
            wolf.hurray()
            if i == 0:
                scene.print_msg("우리는 모두 즐거운 프밍1 친구~")
            elif i == 1:
                scene.print_msg("여러분~한 학기 동안 수고 많으셨습니다!")
            elif i == 2:
                 scene.print_msg("행복한 방학되세요♥")
    else:
        page = Next_page2()    
        time.sleep(2)
        page.print_msg("돼지2 : 뭐라는거니?")
        time.sleep(2)
        page.print_msg("돼지1 : 우리 프밍 과제나 하자. 이번에 빡세대..")
        time.sleep(2)
        for i in range (14):
            page.display(i+1)
            if i == 2:
                page.print_msg("")
            elif i == 5:
                page.print_msg("프밍마을은 언제나 과제중이랍니다~")
            elif i == 7:
                page.print_msg("이번학기 모두들 수고많으셨어요~")
            elif i ==9:
                page.print_msg("종강까지 파이팅!!") 
            elif i == 11:
                page.print_msg("행복한 방학되세요♥")
        time.sleep(2)
        
                

def parody():
    page = Next_page1()
    time.sleep(2)
    page.display(1,1400, 300)
    page.display(2,1000, 300)
    page.display(3,1200, 750)
    page.display(4, 350, 320)
    page.display(5, 350, 700)
    page.display(6, 800, 450)
    time.sleep(2)
    page.page.close()
    
def main():
    scene = Scene()
    animation(scene)
    
main()

# 발표시에 Next_page2를 보여주기 위한 용입니다.
'''
scene = Scene()
page = Next_page2()    
time.sleep(1)
page.print_msg("돼지2 : 뭐라는거니?")
time.sleep(2)
page.print_msg("돼지1 : 우리 프밍 과제나 하자. 이번에 빡세대..")
time.sleep(2)
for i in range (14):
    page.display(i+1)
    if i == 5:
        page.print_msg("프밍마을은 언제나 과제중이랍니다~")
    elif i == 7:
        page.print_msg("이번학기 모두들 수고많으셨어요~")
    elif i ==9:
        page.print_msg("종강까지 파이팅!!") 
    elif i == 11:
        page.print_msg("행복한 방학되세요♥")
time.sleep(2)
'''
