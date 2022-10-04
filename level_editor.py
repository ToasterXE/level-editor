import pygame, os

window = pygame.display.set_mode((1200, 700))
alien1Img = pygame.transform.scale(pygame.image.load((os.path.join("dateien","alien1.png"))),(32,32))
alien2Img_unten = pygame.transform.scale(pygame.image.load((os.path.join("dateien","alien2_unten.png"))),(32,32))
alien3Img = pygame.transform.scale(pygame.image.load((os.path.join("dateien","alien3.png"))),(29,29))
feldtyp_hoverImg = pygame.image.load((os.path.join("dateien", "feldtyp_hover.png")))
feldtyp_ausgImg = pygame.image.load((os.path.join("dateien", "feldtyp_ausgewählt.png")))
ausgewähltImg = pygame.image.load((os.path.join("dateien", "feld_ausgewählt.png")))
leerImg = pygame.image.load((os.path.join("dateien", "leer.png")))
nichtsImg = pygame.image.load(os.path.join("dateien","nichts.png"))
borderImg = pygame.transform.scale(pygame.image.load(os.path.join("dateien", "border.png")),(32,32))
sprengbaresImg = pygame.image.load(os.path.join("dateien", "sprengbares.png"))
leerImg = pygame.image.load(os.path.join("dateien", "leer.png"))
wegraeumbaresImg = pygame.image.load(os.path.join("dateien", "wegräumbares.png"))
spawnfeld = pygame.image.load(os.path.join("dateien", "spawn.png"))
feld_leer = pygame.image.load(os.path.join("dateien", "feld_leer.png"))
slowness_potionImg = pygame.image.load(os.path.join("dateien", "slowness_potion.png"))
speed_potionImg = pygame.image.load(os.path.join("dateien","speed_potion.png"))
bombe_objektImg = pygame.image.load(os.path.join("dateien","bombe_objekt.png"))
hp_boostImg = pygame.image.load(os.path.join("dateien", "hp_boost.png"))


pygame.display.set_caption("Level Editor")
pygame.font.init()
font = pygame.font.SysFont("candara", 40)

Level = []
bListe = []
eListe = []
print("Breite angeben:")
breite = int(input())
print("Höhe angeben:")
hoehe = int(input())
#breite = 50
#hoehe = 50
b = 0
h = 0
while b < breite:
    bListe.append(0)
    b += 1
while h < hoehe:
    tempListe = bListe.copy()   #ansonsten beziehen sich alle Listen in der Breite auf bListe und sind daher identisch
    Level.append(tempListe)
    h += 1
sprites = pygame.sprite.Group()
feldtypensprites = pygame.sprite.Group()
feldListe = []
b = 0
h = 0
while b < breite:
    eListe.append(0)
    b += 1
while h < hoehe:
    tempListe = eListe.copy()   #ansonsten beziehen sich alle Listen in der Breite auf bListe und sind daher identisch
    feldListe.append(tempListe)
    h += 1
bild = feld_leer


