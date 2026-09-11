
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import random
from datetime import datetime
from groq import Groq


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Astronaut Mission Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GROQ
# ============================================================

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    MODEL = "openai/gpt-oss-120b"
except Exception:
    client = None
    MODEL = "openai/gpt-oss-120b"


# ============================================================
# SESSION STATE
# ============================================================

if "mission_mode" not in st.session_state:
    st.session_state.mission_mode = "Normal Mission"

if "mission_day" not in st.session_state:
    st.session_state.mission_day = 42

if "rover_progress" not in st.session_state:
    st.session_state.rover_progress = 0.0

if "logs" not in st.session_state:
    st.session_state.logs = []

if "analysis" not in st.session_state:
    st.session_state.analysis = ""

if "plan" not in st.session_state:
    st.session_state.plan = ""

if "telemetry" not in st.session_state:
    st.session_state.telemetry = {
        "battery": 82,
        "oxygen": 91,
        "temperature": 67,
        "radiation": 12,
        "communication": 89,
        "fuel": 73,
        "speed": 2.4
    }

if "selected_mission" not in st.session_state:
    st.session_state["selected_mission"] = "MARS-01 — Mars Exploration"


# ============================================================
# MISSION LOG
# ============================================================

def log_event(message):

    timestamp = datetime.now().strftime("%H:%M:%S")

    st.session_state.logs.insert(
        0,
        f"{timestamp} — {message}"
    )

    st.session_state.logs = st.session_state.logs[:20]


# ============================================================
# TELEMETRY
# ============================================================

def normal_mission():

    return {
        "battery": 82,
        "oxygen": 91,
        "temperature": 67,
        "radiation": 12,
        "communication": 89,
        "fuel": 73,
        "speed": 2.4
    }


def thermal_emergency():

    return {
        "battery": 32,
        "oxygen": 74,
        "temperature": 96,
        "radiation": 18,
        "communication": 71,
        "fuel": 61,
        "speed": 0.0
    }


def solar_storm():

    return {
        "battery": 34,
        "oxygen": 78,
        "temperature": 88,
        "radiation": 92,
        "communication": 27,
        "fuel": 61,
        "speed": 1.2
    }


def oxygen_emergency():

    return {
        "battery": 63,
        "oxygen": 27,
        "temperature": 68,
        "radiation": 20,
        "communication": 82,
        "fuel": 59,
        "speed": 0.0
    }


def communication_failure():

    return {
        "battery": 71,
        "oxygen": 81,
        "temperature": 69,
        "radiation": 14,
        "communication": 12,
        "fuel": 68,
        "speed": 2.1
    }

def get_mission_config(mission):

    if mission.startswith("MARS-01"):
        return {
            "planet": "Mars",
            "objective": "Mars Surface Exploration",
            "rover": True,
            "orbiter": True
        }

    elif mission.startswith("ORBIT-02"):
        return {
            "planet": "Mars",
            "objective": "Orbital Survey",
            "rover": False,
            "orbiter": True
        }

    elif mission.startswith("ROVER-03"):
        return {
            "planet": "Mars",
            "objective": "Autonomous Rover Exploration",
            "rover": True,
            "orbiter": True
        }

    elif mission.startswith("SCIENCE-04"):
        return {
            "planet": "Mars",
            "objective": "Deep Space Science",
            "rover": False,
            "orbiter": True
        }

    return {
        "planet": "Mars",
        "objective": "Mars Exploration",
        "rover": True,
        "orbiter": True
    }



# ============================================================
# ANOMALY DETECTION
# ============================================================

def detect_anomalies(data):

    anomalies = []

    if data["battery"] < 40:
        anomalies.append("Critical battery level")

    if data["oxygen"] < 50:
        anomalies.append("Low oxygen level")

    if data["temperature"] > 85:
        anomalies.append("High temperature")

    if data["radiation"] > 70:
        anomalies.append("High radiation")

    if data["communication"] < 40:
        anomalies.append("Weak communication")

    if data["fuel"] < 30:
        anomalies.append("Low fuel")

    return anomalies


# ============================================================
# AI
# ============================================================

