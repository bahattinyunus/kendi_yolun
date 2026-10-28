#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kendi Yolun: Felsefi Hata Ayıklama (Debugging) ve Kavram Keşif Motoru
"Okumak veri almaktır; yazmak ve analiz etmek ise modeli eğitmektir."
"""

import sys
import argparse
import random
import os

# Windows konsol ve cp1254 uyumluluğu için UTF-8 stdout yapılandırması
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Terminal Renkleri (ANSI)
USE_COLOR = sys.stdout.isatty() and os.name != 'nt' or os.environ.get('TERM') is not None or os.environ.get('ANSICON') is not None or True

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
        "quote": "Amor Fati: Kaderini sev. Sadece katlanmak değil, ondan kaçmamak değil, onu sevmek.",
        "author": "Friedrich Nietzsche",
        "topic": "Kusursuzluk Yanılgısı",
        "doc": "README.md",
        "insight": "Başına gelen her hata ve acı, seni şu anki bilincine ulaştıran vazgeçilmez bir yapıtaşıdır."
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
    }
}

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

def cmd_quote(args):
    q = random.choice(QUOTES)
    print(colorize("\n" + "="*60, CYAN))
    print(colorize(f"📜 FELSEFİ AFORİZMA [{q['topic']}]", BOLD + GREEN))
    print(colorize("="*60, CYAN))
    print(f"\n\"{colorize(q['quote'], BOLD)}\"\n")
    print(f"— {colorize(q['author'], YELLOW)}")
    print(f"\n💡 {colorize('Derin İçgörü:', BOLD)} {q['insight']}")
    print(f"📖 {colorize('İlgili Belge:', BLUE)} {q['doc']}\n")

def cmd_debug(args):
    issue = args.issue.lower() if args.issue else None
    if not issue or issue not in DEBUG_SCENARIOS:
        print(colorize("\n🛠  ZİHİNSEL HATA AYIKLAMA (PHILOSOPHICAL DEBUGGER)", BOLD + MAGENTA))
        print(colorize("-" * 60, MAGENTA))
        print("Lütfen çözmek istediğiniz zihinsel durumu seçin:\n")
        for key, item in DEBUG_SCENARIOS.items():
            print(f"  • {colorize(key.ljust(12), BOLD + GREEN)} : {item['title']}")
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
    print(colorize("\n🍃 KENDİ YOLUN ARŞİV HARİTASI", BOLD + GREEN))
    print(colorize("=" * 65, GREEN))
    tree = [
        ("01-ogretilerin-reddi", "Zihnin ve Dogmaların Aşılması", [
            "01-budanin-yolu-ve-sinirlari.md",
            "02-soze-dokulenin-sahtelesmesi.md",
            "03-ustanin-yolunu-terk-etmek.md"
        ]),
        ("02-samsara-ve-golge", "Beden, Arzu ve Gölgenin İntegrasyonu", [
            "01-kamala-ve-kamaswami-maddiyat-ve-arzu.md",
            "02-jung-ve-golge-arketipi.md",
            "03-lotus-ve-camur.md"
        ]),
        ("03-nehir-zaman-ve-tao", "Bütünleşme, Nehir ve Wu-Wei Bilgeliği", [
            "01-vasudeva-ve-dinleme-sanati.md",
            "02-zamanin-illuzyonu-ve-ebedi-simdi.md",
            "03-wu-wei-ve-zahmetsiz-eylem.md"
        ]),
        ("04-kavram-haritalari", "Algoritmalar, Matrisler ve Sözlük", [
            "01-capraz-ogreti-matrisi.md",
            "02-felsefi-algoritmalar-ve-hata-ayiklama.md",
            "03-sozluk-ve-kavramlar.md"
        ])
    ]
    for folder, title, files in tree:
        print(f"\n📂 {colorize(folder, BOLD + CYAN)} - {title}")
        for f in files:
            print(f"   └── 📄 {f}")
    print(colorize("\n" + "=" * 65, GREEN) + "\n")

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
    sub_debug = subparsers.add_parser("debug", help="Zihinsel durum hata ayıklayıcısı (dogma, golge, zaman, kontrol, tukenmislik)")
    sub_debug.add_argument("issue", nargs="?", choices=["dogma", "golge", "zaman", "kontrol", "tukenmislik"], help="Hata ayıklamak istediğiniz zihinsel durum")
    sub_debug.set_defaults(func=cmd_debug)

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
