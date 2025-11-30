# 📊 Advanced Sorting & Rating Analysis (Gelişmiş Ürün Sıralama ve Puanlama)

Bu proje, e-ticaret platformlarında ürün listelemeleri ve kullanıcı yorumlarının sıralanması sırasında oluşan yanıltıcı bilgileri (az oyla şişirilmiş puanlar, eski yorumların etkisi) gidermek için geliştirilmiş istatistiksel ve ağırlıklandırma metotlarını uygulamaktadır.

Amacımız, basit ortalamanın ötesine geçerek, **güvenilirliği yüksek ve zamana uygun** bir ürün sıralaması oluşturmaktır.

---

## 🚀 Proje Metotları ve Uygulama Alanları

Bu çalışma, üç temel sıralama ve puanlama felsefesini kullanır:

### 1. Rating Products (Ürün Puanlama Metotları)

Bu metotlar, bir ürünün genel puanını hesaplamanın güvenilirliğini artırır.

| Metot | Amaç | Güncel Hayat Karşılığı |
| :--- | :--- | :--- |
| **Time-Based Weighted Average** | Puanların güncelliğini ölçer. En son verilen puanlara en yüksek ağırlığı (%28, %26, vs.) verir. | *Eski yorumları daha az önemse.* |
| **User-Based Weighted Average** | Puanı veren kullanıcının güvenilirliğini (Örn: İzlenme %'si) ölçer. | *Kursun %90'ını izleyenin puanı daha güvenilirdir.* |
| **Bayesian Average Rating (BAR Score)** | Puan dağılımına (1 yıldız, 5 yıldız sayılarına) göre puanın istatistiksel güvenilirliğini hesaplar. | *2 oyla alınan 5.0 puanı aşağı çek.* |

### 2. Sorting Reviews (Yorum Sıralama Metotları)

Bu metotlar, ürün sayfasında gösterilecek yorumları en faydalı olandan en az faydalı olana doğru sıralar.

| Metot | Amacı | Neden Kullanılır? |
| :--- | :--- | :--- |
| **Up-Down Difference** | Yorumun net popülaritesini ve hacmini ölçer. | En çok etkileşim yaratan yorumu bulmak. |
| **Wilson Lower Bound (WLB)** | **EN ÖNEMLİ METOT.** Yorumların Beğeni/Beğenmeme oranına göre güven aralığının alt sınırını hesaplar. | Yanıltıcı (az oylu) yorumların haksız yere listenin başına çıkmasını engeller. |

### 3. Hibrit Sıralama (Final Score)

* **Logic:** BAR Score (Kalite) ile WSS (Ticari Hacim) skorları, belirlenen ağırlıklarla birleştirilerek tek bir nihai sıralama puanı (`hybrid_sorting_score`) oluşturulur.
* **Kullanım:** E-ticaret sitelerinin vitrininde **hem kaliteli (BAR) hem de popüler (WSS)** olan ürünleri en üste çıkarmak için kullanılır.

---

## 🛠️ Kurulum ve Gereksinimler

Projenin analizi, `pandas`, `numpy`, `scipy.stats` ve `sklearn.preprocessing` kütüphanelerini gerektirir.

```bash
pip install pandas numpy scipy scikit-learn