def ask_ai(prompt):

    if client is None:
        return "AI connection unavailable."

    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "system",

                    "content": """
You are AI Astronaut.

You are an autonomous mission-support AI
operating inside a simulated Mars mission.

Responsibilities:

- Monitor telemetry
- Detect anomalies
- Assess risk
- Explain problems
- Recommend safe actions
- Create emergency plans
- Support astronauts
- Protect mission objectives

This is a simulation.

Never claim to control real spacecraft.

Give concise, structured and logical responses.
"""
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"AI error: {str(e)}"


# ============================================================
# 3D MARS
# ============================================================

def create_mars():

    # Mars sphere

    phi = np.linspace(0, np.pi, 70)

    theta = np.linspace(
        0,
        2 * np.pi,
        100
    )

    x = np.outer(
        np.sin(phi),
        np.cos(theta)
    )

    y = np.outer(
        np.sin(phi),
        np.sin(theta)
    )

    z = np.outer(
        np.cos(phi),
        np.ones_like(theta)
    )

    # Surface variations

    noise = (
        1
        + 0.04 * np.sin(5 * theta)[None, :]
        + 0.025 * np.cos(7 * phi)[:, None]
    )

    x = x * noise
    y = y * noise
    z = z * noise

    fig = go.Figure()

    # Mars

    fig.add_trace(

        go.Surface(

            x=x,
            y=y,
            z=z,

            surfacecolor=z,

            colorscale=[
                [0.0, "#3b0808"],
                [0.25, "#6e1515"],
                [0.5, "#9e2f20"],
                [0.75, "#c65b3c"],
                [1.0, "#e28a62"]
            ],

            showscale=False,

            lighting=dict(
                ambient=0.45,
                diffuse=0.8,
                specular=0.25,
                roughness=0.8
            ),

            lightposition=dict(
                x=5,
                y=3,
                z=5
            ),

            name="Mars"
        )
    )

    # Landing location

    landing_x = 0.45
    landing_y = 0.15
    landing_z = 0.90

    fig.add_trace(

        go.Scatter3d(

            x=[landing_x],
            y=[landing_y],
            z=[landing_z],

            mode="markers+text",

            marker=dict(
                size=8,
                color="yellow",
                symbol="diamond"
            ),

            text=["AI BASE"],
            textposition="top center",

            name="AI Base"
        )
    )

    # Rover path

    t = np.linspace(
        0,
        2 * np.pi,
        120
    )

    path_x = 0.45 + 0.35 * np.cos(t)
    path_y = 0.15 + 0.30 * np.sin(t)
    path_z = np.sqrt(
        np.maximum(
            0.01,
            1 - path_x**2 - path_y**2
        )
    )

    fig.add_trace(

        go.Scatter3d(

            x=path_x,
            y=path_y,
            z=path_z,

            mode="lines",

            line=dict(
                width=5,
                color="cyan"
            ),

            name="Mission Route"
        )
    )

    # Rover current position

    progress = st.session_state.rover_progress

    idx = int(
        progress * (len(path_x) - 1)
    )

    idx = min(
        idx,
        len(path_x) - 1
    )

    rover_x = path_x[idx]
    rover_y = path_y[idx]
    rover_z = path_z[idx]

    # Rover

    fig.add_trace(

        go.Scatter3d(

            x=[rover_x],
            y=[rover_y],
            z=[rover_z],

            mode="markers+text",

            marker=dict(
                size=10,
                color="white",
                symbol="square"
            ),

            text=["🤖 ROVER"],
            textposition="top center",

            name="AI Rover"
        )
    )

    # Rover trail

    if idx > 1:

        fig.add_trace(

            go.Scatter3d(

                x=path_x[:idx],
                y=path_y[:idx],
                z=path_z[:idx],

                mode="lines",

                line=dict(
                    width=8,
                    color="white"
                ),

                name="Rover Trail"
            )
        )

    # ========================================================
    # ORBITER
    # ========================================================

    orbit_t = np.linspace(
        0,
        2 * np.pi,
        200
    )

    orbit_x = 1.7 * np.cos(orbit_t)
    orbit_y = 1.15 * np.sin(orbit_t)
    orbit_z = 0.55 * np.sin(orbit_t)

    fig.add_trace(

        go.Scatter3d(

            x=orbit_x,
            y=orbit_y,
            z=orbit_z,

            mode="lines",

            line=dict(
                width=3,
                color="magenta"
            ),

            name="Orbiter Orbit"
        )
    )

    # Orbiter

    orbit_idx = int(
        st.session_state.mission_day % 200
    )

    fig.add_trace(

        go.Scatter3d(

            x=[orbit_x[orbit_idx]],
            y=[orbit_y[orbit_idx]],
            z=[orbit_z[orbit_idx]],

            mode="markers+text",

            marker=dict(
                size=8,
                color="cyan"
            ),

            text=["🛰️ ORBITER"],

            name="Orbiter"
        )
    )

    # ========================================================
    # COMMUNICATION SIGNAL
    # ========================================================

    signal_x = [
        rover_x,
        0,
        0
    ]

    signal_y = [
        rover_y,
        0,
        0
    ]

    signal_z = [
        rover_z,
        0,
        2.7
    ]

    fig.add_trace(

        go.Scatter3d(

            x=signal_x,
            y=signal_y,
            z=signal_z,

            mode="lines",

            line=dict(
                width=3,
                color="lime"
            ),

            name="Communication Link"
        )
    )

    # ========================================================
    # SATELLITE
    # ========================================================

    fig.add_trace(

        go.Scatter3d(

            x=[0],
            y=[0],
            z=[2.7],

            mode="markers+text",

            marker=dict(
                size=9,
                color="orange"
            ),

            text=["📡 DEEP SPACE RELAY"],

            textposition="top center",

            name="Deep Space Relay"
        )
    )

    # ========================================================
    # STAR FIELD
    # ========================================================

    np.random.seed(42)

    stars_x = np.random.uniform(
        -3,
        3,
        100
    )

    stars_y = np.random.uniform(
        -3,
        3,
        100
    )

    stars_z = np.random.uniform(
        -3,
        3,
        100
    )

    fig.add_trace(

        go.Scatter3d(

            x=stars_x,
            y=stars_y,
            z=stars_z,

            mode="markers",

            marker=dict(
                size=1.5,
                color="white"
            ),

            name="Stars",

            hoverinfo="skip"
        )
    )

    # ========================================================
    # CAMERA / LAYOUT
    # ========================================================

    mission_name = st.session_state.get(
        "selected_mission",
        "MARS-01 — Mars Exploration"
    )

    fig.update_layout(

        title={
            "text": f"🚀 AI ASTRONAUT — {mission_name}",
            "x": 0.5
        },

        scene=dict(

            xaxis=dict(
                visible=False
            ),

            yaxis=dict(
                visible=False
            ),

            zaxis=dict(
                visible=False
            ),

            bgcolor="black",

            aspectmode="cube",

            camera=dict(
                eye=dict(
                    x=1.35,
                    y=1.35,
                    z=0.9
                )
            )
        ),

        paper_bgcolor="black",

        font=dict(
            color="white"
        ),

        height=700,

        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0.5)"
        )
    )

    return fig


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚀 AI ASTRONAUT")

