import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

# Ayarlar: Çıktıların düzgün görünmesi için
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df=pd.read_csv(r'C:\Users\elifi\OneDrive\Masaüstü\olcumlemeProblemleri\product_sorting.csv')

print("Veri Seti Boyutu:", df.shape)
print("\nİlk 5 Satır:")
print(df.head())

"""
purchase_count: Kurs kaç kere satın alındı? (Popülarite)

rating: Kursun ortalama puanı. (Kalite)

commment_count: Kaç yorum yapıldı? (Etkileşim)

5_point, 4_point...: Puanların dağılımı. (Detaylı Kalite)
"""

"""
Elma ile armudu toplayamayız. purchase_count 10.000 olabilirken, rating en fazla 5 olabilir. Bunları çarpar veya toplarsak, satış sayısı skoru domine eder (yutar).

Çözüm: Ölçeklendirme (MinMax Scaling) Her şeyi 1 ile 5 arasına sıkıştıracağız. Böylece 10.000 satış da "5 puanlık satış başarısı" olacak, 5 yıldız da "5 puanlık kalite başarısı" olacak.
"""
# Satın Alma Sayısını 1-5 arasına sıkıştırıyoruz
# feature_range=(1, 5) -> En düşük satış 1, en yüksek satış 5 puan alacak.
df["purchase_count_scaled"] = MinMaxScaler(feature_range=(1, 5)). \
    fit(df[["purchase_count"]]). \
    transform(df[["purchase_count"]])

# Yorum Sayısını 1-5 arasına sıkıştırıyoruz
df["comment_count_scaled"] = MinMaxScaler(feature_range=(1, 5)). \
    fit(df[["commment_count"]]). \
    transform(df[["commment_count"]])

# Kontrol edelim
print(df[["purchase_count", "purchase_count_scaled", "commment_count", "comment_count_scaled"]].head())


"""
Artık her şey aynı dilden konuşuyor (1-5 arası). Şimdi "İş Bilgimizi" (Domain Knowledge) konuşturarak ağırlık vereceğiz.

Yorum (%32): Etkileşim önemli.

Satın Alma (%26): Para kazandırıyor, ama kalite kadar önemli değil.

Puan (%42): En önemlisi kalite.
"""

def weighted_sorting_score(dataframe,w1=32,w2=26,w3=42):
    return(dataframe["comment_count_scaled"] *w1 /100 +
           dataframe["purchase_count_scaled"] *w2 /100 +
           dataframe["rating"] *w3 /100)
df["weighted_sorting_score"] = weighted_sorting_score(df)
print(df.sort_values("weighted_sorting_score",ascending=False).head(10)[["course_name","weighted_sorting_score"]]),

"""
İkinci Çözüm - Bayes Ortalama Derecelendirme (Bayesian Average Rating - BAR)
Burada çok ince bir problem var. Diyelim ki iki kurs var:

Kurs A: Herkes 5 vermiş (Toplam 2 kişi). Ortalama: 5.0

Kurs B: Yarısı 5, yarısı 4 vermiş (Toplam 100 kişi). Ortalama: 4.5

Weighted Score bunları çözer ama puanların dağılımına (distribution) bakmaz. Sadece ortalamaya bakar.

Bayes Yaklaşımı (BAR) şunu der: "Ben sadece ortalamaya bakmam. Puanların dağılımına bakarım. Eğer az oy varsa puanı aşağı çekerim (güvenmem). Eğer çok oy varsa ve hepsi 5 ise, o zaman puanı yükseltirim."

Bu, bir olasılık hesabıdır. Puanın güvenilirliğini hesaplar.
"""

# Bu fonksiyon karmaşık bir matematik içerir ama mantığı şudur:
# "Verilen puan dağılımına göre, bu ürünün puanı %95 ihtimalle en az kaçtır?"

def bayesian_average_rating(n, confidence=0.95):
    if sum(n) == 0:
        return 0
    K = len(n)
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    N = sum(n)
    first_part = 0.0
    second_part = 0.0
    for k, n_k in enumerate(n):
        # DÜZELTME: n[k] yerine n.iloc[k] kullanıyoruz.
        first_part += (k + 1) * (n.iloc[k] + 1) / (N + K)
        second_part += (k + 1) * (k + 1) * (n.iloc[k] + 1) / (N + K)

    score = first_part - z * math.sqrt((second_part - first_part * first_part) / (N + K + 1))
    return score

# Puan dağılımlarını fonksiyona gönderiyoruz
# Puan dağılımlarını fonksiyona gönderiyoruz
df["bar_score"] = df.apply(lambda x: bayesian_average_rating(x[["1_point",
                                                                "2_point",
                                                                "3_point",
                                                                "4_point",
                                                                "5_point"]]), axis=1)

# BAR skoruna göre ilk 5'e bakalım
print(df.sort_values("bar_score", ascending=False).head(5)[["course_name", "bar_score", "rating"]])
"""
Dikkat: bar_score, normal rating'den genellikle biraz daha düşük çıkar. Çünkü sistem "temkinli" davranır. Bu, gerçek kaliteyi yansıtan en bilimsel puandır.
"""

"""
Hibrit Sıralama (Hybrid Sorting)
Gerçek dünyada ne sadece satışa bakarız ne de sadece kaliteye. İkisini birleştirmeliyiz.

BAR Skoru: Ürünün Kalite potansiyelini verir.

WSS Skoru: Ürünün Ticari başarısını (Satış+Yorum) verir.
"""


def hybrid_sorting_score(dataframe, bar_w=60, wss_w=40):
    # Bar skoru (Kalite) %60 etkili olsun
    bar_score = dataframe.apply(
        lambda x: bayesian_average_rating(x[["1_point", "2_point", "3_point", "4_point", "5_point"]]), axis=1)

    # WSS skoru (Ticari Başarı) %40 etkili olsun
    wss_score = weighted_sorting_score(dataframe)

    return bar_score * bar_w / 100 + wss_score * wss_w / 100


df["hybrid_sorting_score"] = hybrid_sorting_score(df)

# VE İŞTE KAZANANLAR LİSTESİ
print(df.sort_values("hybrid_sorting_score", ascending=False).head(10)[["course_name", "hybrid_sorting_score"]])