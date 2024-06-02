import pygame
import sys

# Pygame başlatılır
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 1000 # Ekran genişliği
SCREEN_HEIGHT = 800 # Ekran yüksekliği
CELL_SIZE = 40 # Hücre boyutu

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Ekran oluşturulur
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Pencere boyutunu belirler
pygame.display.set_caption("Logic Gate Simulation") # Pencere başlığını ayarlar


def load_and_scale_image(filename, scale):
    image = pygame.image.load(filename)  # Belirtilen dosya adındaki görüntüyü yükler
    return pygame.transform.scale(image, (scale * 2, scale * 2)) # Görüntüyü boyutlarına ölçeklendirir ve döndürür

# Mantıksal kapı görsellerini yükler ve ölçekler
and_image = load_and_scale_image('and_gate.png', CELL_SIZE)
or_image = load_and_scale_image('or_gate.png', CELL_SIZE)
not_image = load_and_scale_image('not_gate.png', CELL_SIZE)
nor_image = load_and_scale_image('nor_gate.png', CELL_SIZE)
nand_image = load_and_scale_image('nand_gate.png', CELL_SIZE)
xor_image = load_and_scale_image('xor_gate.png', CELL_SIZE)
xnor_image = load_and_scale_image('xnor_gate.png', CELL_SIZE)
buffer_image = load_and_scale_image('buffer_gate.png', CELL_SIZE)

# Anahtar ve LED görsellerini yükler ve ölçekler
switch0_image = load_and_scale_image('switch0.png', CELL_SIZE)
switch1_image = load_and_scale_image('switch1.png', CELL_SIZE)
led0_image = load_and_scale_image('led0.png', CELL_SIZE)
led1_image = load_and_scale_image('led1.png', CELL_SIZE)
truth_table_image = pygame.transform.scale(pygame.image.load('truth_table.png'), (500, 400)) # Doğruluk tablosu görselini yükler ve ölçekler

# Kareli arka planı çizmek için fonksiyon
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

