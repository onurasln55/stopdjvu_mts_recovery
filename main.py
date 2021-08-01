import os

def dosya_ac(dosya_konum):  # verilen dosyayı binary olarak okuma modunda açar.
    dosya = 0
    try:
        dosya = open(dosya_konum, "rb")
        print("dosya açıldı.")
    except IOError:
        print("dosya yok.")
    return dosya

def dosya_boyut(dosya):  # dosyanın içinde kaç offset var onu okur ve getirir
    dosya.seek(0, os.SEEK_END)
    size = dosya.tell()
    print(size)
    dosya.seek(0, 0)
    return size


def oku(dosya):  # dosyada kaldığı yerden itibaren ilk 16 değerini okur
    #print("veri okunuyor")
    veri = dosya.read(16)
    return veri


def imza_ara(veri, imza):  # verilen veri içerisinde yine bizim veridiğimiz hex değeri arar.
    if imza.encode() in veri:
        print(imza + " imza bulundu")
        return 55
    else:
        return 0


def git(dosya, offset):  # dosya içinde istenilen offset değerine gitmemizi sağlar
    dosya.seek(offset,1)


def dizin_sec():
    path = input("Klasor konumunu seçin: ")  # klasör adını url gibi kopyala yada yaz
    ext = input("Bulunacak uzantı girin:")  # uzantıyı başında nokta olmadan yaz
    print("\n")
    try:
        ben_nerdeyim = os.getcwd()  # şuan programın olduğu konumu bul
        liste = open(ben_nerdeyim + "/liste", "w")  # bu konuma dosya oluştur.
    except IOError():
        print("Dosya oluşturulamadı")  # oluşmazsa hata ver
    with os.scandir(path) as tarama:  # verdiğimiz dosya konumunda bulunan dosya ve klasörlerin isimlerini verir
        for belge in tarama:  # dosya ve klasörlerin isimlerini parça parça okur
            if os.path.isfile(belge):  # okunan isim bir klasör ismi mi yoksa dosya ismimi buna bakar.
                if belge.name.endswith(ext):  # bulunan dosyanın bizim verdiğimiz uzantıda olanlarını seçer
                    liste.write(belge.name)  # seçilen dosya adını liste dosyasına yazar.
                    liste.write("\n")  # alt satıra geçer
    liste.close()  # oluşturulan dosya kapatılır.
    return path


def isim_yenile(dosya_adi):  # dosya adının sonundaki kısmı siliyor
    tmp = dosya_adi.split(".")  # ismi parçalar
    new_name = tmp[0] + "." + tmp[1]  # isim içinde bulunan ilk iki bölümün arasına nokta koyarak birleştirir.
    return new_name


def dosya_olustur(path, isim):
    yeni_isim = isim_yenile(isim)
    yeni_dosya = path + "/çözülmüş/" + yeni_isim
    yeni_konum = path + "/çözülmüş"
    try:
        if not os.path.exists(yeni_konum):
            os.makedirs(yeni_konum)
        yeni_olustur = open(yeni_dosya, "wb+")
        yeni_olustur.close()
        return 55
    except IOError():
        print("yeni dosya oluşturulamadı...")
        return 0


def dosya_yaz(veri, isim):
    with open(isim, 'ab') as yeni_dosya:
        yeni_dosya.write(veri)
        yeni_dosya.close()


def dosya_gez(path):
    imza = input("aranacak dosya imzası girin:")
    try:
        liste = open("liste")
    except IOError():
        print("Liste okunamadı")
    dosya_adlari = liste.readlines()
    for dosya_isim in dosya_adlari:
        dosya_isim = dosya_isim.strip()
        dosya_konumu = path + "/" + dosya_isim
        yeni_isim=isim_yenile(dosya_isim)
        yeni_dosya_konumu=path+"/çözülmüş/"+yeni_isim
        print(dosya_konumu)
        d = dosya_ac(dosya_konumu)
        print(d.read(5))
        while True:
            veri = oku(d)
            var_imza = imza_ara(veri, imza)
            if var_imza == 55:
                var_dosya = dosya_olustur(path, dosya_isim.strip())
                if var_dosya == 55:
                    git(d, -224)
                    break
        if var_imza == 55:
            print("dosya kopyalanıyor.")
            while True:
                veri = oku(d)
                if veri!=b'':
                    dosya_yaz(veri, yeni_dosya_konumu)
                else:
                    break

    print("Tüm dosyalar gezildi. imzaları temizlendi.")


konum = dizin_sec()
dosya_gez(konum)

