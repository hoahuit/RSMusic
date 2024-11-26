import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine, text

DATABASE_URI = 'mssql+pyodbc://sa:123@minhhoa/re?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(DATABASE_URI)

def get_recommendations(song_id, top_n=5):
    # Tạo kết nối từ engine
    with engine.connect() as connection:
        # Load dữ liệu từ SQL Server
        query = text("SELECT * FROM Songs")
        df = pd.read_sql(query, connection)

        # Tìm bài nhạc đầu vào theo ID
        song = df[df['SongID'] == song_id]
        if song.empty:
            return None

        # Xử lý dữ liệu bị thiếu
        df = df.fillna(0)  # Thay thế tất cả NaN bằng 0
        song = song.fillna(0)

        # Chuẩn bị dữ liệu đặc trưng
        features = ['Tempo', 'Popularity']
        categorical_features = ['Genre', 'Mood']

        # Xử lý dữ liệu categorical bằng one-hot encoding
        df_encoded = pd.get_dummies(df[categorical_features])
        song_encoded = pd.get_dummies(song[categorical_features])

        # Đảm bảo hai DataFrame có cùng số lượng cột
        df_encoded, song_encoded = df_encoded.align(df_encoded, axis=1, fill_value=0)

        # Kết hợp dữ liệu đặc trưng số và categorical
        df_features = pd.concat([df[features], df_encoded], axis=1)
        song_features = pd.concat([song[features], song_encoded], axis=1)

        # Xử lý NaN trong dữ liệu đặc trưng (nếu còn)
        df_features = df_features.fillna(0)
        song_features = song_features.fillna(0)

        # Chuẩn hóa dữ liệu đặc trưng
        scaler = StandardScaler()
        df_features_scaled = scaler.fit_transform(df_features)
        song_features_scaled = scaler.transform(song_features)

        # Tính độ tương tự cosine
        similarity_scores = cosine_similarity(song_features_scaled, df_features_scaled)[0]

        # Thêm độ tương tự vào DataFrame
        df['similarity'] = similarity_scores

        # Lấy top 5 bài hát tương tự
        recommendations = df.sort_values(by='similarity', ascending=False).iloc[1:top_n+1]

        return recommendations[['SongID', 'Title', 'Artist', 'Genre', 'Mood', 'Tempo', 'Popularity']].to_dict(orient='records')
