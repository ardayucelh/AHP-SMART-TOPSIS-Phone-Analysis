# AHP, SMART ve TOPSIS ile Telefon Analizi

Bu proje, beş telefon alternatifini çok kriterli karar verme yöntemleriyle karşılaştıran Python uygulamasıdır.

## İncelenen alternatifler
- Samsung Galaxy S24
- iPhone 15
- Huawei P40
- Xiaomi Mi 11
- Vivo Y29

## Kriterler ve ağırlıklar

| Kriter | Ağırlık | Yön |
|---|---:|---|
| Batarya | 0.25 | Fayda |
| Performans | 0.25 | Fayda |
| Kamera | 0.20 | Fayda |
| Fiyat | 0.20 | Maliyet |
| Marka | 0.10 | Fayda |

## Yöntemler
- **AHP:** İkili karşılaştırma matrisi üzerinden kriter ağırlıklarını hesaplar ve tutarlılık oranını (CR) raporlar.
- **SMART:** Fayda kriterlerini min-max, maliyet kriterini ters min-max normalizasyonuyla ölçeklendirir ve ağırlıklı toplamı hesaplar.
- **TOPSIS:** Vektör normalizasyonu, ağırlıklandırma ve ideal çözümlere uzaklıklar üzerinden yakınlık katsayısını hesaplar.

## Önemli veri notu
Bu depo, bilgisayar formatlandıktan sonra önceki çalışmaya ait konuşma notlarından yeniden oluşturulmuştur; eski proje dosyalarının birebir kopyası değildir. Telefon alternatifleri ve kriter ağırlıkları önceki çalışmadan kalan bilgilerdir. **Orijinal telefon puanlama tablosu ve AHP anket/ikili karşılaştırma matrisi mevcut olmadığı için** `data/alternatives.csv` içindeki telefon puanları ve fiyatlar yalnızca örnek/temsili demo verileridir.

AHP örneğinde ikili karşılaştırma matrisi, bilinen ağırlıkların oranlarından tutarlı biçimde türetilir. Bu nedenle elde edilen AHP ağırlıkları, bağımsız bir anket sonucunu temsil etmez; bilinen ağırlıkların yöntem içinde gösterilmesini sağlar.

## Kurulum ve çalıştırma

Python 3.10 veya üzeri önerilir.

```bash
pip install -r requirements.txt
python main.py
```

Sonuçlar terminalde her yöntem için ayrı sıralama olarak görüntülenir. Gerçek ders verileri elde edilirse CSV dosyasındaki örnek değerler değiştirilerek analiz tekrarlanabilir.
