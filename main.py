import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="Streamlit 던전 탐험기", page_icon="⚔️", layout="centered"
)


# 게임 데이터 및 상태 초기화
def init_game():
    st.session_state.hp = 100
    st.session_state.max_hp = 100
    st.session_state.attack = 15
    st.session_state.gold = 0
    st.session_state.level = 1
    st.session_state.exp = 0
    st.session_state.monster = None
    st.session_state.log = ["던전에 입장했습니다. 탐험을 시작하세요!"]
    st.session_state.game_over = False


if "hp" not in st.session_state:
    init_game()

# 몬스터 생성 데이터
MONSTERS = [
    {"name": "슬라임 🟢", "hp": 30, "attack": 5, "exp": 20, "gold": 15},
    {"name": "고블린 👺", "hp": 55, "attack": 12, "exp": 45, "gold": 35},
    {"name": "스켈레톤 💀", "hp": 90, "attack": 20, "exp": 80, "gold": 70},
    {"name": "드래곤 🐉", "hp": 200, "attack": 35, "exp": 250, "gold": 200},
]


# 로그 추가 함수
def log_msg(msg):
    st.session_state.log.insert(0, msg)


# 행동 함수
def explore():
    if random.random() < 0.75:
        st.session_state.monster = random.choice(MONSTERS).copy()
        log_msg(f"⚠️ 야생의 **{st.session_state.monster['name']}**이(가) 나타났습니다!")
    else:
        found_gold = random.randint(10, 40)
        st.session_state.gold += found_gold
        log_msg(f"💰 상자를 발견하여 **{found_gold} 골드**를 획득했습니다.")


def attack():
    monster = st.session_state.monster
    # 플레이어 공격
    damage = random.randint(
        st.session_state.attack - 3, st.session_state.attack + 5
    )
    monster["hp"] -= damage
    log_msg(f"⚔️ {monster['name']}에게 **{damage}**의 데미지를 입혔습니다!")

    # 몬스터 처치 확인
    if monster["hp"] <= 0:
        st.session_state.gold += monster["gold"]
        st.session_state.exp += monster["exp"]
        log_msg(
            f"🎉 {monster['name']}를 처치했습니다! (+{monster['gold']} Gold, +{monster['exp']} EXP)"
        )
        st.session_state.monster = None

        # 레벨업 확인
        if st.session_state.exp >= st.session_state.level * 50:
            st.session_state.level += 1
            st.session_state.max_hp += 20
            st.session_state.hp = st.session_state.max_hp
            st.session_state.attack += 5
            log_msg(
                f"✨ **레벨 업!** (Lv.{st.session_state.level}) 공격력과 최대 체력이 상승합니다."
            )
        return

    # 몬스터 반격
    m_damage = random.randint(monster["attack"] - 2, monster["attack"] + 4)
    st.session_state.hp -= m_damage
    log_msg(f"💥 {monster['name']}의 공격으로 **{m_damage}** 데미지를 입었습니다.")

    if st.session_state.hp <= 0:
        st.session_state.hp = 0
        st.session_state.game_over = True
        log_msg("☠️ 쓰러졌습니다... 게임 오버!")


def run_away():
    if random.random() < 0.6:
        log_msg("🏃 도망치는데 성공했습니다!")
        st.session_state.monster = None
    else:
        log_msg("❌ 도망치지 못했습니다!")
        m_damage = random.randint(
            st.session_state.monster["attack"] - 2,
            st.session_state.monster["attack"] + 4,
        )
        st.session_state.hp -= m_damage
        log_msg(
            f"💥 {st.session_state.monster['name']}에게 **{m_damage}** 데미지를 입었습니다."
        )
        if st.session_state.hp <= 0:
            st.session_state.hp = 0
            st.session_state.game_over = True


def buy_potion():
    if st.session_state.gold >= 30:
        st.session_state.gold -= 30
        st.session_state.hp = min(
            st.session_state.max_hp, st.session_state.hp + 40
        )
        log_msg("🧪 물약을 마셔 체력을 40 회복했습니다.")
    else:
        log_msg("❌ 골드가 부족합니다. (필요: 30 Gold)")


def buy_weapon():
    cost = st.session_state.level * 50
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        st.session_state.attack += 8
        log_msg(
            f"🗡️ 무기를 강화하여 공격력이 +8 증가했습니다. (현재: {st.session_state.attack})"
        )
    else:
        log_msg(f"❌ 골드가 부족합니다. (필요: {cost} Gold)")


# UI 레이아웃
st.title("⚔️ 텍스트 던전 RPG")

# 상태 표시 탭
col1, col2, col3, col4 = st.columns(4)
col1.metric("Lv", st.session_state.level)
col2.metric("HP", f"{st.session_state.hp} / {st.session_state.max_hp}")
col3.metric("공격력", st.session_state.attack)
col4.metric("Gold", f"{st.session_state.gold}G")

st.divider()

if st.session_state.game_over:
    st.error("💀 용사가 던전에서 전사했습니다.")
    if st.button("🔄 다시 시작하기", use_container_width=True):
        init_game()
        st.rerun()
else:
    # 전투 또는 탐험 UI
    if st.session_state.monster:
        m = st.session_state.monster
        st.subheader(f"전투 발생: {m['name']}")
        st.progress(
            max(0.0, min(1.0, m["hp"] / 200)), text=f"몬스터 체력: {m['hp']}"
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("⚔️ 공격하기", use_container_width=True):
                attack()
                st.rerun()
        with c2:
            if st.button("🏃 도망치기", use_container_width=True):
                run_away()
                st.rerun()
    else:
        st.subheader("🚶 탐험을 진행할 준비가 되었습니다.")
        if st.button("🔍 깊은 던전으로 들어가기", use_container_width=True):
            explore()
            st.rerun()

    # 상점 UI
    st.divider()
    st.subheader("🛒 상점")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("🧪 체력 포션 구매 (30G)", use_container_width=True):
            buy_potion()
            st.rerun()
    with b2:
        upgrade_cost = st.session_state.level * 50
        if st.button(
            f"🗡️ 무기 강화 ({upgrade_cost}G)", use_container_width=True
        ):
            buy_weapon()
            st.rerun()

# 전투 및 행동 로그
st.divider()
st.subheader("📜 탐험 기록")
for log in st.session_state.log[:7]:
    st.write(log)
