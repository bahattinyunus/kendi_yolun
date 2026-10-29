#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kendi Yolun: Felsefi Hata Ayıklama (Debugging), Kavram Keşif ve Yaşantı Motoru
"Okumak veri almaktır; yazmak ve analiz etmek ise modeli eğitmektir."
"""

import sys
import argparse
import random
import os
import time
import json

# Windows konsol ve cp1254 uyumluluğu için UTF-8 stdout yapılandırması
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Terminal Renkleri (ANSI)
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
RED = "\033[31m"

def colorize(text, color):
    return f"{color}{text}{RESET}"

QUOTES = [
    {
        "quote": "Bilgi aktarılabilir ama bilgelik aktarılamaz. Bilgelik bulunabilir, yaşanabilir... ama söylenemez ve öğretilemez.",
        "author": "Hermann Hesse, Siddhartha",
        "topic": "Öğretilerin Sınırı",
        "doc": "01-ogretilerin-reddi/01-budanin-yolu-ve-sinirlari.md",
        "insight": "Bir kavramı ezberlemek onu yaşamak değildir. Harita arazinin kendisi olamaz."
    },
    {
        "quote": "Söze dökülebilen Tao, mutlak Tao değildir. Adlandırılabilen isim, mutlak isim değildir.",
        "author": "Lao Tzu, Tao Te Ching",
        "topic": "Dil ve Hakikat",
        "doc": "01-ogretilerin-reddi/02-soze-dokulenin-sahtelesmesi.md",
        "insight": "Dile gelen her hakikat donar. Yaşam ise sürekli bir akıştır."
    },
    {
        "quote": "Bu benim yolum. Seninki nerede? Çünkü mutlak bir 'yol' diye bir şey yoktur!",
        "author": "Friedrich Nietzsche, Böyle Buyurdu Zerdüşt",
        "topic": "Bireyleşme Cesareti",
        "doc": "01-ogretilerin-reddi/03-ustanin-yolunu-terk-etmek.md",
        "insight": "Bir ustaya saygı duymanın en yüce yolu, onun yolunu taklit etmek değil kendi patikanı açmaktır."
    },
    {
        "quote": "Benim, sırf dünyayı sevebilmek için günaha, şehvete, mala mülke, kibre ve en utanç verici umutsuzluğa ihtiyacım vardı.",
        "author": "Hermann Hesse, Siddhartha",
        "topic": "Samsara ve Gölge",
        "doc": "02-samsara-ve-golge/01-kamala-ve-kamaswami-maddiyat-ve-arzu.md",
        "insight": "Çamura batmadan lotus çiçeği açamaz. Çöküş, kibrin yok oluşu ve yeniden doğuş için zorunludur."
    },
    {
        "quote": "Kişi, ışık figürleri hayal ederek değil, karanlığı bilincine katarak aydınlanır.",
        "author": "Carl Gustav Jung",
        "topic": "Gölge Entegrasyonu",
        "doc": "02-samsara-ve-golge/02-jung-ve-golge-arketipi.md",
        "insight": "Bastırdığın her karanlık yön yeraltında büyür ve günün birinde seni yönetir."
    },
    {
        "quote": "Hayat, bir sarkaç gibi ıstırap ile can sıkıntısı arasında gidip gelir.",
        "author": "Arthur Schopenhauer",
        "topic": "Arzu ve İstenç",
        "doc": "02-samsara-ve-golge/04-arzu-takintisi-ve-schopenhauer.md",
        "insight": "Arzulamak ıstırap, elde etmek can sıkıntısıdır. Kurtuluş sarkacı kırmaktan geçer."
    },
    {
        "quote": "Siddhartha nehirden şunu öğrendi: Zaman diye bir şey yoktur.",
        "author": "Hermann Hesse, Siddhartha",
        "topic": "Zamanın İllüzyonu",
        "doc": "03-nehir-zaman-ve-tao/02-zamanin-illuzyonu-ve-ebedi-simdi.md",
        "insight": "Su aynı anda hem kaynakta, hem şelalede, hem de okyanustadır. Yalnızca ŞİMDİ vardır."
    },
    {
        "quote": "Zihnini boşalt. Su gibi formsuz, şekilsiz ol. Su akabilir de, yıkabilir de. Su gibi ol dostum.",
        "author": "Bruce Lee (Zen & Taoizm)",
        "topic": "Wu-Wei (Zahmetsiz Akış)",
        "doc": "03-nehir-zaman-ve-tao/03-wu-wei-ve-zahmetsiz-eylem.md",
        "insight": "Sert olan kırılır; yumuşak ve esnek olan her engelin etrafından dolanır."
    },
    {
        "quote": "Aydınlanmadan önce: Odun kes, su taşı. Aydınlandıktan sonra: Odun kes, su taşı.",
        "author": "Zen Özdeyişi",
        "topic": "Anlık Farkındalık",
        "doc": "03-nehir-zaman-ve-tao/04-anlik-farkindalik-ve-zen-ustaligi.md",
        "insight": "Değişen şey eylemin kendisi değil, eyleme sunulan saf mevcudiyettir."
    },
    {
        "quote": "Girmekten en çok korktuğun mağara, aradığın en büyük hazineyi saklar.",
        "author": "Joseph Campbell",
        "topic": "Kahramanın Yolculuğu",
        "doc": "05-bireylesme-ve-varolus/02-kendini-gerceklestirme-ve-kahramanin-yolculugu.md",
        "insight": "Korku, büyümenin pusulasıdır. Rahatsızlık hissettiğin yön senin dönüşüm kapındır."
    },
    {
        "quote": "İnsan ancak kendi ölümünün kaçınılmazlığını göğüslediği zaman otantik bir yaşama adım atabilir.",
        "author": "Martin Heidegger",
        "topic": "Ölüm ve Otantiklik",
        "doc": "05-bireylesme-ve-varolus/03-olum-bilinci-ve-otantik-yasam.md",
        "insight": "Memento Mori: Ölüm hayatı eksiltmez; her nefese emsalsiz bir değer kazandırır."
    },
    {
        "quote": "Harry Haller kendini ikiye bölünmüş sanıyordu: İnsan ve Kurt. Oysa insan binlerce ruhun orkestrasıdır.",
        "author": "Hermann Hesse, Bozkırkurdu",
        "topic": "İkiliğin Aşılması",
        "doc": "06-karsilastirmali-metin-okumalari/01-siddhartha-ve-bozkirkurdu-karsilastirmasi.md",
        "insight": "Kendini tek bir ahlaki ya da felsefi kutba hapsetme; içindeki çoksesliliği kucakla."
    },
    {
        "quote": "2x2=4 artık hayat değil, ölümün başlangıcıdır.",
        "author": "Fyodor Dostoyevski, Yeraltından Notlar",
        "topic": "İrrasyonel Doğa",
        "doc": "06-karsilastirmali-metin-okumalari/02-dostoyevski-yeraltindan-notlar-ve-samsara.md",
        "insight": "İnsan salt bir formül değildir. Hata yapmak ve günaha girmek insan oluşun ispatıdır."
    },
    {
        "quote": "Tanrı'yı seven bir kimse, Tanrı'nın da kendisini sevmesini bekleyemez.",
        "author": "Baruch Spinoza, Etika",
        "topic": "Panteist Bütünlük",
        "doc": "06-karsilastirmali-metin-okumalari/03-spinoza-etik-ve-nehirdeki-tanri.md",
        "insight": "Evrenden kişisel bir lütuf bekleme; evrenin kendisi zaten Tanrı'nın bedenidir."
    },
    {
        "quote": "Sisifos'u tepeye tırmanırken mutlu hayal etmek gerekir.",
        "author": "Albert Camus",
        "topic": "Absürt ve İsyan",
        "doc": "06-karsilastirmali-metin-okumalari/04-albert-camus-sisifos-soyleni-ve-anlamsizlik.md",
        "insight": "Kayanın tekrar yuvarlanacağını bilsen dahi mücadele kalbini doyurmaya yeter."
    },
    {
        "quote": "Rüzgâr mumu söndürür; ama yangını alevlendirir. Sen yangın ol, rüzgârı bekle.",
        "author": "Nassim Nicholas Taleb, Antifragile",
        "topic": "Antifrajillik",
        "doc": "08-zihinsel-modeller-ve-felsefi-notasyonlar/02-antifrajillik-ve-amor-fati.md",
        "insight": "Krizlerden kaçmaya çalışma; krizleri seni derinleştiren bir usta olarak kucakla."
    },
    {
        "quote": "Nerede öleceğimi bilmek isterdim; böylece oraya hiç gitmezdim.",
        "author": "Charlie Munger",
        "topic": "İnversiyon (Via Negativa)",
        "doc": "08-zihinsel-modeller-ve-felsefi-notasyonlar/04-inversiyon-ve-via-negativa.md",
        "insight": "Nasıl başarılı olacağını düşünmeden önce, seni kesinlikle batıracak hataları hayatından çıkar."
    },
    {
        "quote": "Amor Fati: Kaderini sev. Sadece katlanmak değil, ondan kaçmamak değil, onu sevmek.",
        "author": "Friedrich Nietzsche",
        "topic": "Kusursuzluk Yanılgısı",
        "doc": "README.md",
        "insight": "Başına gelen her yara seni şu anki idrakine ulaştıran kutsal bir yapıtaşıdır."
    }
]

DEBUG_SCENARIOS = {
    "dogma": {
        "title": "Dogma ve Dış Otorite Tuzağı",
        "code": "ERR_DOGMA_INFINITY_LOOP",
        "symptoms": "Başkalarının ilkelerine sığınma, kendi deneyimlerine güvenememe, sorgulamaktan korkma.",
        "cause": "Belirsizlik korkusu nedeniyle zihnin hazır haritalara teslim olması.",
        "fix": [
            "1. Harita arazinin kendisi değildir: Kitaplardaki formülleri mutlak gerçek saymayı bırak.",
            "2. Gotama'nın uyarısını hatırla: Usta uyanışını bir öğretiyi dinleyerek değil, yalnız yürüyerek buldu.",
            "3. Kendi deneyimsel verini topla ve dogmayı askıya al."
        ],
        "doc": "01-ogretilerin-reddi/01-budanin-yolu-ve-sinirlari.md"
    },
    "golge": {
        "title": "Gölge İnkarı ve Sahte Saflık (Shadow Repression)",
        "code": "ERR_SHADOW_OVERFLOW",
        "symptoms": "Başkalarının kusurlarına aşırı öfkelenme, kusursuz görünme çabası, içsel suçluluk patlamaları.",
        "cause": "Kendi karanlığını, kibrini ve dünyevi arzularını bastırıp Persona ile özdeşleşme.",
        "fix": [
            "1. Ayna İlkesi: Rahatsız olduğun kişide kendi bastırdığın gölgeni tanı.",
            "2. Lotus Çiçeği Kuralı: Köklerin çamurda olduğunu kabul et; çamursuz lotus açmaz.",
            "3. Enantiodromia riskini gör: Bastırılan arzu zıttına dönüşerek seni esir almadan önce onu bilinçle kucakla."
        ],
        "doc": "02-samsara-ve-golge/02-jung-ve-golge-arketipi.md"
    },
    "zaman": {
        "title": "Zaman İllüzyonu ve Gelecek Kaygısı (Time Glitch)",
        "code": "ERR_FUTURE_DEADLOCK",
        "symptoms": "Şimdiki anı gelecekteki bir amaca feda etmek, geçmiş pişmanlıklarında takılı kalmak.",
        "cause": "Zihnin doğrusal zaman illüzyonuna tutsak olması.",
        "fix": [
            "1. Nehir Ontolojisi: Su aynı anda her yerdedir. Geçmiş bir yük, gelecek bir tehdit değildir.",
            "2. Marcus Aurelius'u an: Yalnızca şu anki iraden ve nefesin sana aittir.",
            "3. 'Bir gün her şey çözülecek' fantezisini bırak; varoluş sadece 'şimdi' içinde gerçekleşir."
        ],
        "doc": "03-nehir-zaman-ve-tao/02-zamanin-illuzyonu-ve-ebedi-simdi.md"
    },
    "kontrol": {
        "title": "Aşırı Kontrol ve Direnç Tuzağı (Ego Resistance)",
        "code": "ERR_CONTROL_FRICTION",
        "symptoms": "Olayları ve insanları zorla değiştirmeye çalışma, akışa öfkelenme, tükenmişlik.",
        "cause": "Egonun evrenden ayrı ve ona hükmeden bir güç olduğunu sanması.",
        "fix": [
            "1. Wu-Wei Uygula: Akıntıya karşı yüzmek yerine akıntının enerjisini kullan.",
            "2. Siddhartha'nın Oğlunu Hatırla: Sevdiğin kişileri bile kendi kaderlerinden ve acılarından koruyamazsın.",
            "3. Su gibi ol: Engellerle çarpışma, etraflarından dolan."
        ],
        "doc": "03-nehir-zaman-ve-tao/03-wu-wei-ve-zahmetsiz-eylem.md"
    },
    "tukenmislik": {
        "title": "Samsara Hastalığı ve Anlamsızlık (Dead Bird Crisis)",
        "code": "ERR_SAMSARA_BURNOUT",
        "symptoms": "Başarıya, paraya ve hedeflere ulaştığın halde içsel donukluk, hayatın anlamsızlaşması.",
        "cause": "Kafesteki ötücü kuşun (ilahi kıvılcımın) madde ve konfor bataklığında nefessiz kalması.",
        "fix": [
            "1. Çöküşü bir uyarı sinyali olarak oku: Bu depresyon değil, sahte bir hayatın iflasıdır.",
            "2. Siddhartha gibi yüklerini bırak: Altın kafesi terk et ve nehir kıyısına çekil.",
            "3. Vasudeva gibi dinlemeyi öğren: Yeniden üretmek için önce sessizleş."
        ],
        "doc": "02-samsara-ve-golge/01-kamala-ve-kamaswami-maddiyat-ve-arzu.md"
    },
    "olum_kaygisi": {
        "title": "Ölüm Kaygısı ve Geçicilik Şoku (Mortality Shock)",
        "code": "ERR_MORTALITY_PANIC",
        "symptoms": "Ölüm düşüncesiyle felç olma, yaşlanma korkusu, her şeyi beyhude görme.",
        "cause": "Egonun kalıcı bir mülk olduğunu sanması ve ölüme-doğru-varlığı inkar etmesi.",
        "fix": [
            "1. Heidegger Perspektifi: Ölüm bilinci hayatı anlamsızlaştırmaz, her ânı biricik kılar.",
            "2. Nehir Metaforu: Su yok olmaz; buharlaşır, bulut olur, yağmur olur. Varlık dönüşümdür.",
            "3. Memento Mori: Bugünü son gününmüş gibi dürüst ve derin yaşa."
        ],
        "doc": "05-bireylesme-ve-varolus/03-olum-bilinci-ve-otantik-yasam.md"
    },
    "anlamsizlik": {
        "title": "Varoluşsal Boşluk ve Absürt Duygusu",
        "code": "ERR_EXISTENTIAL_VACUUM",
        "symptoms": "Sabah kalkacak bir neden bulamama, dünyanın kayıtsızlığından ezilme.",
        "cause": "Anlamın dışarıdan verilecek hazır bir ödül olduğunu beklemek.",
        "fix": [
            "1. Camus İsyanı: Evren anlamsız olabilir; ama sen ona anlam katma özgürlüğüne sahipsin.",
            "2. Sisifos Ol: Dağın tepesine doğru mücadele bile tek başına kalbini doldurmaya yeter.",
            "3. Frankl İlkesi: Hayatın senden ne beklediğine odaklan; sorumluluğu üstlen."
        ],
        "doc": "06-karsilastirmali-metin-okumalari/04-albert-camus-sisifos-soyleni-ve-anlamsizlik.md"
    },
    "suru_baskisi": {
        "title": "Sürüye Boyun Eğme ve Otantiklik Kaybı",
        "code": "ERR_CONFORMITY_TRAP",
        "symptoms": "Başkaları ne der korkusuyla kendi arzularını ertelemek, sahte roller oynamak.",
        "cause": "Yalnız kalma korkusunun benlik saygısının önüne geçmesi.",
        "fix": [
            "1. Siddhartha'nın Duruşu: Babasının sarayını ve onayını terk etme cesaretini hatırla.",
            "2. Yalnızlık Tapınağı: Yalnızlık tecrit değil, benliğin dövüldüğü ocaktır.",
            "3. Kendi Yasanı Koy: Başkalarının onayına dayanan hayat kiralanmış bir hayattır."
        ],
        "doc": "05-bireylesme-ve-varolus/01-birey-olma-korkusu-ve-suru-psikolojisi.md"
    },
    "ask_acisi": {
        "title": "Aşk Acısı ve Mülkiyetçi Tutunma",
        "code": "ERR_ATTACHMENT_SUFFERING",
        "symptoms": "Terk edilme, ayrılık veya kayıp sonrası takıntılı yas, kabullenememe.",
        "cause": "Karşındakini bir mülkiyet sanmak; onun bağımsız bir nehir olduğunu unutmak.",
        "fix": [
            "1. Kamala'nın Vedasını Oku: Aşk tutunmak değil, sevdiğinin özgürce akmasına izin vermektir.",
            "2. Siddhartha'nın Oğluyla İmtihanı: Sevdiklerini kendi ellerinle inşa ettiğin fanusta koruyamazsın.",
            "3. Kozmik Şefkate Genişle: Bireysel sevgiyi evrensel bir sevgiye dönüştür."
        ],
        "doc": "05-bireylesme-ve-varolus/04-ask-ve-ayrilik-kamalanin-vedasi.md"
    },
    "karma_korlugu": {
        "title": "Kısa Vade Hazzı ve Karma Körlüğü (Second-Order Failure)",
        "code": "ERR_SECOND_ORDER_BLINDNESS",
        "symptoms": "Anlık rahatlıklar için gelecekteki huzuru satmak, 've sonra ne olacak?' sorusunu sormamak.",
        "cause": "Birinci dereceden düşünmeye hapsolup sistemik yankıları görememek.",
        "fix": [
            "1. İkinci Dereceden Düşün: 'Ve sonra ne olacak?' sorusunu 3 kez ardışık sor.",
            "2. Karma ilkesini hatırla: Ektiğin her tohum gecikmeli olarak kapına döner.",
            "3. Anlık dopamin avcılığını bırak; uzun vadeli dinginliğe yatırım yap."
        ],
        "doc": "08-zihinsel-modeller-ve-felsefi-notasyonlar/01-ikinci-dereceden-dusunme-ve-karma.md"
    }
}

PRACTICES = [
    {
        "title": "15 Dakikalık Nehir Meditasyonu",
        "category": "Meditasyon & Farkındalık",
        "summary": "Düşünceleri, kaygıları ve duyguları nehirde sürüklenen sonbahar yaprakları gibi izle.",
        "rule": "Yaprağı durdurma, ardına atlama; sadece geçişine tanıklık et.",
        "doc": "07-gunluk-pratikler-ve-meditasyonlar/01-nehir-meditasyonu-rehberi.md"
    },
    {
        "title": "Gölge Günlüğü Yazımı (Ayna Testi)",
        "category": "Psikanalitik Çalışma",
        "summary": "Bugün seni en çok öfkelendiren kişinin kusurunu yaz ve sor: 'Bu bende nasıl gizli?'",
        "rule": "Kendini yargılama ya da aklama; çıplak bir dürüstlükle itiraf et.",
        "doc": "07-gunluk-pratikler-ve-meditasyonlar/02-golge-gunlugu-ve-yazma-egzersizleri.md"
    },
    {
        "title": "Stoacı Akşam Muhasebesi",
        "category": "Stoacı Pratik",
        "summary": "3 Filtre: Kontrol dairesi ayrımı, kusur analizi ve evrensel şükran.",
        "rule": "Bugün kontrolün dışında olan bir şeyi zihninde serbest bırak ve uyu.",
        "doc": "07-gunluk-pratikler-ve-meditasyonlar/03-stoaci-aksam-muhasebesi.md"
    },
    {
        "title": "Wu-Wei Sürtünmesiz Eylem Protokolü",
        "category": "Eylem ve Karar",
        "summary": "Günün en zor görevinde direnç göstermeyi bırak; suyun kayanın etrafından akışı gibi ilerle.",
        "rule": "Zorlama, acele etme; doğru anı bekle ve zahmetsizce bitir.",
        "doc": "07-gunluk-pratikler-ve-meditasyonlar/04-wu-wei-eylem-protokolu.md"
    },
    {
        "title": "Via Negativa Yontma Egzersizi",
        "category": "Zihinsel Sadeleşme",
        "summary": "Hayatına yeni bir hedef eklemek yerine, huzurunu çalan tek bir alışkanlığı hayatından çıkar.",
        "rule": "Michelangelo gibi fazlalığı yont; bilgelik eklemekle değil, eksiltmekle doğar.",
        "doc": "08-zihinsel-modeller-ve-felsefi-notasyonlar/04-inversiyon-ve-via-negativa.md"
    }
]

MATRIX_DATA = [
    {
        "school": "Budizm",
        "truth": "4 Yüce Gerçek; zihinsel aydınlanma",
        "ego": "Anatta (Sabit benlik yoktur)",
        "time": "Döngüsel Samsara",
        "shadow": "Dukkha (Acı arzudan doğar)",
        "method": "Sekiz Dilimli Yol & Meditasyon"
    },
    {
        "school": "Taoizm",
        "truth": "Tao (Söze dökülemeyen düzen)",
        "ego": "Bütünün doğal parçası",
        "time": "Sonsuz akış",
        "shadow": "Yin & Yang (Karşıtların uyumu)",
        "method": "Wu-Wei (Zahmetsiz eylem)"
    },
    {
        "school": "Stoacılık",
        "truth": "Logos (Akıl ve doğa kanunu)",
        "ego": "İçsel kale / İrade merkezi",
        "time": "Şimdiki an (Hic et Nunc)",
        "shadow": "Acı olaydan değil yargıdan doğar",
        "method": "Amor Fati & Kontrol ayrımı"
    },
    {
        "school": "Varoluşçuluk",
        "truth": "Öznel yaşantı ve seçim",
        "ego": "İnşa edilen varoluş",
        "time": "Geleceğe fırlatılmışlık",
        "shadow": "Acı insanı bileyleyen yakıttır",
        "method": "Kendi yolunu ve değerini yaratma"
    },
    {
        "school": "Jungiyen Psikoloji",
        "truth": "Bilinç ile bilinçdışı sentezi",
        "ego": "Buzdağının tepesi; Öz (Self)",
        "time": "Eşzamanlılık (Synchronicity)",
        "shadow": "Gölge (Bastırılan karanlık güç)",
        "method": "Bireyleşme (Individuation)"
    }
]

TREE_DATA = [
    ("01-ogretilerin-reddi", "Zihnin ve Dogmaların Aşılması", [
        "01-budanin-yolu-ve-sinirlari.md",
        "02-soze-dokulenin-sahtelesmesi.md",
        "03-ustanin-yolunu-terk-etmek.md",
        "04-sokratik-bilgisizlik-ve-bos-kadeh.md"
    ]),
    ("02-samsara-ve-golge", "Beden, Arzu ve Gölgenin İntegrasyonu", [
        "01-kamala-ve-kamaswami-maddiyat-ve-arzu.md",
        "02-jung-ve-golge-arketipi.md",
        "03-lotus-ve-camur.md",
        "04-arzu-takintisi-ve-schopenhauer.md"
    ]),
    ("03-nehir-zaman-ve-tao", "Bütünleşme, Nehir ve Wu-Wei Bilgeliği", [
        "01-vasudeva-ve-dinleme-sanati.md",
        "02-zamanin-illuzyonu-ve-ebedi-simdi.md",
        "03-wu-wei-ve-zahmetsiz-eylem.md",
        "04-anlik-farkindalik-ve-zen-ustaligi.md"
    ]),
    ("04-kavram-haritalari", "Algoritmalar, Matrisler ve Sözlük", [
        "01-capraz-ogreti-matrisi.md",
        "02-felsefi-algoritmalar-ve-hata-ayiklama.md",
        "03-sozluk-ve-kavramlar.md",
        "04-varolussal-kriz-rehberi.md"
    ]),
    ("05-bireylesme-ve-varolus", "Kalabalıktan Ayrılma ve Özgürleşme", [
        "01-birey-olma-korkusu-ve-suru-psikolojisi.md",
        "02-kendini-gerceklestirme-ve-kahramanin-yolculugu.md",
        "03-olum-bilinci-ve-otantik-yasam.md",
        "04-ask-ve-ayrilik-kamalanin-vedasi.md"
    ]),
    ("06-karsilastirmali-metin-okumalari", "Edebi ve Felsefi Paralellikler", [
        "01-siddhartha-ve-bozkirkurdu-karsilastirmasi.md",
        "02-dostoyevski-yeraltindan-notlar-ve-samsara.md",
        "03-spinoza-etik-ve-nehirdeki-tanri.md",
        "04-albert-camus-sisifos-soyleni-ve-anlamsizlik.md"
    ]),
    ("07-gunluk-pratikler-ve-meditasyonlar", "Uygulamalı Bilgelik Protokolleri", [
        "01-nehir-meditasyonu-rehberi.md",
        "02-golge-gunlugu-ve-yazma-egzersizleri.md",
        "03-stoaci-aksam-muhasebesi.md",
        "04-wu-wei-eylem-protokolu.md"
    ]),
    ("08-zihinsel-modeller-ve-felsefi-notasyonlar", "Bilişsel Modeller ve Düşünce Algoritmaları", [
        "01-ikinci-dereceden-dusunme-ve-karma.md",
        "02-antifrajillik-ve-amor-fati.md",
        "03-occam-usturasi-ve-wu-wei.md",
        "04-inversiyon-ve-via-negativa.md"
    ])
]

def cmd_quote(args):
    q = random.choice(QUOTES)
    print(colorize("\n" + "="*65, CYAN))
    print(colorize(f"📜 FELSEFİ AFORİZMA [{q['topic']}]", BOLD + GREEN))
    print(colorize("="*65, CYAN))
    print(f"\n\"{colorize(q['quote'], BOLD)}\"\n")
    print(f"— {colorize(q['author'], YELLOW)}")
    print(f"\n💡 {colorize('Derin İçgörü:', BOLD)} {q['insight']}")
    print(f"📖 {colorize('İlgili Belge:', BLUE)} {q['doc']}\n")

def cmd_debug(args):
    issue = args.issue.lower() if args.issue else None
    if not issue or issue not in DEBUG_SCENARIOS:
        print(colorize("\n🛠  ZİHİNSEL HATA AYIKLAMA (PHILOSOPHICAL DEBUGGER)", BOLD + MAGENTA))
        print(colorize("-" * 65, MAGENTA))
        print("Lütfen çözmek istediğiniz zihinsel durumu seçin:\n")
        for key, item in DEBUG_SCENARIOS.items():
            print(f"  • {colorize(key.ljust(18), BOLD + GREEN)} : {item['title']}")
        print(f"\nÖrnek kullanım: {colorize('python kendi_yolun.py debug dogma', YELLOW)}\n")
        return

    scenario = DEBUG_SCENARIOS[issue]
    print(colorize("\n" + "="*65, RED))
    print(colorize(f"🚨 HATA KODU: {scenario['code']}", BOLD + RED))
    print(colorize(f"📌 TEŞHİS: {scenario['title']}", BOLD + YELLOW))
    print(colorize("="*65, RED))
    print(f"\n🔍 {colorize('Belirtiler:', BOLD)} {scenario['symptoms']}")
    print(f"⚡ {colorize('Kök Neden:', BOLD)} {scenario['cause']}\n")
    print(colorize("🔧 REFACTORING / ÇÖZÜM ADIMLARI:", BOLD + GREEN))
    for step in scenario['fix']:
        print(f"   {step}")
    print(f"\n📚 {colorize('İlgili Okuma:', BLUE)} {scenario['doc']}\n")

def cmd_practice(args):
    p = random.choice(PRACTICES)
    print(colorize("\n" + "="*65, GREEN))
    print(colorize(f"🧘 GÜNLÜK PRATİK: {p['title']}", BOLD + YELLOW))
    print(colorize("="*65, GREEN))
    print(f"🏷  {colorize('Kategori:', BOLD)} {p['category']}")
    print(f"📋 {colorize('Özet:', BOLD)} {p['summary']}")
    print(f"⚡ {colorize('Altın Kural:', BOLD + RED)} {p['rule']}")
    print(f"📖 {colorize('Uygulama Rehberi:', BLUE)} {p['doc']}\n")

def cmd_meditate(args):
    cycles = args.cycles if hasattr(args, 'cycles') and args.cycles else 1
    print(colorize("\n" + "="*65, CYAN))
    print(colorize("🌊 NEHİR NEFES PROTOKOLÜ (4-2-6)", BOLD + GREEN))
    print(colorize("="*65, CYAN))
    print("Sırtınızı dik tutun, gözlerinizi kapatmaya hazırlanın.")
    print(f"Döngü Sayısı: {cycles} | Çıkmak için Ctrl+C\n")

    try:
        for c in range(1, cycles + 1):
            print(colorize(f"--- Döngü {c}/{cycles} ---", BOLD + YELLOW))
            # 1. Nefes Al (4 sn)
            sys.stdout.write(colorize("🌿 [4 sn] Nefes Al  : ", CYAN))
            for _ in range(4):
                sys.stdout.write("● ")
                sys.stdout.flush()
                time.sleep(1)
            print(" (Doldur)")

            # 2. Tut (2 sn)
            sys.stdout.write(colorize("⏳ [2 sn] Nefesi Tut: ", YELLOW))
            for _ in range(2):
                sys.stdout.write("■ ")
                sys.stdout.flush()
                time.sleep(1)
            print(" (Hareketsiz kal)")

            # 3. Ver (6 sn)
            sys.stdout.write(colorize("🍃 [6 sn] Yavaşça Ver: ", GREEN))
            for _ in range(6):
                sys.stdout.write("○ ")
                sys.stdout.flush()
                time.sleep(1)
            print(" (Serbest bırak)\n")

        print(colorize("✨ Pratik tamamlandı. Nehir gibi dingin ve mevcudiyette kal.", BOLD + GREEN))
    except KeyboardInterrupt:
        print(colorize("\nPratik erken durduruldu. Huzurla kal.", YELLOW))

def cmd_journal(args):
    jtype = args.type.lower() if args.type else "stoic"
    print(colorize("\n" + "="*65, MAGENTA))
    if jtype == "shadow":
        print(colorize("🌑 GÖLGE ÇALIŞMASI GÜNLÜK ŞABLONU", BOLD + YELLOW))
        print(colorize("="*65, MAGENTA))
        print("""
