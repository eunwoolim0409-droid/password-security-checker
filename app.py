import hashlib
import re
import streamlit as st

st.set_page_config(
    page_title="비밀번호 안전도 진단 및 해시 변환 툴",
    page_icon="🔒",
    layout="centered",
)

st.title("🔒 비밀번호 안전도 진단 및 해시(Hash) 변환 툴")
st.write(
    "비밀번호를 두 번 입력한 뒤 '분석하기' 버튼을 누르면 안전도를 진단하고,"
    " 50점 이하일 때 해시(SHA-256) 변환을 실행합니다."
)


def evaluate_password(pwd: str):
  """4가지 기준(각 25점, 총 100점)으로 비밀번호 안전도를 평가한다."""
  score = 0
  checks = []

  # 1) 길이 8자 이상 (25점)
  if len(pwd) >= 8:
    score += 25
    checks.append(("✅", "길이 8자 이상 사용 (+25점)"))
  else:
    checks.append(("❌", "길이 8자 미만 (+0점) — 8자 이상으로 입력하세요."))

  # 2) 특수문자 사용 (25점)
  if re.search(r"[^A-Za-z0-9]", pwd):
    score += 25
    checks.append(("✅", "특수문자 사용 (+25점)"))
  else:
    checks.append(("❌", "특수문자 미사용 (+0점) — 특수문자를 추가하세요."))

  # 3) 대소문자 구별 (25점)
  if re.search(r"[A-Z]", pwd) and re.search(r"[a-z]", pwd):
    score += 25
    checks.append(("✅", "대소문자 구별/혼용 (+25점)"))
  else:
    checks.append(
        ("❌", "대소문자 미구별 (+0점) — 대문자와 소문자를 함께 쓰세요.")
    )

  # 4) 숫자 사용 (25점)
  if re.search(r"[0-9]", pwd):
    score += 25
    checks.append(("✅", "숫자 사용 (+25점)"))
  else:
    checks.append(("❌", "숫자 미사용 (+0점) — 숫자를 추가하세요."))

  return score, checks


# 1. 비밀번호 2번 입력받기
password = st.text_input("1. 비밀번호를 입력하세요", type="password")
password_confirm = st.text_input(
    "2. 같은 비밀번호를 한 번 더 입력하세요", type="password"
)

# 2. 분석하기 버튼
if st.button("분석하기"):
  if not password or not password_confirm:
    st.warning("비밀번호를 두 칸 모두 입력해 주세요.")
  elif password != password_confirm:
    st.error("입력한 두 비밀번호가 일치하지 않습니다. 다시 확인해 주세요.")
  else:
    # 두 비밀번호가 모두 입력되고 일치할 때만 분석 실행
    score, checks = evaluate_password(password)

    st.divider()
    st.subheader("📋 보안 체크리스트")
    # 체크리스트를 화면에 바로 출력
    for icon, message in checks:
      st.write(f"{icon} {message}")

    st.subheader(f"📊 최종 진단 결과: {score}점")
    st.progress(score / 100)

    # 3. 점수별 판정 문구 및 50점 이하 해시 변환 툴 발동
    if score >= 100:
      st.success("안전합니다")
    elif score == 75:
      st.warning("보통입니다")
    elif score <= 50:
      st.error("위험합니다")

      st.subheader("🔐 해시 변환 툴 발동 (SHA-256)")
      sha256_value = hashlib.sha256(password.encode("utf-8")).hexdigest()
      st.code(sha256_value, language="text")
      st.caption(
          "50점 이하(위험)로 판정되어 입력한 비밀번호의 단방향 해시(SHA-256)"
          " 변환 결과를 출력합니다."
      )
