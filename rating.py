import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

pd.set_option('display.float_format', lambda x: '%.5f' % x)
df=pd.read_csv(r'C:\Users\elifi\OneDrive\Masaüstü\olcumlemeProblemleri\course_reviews.csv')
print(df.head())
# Tarih sütunlarını datetime tipine çevirme
df["Timestamp"] = pd.to_datetime(df['Timestamp'])
df["Enrolled"]=pd.to_datetime(df['Enrolled'])

#Analiz tarihi
current_date = pd.to_datetime('2021-02-10 0:0:0')

#Puanın kaç gün önce verildiğini hesaplama (Time-Based için kritik)
df["days"] = (current_date - df["Timestamp"]).dt.days

#Ortalamayı kontrol edelim
simple_avg = df["Rating"].mean()
print(f"Basit Ortalama Puanı:{simple_avg:.4f}")

def time_based_weighted_average(dataframe, w1=30 ,w2=26, w3=24,w4=20):
    rating_w1 = dataframe.loc[dataframe["days"] <= 30, "Rating"].mean()
    rating_w2 = dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "Rating"].mean()
    rating_w3 = dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "Rating"].mean()
    rating_w4 = dataframe.loc[dataframe["days"] > 180, "Rating"].mean()

    # NaN değerlerini 0 veya genel ortalama ile doldurmak gerekebilir, ancak bu veri setinde
    # genel ortalama kullanmak daha güvenli olacaktır.
    final_score = (rating_w1 * w1 / 100) + \
                  (rating_w2 * w2 / 100) + \
                  (rating_w3 * w3 / 100) + \
                  (rating_w4 * w4 / 100)
    return final_score

time_w_avg= time_based_weighted_average(df)
print(f"Zaman Aralığı Puan (Güncellik): {time_w_avg:.4f}")

def user_based_weight_average(dataframe,w1=22,w2 =24,w3=26,w4=28):
    rating_p1=dataframe.loc[dataframe["Progress"] <= 10, "Rating"].mean()
    rating_p2=dataframe.loc[(dataframe["Progress"] > 10) & (dataframe["Progress"] <= 45),"Rating"].mean()
    rating_p3=dataframe.loc[(dataframe["Progress"] > 45) & (dataframe["Progress"] <= 75),"Rating"].mean()
    rating_p4 = dataframe.loc[dataframe["Progress"] > 75,"Rating"].mean()

    final_score = (rating_p1 *w1 /100) + \
                  (rating_p2 *w2 /100) + \
                  (rating_p3 *w3 /100) + \
                  (rating_p4 *w4 /100)
    return final_score
user_w_avg=user_based_weight_average(df)
print(f"Kullanıcı Temelli Ağırlıklı Puan (Güvenilirlik): {user_w_avg:.4f}")

def final_course_weighted_rating(time_score, user_score, time_w=50, user_w=50):
    return (time_score * time_w / 100) + (user_score * user_w / 100)

final_score = final_course_weighted_rating(time_w_avg, user_w_avg)

print("\n----------------------------------------------------")
print(f"Kursun Basit Ortalaması:             {simple_avg:.4f}")
print(f"Kursun Nihai Ağırlıklı Puanı:        {final_score:.4f}")