Tarih: ______________
1. Bugün en çok kime ve hangi davranışa öfkelendim/tahammülsüzleştim?
   -> 
2. Bu öfkelendiğim nitelik benim içimde hangi biçimde bastırılmış durumda?
   -> 
3. Başkalarına kusursuz görünmek için bugün kendimi nasıl sansürledim?
   -> 
4. Bu karanlık yönümü suçlamadan, ona merhametle ne söyleyebilirim?
   -> 
""")
    else:
        print(colorize("🏛 STOACI AKŞAM MUHASEBESİ ŞABLONU", BOLD + CYAN))
        print(colorize("="*65, MAGENTA))
        print("""
Tarih: ______________
1. Kontrolümün Dışında Olanlar (Bırakılması Gerekenler):
   -> 
2. Kontrolümde Olanlar (Tutumum, Eylemim, İradem):
   -> 
3. Bugün Nerede Zaaf Gösterdim ve Yarın Nasıl Düzeltebilirim?
   -> 
4. Evrenin Akışına Şükran Duyduğum 3 Basit Şey:
   [1] ___________________________________________________________
   [2] ___________________________________________________________
   [3] ___________________________________________________________
""")
    print(f"Detaylı pratik için: {colorize('07-gunluk-pratikler-ve-meditasyonlar/', BLUE)}\n")

def cmd_export(args):
    fmt = args.format.lower() if args.format else "json"
    if fmt == "json":
        data = {
            "title": "Kendi Yolun - Felsefe Arşivi",
            "modules_count": len(TREE_DATA),
            "quotes_count": len(QUOTES),
            "scenarios_count": len(DEBUG_SCENARIOS),
            "modules": [{"folder": f, "title": t, "docs": d} for f, t, d in TREE_DATA],
            "quotes": QUOTES
        }
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("# Kendi Yolun - Arşiv Dökümü\n")
        for folder, title, files in TREE_DATA:
            print(f"## {folder} — {title}")
            for f in files:
                print(f"- {f}")
            print()

def cmd_search(args):
    query = args.query.lower() if args.query else ""
    if not query:
        print(colorize("Lütfen bir arama terimi girin: python kendi_yolun.py search <terim>", RED))
        return
    print(colorize(f"\n🔍 '{query}' İÇİN ARAMA SONUÇLARI", BOLD + CYAN))
    print(colorize("=" * 65, CYAN))
    found = 0
    # Aforizmalarda ara
    for q in QUOTES:
        if query in q['quote'].lower() or query in q['author'].lower() or query in q['topic'].lower() or query in q['insight'].lower():
            found += 1
            print(f"\n📜 [Aforizma] {colorize(q['author'], YELLOW)}: \"{q['quote'][:70]}...\"")
            print(f"   İçgörü: {q['insight']}")
            print(f"   Belge: {colorize(q['doc'], BLUE)}")

    # Debug senaryolarında ara
    for k, v in DEBUG_SCENARIOS.items():
        if query in k or query in v['title'].lower() or query in v['symptoms'].lower() or query in v['cause'].lower():
            found += 1
            print(f"\n🚨 [Debugger: {k}] {colorize(v['title'], RED)}")
            print(f"   Belirtiler: {v['symptoms'][:80]}...")
            print(f"   Belge: {colorize(v['doc'], BLUE)}")

    # Dosya ağacında ara
    for folder, title, files in TREE_DATA:
        for f in files:
            if query in f.lower() or query in folder.lower() or query in title.lower():
                found += 1
                print(f"\n📄 [Arşiv Belgesi] {colorize(folder + '/' + f, GREEN)} ({title})")

    if found == 0:
        print(f"'{query}' terimiyle eşleşen içerik bulunamadı. Başka bir kavram deneyin (örn: nehir, zaman, gölge, aşk, ölüm, karma).")
    else:
        print(colorize(f"\nToplam {found} eşleşme bulundu.\n", GREEN))

def cmd_matrix(args):
    print(colorize("\n📊 ÇAPRAZ ÖĞRETİ MATRİSİ", BOLD + CYAN))
    print(colorize("=" * 75, CYAN))
    for item in MATRIX_DATA:
        print(f"\n{colorize('✦ ' + item['school'], BOLD + YELLOW)}")
        print(f"  • Hakikat : {item['truth']}")
        print(f"  • Benlik  : {item['ego']}")
        print(f"  • Zaman   : {item['time']}")
        print(f"  • Gölge   : {item['shadow']}")
        print(f"  • Yöntem  : {colorize(item['method'], GREEN)}")
    print(colorize("\n" + "=" * 75, CYAN))
    print(f"Detaylı doküman için: {colorize('04-kavram-haritalari/01-capraz-ogreti-matrisi.md', BLUE)}\n")

def cmd_explore(args):
    print(colorize("\n🍃 KENDİ YOLUN GENİŞLETİLMİŞ ARŞİV HARİTASI (8 MODÜL, 32 METİN)", BOLD + GREEN))
    print(colorize("=" * 70, GREEN))
    for folder, title, files in TREE_DATA:
        print(f"\n📂 {colorize(folder, BOLD + CYAN)} — {title}")
        for f in files:
            print(f"   └── 📄 {f}")
    print(colorize("\n" + "=" * 70, GREEN) + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Kendi Yolun - Deneyimsel Bilgelik ve Karşılaştırmalı Felsefe Motoru",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Kullanılabilir komutlar")

    # quote
    sub_quote = subparsers.add_parser("quote", help="Rastgele felsefi aforizma ve içgörü getirir")
    sub_quote.set_defaults(func=cmd_quote)

    # debug
    sub_debug = subparsers.add_parser("debug", help="Zihinsel durum hata ayıklayıcısı")
    sub_debug.add_argument("issue", nargs="?", choices=list(DEBUG_SCENARIOS.keys()), help="Hata ayıklamak istediğiniz zihinsel durum")
    sub_debug.set_defaults(func=cmd_debug)

    # practice
    sub_practice = subparsers.add_parser("practice", help="Günlük felsefi pratik ve meditasyon önerisi")
    sub_practice.set_defaults(func=cmd_practice)

    # meditate
    sub_meditate = subparsers.add_parser("meditate", help="Terminal nefes meditasyon protokolü")
    sub_meditate.add_argument("-c", "--cycles", type=int, default=1, help="Nefes döngüsü sayısı (varsayılan: 1)")
    sub_meditate.set_defaults(func=cmd_meditate)

    # journal
    sub_journal = subparsers.add_parser("journal", help="Stoacı veya gölge çalışması günlük şablonu üretir")
    sub_journal.add_argument("type", nargs="?", choices=["stoic", "shadow"], default="stoic", help="Günlük tipi (stoic / shadow)")
    sub_journal.set_defaults(func=cmd_journal)

    # export
    sub_export = subparsers.add_parser("export", help="Felsefi arşiv veya şablon dökümünü dışa aktarır")
    sub_export.add_argument("format", nargs="?", choices=["json", "md"], default="json", help="Dışa aktarma formatı (json / md)")
    sub_export.set_defaults(func=cmd_export)

    # search
    sub_search = subparsers.add_parser("search", help="Arşiv ve kavramlar arasında akıllı arama")
    sub_search.add_argument("query", help="Aranacak terim (örn: zaman, gölge, ölüm, tao, karma)")
    sub_search.set_defaults(func=cmd_search)

    # matrix
    sub_matrix = subparsers.add_parser("matrix", help="Karşılaştırmalı felsefe matrisini gösterir")
    sub_matrix.set_defaults(func=cmd_matrix)

    # explore
    sub_explore = subparsers.add_parser("explore", help="Depo mimarisini ve belgeleri listeler")
    sub_explore.set_defaults(func=cmd_explore)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        cmd_quote(args)
        cmd_explore(args)

if __name__ == "__main__":
    main()
