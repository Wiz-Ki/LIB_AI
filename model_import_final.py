from flask import Flask, request, jsonify
import h5py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

app = Flask(__name__)

# .h5 파일 경로 설정
vector_matrix_path = 'final_matrix_isbn.h5'

# .h5 파일에서 최종 벡터 행렬과 ISBN 리스트 불러오기
with h5py.File(vector_matrix_path, 'r') as h5_file:
    final_matrix = h5_file['final_matrix'][:]
    isbn_list = h5_file['isbn_list'][:].astype(str)  # ISBN 리스트를 문자열로 변환

# 불러온 데이터를 DataFrame으로 변환
final_matrix_df = pd.DataFrame(final_matrix, index=isbn_list)

# 추천 결과 계산 함수
def get_recommendations(isbn_list):
    if len(isbn_list) == 1:
        # 2번 알고리즘 실행
        isbn = str(isbn_list[0])  # 입력된 ISBN을 문자열로 변환

        # 입력된 ISBN이 ISBN 리스트에 존재하는지 확인
        if isbn not in final_matrix_df.index:
            return []

        try:
            # 입력된 ISBN에 해당하는 벡터 추출
            book_vector = final_matrix_df.loc[isbn].values.reshape(1, -1)

            # 코사인 유사도 계산
            cosine_sim = cosine_similarity(book_vector, final_matrix_df)

            # 유사도가 높은 상위 5개 도서의 ISBN 추출 (자기 자신 제외)
            top_indices = cosine_sim.argsort()[0][-6:-1][::-1]
            top_isbns = final_matrix_df.index[top_indices]
            recommended_isbns = [isbn for isbn in top_isbns if isbn != isbn_list[0]][:5]

            return recommended_isbns  # 추천 결과 반환

        except KeyError:
            return []
    else:
        # 3번 알고리즘 실행
        try:
            # 입력된 ISBN들이 ISBN 리스트에 존재하는지 확인
            valid_isbns = [str(isbn) for isbn in isbn_list if str(isbn) in final_matrix_df.index]
            if not valid_isbns:
                return []

            # 개별 유사도 점수 계산
            individual_scores = []
            for isbn in valid_isbns:
                book_vector = final_matrix_df.loc[isbn].values.reshape(1, -1)
                scores = cosine_similarity(book_vector, final_matrix_df)[0]
                individual_scores.append(scores)

            # 개별 유사도 점수 합산 (평균 사용)
            combined_scores = np.mean(individual_scores, axis=0)

            # 유사도 점수 기준으로 정렬
            sim_scores = list(enumerate(combined_scores))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # 북카트에 담긴 책들 제외하고 상위 5개 책 추천
            recommended_isbns = [final_matrix_df.index[i] for i, _ in sim_scores if final_matrix_df.index[i] not in valid_isbns][:5]

            return recommended_isbns
        except KeyError:
            return []

# GET
@app.route('/')
def Running():
    return 'Running'

@app.route('/recommend', methods=['POST'])
def recommend():
    # 요청 데이터 받기
    data = request.get_json()
    isbn_list = [str(isbn) for isbn in data['isbn_list']]  # ISBN 리스트를 문자열로 변환

    # 추천 결과 계산
    recommended_isbns = get_recommendations(isbn_list)

    if not recommended_isbns:
        return jsonify({'error': 'No recommendations found'}), 404
    else:
        # 추천 결과 반환
        return jsonify({'recommended_isbns': recommended_isbns})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
