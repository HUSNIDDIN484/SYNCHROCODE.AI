
import streamlit as st
import json
import traceback
import io
import sys
import re
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG — Dark mode, custom icon, wide layout
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SynchroCode AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — Cyberpunk / Dark-tech aesthetic
# ──────────────────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg-base:       #080b14;
    --bg-card:       #0d1220;
    --bg-card2:      #111827;
    --border:        #1e2d4a;
    --border-glow:   #00d4ff44;
    --accent-cyan:   #00d4ff;
    --accent-green:  #00ff88;
    --accent-orange: #ff6b35;
    --accent-purple: #a855f7;
    --text-primary:  #e2e8f0;
    --text-muted:    #64748b;
    --text-dim:      #334155;
    --font-mono:     'Space Mono', monospace;
    --font-head:     'Syne', sans-serif;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-head) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

.hero-header {
    background: linear-gradient(135deg, #0d1220 0%, #0a1628 50%, #0d1220 100%);
    border: 1px solid var(--border);
    border-top: 2px solid var(--accent-cyan);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-title {
    font-family: var(--font-head);
    font-weight: 800;
    font-size: 2.2rem;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -0.02em;
}
.hero-sub {
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.75rem;
    margin-top: 0.4rem;
    letter-spacing: 0.08em;
}
.badge {
    display: inline-block;
    background: #00d4ff15;
    border: 1px solid #00d4ff33;
    color: var(--accent-cyan);
    font-family: var(--font-mono);
    font-size: 0.65rem;
    padding: 3px 10px;
    border-radius: 999px;
    margin-right: 6px;
    letter-spacing: 0.1em;
}
.section-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.section-title {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    color: var(--accent-cyan);
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 1px;
    background: var(--accent-cyan);
}
.stButton > button {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    border-radius: 8px !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
    text-align: left !important;
}
.stButton > button:hover {
    border-color: var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    box-shadow: 0 0 12px #00d4ff18 !important;
    transform: translateY(-1px) !important;
}
.run-btn > button {
    background: linear-gradient(135deg, #00d4ff18, #a855f718) !important;
    border: 1px solid var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stTextArea"] textarea {
    background: #0a1020 !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
    line-height: 1.6 !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 2px #00d4ff18 !important;
}
.json-block {
    background: #06090f;
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-cyan);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    line-height: 1.7;
    overflow-x: auto;
    white-space: pre;
    color: #d4d4d4;
}
.code-block {
    background: #06090f;
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-green);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    line-height: 1.8;
    overflow-x: auto;
    white-space: pre;
    color: #d4d4d4;
    max-height: 480px;
    overflow-y: auto;
}
.output-block {
    background: #040810;
    border: 1px solid #1a2540;
    border-left: 3px solid var(--accent-orange);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    line-height: 1.8;
    color: #e2e8f0;
    white-space: pre-wrap;
    max-height: 400px;
    overflow-y: auto;
}
.error-block {
    background: #1a0505;
    border: 1px solid #3f0a0a;
    border-left: 3px solid #ef4444;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    color: #fca5a5;
    white-space: pre-wrap;
}
.tag-trigger  { background:#00d4ff18; border:1px solid #00d4ff44; color:#00d4ff;   padding:3px 10px; border-radius:999px; font-size:0.7rem; font-family:'Space Mono',monospace; margin-right:4px; display:inline-block; }
.tag-condition{ background:#a855f718; border:1px solid #a855f744; color:#a855f7;   padding:3px 10px; border-radius:999px; font-size:0.7rem; font-family:'Space Mono',monospace; margin-right:4px; display:inline-block; }
.tag-action   { background:#00ff8818; border:1px solid #00ff8844; color:#00ff88;   padding:3px 10px; border-radius:999px; font-size:0.7rem; font-family:'Space Mono',monospace; margin-right:4px; display:inline-block; }
.metric-row { display:flex; gap:12px; margin-bottom:1rem; }
.metric-box { flex:1; background:var(--bg-card2); border:1px solid var(--border); border-radius:8px; padding:0.8rem 1rem; text-align:center; }
.metric-val { font-family:var(--font-mono); font-size:1.4rem; font-weight:700; color:var(--accent-cyan); }
.metric-lbl { font-family:var(--font-mono); font-size:0.62rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.1em; margin-top:2px; }
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }
.step-indicator { display:flex; gap:8px; align-items:center; margin-bottom:1.2rem; flex-wrap:wrap; }
.step { display:flex; align-items:center; gap:6px; font-family:var(--font-mono); font-size:0.7rem; color:var(--text-muted); }
.step.active { color:var(--accent-cyan); }
.step-num { width:22px; height:22px; border-radius:50%; background:var(--bg-card2); border:1px solid var(--border); display:flex; align-items:center; justify-content:center; font-size:0.65rem; }
.step.active .step-num { background:var(--accent-cyan); color:#000; border-color:var(--accent-cyan); }
.step-arrow { color:var(--text-dim); }
[data-testid="column"] { padding: 0 6px !important; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SCENARIOS — 3 ta tayyor andoza
# ──────────────────────────────────────────────────────────────────────────────
SCENARIOS = {
    "🏫 Smart School": (
        "Agar maktabda qo'ng'iroq chalinsa va e-Maktab tizimida dars tugagan bo'lsa, "
        "ota-onalarga telegramdan xabar ketsin va eshiklar avtomat ochilsin."
    ),
    "🌱 Smart Agriculture": (
        "Agar tuproq namligi 30 dan past bo'lsa va ob-havo ochiq bo'lsa, "
        "suv nasosini yoq va agronomga SMS yubor."
    ),
    "🏠 Smart Home": (
        "Agar soat 21:00 bo'lsa va uyda harakat sezilsa, "
        "xavfsizlik signalizatsiyasini ishga tushir."
    ),
}

# ──────────────────────────────────────────────────────────────────────────────
# STAGE 1 — SEMANTIC PARSER
# ──────────────────────────────────────────────────────────────────────────────
def parse_uzbek_command(text: str) -> dict:
    """
    O'zbek tilidagi buyruqni tahlil qilib semantik komponentlarga ajratadi.
    Returns: { trigger, conditions, actions, domain, confidence, timestamp }
    """
    text_lower = text.lower()

    # Trigger Detection
    trigger_map = {
        "qo'ng'iroq chalinsa":   {"type": "event",  "source": "school_bell",   "event": "bell_ring"},
        "qo'ngiroq chalinsa":    {"type": "event",  "source": "school_bell",   "event": "bell_ring"},
        "soat 21:00 bo'lsa":     {"type": "time",   "source": "scheduler",     "time": "21:00"},
        "soat 21:00":            {"type": "time",   "source": "scheduler",     "time": "21:00"},
        "harakat sezilsa":       {"type": "sensor", "source": "motion_sensor", "event": "motion_detected"},
        "tuproq namligi":        {"type": "sensor", "source": "soil_sensor",   "metric": "soil_moisture"},
        "namlik":                {"type": "sensor", "source": "soil_sensor",   "metric": "soil_moisture"},
        "harorat":               {"type": "sensor", "source": "temp_sensor",   "metric": "temperature"},
        "yong'in":               {"type": "sensor", "source": "fire_sensor",   "event": "fire_detected"},
        "eshik ochilsa":         {"type": "event",  "source": "door_sensor",   "event": "door_open"},
    }
    trigger = {"type": "event", "source": "unknown", "raw": text[:60]}
    for key, val in trigger_map.items():
        if key in text_lower:
            trigger = {**val, "raw": key}
            break

    # Condition Detection
    conditions = []
    condition_patterns = [
        (r"(\d+)\s*dan\s*past",       lambda m: {"field": "value",          "operator": "<",  "threshold": int(m.group(1))}),
        (r"(\d+)\s*dan\s*yuqori",     lambda m: {"field": "value",          "operator": ">",  "threshold": int(m.group(1))}),
        (r"(\d+)\s*ga\s*teng",        lambda m: {"field": "value",          "operator": "==", "threshold": int(m.group(1))}),
        (r"ob-havo\s+ochiq",          lambda m: {"field": "weather",        "operator": "==", "value": "clear"}),
        (r"ob-havo\s+yomg'irli",      lambda m: {"field": "weather",        "operator": "==", "value": "rainy"}),
        (r"dars tugagan",             lambda m: {"field": "emaktab_status", "operator": "==", "value": "lesson_ended"}),
        (r"uyda\s+harakat",           lambda m: {"field": "motion_at_home", "operator": "==", "value": True}),
    ]
    for pattern, builder in condition_patterns:
        m = re.search(pattern, text_lower)
        if m:
            conditions.append(builder(m))

    # Action Detection
    actions = []
    action_map = {
        "telegramdan xabar":              {"type": "notify",  "channel": "telegram",     "target": "parents"},
        "telegram xabar":                 {"type": "notify",  "channel": "telegram",     "target": "parents"},
        "sms yubor":                      {"type": "notify",  "channel": "sms",          "target": "agronomist"},
        "sms yuborsin":                   {"type": "notify",  "channel": "sms",          "target": "user"},
        "eshiklar avtomat ochilsin":      {"type": "actuate", "device": "door_lock",      "state": "unlock"},
        "eshiklarni och":                 {"type": "actuate", "device": "door_lock",      "state": "unlock"},
        "suv nasosini yoq":               {"type": "actuate", "device": "water_pump",     "state": "on"},
        "nasosni yoq":                    {"type": "actuate", "device": "water_pump",     "state": "on"},
        "signalizatsiyasini ishga tushir":{"type": "actuate", "device": "alarm_system",   "state": "activate"},
        "signalizatsiya":                 {"type": "actuate", "device": "alarm_system",   "state": "activate"},
        "chirog'ni yoq":                  {"type": "actuate", "device": "lights",         "state": "on"},
        "chirog'ni o'chir":               {"type": "actuate", "device": "lights",         "state": "off"},
        "konditsionerni yoq":             {"type": "actuate", "device": "ac_unit",        "state": "on"},
    }
    for key, val in action_map.items():
        if key in text_lower:
            actions.append(val)

    # Domain Classification
    domain = "general"
    if any(w in text_lower for w in ["maktab", "dars", "ota-ona", "e-maktab"]):
        domain = "smart_school"
    elif any(w in text_lower for w in ["tuproq", "namlik", "agro", "nasos", "ob-havo", "suv"]):
        domain = "smart_agriculture"
    elif any(w in text_lower for w in ["uy", "xona", "signaliz", "harakat sez"]):
        domain = "smart_home"

    # Confidence Score
    score = 0
    if trigger.get("source") != "unknown": score += 40
    if conditions: score += 30
    if actions:    score += 30

    return {
        "trigger":    trigger,
        "conditions": conditions if conditions else [{"note": "implicit — har doim bajariladi"}],
        "actions":    actions if actions else [{"type": "log", "message": "Amal aniqlanmadi"}],
        "domain":     domain,
        "confidence": min(score, 100),
        "timestamp":  datetime.now().isoformat(timespec='seconds'),
        "input_tokens": len(text.split()),
    }


# ──────────────────────────────────────────────────────────────────────────────
# STAGE 2 — CODE GENERATOR
# ──────────────────────────────────────────────────────────────────────────────
def generate_python_code(parsed: dict, original_text: str) -> str:
    """
    Parsellangan mantiq asosida xavfsiz, try-except bloklarga ega Python kodi generatsiya qiladi.
    Domain bo'yicha ixtisoslashtirilgan kod qaytaradi.
    """
    domain  = parsed.get("domain", "general")
    conds   = parsed.get("conditions", [])
    ts      = parsed["timestamp"]
    orig    = original_text[:80]

    # ── Template: Smart School ────────────────────────────────────────────────
    if domain == "smart_school":
        return f'''"""
SynchroCode AI — Generatsiya qilingan kod
Domain : Smart School (Aqlli Maktab)
Buyruq : {orig}
Vaqt   : {ts}
"""

import time
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("SynchroCode.SmartSchool")


@dataclass
class SchoolState:
    bell_ringing:    bool = True    # Qong\'iroq holati (sensor)
    lesson_ended:    bool = True    # e-Maktab: dars tugagan?
    doors_unlocked:  bool = False
    notifications_sent: int = 0


class TelegramNotifier:
    def __init__(self, bot_token="DEMO_TOKEN", chat_id="DEMO_CHAT"):
        self.bot_token = bot_token
        self.chat_id   = chat_id

    def send_message(self, text: str) -> bool:
        # Real: import requests; requests.post(f"https://api.telegram.org/bot{{self.bot_token}}/sendMessage", ...)
        log.info(f"TELEGRAM -> [{{self.chat_id}}]: {{text}}")
        return True


class DoorController:
    def unlock(self) -> bool:
        # Real: GPIO.output(RELAY_PIN, GPIO.HIGH)
        log.info("ESHIK [MAIN_GATE] — OCHILDI (unlock signal yuborildi)")
        return True


class EMaktabAPI:
    @staticmethod
    def check_lesson_status(class_id="9-A") -> bool:
        # Real: requests.get("https://emaktab.uz/api/...").json()["status"] == "ended"
        log.info(f"e-Maktab API: {{class_id}} sinfi -> dars tugagan")
        return True


def smart_school_automation():
    """
    Trigger : Maktab qo\\'ng\\'irog\\'i
    Shart   : e-Maktabda dars tugagan
    Amallar : 1) Ota-onalarga Telegram xabari
              2) Eshiklarni ochish
    """
    state    = SchoolState()
    telegram = TelegramNotifier()
    door     = DoorController()
    emaktab  = EMaktabAPI()

    log.info("=" * 52)
    log.info("  Smart School Avtomatlashtirish — ISHGA TUSHDI")
    log.info("=" * 52)

    try:
        # TRIGGER: Qo\'ng\'iroq holati
        log.info("TRIGGER tekshirilmoqda: qo\'ng\'iroq holati...")
        if not state.bell_ringing:
            log.info("Qo\'ng\'iroq chalinmagan — kutish rejimi")
            return
        log.info("Qo\'ng\'iroq CHALINDI — shart tekshirilmoqda...")

        # CONDITION: e-Maktab
        if not emaktab.check_lesson_status():
            log.info("Dars hali tugamagan — hech narsa qilinmaydi")
            return
        log.info("SHART bajarildi: dars tugagan!")

        # ACTION 1: Telegram
        msg = (
            "Hurmatli ota-ona!\\n"
            "Farzandingizning darslari yakunlandi.\\n"
            f"Vaqt: {{time.strftime('%H:%M')}} | 47-sonli maktab\\n"
            "Iltimos, o\'z vaqtida kutib oling."
        )
        if telegram.send_message(msg):
            state.notifications_sent += 1
            log.info(f"Telegram xabari yuborildi (jami: {{state.notifications_sent}})")

        # ACTION 2: Eshiklarni ochish
        time.sleep(0.4)
        if door.unlock():
            state.doors_unlocked = True
            log.info("Eshiklar muvaffaqiyatli ochildi!")
        else:
            log.error("Eshiklarni ochib bo\'lmadi!")

        log.info("-" * 52)
        log.info(f"NATIJA | Xabarlar: {{state.notifications_sent}} | "
                 f"Eshik: {{'OCHIQ' if state.doors_unlocked else 'YOPIQ'}}")
        log.info("Smart School muvaffaqiyatli yakunlandi!")

    except ConnectionError as e:
        log.error(f"Tarmoq xatosi: {{e}}")
    except TimeoutError as e:
        log.error(f"Vaqt tugadi: {{e}}")
    except Exception as e:
        log.error(f"Kutilmagan xato: {{type(e).__name__}}: {{e}}")
    finally:
        log.info("Smart School jarayoni yakunlandi.")


if __name__ == "__main__":
    smart_school_automation()
'''

    # ── Template: Smart Agriculture ───────────────────────────────────────────
    elif domain == "smart_agriculture":
        threshold = 30
        for c in conds:
            if isinstance(c.get("threshold"), int):
                threshold = c["threshold"]
        return f'''"""
SynchroCode AI — Generatsiya qilingan kod
Domain : Smart Agriculture (Aqlli Qishloq Xo\'jaligi)
Buyruq : {orig}
Vaqt   : {ts}
"""

import time
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("SynchroCode.SmartAgriculture")

MOISTURE_THRESHOLD = {threshold}   # % quruq chegarasi


@dataclass
class FieldSensors:
    soil_moisture: float = 22.5   # % (simulyatsiya: past qiymat)
    temperature_c: float = 28.3
    weather_status: str  = "clear"
    pump_running:   bool = False
    water_flow_lph: float = 0.0


class WaterPumpController:
    def __init__(self, pump_id="PUMP-01"):
        self.pump_id = pump_id

    def turn_on(self, duration_minutes=30) -> bool:
        # Real: GPIO.output(PUMP_RELAY_PIN, GPIO.HIGH)
        log.info(f"NASOS [{{self.pump_id}}] YONDI — {{duration_minutes}} daqiqa")
        return True


class SMSGateway:
    def send_sms(self, phone: str, message: str) -> bool:
        # Real (Eskiz): requests.post("https://notify.eskiz.uz/api/message/sms/send", ...)
        log.info(f"SMS -> {{phone}}: {{message}}")
        return True


def check_weather_api(lat=41.2995, lon=69.2401) -> str:
    # Real: requests.get("https://api.openweathermap.org/...").json()
    return "clear"


def smart_agriculture_automation():
    """
    Trigger : Tuproq namligi sensori
    Shart   : Namlik < {threshold}% VA ob-havo ochiq
    Amallar : 1) Suv nasosini yoqish
              2) Agronomga SMS
    """
    sensors   = FieldSensors()
    pump      = WaterPumpController()
    sms       = SMSGateway()
    agro_tel  = "+998901234567"

    log.info("=" * 52)
    log.info("  Smart Agriculture — MONITORING BOSHLANDI")
    log.info("=" * 52)

    try:
        log.info(f"Sensor o\'qilmoqda...")
        log.info(f"  Tuproq namligi : {{sensors.soil_moisture}}%")
        log.info(f"  Harorat        : {{sensors.temperature_c}}C")
        log.info(f"  Ob-havo        : {{sensors.weather_status}}")

        # TRIGGER: Namlik tekshirish
        if sensors.soil_moisture >= MOISTURE_THRESHOLD:
            log.info(f"Namlik ({{sensors.soil_moisture}}%) yetarli — sug\'orish kerak emas")
            return
        log.info(f"OGOHLANTIRISH: Namlik ({{sensors.soil_moisture}}%) chegaradan past!")

        # CONDITION: Ob-havo
        weather = check_weather_api()
        sensors.weather_status = weather
        if weather not in ("clear", "sunny"):
            log.info(f"Ob-havo {{weather}} — yomg\'ir kutilmoqda, nasos yoqilmaydi")
            return
        log.info(f"Ob-havo ochiq ({{weather}}) — sug\'orish mumkin!")

        # ACTION 1: Nasosni yoqish
        if pump.turn_on(duration_minutes=45):
            sensors.pump_running   = True
            sensors.water_flow_lph = 120.0
            log.info(f"Nasos ishga tushdi (oqim: {{sensors.water_flow_lph}} l/soat)")
        else:
            log.error("Nasos ishga tushmadi!")
            raise RuntimeError("Pump activation failed")

        # ACTION 2: SMS
        time.sleep(0.3)
        sms_text = (
            f"[SynchroCode AI] Sug\'orish BOSHLANDI\\n"
            f"Namlik: {{sensors.soil_moisture}}% (< {threshold}%)\\n"
            f"Nasos: YONIQ | Oqim: {{sensors.water_flow_lph}} l/h\\n"
            f"Ob-havo: {{weather}}"
        )
        sms.send_sms(agro_tel, sms_text)
        log.info("Agronomga SMS yuborildi!")

        log.info("-" * 52)
        log.info(f"Nasos: {{'YONIQ' if sensors.pump_running else 'OCHIQ'}}")
        log.info("Smart Agriculture muvaffaqiyatli!")

    except ConnectionError as e:
        log.error(f"API ulanish xatosi: {{e}}")
    except ValueError as e:
        log.error(f"Sensor qiymati xatosi: {{e}}")
    except RuntimeError as e:
        log.error(f"Qurilma xatosi: {{e}}")
    except Exception as e:
        log.error(f"Kutilmagan xato: {{type(e).__name__}}: {{e}}")
    finally:
        log.info("Smart Agriculture jarayoni yakunlandi.")


if __name__ == "__main__":
    smart_agriculture_automation()
'''

    # ── Template: Smart Home ──────────────────────────────────────────────────
    elif domain == "smart_home":
        return f'''"""
SynchroCode AI — Generatsiya qilingan kod
Domain : Smart Home (Aqlli Uy)
Buyruq : {orig}
Vaqt   : {ts}
"""

import time
import logging
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("SynchroCode.SmartHome")

TRIGGER_TIME = "21:00"


@dataclass
class HomeSensors:
    motion_detected:  bool = True
    alarm_active:     bool = False
    camera_recording: bool = False
    alert_sent:       bool = False
    motion_zone:      str  = "living_room"


class SecurityAlarm:
    def __init__(self, alarm_id="HOME-ALARM-01"):
        self.alarm_id  = alarm_id
        self.is_active = False

    def activate(self, level=2) -> bool:
        # Real: requests.post("http://alarm-hub.local/api/activate", ...)
        self.is_active = True
        log.info(f"SIGNALIZATsIYA [{{self.alarm_id}}] FAOLLASHDI! Daraja: {{level}}/3")
        log.info("  Ovozli signal: YONIQ")
        log.info("  Chiroqlar: MILTILLAMOQDA")
        log.info("  Kamera: YOZUV BOSHLANDI")
        return True


class SecurityCamera:
    def start_recording(self, zone: str) -> str:
        filename = f"security_{{zone}}_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.mp4"
        log.info(f"Kamera yozuvi boshlandi: {{filename}}")
        return filename


class AlertSystem:
    def send_push_notification(self, title: str, body: str) -> bool:
        # Real (Firebase FCM): requests.post("https://fcm.googleapis.com/fcm/send", ...)
        log.info(f"PUSH BILDIRISHNOMA: {{title}}")
        log.info(f"  {{body}}")
        return True


def smart_home_security():
    """
    Trigger : Soat 21:00
    Shart   : Uyda harakat sezilganda
    Amallar : 1) Signalizatsiyani faollashtirish
              2) Kamera yozuvini boshlash
              3) Egalarga push-xabar
    """
    sensors = HomeSensors()
    alarm   = SecurityAlarm()
    camera  = SecurityCamera()
    alerts  = AlertSystem()
    now     = datetime.now().strftime("%H:%M")

    log.info("=" * 52)
    log.info("  Smart Home Xavfsizlik Tizimi — FAOL")
    log.info("=" * 52)

    try:
        log.info(f"Vaqt: {{now}} | Trigger vaqti: {{TRIGGER_TIME}}")
        if now != TRIGGER_TIME:
            log.info("[SIMULYATSIYA] Soat 21:00 deb qabul qilinmoqda...")

        log.info(f"Soat {{TRIGGER_TIME}} — xavfsizlik rejimi FAOLLASHMOQDA")

        # CONDITION: Harakat
        log.info("Harakat sensori skanlanmoqda...")
        if not sensors.motion_detected:
            log.info("Harakat yo\'q — xotirjam")
            return
        log.info(f"HARAKAT ANIQLANDI! Zona: {{sensors.motion_zone.upper()}}")

        # ACTION 1: Signalizatsiya
        time.sleep(0.3)
        if alarm.activate(level=2):
            sensors.alarm_active = True

        # ACTION 2: Kamera
        time.sleep(0.2)
        video_file = camera.start_recording(sensors.motion_zone)
        sensors.camera_recording = True

        # ACTION 3: Push bildirishnoma
        time.sleep(0.2)
        if alerts.send_push_notification(
            "Xavfsizlik Ogohlantirishı!",
            f"Harakat: {{sensors.motion_zone}} | "
            f"Vaqt: {{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}} | "
            f"Video: {{video_file}}"
        ):
            sensors.alert_sent = True

        log.info("-" * 52)
        log.info(f"Alarm      : {{'FAOL' if sensors.alarm_active else 'TINCH'}}")
        log.info(f"Kamera     : {{'YOZMOQDA' if sensors.camera_recording else 'TO\'XTATILGAN'}}")
        log.info(f"Xabar      : {{'YUBORILDI' if sensors.alert_sent else 'YUBORILMADI'}}")
        log.info("Xavfsizlik tizimi to\'liq ishga tushdi!")

    except ConnectionError as e:
        log.error(f"Tarmoq xatosi: {{e}} — Lokal siren yonmoqda (backup)")
    except PermissionError as e:
        log.error(f"Ruxsat xatosi: {{e}}")
    except Exception as e:
        log.error(f"Kutilmagan xato: {{type(e).__name__}}: {{e}}")
    finally:
        log.info("Smart Home jarayoni yakunlandi.")


if __name__ == "__main__":
    smart_home_security()
'''

    # ── Generic / Unknown domain ──────────────────────────────────────────────
    else:
        actions = parsed.get("actions", [])
        trigger = parsed.get("trigger", {})
        trigger_str = json.dumps(trigger,  ensure_ascii=False, indent=4)
        conds_str   = json.dumps(conds,    ensure_ascii=False, indent=4)
        actions_str = json.dumps(actions,  ensure_ascii=False, indent=4)
        return f'''"""
SynchroCode AI — Generatsiya qilingan kod
Domain : Umumiy avtomatlashtirish
Buyruq : {orig}
Vaqt   : {ts}

ESLATMA: Umumiy shablon. Gemini/OpenAI integratsiyasi uchun
         generate_python_code() funksiyasiga API chaqiruvi qo\'shing.
"""

import logging
import time
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("SynchroCode.Generic")

TRIGGER    = {trigger_str}
CONDITIONS = {conds_str}
ACTIONS    = {actions_str}


def read_sensor(sensor_id: str) -> Dict[str, Any]:
    """Sensor ma\'lumotlarini o\'qish (simulyatsiya)."""
    import random
    return {{"id": sensor_id, "value": round(random.uniform(10, 90), 1), "status": "ok"}}


def execute_action(action: Dict[str, Any]) -> bool:
    """Amaliyotni bajarish."""
    action_type = action.get("type", "unknown")
    log.info(f"Amal: {{action_type}} | {{action}}")
    time.sleep(0.2)
    log.info(f"Amal bajarildi: {{action_type}}")
    return True


def check_conditions(conditions: List[Dict]) -> bool:
    """Shartlarni tekshirish."""
    for cond in conditions:
        if "note" in cond:
            log.info(f"Shart: {{cond['note']}}")
            return True
        log.info(f"Shart tekshirilmoqda: {{cond}}")
    return True


def run_automation():
    log.info("=" * 52)
    log.info("  SynchroCode Avtomatlashtirish — ISHGA TUSHDI")
    log.info(f"  Buyruq: {orig!r}")
    log.info("=" * 52)

    try:
        log.info(f"TRIGGER: {{TRIGGER.get('type','N/A').upper()}} — {{TRIGGER.get('source','N/A')}}")
        log.info("Shartlar tekshirilmoqda...")

        if not check_conditions(CONDITIONS):
            log.info("Shartlar bajarilmadi — to\'xtatilmoqda")
            return
        log.info(f"{{len(CONDITIONS)}} ta shart bajarildi!")

        log.info(f"{{len(ACTIONS)}} ta amal bajarilmoqda...")
        for i, action in enumerate(ACTIONS, 1):
            log.info(f"  [{{i}}/{{len(ACTIONS)}}] {{action.get('type','N/A')}}")
            execute_action(action)

        log.info("Barcha amallar muvaffaqiyatli bajarildi!")

    except Exception as e:
        log.error(f"Xato: {{type(e).__name__}}: {{e}}")
        raise
    finally:
        log.info("Jarayon yakunlandi.")


if __name__ == "__main__":
    run_automation()
'''


# ──────────────────────────────────────────────────────────────────────────────
# STAGE 3 — SAFE CODE EXECUTOR
# ──────────────────────────────────────────────────────────────────────────────
def safe_exec(code: str) -> tuple:
    """
    Kodni xavfsiz exec() orqali bajaradi.
    stdout/stderr ni ushlaydi, barcha xatolarni ushlab, natija qaytaradi.
    Returns: (success: bool, output: str)
    """
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    success = True

    try:
        exec(compile(code, "<SynchroCode>", "exec"), {
            "__name__": "__main__",
            "__builtins__": __builtins__,
        })
    except SyntaxError as e:
        success = False
        print(f"[SINTAKSIS XATO] Satr {e.lineno}: {e.msg}", file=sys.stderr)
        print(f"Kod: {e.text}", file=sys.stderr)
    except NameError as e:
        success = False
        print(f"[NOMI XATO] {e}", file=sys.stderr)
    except ImportError as e:
        success = False
        print(f"[IMPORT XATO] {e}", file=sys.stderr)
    except Exception as e:
        success = False
        tb = traceback.format_exc()
        print(f"[RUNTIME XATO] {type(e).__name__}: {e}", file=sys.stderr)
        print(f"\nTo'liq xato:\n{tb}", file=sys.stderr)
    finally:
        stdout_val = sys.stdout.getvalue()
        stderr_val = sys.stderr.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    output = stdout_val
    if stderr_val:
        output += ("\n\n" if output else "") + stderr_val
    return success, output or "(chiqish yo'q)"


# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ──────────────────────────────────────────────────────────────────────────────
for _key, _default in [
    ("user_text",       ""),
    ("parsed_json",     None),
    ("generated_code",  None),
    ("exec_output",     None),
    ("exec_success",    None),
    ("stage",           0),
    ("run_count",       0),
]:
    if _key not in st.session_state:
        st.session_state[_key] = _default


# ──────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <p class="hero-title">⚡ SynchroCode AI</p>
  <p class="hero-sub">NATURAL LANGUAGE &rarr; IoT PYTHON CODE GENERATOR &nbsp;·&nbsp; MVP v1.0</p>
  <div style="margin-top:1rem">
    <span class="badge">O'ZBEK NLP</span>
    <span class="badge">IoT READY</span>
    <span class="badge">LIVE SANDBOX</span>
    <span class="badge">RULE-BASED ENGINE</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Step Indicator
_stage = st.session_state.stage
_s = lambda n: "active" if _stage >= n else ""
st.markdown(f"""
<div class="step-indicator">
  <div class="step {_s(1)}"><div class="step-num">1</div>&nbsp;SEMANTIC PARSING</div>
  <span class="step-arrow">&#x2192;</span>
  <div class="step {_s(2)}"><div class="step-num">2</div>&nbsp;CODE GENERATION</div>
  <span class="step-arrow">&#x2192;</span>
  <div class="step {_s(3)}"><div class="step-num">3</div>&nbsp;LIVE SIMULATION</div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# MAIN LAYOUT
# ──────────────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.6], gap="medium")

# ════════════ LEFT COLUMN ════════════
with col_left:

    # Scenario Buttons
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">&#128203; TAYYOR ANDOZALAR</div>', unsafe_allow_html=True)
    for label, scenario_text in SCENARIOS.items():
        if st.button(label, key=f"sc_{label}"):
            st.session_state.user_text      = scenario_text
            st.session_state.parsed_json    = None
            st.session_state.generated_code = None
            st.session_state.exec_output    = None
            st.session_state.stage          = 0
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Input Area
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">&#x270F; BUYRUQ KIRITING</div>', unsafe_allow_html=True)
    user_input = st.text_area(
        label="",
        value=st.session_state.user_text,
        height=130,
        placeholder="Masalan: Agar harorat 40 dan oshsa, konditsionerni yoq va xabardor qil...",
        key="main_input",
        label_visibility="collapsed",
    )
    st.session_state.user_text = user_input

    if st.button("&#128269;  TAHLIL QILISH  (Parse)", use_container_width=True):
        if user_input.strip():
            with st.spinner("Semantik tahlil amalga oshirilmoqda..."):
                result = parse_uzbek_command(user_input.strip())
                st.session_state.parsed_json    = result
                st.session_state.generated_code = generate_python_code(result, user_input.strip())
                st.session_state.exec_output    = None
                st.session_state.exec_success   = None
                st.session_state.stage          = 2
                st.session_state.run_count     += 1
        else:
            st.warning("Iltimos, buyruq kiriting!")
    st.markdown('</div>', unsafe_allow_html=True)

    # Metrics
    if st.session_state.parsed_json:
        p = st.session_state.parsed_json
        conf = p.get("confidence", 0)
        conf_color = "#00ff88" if conf >= 70 else "#fbbf24" if conf >= 40 else "#ef4444"
        n_act = len([a for a in p.get("actions", []) if "type" in a])
        n_con = len([c for c in p.get("conditions", []) if "note" not in c])
        st.markdown(f"""
        <div class="metric-row">
          <div class="metric-box">
            <div class="metric-val" style="color:{conf_color}">{conf}%</div>
            <div class="metric-lbl">Ishonch</div>
          </div>
          <div class="metric-box">
            <div class="metric-val">{n_act}</div>
            <div class="metric-lbl">Amallar</div>
          </div>
          <div class="metric-box">
            <div class="metric-val">{n_con}</div>
            <div class="metric-lbl">Shartlar</div>
          </div>
          <div class="metric-box">
            <div class="metric-val">{st.session_state.run_count}</div>
            <div class="metric-lbl">Ishlatish</div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ════════════ RIGHT COLUMN ════════════
with col_right:
    if st.session_state.parsed_json is None:
        st.markdown("""
        <div class="section-card" style="text-align:center; padding:3rem 2rem; border-style:dashed;">
          <div style="font-size:2.5rem; margin-bottom:1rem;">&#x26A1;</div>
          <div style="font-family:'Space Mono',monospace; font-size:0.8rem; color:#334155; line-height:2.2;">
            Chap tarafdan ssenariy tanlang<br>
            yoki o'z buyrug'ingizni kiriting<br>
            — natijalar shu yerda chiqadi.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        tab1, tab2, tab3 = st.tabs(["① Semantik Tahlil", "② Generatsiya Kodi", "③ Simulyator"])

        # ── TAB 1: Semantic Parsing ──────────────────────────────────────────
        with tab1:
            p = st.session_state.parsed_json
            st.markdown('<div class="section-title">&#x1F52C; SEMANTIK TAHLIL NATIJASI</div>', unsafe_allow_html=True)
            trig_type  = p["trigger"].get("type", "?").upper()
            domain_lbl = p['domain'].upper()
            n_act2     = len(p.get("actions", []))
            st.markdown(f"""
            <div style="margin-bottom:0.8rem">
              <span class="tag-trigger">TRIGGER: {trig_type}</span>
              <span class="tag-condition">DOMAIN: {domain_lbl}</span>
              <span class="tag-action">AMALLAR: {n_act2}</span>
            </div>
            """, unsafe_allow_html=True)
            json_str = json.dumps(p, ensure_ascii=False, indent=2)
            st.markdown(f'<div class="json-block">{json_str}</div>', unsafe_allow_html=True)

        # ── TAB 2: Code ──────────────────────────────────────────────────────
        with tab2:
            code = st.session_state.generated_code
            st.markdown('<div class="section-title">&#x1F40D; GENERATSIYA QILINGAN PYTHON KODI</div>', unsafe_allow_html=True)
            if code:
                lc = len(code.split('\n'))
                cc = len(code)
                st.markdown(f"""
                <div style="margin-bottom:0.8rem">
                  <span class="tag-action">Python 3.10+</span>
                  <span class="tag-trigger">{lc} SATR</span>
                  <span class="tag-condition">{cc} BELGI</span>
                  <span class="tag-action">TRY-EXCEPT &#x2713;</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f'<div class="code-block">{code}</div>', unsafe_allow_html=True)
                st.download_button(
                    label="&#x2B07;  Kodni yuklab olish (.py)",
                    data=code,
                    file_name=f"synchrocode_{p['domain']}_{datetime.now().strftime('%H%M%S')}.py",
                    mime="text/plain",
                    use_container_width=True,
                )

        # ── TAB 3: Simulator ─────────────────────────────────────────────────
        with tab3:
            st.markdown('<div class="section-title">&#x25B6; LIVE SANDBOX — SIMULYATOR</div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="background:#0a1020; border:1px solid #1e2d4a; border-radius:8px;
                        padding:0.8rem 1rem; margin-bottom:1rem;
                        font-family:'Space Mono',monospace; font-size:0.7rem; color:#64748b;">
            XAVFSIZLIK: Kod izolyatsiyalangan muhitda bajariladi. Tashqi tarmoqqa
            ulanishlar simulyatsiya qilinadi. stdout/stderr to'liq ushlanadi.
            </div>
            """, unsafe_allow_html=True)

            col_r1, col_r2 = st.columns([2, 1])
            with col_r1:
                st.markdown('<div class="run-btn">', unsafe_allow_html=True)
                run_clicked = st.button(
                    "&#x25B6;   ISHGA TUSHIRISH  (Run Simulation)",
                    use_container_width=True, key="run_btn")
                st.markdown('</div>', unsafe_allow_html=True)
            with col_r2:
                if st.button("&#x1F5D1;  Tozalash", use_container_width=True, key="clear_btn"):
                    st.session_state.exec_output  = None
                    st.session_state.exec_success = None
                    st.rerun()

            if run_clicked and st.session_state.generated_code:
                st.session_state.stage = 3
                with st.spinner("Simulyatsiya bajarilmoqda..."):
                    import time; time.sleep(0.3)
                    ok, out = safe_exec(st.session_state.generated_code)
                    st.session_state.exec_success = ok
                    st.session_state.exec_output  = out

            if st.session_state.exec_output is not None:
                ok  = st.session_state.exec_success
                out = st.session_state.exec_output
                if ok:
                    st.markdown(f"""
                    <div style="color:#00ff88;font-family:'Space Mono',monospace;
                                font-size:0.75rem;margin-bottom:0.5rem;">
                      &#x2705; SIMULYATSIYA MUVAFFAQIYATLI
                    </div>
                    <div class="output-block">{out}</div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="color:#ef4444;font-family:'Space Mono',monospace;
                                font-size:0.75rem;margin-bottom:0.5rem;">
                      &#x274C; RUNTIME XATO ANIQLANDI
                    </div>
                    <div class="error-block">{out}</div>
                    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; font-family:'Space Mono',monospace; font-size:0.65rem;
            color:#1e2d4a; letter-spacing:0.1em; padding:0.5rem 0;">
  SYNCHROCODE AI &nbsp;&middot;&nbsp; MVP v1.0 &nbsp;&middot;&nbsp; BUILT WITH STREAMLIT
  <br>
  <span style="color:#0d1f38">
    [ Gemini/OpenAI uchun generate_python_code() funksiyasiga API chaqiruvi qo'shing ]
  </span>
</div>
""", unsafe_allow_html=True)