st.sidebar.caption(
    "Autonomous Mission Support System"
)

st.sidebar.divider()

st.sidebar.subheader("🛰️ Select Mission")

mission_options = [
    "MARS-01 — Mars Exploration",
    "ORBIT-02 — Mars Orbital Survey",
    "ROVER-03 — Autonomous Rover",
    "SCIENCE-04 — Deep Space Science"
]

selected_mission = st.sidebar.selectbox(
    "Active Mission",
    mission_options
)

st.session_state["selected_mission"] = selected_mission

st.sidebar.divider()

st.sidebar.subheader("Mission Control")

if st.sidebar.button(
    "🟢 Normal Mission",
    use_container_width=True
):

    st.session_state.mission_mode = "Normal Mission"

    st.session_state.telemetry = normal_mission()

    log_event(
        "Mission returned to nominal conditions"
    )

    st.rerun()


if st.sidebar.button(
    "🔥 Thermal Failure",
    use_container_width=True
):

    st.session_state.mission_mode = "Thermal Emergency"

    st.session_state.telemetry = thermal_emergency()

    log_event(
        "THERMAL FAILURE detected"
    )

    st.rerun()


if st.sidebar.button(
    "☀️ Solar Storm",
    use_container_width=True
):

    st.session_state.mission_mode = "Solar Storm"

    st.session_state.telemetry = solar_storm()

    log_event(
        "SOLAR STORM detected"
    )

    st.rerun()


