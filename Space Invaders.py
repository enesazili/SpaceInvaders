#Gerekli kütüphaneleri import et
import pygame
import random

# Pygame'i başlat
pygame.init()

# Ses dosyalarını yükle
ATES_SES = pygame.mixer.Sound("Assests/ates.wav") 
PATLAMA_SES = pygame.mixer.Sound("Assests/olme.wav")   

# Ekran boyutlarını tanımla
EKRAN_GENISLIK = 800
EKRAN_YUKSEKLIK = 600
EKRAN = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK))

# Oyun başlığı
pygame.display.set_caption("Space Invaders Oyunu")

# Renk tanımlamaları
ARKAPLAN_RENGI = (0, 0, 0)
FONT_RENGI = (255, 0, 0)

# Oyuncu ve düşman resimlerini yükle
OYUNCU_RESIM = pygame.image.load("Assests/gemi.png")
OYUNCU_X = 370
OYUNCU_Y = 480
OYUNCU_X_DEGISIM = 0

DUSMAN_RESIM = pygame.image.load("Assests/dusman.png")
DUSMAN_X = random.randint(0, 736)
DUSMAN_Y = random.randint(50, 150)
DUSMAN_X_DEGISIM = 4
DUSMAN_Y_DEGISIM = 40

LAZER_RESIM = pygame.image.load("Assests/lazer.png")
LAZER_X = 0
LAZER_Y = 480
LAZER_Y_DEGISIM = 10
LAZER_DURUM = "ready"  # Merminin durumu, "ready" veya "fire"

SKOR = 0  # Başlangıç skoru

FPS = pygame.time.Clock()  # FPS kontrolü için

# Oyuncu fonksiyonu
def oyuncu(x, y):
    EKRAN.blit(OYUNCU_RESIM, (x, y))

# Düşman fonksiyonu
def dusman(x, y):
    EKRAN.blit(DUSMAN_RESIM, (x, y))

# Ateş etme fonksiyonu
def ates_etme(x, y):
    global LAZER_DURUM
    LAZER_DURUM = "fire"  # Mermiyi ateşle
    EKRAN.blit(LAZER_RESIM, (x + 16, y + 10))
    ATES_SES.play()  # Ateş sesi çal

# Çarpışma kontrol fonksiyonu
def carpisma(dusman_x, dusman_y, mermi_x, mermi_y):
    mesafe = ((dusman_x - mermi_x)**2 + (dusman_y - mermi_y)**2) ** 0.5
    return mesafe < 27  # Eğer mesafe 27'den küçükse çarpışma var

# Skor gösterim fonksiyonu
def skorbord(durum, renk, font, boyut):
    Skor_Font = pygame.font.SysFont(font, boyut)  # Font oluştur
    Skor = Skor_Font.render(f"Skor : {SKOR}", True, renk)  # Skoru render et
    Skor_Koordinat = Skor.get_rect()  # Skorun dikdörtgen alanını al
    if durum == 1:
        Skor_Koordinat.midleft = (20, 20)  # Sol üst köşe
    else:
        Skor_Koordinat.midtop = (EKRAN_GENISLIK / 2, EKRAN_YUKSEKLIK / 1.25)  # Ortada üst
    EKRAN.blit(Skor, Skor_Koordinat)  # Skoru ekrana yerleştir

OYUN_CALISMA = True
while OYUN_CALISMA:
    EKRAN.fill(ARKAPLAN_RENGI)  # Ekranı arka plan rengi ile doldur

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Pencere kapatıldığında
            OYUN_CALISMA = False
        
        if event.type == pygame.KEYDOWN:  # Tuşlara basıldığında
            if event.key == pygame.K_LEFT:
                OYUNCU_X_DEGISIM = -5  # Sol tuşu için hız değişimi
            if event.key == pygame.K_RIGHT:
                OYUNCU_X_DEGISIM = 5  # Sağ tuşu için hız değişimi
            if event.key == pygame.K_SPACE:  # Boşluk tuşuna basıldığında
                if LAZER_DURUM == "ready":  # Eğer mermi hazırsa
                    LAZER_X = OYUNCU_X  # Mermiyi oyuncunun konumuna yerleştir
                    ates_etme(LAZER_X, LAZER_Y)  # Ateş et

        if event.type == pygame.KEYUP:  # Tuş bırakıldığında
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                OYUNCU_X_DEGISIM = 0  # Hızı sıfırla

    # Oyuncunun konumunu güncelle
    OYUNCU_X += OYUNCU_X_DEGISIM
    OYUNCU_X = max(0, min(OYUNCU_X, 736))  # Ekranın sınırları içinde kal

    # Düşman hareketi
    DUSMAN_X += DUSMAN_X_DEGISIM
    if DUSMAN_X <= 0 or DUSMAN_X >= 736:  # Eğer düşman ekran sınırını geçerse
        DUSMAN_X_DEGISIM *= -1  # Yön değiştir
        DUSMAN_Y += DUSMAN_Y_DEGISIM  # Düşmanı aşağıya kaydır

    # Mermi hareketi
    if LAZER_DURUM == "fire":
        ates_etme(LAZER_X, LAZER_Y)  # Mermiyi ekrana çiz
        LAZER_Y -= LAZER_Y_DEGISIM  # Mermiyi yukarıya hareket ettir

    if LAZER_Y <= 0:  # Eğer mermi üst sınırı geçerse
        LAZER_Y = 480  # Mermiyi başlangıç konumuna getir
        LAZER_DURUM = "ready"  # Mermi durumu "ready" yap

    # Düşman ile mermi çarpışmasını kontrol et
    if carpisma(DUSMAN_X, DUSMAN_Y, LAZER_X, LAZER_Y):
        LAZER_Y = 480  # Mermiyi başlangıç konumuna getir
        LAZER_DURUM = "ready"  # Mermi durumu "ready" yap
        SKOR += 1  # Skoru artır
        PATLAMA_SES.play()  # Patlama sesi çal
        DUSMAN_X = random.randint(0, 736)  # Düşmanı rastgele yeni bir konuma yerleştir
        DUSMAN_Y = random.randint(50, 150)

    skorbord(1, FONT_RENGI, "none", 50)  # Skoru göster
    oyuncu(OYUNCU_X, OYUNCU_Y)  # Oyuncuyu ekrana çiz
    dusman(DUSMAN_X, DUSMAN_Y)  # Düşmanı ekrana çiz

    pygame.display.update()  # Ekranı güncelle
    FPS.tick(60)  # FPS kontrolü

pygame.quit()  # Oyun bittiğinde Pygame'i kapat