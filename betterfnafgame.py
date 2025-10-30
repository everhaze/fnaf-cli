import random
import threading
import time

class clifnaf():
    def __init__(self):
        self.night = 1
        self.locations()
        self.setdefaults()
        self.mainmenu()

    def setdefaults(self): #default settings
        self.q = False
        self.e = False
        self.a = False
        self.d = False
        self.w = False
        self.backgroundtime = 0
        self.playertime = 0
        self.gameon = False
        self.ActivateFoxy = False
        self.foxycounter = 0
        self.powerperc = 100

    def AI_level(self): #doors/lights/cams scale with nights
        AI_list = ([1, 1, 0, 0],
                   [3, 3, 1, 2],
                   [5, 5, 3, 5],
                   [8, 8, 5, 7],
                   [10, 10, 10, 10],
                   [15, 15, 15, 15]) #Bonnie, Chica, Freddy, Foxy
        self.Freddylevel = AI_list[self.night - 1][2]
        self.Bonnielevel = AI_list[self.night - 1][0]
        self.Chicalevel = AI_list[self.night - 1][1]
        self.Foxylevel = AI_list[self.night - 1][3]
        print(f"Difficulty: Freddy {self.Freddylevel}, Bonnie {self.Bonnielevel}, Chica {self.Chicalevel}, Foxy {self.Foxylevel}")

    def locations(self):
        self.cam_1a = ["Freddy", "Bonnie", "Chica"]
        self.cam_1b = []
        self.cam_1c = ["Foxy"]
        self.cam_2a = []
        self.cam_2b = []
        self.cam_3 = []
        self.cam_4a = []
        self.cam_4b = []
        self.cam_5 = []
        self.cam_6 = []
        self.cam_7 = []
        self.leftplayerofficedoor = []
        self.rightplayerofficedoor = []
    
    def mainmenu(self):
        while True:
            print("""         
Five Nights at Python 1
    Main Menu
1. Play      
2. Exit
              
                """)
            userinput = input(">>")
            match userinput:
                case "1":
                    self.game()
                    break
                case "2":
                    exit(0)
                case _:
                    continue

    def game(self):
        print("Select your night. 1-6")
        nightinput = input(">")
        match nightinput:
            case "1": self.night = 1
            case "2": self.night = 2
            case "3": self.night = 3
            case "4": self.night = 4
            case "5": self.night = 5
            case "6": self.night = 6
            case _:
                print("Invalid input, selecting 1 by default...")
                self.night = 1
        self.AI_level()
        time.sleep(2)
        self.gameon = True
        self.tickmanager()
        self.animatronicthreads()
        while self.gameon:
            print("""
    -- -- Office -- --
q/e = left/right door
a/d = left/right light
w = cameras
t = check time
b = check power
                  
                """)
            userinput = input(">")
            match userinput:
                case "q":
                    if not self.q:
                        print("Closed left door")
                        self.q = True
                    elif self.q:
                        print("Opened left door")
                        self.q = False
                case "e":
                    if not self.e:
                        print("Closed right door")
                        self.e = True
                    elif self.e:
                        print("Opened right door")
                        self.e = False
                case "a":
                    if not self.a:
                        print("Flashing left")
                        print(f"Left door: {self.leftplayerofficedoor}")
                        self.a = True
                    elif self.a:
                        print("No longer flashing left")
                        self.a = False
                case "d":
                    if not self.d:
                        print("Flashing right")
                        print(f"Right door: {self.rightplayerofficedoor}")
                        self.d = True
                    elif self.d:
                        print("No longer flashing right")
                        self.d = False
                case "t":
                    print(f"{self.playertime}am")
                case "b":
                    print(f"Power: {round(self.powerperc, 2)}%")
                case "w":
                    self.w = True
                    while self.w and self.gameon:
                        if self.powerperc <= 0:
                            break
                        print("""
                            
    - Available Cameras -
1a, 1b, 1c | 2a, 2b | 4a, 4b
        3, 5, 6, 7
-- Type in anything else to return. --
                              
                              """)
                        camerainput = input(">")
                        match camerainput:
                            case "1a": print(f"Stage: {self.cam_1a}")
                            case "1b": print(f"Diner Area: {self.cam_1b}")
                            case "1c": print(f"Pirates Cove: {self.cam_1c}")
                            case "2a": print(f"Left Hall: {self.cam_2a}")
                            case "2b": print(f"Left Hall Corner: {self.cam_2b}")
                            case "3": print(f"Supply Closet: {self.cam_3}")
                            case "4a": print(f"Right Hall: {self.cam_4a}")
                            case "4b": print(f"Right Hall Corner: {self.cam_4b}")
                            case "5": print(f"Parts & Service: {self.cam_5}")
                            case "6": print(f"Kitchen: - CAMERA DISABLED -  {self.cam_6}")
                            case "7": print(f"Restrooms: {self.cam_7}")
                            case _:
                                self.w = False
                                break

    def powerdrainer(self):
        while self.gameon:
            drain = 0
            if self.q: drain += 0.005 * self.night
            if self.e: drain += 0.005 * self.night
            if self.a: drain += 0.0025 * self.night
            if self.d: drain += 0.0025 * self.night
            if self.w: drain += 0.0025 * self.night
            self.powerperc -= drain
            if self.powerperc <= 0:
                self.q = False
                self.e = False
                self.a = False
                self.d = False
            time.sleep(0.1)

    def Freddyshome(self):
        self.Freddy = "Freddy"
        while self.gameon:
            chance2move = random.randint(1, 20)
            if chance2move <= self.Freddylevel:
                if self.Freddy in self.cam_1a:
                    self.cam_1a.remove(self.Freddy)
                    self.cam_4a.append(self.Freddy)
                elif self.Freddy in self.cam_4a:
                    self.cam_4a.remove(self.Freddy)
                    self.cam_4b.append(self.Freddy)
                elif self.Freddy in self.cam_4b:
                    self.cam_4b.remove(self.Freddy)
                    self.rightplayerofficedoor.append(self.Freddy)
                    print("You hear something at the right door...")
                elif self.Freddy in self.rightplayerofficedoor:
                    self.rightplayerofficedoor.remove(self.Freddy)
                    if self.e:
                        self.cam_1a.append(self.Freddy)
                    elif not self.e:
                        self.death(self.Freddy)
                        break
            time.sleep(5)

    def Bonnieshome(self):
        self.Bonnie = "Bonnie"
        while self.gameon:
            chance2move = random.randint(1, 20)
            pathchance = random.randint(1, 4)
            if chance2move <= self.Bonnielevel:
                if self.Bonnie in self.cam_1a:
                    self.cam_1a.remove(self.Bonnie)
                    self.cam_1b.append(self.Bonnie)
                elif self.Bonnie in self.cam_1b:
                    self.cam_1b.remove(self.Bonnie)
                    if pathchance <= 3:
                        self.cam_2a.append(self.Bonnie)
                    elif pathchance == 4:
                        self.cam_5.append(self.Bonnie)
                elif self.Bonnie in self.cam_5:
                    self.cam_5.remove(self.Bonnie)
                    self.cam_1b.append(self.Bonnie)
                elif self.Bonnie in self.cam_2a:
                    self.cam_2a.remove(self.Bonnie)
                    if pathchance == 1:
                        self.cam_2b.append(self.Bonnie)
                    elif pathchance == 2:
                        self.cam_3.append(self.Bonnie)
                elif self.Bonnie in self.cam_3:
                    self.cam_3.remove(self.Bonnie)
                    self.cam_2b.append(self.Bonnie)
                elif self.Bonnie in self.cam_2b:
                    self.cam_2b.remove(self.Bonnie)
                    self.leftplayerofficedoor.append(self.Bonnie)
                    print("You hear something at the left door...")
                elif self.Bonnie in self.leftplayerofficedoor:
                    self.leftplayerofficedoor.remove(self.Bonnie)
                    if self.q:
                        self.cam_1a.append(self.Bonnie)
                    elif not self.q:
                        self.death(self.Bonnie)
                        break
            time.sleep(5)

    def Chicashome(self):
        self.Chica = "Chica"
        while self.gameon:
            chance2move = random.randint(1, 20)
            pathchance = random.randint(1, 4)
            if chance2move <= self.Chicalevel:
                if self.Chica in self.cam_1a:
                    self.cam_1a.remove(self.Chica)
                    self.cam_1b.append(self.Chica)
                elif self.Chica in self.cam_1b:
                    self.cam_1b.remove(self.Chica)
                    if pathchance <= 3:
                        self.cam_6.append(self.Chica)
                    elif pathchance == 4:
                        self.cam_7.append(self.Chica)
                elif self.Chica in self.cam_7:
                    self.cam_7.remove(self.Chica)
                    self.cam_1b.append(self.Chica)
                elif self.Chica in self.cam_6:
                    self.cam_6.remove(self.Chica)
                    self.cam_4a.append(self.Chica)
                elif self.Chica in self.cam_4a:
                    self.cam_4a.remove(self.Chica)
                    self.cam_4b.append(self.Chica)
                elif self.Chica in self.cam_4b:
                    self.cam_4b.remove(self.Chica)
                    self.rightplayerofficedoor.append(self.Chica)
                    print("You hear something at the right door...")
                elif self.Chica in self.rightplayerofficedoor:
                    self.rightplayerofficedoor.remove(self.Chica)
                    if self.e:
                        self.cam_1a.append(self.Chica)
                    elif not self.e:
                        self.death(self.Chica)
                        break
            time.sleep(5)

    def Foxyshome(self):
        self.Foxy = "Foxy"
        self.foxycounter += self.Foxylevel
        while self.gameon:
            if self.foxycounter >= 45 and self.Foxylevel != 0:
                self.ActivateFoxy = True
                self.foxycounter = 0
            else:
                self.foxycounter += self.Foxylevel
            if self.ActivateFoxy:
                if self.Foxy in self.cam_1c:
                    self.cam_1c.remove(self.Foxy)
                    print("You hear loud footsteps from the left hall...")
                    time.sleep(5)
                    self.cam_2a.append(self.Foxy)
                if self.Foxy in self.cam_2a:
                    self.cam_2a.remove(self.Foxy)
                if self.q:
                    print("You hear scratching outside the left door...")
                    self.powerperc -= self.Foxylevel / 2
                    self.ActivateFoxy = False
                    self.cam_1c.append(self.Foxy)
                elif not self.q:
                    self.death(self.Foxy)
                    self.ActivateFoxy = False
                    break
            time.sleep(5)

    def death(self, animatronic):
        self.gameon = False
        print(f"Game Over. Died to: {animatronic}")
        time.sleep(5)
        exit(0)

    def tick(self): #45s hours, 0.112 drain per second
        while self.gameon:
            self.backgroundtime += 1
            self.powerperc -= 0.112
            if self.backgroundtime == 45 or self.backgroundtime == 90 or self.backgroundtime == 135 or self.backgroundtime == 180 or self.backgroundtime == 225:
                self.playertime += 1
            if self.backgroundtime >= 270:
                print("Congratulations! It is now 6am.")
                self.setdefaults()
                time.sleep(3)
                break
            time.sleep(1)
    
    def tickmanager(self):
        self.tickthread = threading.Thread(target=self.tick, daemon=True)
        self.tickthread.start()
        self.drainingthread = threading.Thread(target=self.powerdrainer, daemon=True)
        self.drainingthread.start()

    def animatronicthreads(self):
        self.freddythread = threading.Thread(target=self.Freddyshome, daemon=True)
        self.freddythread.start()
        self.bonniethread = threading.Thread(target=self.Bonnieshome, daemon=True)
        self.bonniethread.start()
        self.chicathread = threading.Thread(target=self.Chicashome, daemon=True)
        self.chicathread.start()
        self.foxythread = threading.Thread(target=self.Foxyshome, daemon=True)
        self.foxythread.start()

run = clifnaf()