if st.sidebar.button(
    "🫁 Oxygen Leak",
    use_container_width=True
):

    st.session_state.mission_mode = "Oxygen Emergency"

    st.session_state.telemetry = oxygen_emergency()

    log_event(
        "OXYGEN LEAK detected"
    )

    st.rerun()


if st.sidebar.button(
    "📡 Communication Failure",
    use_container_width=True
):

    st.session_state.mission_mode = "Communication Failure"

    st.session_state.telemetry = communication_failure()

    log_event(
        "COMMUNICATION FAILURE detected"
    )

    st.rerun()


st.sidebar.divider()

st.sidebar.subheader("Mission Day")

mission_day = st.sidebar.slider(
    "Mission Day",
    1,
    500,
    st.session_state.mission_day
)

st.session_state.mission_day = mission_day


# ============================================================
# HEADER
# ============================================================

st.title(
    "🚀 AI ASTRONAUT"
)

st.caption(
    "Autonomous AI Mission Control • Mars Exploration Digital Twin"
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "MISSION",
        st.session_state.get(
            "selected_mission",
            "MARS-01"
        ).split(" — ")[0]
    )

with col2:

    st.metric(
        "MISSION DAY",
        st.session_state.mission_day
    )

with col3:

    st.metric(
        "MODE",
        st.session_state.mission_mode
    )

with col4:

    anomalies = detect_anomalies(
        st.session_state.telemetry
    )

    if anomalies:
        st.metric(
            "ALERTS",
            len(anomalies)
        )
    else:
        st.metric(
            "ALERTS",
            "0"
        )

st.divider()

mission_config = get_mission_config(
    st.session_state.get(
        "selected_mission",
        "MARS-01 — Mars Exploration"
    )
)

st.info(
    f"🎯 Mission Objective: {mission_config['objective']}"
)



# ============================================================
# 3D DIGITAL TWIN
# ============================================================

st.subheader(
    "🌌 Mission Digital Twin"
)

fig = create_mars()

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displaylogo": False,
        "scrollZoom": True
    }
)


# ============================================================
# ROVER CONTROL
# ============================================================

st.subheader(
    "🤖 Rover Control"
)

r1, r2, r3 = st.columns(3)

with r1:

    if st.button(
        "⬅️ Move Rover",
        use_container_width=True
    ):

        st.session_state.rover_progress -= 0.05

        st.session_state.rover_progress = max(
            0,
            st.session_state.rover_progress
        )

        log_event(
            "Rover moved to previous waypoint"
        )

        st.rerun()


with r2:

    if st.button(
        "🚀 Advance Rover",
        use_container_width=True
    ):

        st.session_state.rover_progress += 0.05

        st.session_state.rover_progress = min(
            1,
            st.session_state.rover_progress
        )

        log_event(
            "Rover advanced to next waypoint"
        )

        st.rerun()


with r3:

    if st.button(
        "🏠 Return to Base",
        use_container_width=True
    ):

        st.session_state.rover_progress = 0

        log_event(
            "Rover returning to AI Base"
        )

        st.rerun()


# ============================================================
# TELEMETRY
# ============================================================

st.subheader(
    "📡 Live Telemetry"
)

data = st.session_state.telemetry

t1, t2, t3, t4, t5, t6, t7 = st.columns(7)

with t1:
    st.metric(
        "🔋 Battery",
        f"{data['battery']}%"
    )

with t2:
    st.metric(
        "🫁 Oxygen",
        f"{data['oxygen']}%"
    )

with t3:
    st.metric(
        "🌡️ Temperature",
        f"{data['temperature']}°C"
    )

with t4:
    st.metric(
        "☢️ Radiation",
        f"{data['radiation']}%"
    )

with t5:
    st.metric(
        "📡 Communication",
        f"{data['communication']}%"
    )

with t6:
    st.metric(
        "⛽ Fuel",
        f"{data['fuel']}%"
    )

with t7:
    st.metric(
        "🚀 Speed",
        f"{data['speed']} km/s"
    )


# ============================================================
# MISSION STATUS
# ============================================================

anomalies = detect_anomalies(data)

if data["temperature"] > 90 or data["oxygen"] < 30:

    status = "🔴 CRITICAL"

elif anomalies:

    status = "🟠 HIGH RISK"

else:

    status = "🟢 OPERATIONAL"


st.subheader(
    f"Mission Status: {status}"
)


