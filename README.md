# LIB_AI

프로젝트 기록의서재의 AI 부분입니다.

.gitattributes 파일은 모델을 학습시킨 파일(final_matrix_isbn.h5)을 깃허브에 업로드하기 위한 용도로 100Mb가 넘어가는 대용량 파일을 업로드하기 위하여
Git LFS(Git Large File Storage)를 사용하기 위해 필요한 파일입니다.

Book_recomend.ipynb 파일은 모델 초기 디자인 당시 모델 학습 및 라이브러리 테스트를 위해 작성한 코드가 담겨있는 파일입니다. 

model_import_final.py 파일은 배포를 위해 Flask를 활용하여 기존에 존재하던 Book_recommend.ipynb파일에 추가로 백엔드와 통신하는 부분을 추가한 파일입니다
