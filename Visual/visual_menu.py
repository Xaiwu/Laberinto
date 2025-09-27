from Visual import visual_controller as CONFIG #type:ignore
import pygame

class Menu:
    def __init__(self):
        self.buttons = []
        self.selectores = []
        pass

    def run(self,pantalla):
        self.__pantalla = pantalla
        self.__pantalla.fill(CONFIG.NEGRO)

        for b in self.buttons:
            b.draw(pantalla)
        for s in self.selectores:
            s.draw(pantalla)

    def create_button(self,x,y,w,h,func):
        b = button(x,y,w,h,func)
        self.buttons.append(b)
        return b

    def create_selector(self,x,y,w,enum):
        s = selector(x,y,w,enum)
        self.selectores.append(s)
        return s

    def event(self, event):
        for b in self.buttons:
            b.event(event)
        for s in self.selectores:
            s.button_left.event(event)
            s.button_right.event(event)

class button:
    def __init__(self,x_pos,y_pos,w_size,h_size,func):
        self.pos = (x_pos-w_size/2,y_pos-h_size/2)
        self.size = (w_size,h_size)
        self.button_rect = pygame.Rect(self.pos,self.size)
        self.func = func
        self.title = ""
        pass

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.func()

    def draw(self,pantalla):
        pygame.draw.rect(pantalla,CONFIG.BLANCO, self.button_rect)
        if self.title != "":
            fuente = pygame.font.SysFont(None, 40)
            texto = fuente.render(self.title, True, (0, 0, 0))
            rect_texto = texto.get_rect(center=self.button_rect.center)
            pantalla.blit(texto, rect_texto)

    def set_title(self,title:str): 
        self.title = title

class selector:
    def __init__(self,x,y,size,values:list[str]):
        self.x = x
        self.y = y
        self.offset = 120
        self.size = size
        self.__val = 0
        self.values = values
        self.pantalla = None
        self.actual_value = values[self.__val]
        self.button_left = button(x-self.offset,y,size,size, self.left)
        self.button_right = button(x+self.offset,y,size,size, self.right)
        self.button_left.set_title("<")
        self.button_right.set_title(">")


    def draw(self,pantalla):
        self.button_left.draw(pantalla)
        self.button_right.draw(pantalla)
        self.pantalla = pantalla
        self.update_value()

    def update_value(self):
        fuente = pygame.font.SysFont(None, 40)
        self.actual_value = self.values[self.__val]
        texto = fuente.render(self.actual_value, True, CONFIG.BLANCO)
        rect_texto = texto.get_rect(center=(self.x,self.y))
        if self.pantalla != None:
            self.pantalla.blit(texto, rect_texto)

    def left(self):
        if self.__val > 0:
            self.__val -= 1
        self.update_value()

    def right(self):
        if self.__val < self.values.__len__() - 1:
            self.__val += 1
        self.update_value()