# Mantıksal kapıların temel sınıfı
class LogicGate:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image # Kapının görseli
        self.rect = pygame.Rect(x, y, CELL_SIZE * 2, CELL_SIZE * 2) # Kapının ekran üzerindeki alanı
        self.inputs = [(self.x, self.y + CELL_SIZE // 2), (self.x, self.y + CELL_SIZE * 3 // 2)] # Kapının giriş noktaları
        self.output = (self.x + CELL_SIZE * 2, self.y + CELL_SIZE) # Kapının çıkış noktası

    def draw(self, screen):
        screen.blit(self.image, self.rect) # Kapının görselini ekrana çizer
        for point in self.inputs:
            pygame.draw.circle(screen, RED, point, 5) # Giriş noktalarını kırmızı daire olarak çizer
        pygame.draw.circle(screen, RED, self.output, 5) # Çıkış noktalarını kırmızı daire olarak çizer

    def process(self, input_values): # Giriş değerlerini işleyen fonksiyon
        pass

    def update(self): # Güncelleme fonksiyonu
        pass

# AND Kapısı sınıfı
class AndGate(LogicGate):
    def __init__(self, x, y):
        super().__init__(x, y, and_image)

    def process(self, input_values):
        return all(input_values)

# OR Kapısı sınıfı
class OrGate(LogicGate):
    def __init__(self, x, y):
        super().__init__(x, y, or_image)

    def process(self, input_values):
        return any(input_values) # Herhangi bir giriş doğruysa  çıkış doğru

# NOT Kapısı sınıfı
class NotGate(LogicGate):
    def __init__(self, x, y):
        super().__init__(x, y, not_image)
        self.inputs = [(self.x, self.y + CELL_SIZE)] # NOT kapısının tek giriş noktası var

    def draw(self, screen):
        screen.blit(self.image, self.rect) # Kapının görselini ekrana çizer
        pygame.draw.circle(screen, RED, self.inputs[0], 5) # Giriş noktasını kırmızı daire olarak çizer
        pygame.draw.circle(screen, RED, self.output, 5) # Çıkış noktasını kırmızı daire olarak çizer

    def process(self, input_values):
        return not input_values[0] # Girişin tersini  döndür

    def update(self):
        pass

# NOR Kapısı sınıfı
class NorGate(LogicGate):
    def __init__(self, x, y):
        super().__init__(x, y, nor_image)

    def process(self, input_values):
        return not any(input_values) # Herhangi bir giriş doğruysa çıkış yanlış

# NAND Kapısı sınıfı
class NandGate(LogicGate):
    def __init__(self, x, y):
        super().__init__(x, y, nand_image)

    def process(self, input_values):
        return not all(input_values) # Tüm girişler doğruysa çıkış yanlış

# XOR Kapısı sınıfı
class XorGate(LogicGate):
    def __init__(self, x, y):
        super().__init__(x, y, xor_image)

    def process(self, input_values):
        return input_values[0] != input_values[1] # Girişler birbirinden farklıysa doğru

# XNOR Kapısı sınıfı
class XnorGate(LogicGate):
    def __init__(self, x, y):
        super().__init__(x, y, xnor_image)

    def process(self, input_values):
        return input_values[0] == input_values[1] # Girişler birbirine eşitse doğru

# Buffer Kapısı sınıfı
class BufferGate(LogicGate):
    def __init__(self, x, y):
        super().__init__(x, y, buffer_image)
        self.inputs = [(self.x, self.y + CELL_SIZE)]  # Buffer kapısının tek giriş noktası var

    def process(self, input_values):
        return input_values[0]  # Giriş sinyalini doğrudan çıkışa aktarır

    def update(self):
        pass

# Anahtar sınıfı
class Switch:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = False # Anahtarın başlangıç durumu,başta kapalı
        self.rect = pygame.Rect(x, y, CELL_SIZE * 2, CELL_SIZE * 2) # Anahtarın ekran üzerindeki alanı

    def toggle(self):
        self.state = not self.state # Anahtarın durumunu değiştirilir,aç/kapat

    def draw(self, screen):
        image = switch1_image if self.state else switch0_image # Anahtarın durumuna göre görseli seçilir
        screen.blit(image, self.rect) # Anahtarın görselini ekrana çizilir
        output = (self.x + CELL_SIZE * 2, self.y + CELL_SIZE) # Anahtarın çıkış noktası
        pygame.draw.circle(screen, RED, output, 5) # Çıkış noktası kırmızı daire olarak çizilir

# LED sınıfı
class Led:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = False # LED'in başlangıç durumu,başta kapalı
        self.rect = pygame.Rect(x, y, CELL_SIZE * 2, CELL_SIZE * 2) # LED'in ekran üzerindeki alanı

    def set_state(self, state):
        self.state = state  # LED'in durumunu belirler

    def draw(self, screen):
        image = led1_image if self.state else led0_image # LED'in durumuna göre görseli seçilir
        screen.blit(image, self.rect) # LED'in görselini ekrana çizilir
        input_pos = (self.x, self.y + CELL_SIZE) # LED'in giriş noktası
        pygame.draw.circle(screen, RED, input_pos, 5) # Giriş noktasını kırmızı daire olarak çizilir

# Kablo sınıfı
class Wire:
    def __init__(self, start_pos):
        self.start_pos = start_pos # Kablonun başlangıç pozisyonu
        self.end_pos = start_pos # Kablonun bitiş pozisyonu
        self.color = BLACK # Kablonun rengi

    def set_end_pos(self, end_pos):
        self.end_pos = end_pos  # Kablonun bitiş pozisyonunu ayarlar

    def set_color(self, color):
        self.color = color # Kablonun rengini ayarlar

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, 2) # Kablonun ekrana çizimi

# Çıkış sınıfı
class Exit:
    def handle_event(event):
        if event.type == pygame.QUIT: # Pencere kapatılır
            pygame.quit() # Pygame kapatılır
            sys.exit() # Program sonlandırılır

gates = [] # Mantıksal kapıların listesi
switches = [] # Anahtarların listesi
leds = [] # LED'lerin listesi
wires = []  # Kabloların listesi

current_wire = None # Şu anda çizilmekte olan kablo
adding_led = False # LED eklenip eklenmediğini belirtir
adding_switch = False # Anahtar eklenip eklenmediğini belirtir
current_gate_type = None # Şu anda eklenmek istenen mantıksal kapı türü

gate_menu_open = False  # Mantıksal kapı menüsünün açık olup olmadığını belirtir
truth_table_open = False # Doğruluk tablosunun açık olup olmadığını belirtir
simulation_running = False  # Simülasyonun çalışıp çalışmadığını belirtir

# Mantıksal kapı menüsünü ekrana çizen fonksiyon
def draw_gate_menu():
    menu_items = [
        ("NOT", not_image, NotGate),
        ("AND", and_image, AndGate),
        ("OR", or_image, OrGate),
        ("NAND", nand_image, NandGate),
        ("NOR", nor_image, NorGate),
        ("XOR", xor_image, XorGate),
        ("XNOR", xnor_image, XnorGate),
        ("BUFFER", buffer_image, BufferGate)
    ]

    x_start = 10
    y_start = 40
    # Her menü öğesini ekrana çizer
    for index, (label, image, gate_class) in enumerate(menu_items):
        screen.blit(image, (x_start + index * (CELL_SIZE * 2 + 10), y_start)) # Görseli ekrana çizer
        font = pygame.font.SysFont(None, 24) # Yazı tipi ve boyutu belirler
        text = font.render(label, True, BLACK) # Etiketi oluşturur
        screen.blit(text, (x_start + index * (CELL_SIZE * 2 + 10), y_start + CELL_SIZE * 2))  # Etiketi ekrana çizer

# Ana menü öğelerini ekrana çizen fonksiyon
def draw_main_menu():
    pygame.draw.rect(screen, BLACK, (10, 10, 50, 20)) # 'Gates' düğmesi
    font = pygame.font.SysFont(None, 24) # Yazı tipi ve boyutu belirler
    text = font.render('Gates', True, WHITE)  # 'Gates' metnini oluştur
    screen.blit(text, (14, 10)) # 'Gates' metnini ekrana çizer

    pygame.draw.rect(screen, BLACK, (70, 10, 100, 20))
    text = font.render('Truth Table', True, WHITE)
    screen.blit(text, (74, 10))

    pygame.draw.rect(screen, BLACK, (180, 10, 100, 20))
    text = font.render('Add Switch', True, WHITE)
    screen.blit(text, (185, 10))

    pygame.draw.rect(screen, BLACK, (290, 10, 80, 20))
    text = font.render('Add LED', True, WHITE)
    screen.blit(text, (295, 10))

    pygame.draw.rect(screen, BLACK, (380, 10, 50, 20))
    text = font.render('Start', True, WHITE)
    screen.blit(text, (385, 10))

    pygame.draw.rect(screen, BLACK, (440, 10, 50, 20))
    text = font.render('Pause', True, WHITE)
    screen.blit(text, (445, 10))

    pygame.draw.rect(screen, BLACK, (500, 10, 50, 20))
    text = font.render('Reset', True, WHITE)
    screen.blit(text, (505, 10))

    pygame.draw.rect(screen, RED, (630, 10, 60, 20))
    text = font.render('Exit', True, WHITE)
    screen.blit(text, (635, 10))

# Simülasyonu sıfırlama fonksiyonu
def reset_simulation():
    global gates, switches, leds, wires, current_wire, adding_led, adding_switch, current_gate_type
    gates = [] # Mantıksal kapıların listesini sıfırlar
    switches = []  # Anahtarların listesini sıfırlar
    leds = [] # LED'lerin listesini sıfırlar
    wires = [] # Kabloların listesini sıfırlar
    current_wire = None
    adding_led = False
    adding_switch = False
    current_gate_type = None


def main():
    # Global değişkenlerin durumları
    global gate_menu_open, truth_table_open, current_gate_type, adding_switch, adding_led, current_wire, simulation_running

    clock = pygame.time.Clock() # Oyun zamanlayıcısı

    # Ana oyun döngüsü
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            Exit.handle_event(event) # Çıkış işlemleri kontrol edilir

            if event.type == pygame.MOUSEBUTTONDOWN: # Fare tıklamaları kontrol edilir
                x, y = event.pos
                # Ana menü işlemleri
                if 10 <= x <= 60 and 10 <= y <= 30:
                    gate_menu_open = not gate_menu_open # Kapı menüsünü aç/kapat
                    truth_table_open = False
                elif 70 <= x <= 170 and 10 <= y <= 30:
                    truth_table_open = not truth_table_open # Doğruluk tablosunu aç/kapat
                    gate_menu_open = False
                elif 180 <= x <= 280 and 10 <= y <= 30:
                    adding_switch = True # Anahtar ekleme modu açılır
                    adding_led = False
                    gate_menu_open = False
                    truth_table_open = False
                elif 290 <= x <= 370 and 10 <= y <= 30:
                    adding_led = True # LED ekleme modu açılır
                    adding_switch = False
                    gate_menu_open = False
                    truth_table_open = False
                elif 380 <= x <= 430 and 10 <= y <= 30:
                    simulation_running = True  # Simülasyon başlatılır
                elif 440 <= x <= 490 and 10 <= y <= 30:
                    simulation_running = False # Simülasyon duraklatılır
                elif 500 <= x <= 550 and 10 <= y <= 30:
                    reset_simulation() # Simülasyon sıfırlanır
                elif 630 <= x <= 690 and 10 <= y <= 30:
                    pygame.quit() # Çıkış yapılır
                    sys.exit()
                # Kapı menüsünden kapı seçimi yapılır
                elif gate_menu_open:
                    menu_items = [
                        ("NOT", not_image, NotGate),
                        ("AND", and_image, AndGate),
                        ("OR", or_image, OrGate),
                        ("NAND", nand_image, NandGate),
                        ("NOR", nor_image, NorGate),
                        ("XOR", xor_image, XorGate),
                        ("XNOR", xnor_image, XnorGate),
                        ("BUFFER", buffer_image, BufferGate)
                    ]

                    x_start = 10
                    y_start = 40

                    # Kapı menüsündeki her bir kapı resmini kontrol eder
                    for index, (label, image, gate_class) in enumerate(menu_items):
                        icon_rect = pygame.Rect(x_start + index * (CELL_SIZE * 2 + 10), y_start, CELL_SIZE * 2,
                                                CELL_SIZE * 2) # Kapı resimlerinin etrafındaki dikdörtgenleri oluşturulur
                        # Tıklanan yere göre seçilen kapı türünü ayarlar
                        if icon_rect.collidepoint(x, y):
                            current_gate_type = gate_class
                            gate_menu_open = False # Kapı menüsü kapatılır
                            break
                else:
                    # Kapı menüsü kapalıysa, fare tıklamaları işlenir
                    grid_x = (x // CELL_SIZE) * CELL_SIZE
                    grid_y = (y // CELL_SIZE) * CELL_SIZE
                    # LED veya anahtar ekleme durumu
                    if adding_led:
                        leds.append(Led(grid_x, grid_y))
                        adding_led = False
                    elif adding_switch:
                        switches.append(Switch(grid_x, grid_y))
                        adding_switch = False
                    elif event.button == 1:  # Sol tıklama
                        # Anahtarlar arasında çakışma yoksa ve bir kapı seçiliyse, kapı eklenir
                        if not any(sw.rect.collidepoint(x, y) for sw in switches)  and current_gate_type:
                            gates.append(current_gate_type(grid_x, grid_y))
                    elif event.button == 3:  # Sağ tıklama
                        if current_wire is None:
                            # Kapıların giriş ve çıkış noktalarını kontrol eder
                            for gate in gates:
                                for point in gate.inputs + [gate.output]:
                                    # Fare tıklama noktası, kapının giriş veya çıkış noktasına yakınsa yeni bir kablo başlangıcı oluşturulur
                                    if (x - point[0]) ** 2 + (y - point[1]) ** 2 <= 25:
                                        current_wire = Wire(point)
                                        break
                            for switch in switches:
                                output = (switch.x + CELL_SIZE * 2, switch.y + CELL_SIZE)
                                if (x - output[0]) ** 2 + (y - output[1]) ** 2 <= 25:
                                    current_wire = Wire(output)
                                    break
                            for led in leds:
                                input_pos = (led.x, led.y + CELL_SIZE)
                                if (x - input_pos[0]) ** 2 + (y - input_pos[1]) ** 2 <= 25:
                                    current_wire = Wire(input_pos)
                                    break
                        else:
                            for gate in gates:
                                for point in gate.inputs + [gate.output]:
                                    if (x - point[0]) ** 2 + (y - point[1]) ** 2 <= 25:
                                        current_wire.set_end_pos(point)
                                        wires.append(current_wire)
                                        current_wire = None
                                        break
                            for switch in switches:
                                output = (switch.x + CELL_SIZE * 2, switch.y + CELL_SIZE)
                                if (x - output[0]) ** 2 + (y - output[1]) ** 2 <= 25:
                                    current_wire.set_end_pos(output)
                                    wires.append(current_wire)
                                    current_wire = None
                                    break
                            for led in leds:
                                input_pos = (led.x, led.y + CELL_SIZE)
                                if (x - input_pos[0]) ** 2 + (y - input_pos[1]) ** 2 <= 25:
                                    current_wire.set_end_pos(input_pos)
                                    wires.append(current_wire)
                                    current_wire = None
                                    break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # 's' tuşuna basıldığında switch eklenir
                    adding_switch = True
                elif event.key == pygame.K_l:  # 'l' tuşuna basıldığında led eklenir
                    adding_led = True

        if simulation_running:
            # Eğer simülasyon çalışıyorsa mantık kapılarını ve anahtarları güncelle
            for gate in gates:
                gate.update() if hasattr(gate, 'update') else None # Güncelleme metodu varsa çalıştırılır
            for switch in switches:
                if switch.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    switch.toggle()

            # Bağlantılar kontrol edilir ve sinyal renklerini belirlenir
            for wire in wires:
                wire.set_color(BLACK)
            for switch in switches:
                if switch.state: # Açık anahtarlar için kablolar yeşil renk olacak şekilde ayarlanır
                    for wire in wires:
                        if wire.start_pos == (switch.x + CELL_SIZE * 2, switch.y + CELL_SIZE):
                            wire.set_color(GREEN)
            for gate in gates:
                input_values = []
                for input_pos in gate.inputs:
                    for wire in wires:
                        if wire.end_pos == input_pos and wire.color == GREEN:
                            input_values.append(True)
                            break
                    else:
                        input_values.append(False)
                output_value = gate.process(input_values)
                for wire in wires:
                    if wire.start_pos == gate.output:
                        wire.set_color(GREEN if output_value else BLACK)
            for led in leds:
                led.set_state(False)
                for wire in wires:
                    if wire.end_pos == (led.x, led.y + CELL_SIZE) and wire.color == GREEN:
                        led.set_state(True)

        screen.fill(WHITE) # Ekran beyaz renkle doldurulur
        draw_grid() # Izgara çizgileri eklenir

        # Anahtarları, mantık kapıları, LED'leri ve kabloları ekrana çizer
        for switch in switches:
            switch.draw(screen)
        for gate in gates:
            gate.draw(screen)
        for led in leds:
            led.draw(screen)
        for wire in wires:
            wire.draw(screen)
        if current_wire is not None:
            current_wire.draw(screen)

        draw_main_menu() # Ana menü ekrana çizilir

        if gate_menu_open:
            draw_gate_menu() # Mantık kapıları menüsü ekrana çizilir

        if truth_table_open:
            screen.blit(truth_table_image, (SCREEN_WIDTH - 500, 30)) # Doğruluk tablosu resmi ekranda gösterilir

        pygame.display.flip() # Ekran güncellenir

if __name__ == "__main__":
    main() # Ana fonksiyon çağrılır


