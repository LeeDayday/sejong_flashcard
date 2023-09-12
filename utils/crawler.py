# 세종대학교 구성원 인증 라이브러리
from sejong_univ_auth import auth, ClassicSession


def get_user_info(id, pw):
    # ClassicSession: 대양휴머니티칼리지 사이트의 세션 인증 방식
    # 이름, 학과, 학년, 재학 상태, 고전독서 인증 현황 조회 가능
    res = auth(id=id, password=pw, methods=ClassicSession)

    # 대휴칼 사이트 오류
    if res.status_code != 200:
        return "err_server"

    # 로그인 오류 (ID/PW 틀림 or 가입 불가 재학생)
    if not res.is_auth:
        return "err_auth"

    # 사용자 정보
    name = res.body["name"]
    major = res.body["major"]

    context = {
        "name": name,
        "major": major,
    }
    return context