class feld(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(sprites)
        self.image = feld_leer
        self.rect = self.image.get_rect(top = y, left = x) 
        feldListe[int(y/32)][int(x/32)] = self
        self.selected = False


for spalte_index, spalte in enumerate(Level):
    for zeile_index, spalte in enumerate(spalte):
        x = zeile_index * 32
        y = spalte_index * 32
        feld(x,y)
bild = feld_leer

def update_Liste():
    global bild
    for spalte_index, zeile in enumerate(Level):
        for zeile_index, spalte in enumerate(zeile):
            x = zeile_index
            y = spalte_index 
            
            if spalte == 1:
                bild = borderImg

            elif spalte == 5:
                bild = spawnfeld
                
            elif spalte == 2:
                bild = sprengbaresImg

            elif spalte == 3:
                bild = wegraeumbaresImg

            elif spalte == 77:
                bild = ausgewähltImg
            
            elif spalte == 10:
                bild = alien1Img
            
            elif spalte == 11:
                bild = alien2Img_unten

            elif spalte == 12:
                bild = alien3Img

            elif spalte == 50:
                bild = bombe_objektImg

            elif spalte == 51:
                bild = slowness_potionImg

            elif spalte == 52:
                bild = speed_potionImg

            elif spalte == 53:
                bild = hp_boostImg

            else:
                bild = feld_leer

            feldListe[y][x].image = bild

mode = "select"
maus_alt = (0,0)
def update_Maus():
    global position, maus_alt
    mausPos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] == 1:
        if mausPos[0] < 950:
            mausPos += camAbstand
            feld = pygame.math.Vector2(mausPos[0] // 32, mausPos[1] // 32)
            if feld.y < len(Level) and feld.x < len(Level[0]):
                feld_current = feldListe[int(feld.y)][int(feld.x)]
                if mode == "unselect":
                    feld_current.image = feld_leer
                    Level[int(feld.y)][int(feld.x)] = 0
                    feld_current.selected = False
                elif mode == "select":
                    feld_current.selected = True
                    feld_current.image = ausgewähltImg
                    Level[int(feld.y)][int(feld.x)] = 77

    if pygame.mouse.get_pressed()[2] == 1:
        if mausPos == maus_alt:
            pass
        else:
            position.x += maus_alt[0] - mausPos[0]
            position.y += maus_alt[0] - mausPos[0]
    maus_alt = mausPos

def switch_mode():
    global mode
    if mode == "select":
        mode = "unselect"
    else:
        mode = "select"

def replace_selected(typ):
    h = 0
    while h < len(feldListe):
        b = 0
        while b < len(feldListe[0]):
            if feldListe[h][b].selected:
                feldListe[h][b].selected = False
                Level[h][b] = typ
            b += 1 
        h += 1

def update_replacebutton():
    mausPos = pygame.mouse.get_pos()
    rect_color = (30,30,30)
    schrift = font.render("Replace", True, (183, 0, 255))
    schrift_rect = schrift.get_rect(topleft = (1000, 30))
    if schrift_rect.collidepoint(mausPos):
        rect_color = (40,40,40)
        if pygame.mouse.get_pressed()[0] == 1:
            rect_color = (60,60,60)
            replace_selected(feldtyp_selected)

    pygame.draw.rect(window, rect_color, schrift_rect)
    window.blit(schrift,schrift_rect)

class feldtypen(pygame.sprite.Sprite):
    def __init__(self,pos,groups,typ,image):
        super().__init__(groups)
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.typ = typ

sprengbarestyp = feldtypen((1000, 150), feldtypensprites, 2, sprengbaresImg)
grenzfeldertyp = feldtypen((1100, 150), feldtypensprites, 1, borderImg)
leerfeldtyp = feldtypen((1000, 250), feldtypensprites, 0, feld_leer)
wegraeumbarestyp = feldtypen((1100, 250), feldtypensprites, 3, wegraeumbaresImg)
alien1typ = feldtypen((1000, 350), feldtypensprites, 10, alien1Img)
alien2typ = feldtypen((1100, 350), feldtypensprites, 11, alien2Img_unten)
alien3typ = feldtypen((1000, 450), feldtypensprites, 12, alien3Img)
spawnfeldtyp = feldtypen((1100, 450), feldtypensprites, 5, spawnfeld)
speedpottyp = feldtypen((1000, 550), feldtypensprites, 52, speed_potionImg)
slownesspottyp = feldtypen((1100, 550), feldtypensprites, 51, slowness_potionImg)
hpboosttyp = feldtypen((1000, 650), feldtypensprites, 53, hp_boostImg)
bomeobjekttyp = feldtypen((1100, 650), feldtypensprites, 50, bombe_objektImg)
feldtyp_selected = 0

def update_feldtypen():
    global feldtyp_selected
    mausPos = pygame.mouse.get_pos()
    for feldtyp in feldtypensprites:
        if feldtyp.rect.collidepoint(mausPos):
            window.blit(feldtyp_hoverImg, (feldtyp.rect.left - 5, feldtyp.rect.top - 5))
            if pygame.mouse.get_pressed()[0] == 1:
                feldtyp_selected = feldtyp.typ
        if feldtyp.typ == feldtyp_selected:
                window.blit(feldtyp_ausgImg, (feldtyp.rect.left - 5, feldtyp.rect.top - 5))   
    feldtypensprites.draw(window)
Levelbreite = 950
Levelhoehe = 700
position = pygame.math.Vector2(300,300)
camAbstand = pygame.math.Vector2()

def update_position():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        position.x += 6
    if keys[pygame.K_a]:
        position.x -= 6
    if keys[pygame.K_w]:
        position.y -= 6
    if keys[pygame.K_s]:
        position.y += 6

    if position.x > len(Level[0]) * 32:
        position.x = len(Level[0]) * 32
    if position.y > len(Level) * 32:
        position.y = len(Level) * 32

def level_draw():
    maphoehe = len(Level) * 32
    mapbreite = len(Level[0]) * 32
    if mapbreite <= Levelbreite: #kamerabewegung x
        camAbstand.x = 0
    else:
        camAbstand.x = (position.x - Levelbreite/2) 
            
        if position.x <= Levelbreite/2:
            camAbstand.x = 0
        
        if position.x >= mapbreite - Levelbreite/2:
            camAbstand.x = mapbreite - Levelbreite    
    
    if maphoehe <= Levelhoehe:   #kamerabewegung y
        camAbstand.y = 0
    else:
        camAbstand.y = (position.y - Levelhoehe/2) 
        
        if position.y <= Levelhoehe/2:     
            camAbstand.y = 0
            
        if position.y >= maphoehe - Levelhoehe/2:
            camAbstand.y = maphoehe - Levelhoehe
            
    for sprite in sprites:
        window.blit(sprite.image, (sprite.rect.topleft - camAbstand))

def expand_hoehe(): #kaputt
    tempListe = bListe.copy()
    Level.append(tempListe)
    temp2Liste = bListe.copy()
    feldListe.append(temp2Liste)
    for spalte_index, spalte in enumerate(Level):
        for zeile_index, spalte in enumerate(spalte):
            if spalte == 0:
                x = zeile_index * 32
                y = spalte_index * 32
                feld(x,y)

def expand_breite():    #kaputt
    i = 0
    while i < len(Level):
        Level[i].append(0)
        feldListe[i].append(0)
        i += 1        
    for spalte_index, spalte in enumerate(Level):
        for zeile_index, spalte in enumerate(spalte):
            if spalte == 0:
                x = zeile_index * 32
                y = spalte_index * 32
                feld(x,y)

def main():
    run = True
    while run:
        #print(position)
        #print(camAbstand)
        #print(Level)
        #print(feldListe)
        window.fill((20,20,20))
        update_Liste()
        update_Maus()
        update_position()
        level_draw()
        pygame.draw.rect(window,(24,24,24),pygame.rect.Rect(950,0,250,900))
        #pygame.draw.rect(window,(24,24,24),pygame.rect.Rect(0,700,1200,200))
        update_feldtypen()
        update_replacebutton()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    switch_mode()


                if event.key == pygame.K_4:
                    print(Level)
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
main()