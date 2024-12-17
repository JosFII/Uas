import streamlit as st
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import seaborn as sns
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpg;base64,%s");
    background-size: 100vw 300vh;
    background-position: center;  
    background-repeat: no-repeat;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('432e2f06bceeb0ed5dbd36bd882284b6.png')


st.write("Ini merupakan hasil data yang telah didapatkan dari twitter. Data memiliki topik kamen rider ryuki.")
df = pd.read_csv(r'Ryuki_rev.csv')
df[['text','created_at','context_annotations']]

st.write("Sebelum kita dapat melakukan analisa, kita perlu membersihkan data.Dalam pembersihan data kita perlu menghilangkan bagian yang tidak diperlukan seperti link, emoji, tanda baca, dll. Berikut adalah hasil data yang telah dibersihkan.")
df['clean_review']


st.write("Sekarang kita akan membuat word cloud dari data yang telah dibersihkan. Word cloud berguna untuk melihat kata kata apa saja yang sering terlihat, lebih besar katanya, lebing sering kata itu ditemukan.")
comment_words = ''
stopwords = set(STOPWORDS)
 
# iterate through the csv file
for val in df.clean_review:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()
     
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
# plot the WordCloud image                       
fig, ax = plt.subplots(figsize = (12, 8))
ax.imshow(wordcloud)
plt.axis("off")
st.pyplot(fig)

st.write("Jadi bisa dilihat bahwa kata kata yang paling sering keluar adalah kamen rider, dan rider ryuki.")

st.write("Sekarang saya akan melakukan analisa sentiment pada data dari twitter. Model yang digunakan untuk analisa dibuat dengan review film yang diambil dari imdb. Hasil analisis bernilai satu adalah sentiment satu dan bernilai nol jika bersentiment negatif")
df[['clean_review','predicted_sentiment']]

st.write("Jika dilihat hasil analisa sentiment, bisa dilihat bahwa kebanyakan sentiment terlihat benar, tetapi terlihat bahwa ada beberapa kesalahan.")

st.write("Sekarang saya akan membuat pie chart untuk distribusi sentimen yang didapatkan.")

postif=0
negatif=0
for x in df['predicted_sentiment']:
    if x == 1 :
        postif=postif+1
    else:
        negatif=negatif+1



fig2,ax=plt.subplots(figsize = (12, 8))
plt.pie(
    [postif,negatif], 
    labels=["Positif","Negative"],
    autopct='%1.1f%%', 
    startangle=90, 
    colors=sns.color_palette("pastel")
)
plt.title("Distribusi Sentimen")
plt.show()
st.pyplot(fig2)

st.write("Bisa dilihat bahwa 68% dari tweet dari twitter memiliki sentimen postif menurut model, dan 32% memiliki sentimen negatif.")