if anomalies:

    st.warning(
        "Detected anomalies: "
        + " | ".join(anomalies)
    )

else:

    st.success(
        "All primary mission systems are within nominal limits."
    )


# ============================================================
# AI ANALYSIS
# ============================================================

st.subheader(
    "🧠 AI Astronaut Brain"
)

a1, a2 = st.columns(2)

with a1:

    if st.button(
        "🧠 Analyze Mission",
        use_container_width=True
    ):

        telemetry_text = "\n".join(
            f"{k}: {v}"
            for k, v in data.items()
        )

        anomaly_text = (
            "\n".join(anomalies)
            if anomalies
            else "None"
        )

        prompt = f"""

Analyze the following simulated Mars mission.

Mission Day:
{mission_day}

Mission Mode:
{st.session_state.mission_mode}

Telemetry:
{telemetry_text}

Anomalies:
{anomaly_text}

Return:

MISSION STATUS:
RISK LEVEL:
PRIMARY THREAT:
PROBABLE CAUSE:

RECOMMENDED ACTIONS:
1.
2.
3.
4.

MISSION IMPACT:

FINAL DECISION:
Continue / Pause / Return to Base

"""

        st.session_state.analysis = ask_ai(
            prompt
        )

        log_event(
            "AI completed mission analysis"
        )


with a2:

    if st.button(
        "🚨 Generate Emergency Plan",
        use_container_width=True
    ):

        telemetry_text = "\n".join(
            f"{k}: {v}"
            for k, v in data.items()
        )

        anomaly_text = (
            "\n".join(anomalies)
            if anomalies
            else "None"
        )

        prompt = f"""

Create an emergency response plan
for this simulated Mars mission.

Mission:
{st.session_state.mission_mode}

Telemetry:
{telemetry_text}

Anomalies:
{anomaly_text}

Create:

PRIORITY:
RISK:

IMMEDIATE ACTIONS:
1.
2.
3.
4.

RESOURCE MANAGEMENT:

EXPECTED RESULT:

MISSION DECISION:

"""

        st.session_state.plan = ask_ai(
            prompt
        )

        log_event(
            "AI generated emergency response plan"
        )


if st.session_state.analysis:

    st.markdown(
        "### 🧠 Mission Analysis"
    )

    st.info(
        st.session_state.analysis
    )


if st.session_state.plan:

    st.markdown(
        "### 🚨 AI Emergency Response Plan"
    )

    st.warning(
        st.session_state.plan
    )


# ============================================================
# SIMULATED AUTONOMOUS EXECUTION
# ============================================================

st.subheader(
    "⚙️ Autonomous Simulation"
)

if st.button(
    "▶️ Execute AI Plan",
    use_container_width=True
):

    mode = st.session_state.mission_mode

    if mode == "Thermal Emergency":

        data["temperature"] = 74
        data["battery"] = 38
        data["communication"] = 78

    elif mode == "Solar Storm":

        data["radiation"] = 45
        data["communication"] = 61
        data["battery"] = 41

    elif mode == "Oxygen Emergency":

        data["oxygen"] = 48

    elif mode == "Communication Failure":

        data["communication"] = 68

    st.session_state.telemetry = data

    log_event(
        "AI emergency plan simulated successfully"
    )

    st.success(
        "Simulated recovery sequence completed."
    )

    st.rerun()


# ============================================================
# MISSION LOG
# ============================================================

st.subheader(
    "📋 Mission Event Log"
)

if st.session_state.logs:

    for event in st.session_state.logs:

        st.write(
            "• " + event
        )

else:

    st.write(
        "No mission events recorded."
    )


# ============================================================
# AI CHAT
# ============================================================

st.subheader(
    "💬 Communicate with AI Astronaut"
)

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


for message in st.session_state.chat_history:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


question = st.chat_input(
    "Ask AI Astronaut about the mission..."
)


if question:

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    context = f"""

Current Mars Mission:

Mission Day:
{mission_day}

Mode:
{st.session_state.mission_mode}

Telemetry:
{data}

Anomalies:
{anomalies}

Astronaut Question:
{question}

Answer as AI Astronaut.
"""

    answer = ask_ai(context)

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI ASTRONAUT • Mars Mission Simulation • "
    "AI decisions and spacecraft operations are simulated."
)
