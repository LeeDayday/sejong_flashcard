from .models import NewUserInfo
from ..utils.crawler import get_user_info
from django.contrib import messages
from bcrypt import hashpw, gensalt

def f_certify(request):
    # 입력 받은 id/pw 꺼낸다
    user_id = request.POST.get('id')
    user_pw = request.POST.get('pw')

    # 대양 휴머니티 칼리지 인증
    user_info = get_user_info(id=user_id, pw=user_pw)

    # 대양 휴머니티 칼리지 인증 오류 처리
    # id/pw 이 틀린 경우, 가입이 불가한 재학생인 경우
    if user_info == 'err_auth':
        messages.error(request, "세종대학교 포털 ID/PW를 다시 확인하세요. / 재외국민전형 입학자, 계약학과, 편입생은 로그인이 불가합니다.")
    # 대양 휴머니티 칼리지 사이트의 오류인 경우
    elif user_info == 'err_server':
        messages.error(request, "대양 휴머니티 칼리지 서버 오류. 잠시 후 시도해주세요.")

    # 비밀번호 암호화
    user_pw = hashpw(user_pw.encode('utf-8'), gensalt())
    user_pw = user_pw.decode('utf-8')

    # table에 데이터 입력
    new_user = NewUserInfo()
    new_user.student_id = user_id
    new_user.password = user_pw
    new_user.year = user_id[:2]
    # 대휴칼 인증을 통해 가져온 정보
    new_user.name = user_info.get('name')
    new_user.major = user_info.get('major')

    new_user.save()


def f_login(request):
    # 입력 받은 id/pw 꺼낸다
    user_id = request.POST.get('id')
    user_pw = request.POST.get('pw')

    # Model에서 행 추출
    user_row = NewUserInfo.objects.filter(student_id=user_id)

    # 처음 로그인한 경우 대양 휴머니티 인증 작업 진행
    if not user_row.exists():
        f_certify(request, user_id, user_pw)





