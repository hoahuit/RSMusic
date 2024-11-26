from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import text
from .content_filtering import get_recommendations
from .db_connection import get_session

app_bp = Blueprint('app', __name__)

@app_bp.route('/')
def index():
    # Kết nối cơ sở dữ liệu và lấy danh sách bài nhạc
    session = get_session()
    songs = session.execute(text("SELECT SongID, Title FROM Songs ORDER BY Title")).fetchall()
    session.close()

    # Truyền danh sách bài nhạc vào template
    return render_template('index.html', songs=songs)

@app_bp.route('/recommend', methods=['POST'])
def recommend():
    song_id = request.form.get('song_id')
    if not song_id:
        return redirect(url_for('app.index'))

    recommendations = get_recommendations(int(song_id), top_n=5)
    if not recommendations:
        return render_template('recommendations.html', recommendations=[], error="Song not found.")

    return render_template('recommendations.html', recommendations=recommendations)
