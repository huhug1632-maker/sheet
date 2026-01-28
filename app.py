from nicegui import ui
import pandas as pd
import webbrowser

# ================== Google Sheet ==================
SHEET_ID = "1WQWL2aRzD5lvqVgUzXNi_B2poEV8YCUBOd60sRnfy1Q"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"

def load_data():
    return pd.read_csv(CSV_URL).fillna("")

data = load_data()

# ================== HEADER ==================
with ui.element("div").classes(
    "w-full bg-gradient-to-r from-slate-100 to-slate-200 py-12 mb-10 rounded-b-3xl shadow"
):
    ui.label("منصة متابعة أوامر الشراء").classes(
        "text-5xl font-bold italic text-center tracking-wide"
    )
    ui.label("Procurement • Tracking • Smart Workflow Control").classes(
        "text-center text-gray-600 mt-3 italic text-base tracking-wider"
    )

# ================== SEARCH ==================
with ui.row().classes("w-full gap-3 mb-8 px-6"):
    search_input = ui.input(
        placeholder="بحث بالعنوان أو رقم الطلب"
    ).classes("flex-1 italic text-lg")

    ui.button(
        "بحث",
        on_click=lambda: render_cards(search_input.value),
    ).props("color=primary").classes("italic")

    ui.button(
        "مسح",
        on_click=lambda: (
            search_input.set_value(""),
            render_cards("")
        ),
    ).props("outline").classes("italic")

cards_container = ui.column().classes("w-full gap-8 px-6")

# ================== STAGES ==================
def get_stages(row):
    stages = []
    for i in range(1, 8):
        name = row.get(f"stage_{i}_name", "")
        date = row.get(f"stage_{i}_date", "")
        if name:
            stages.append({"name": name, "date": date})
    return stages

# ================== CURRENT STAGE ==================
def get_current_stage(stages):
    if not stages:
        return ""

    if all(stage["date"] == "" for stage in stages):
        return stages[0]["name"]

    for i, stage in enumerate(stages):
        if stage["date"] == "":
            if i == 0 or stages[i - 1]["date"] != "":
                return stage["name"]

    return stages[-1]["name"]

# ================== STAGE BOX ==================
def stage_box(name, date, is_current):
    if date:
        color = "bg-emerald-100 text-emerald-800"
        subtitle = date
        icon = "✔"

    elif is_current:
        color = "bg-red-100 text-red-800 scale-105"
        subtitle = "قيد التنفيذ"
        icon = "➤"

    else:
        color = "bg-gray-100 text-gray-500"
        subtitle = "بانتظار التنفيذ"
        icon = "○"

    with ui.card().classes(
        f"p-4 w-48 text-center rounded-2xl shadow-sm transition {color}"
    ):
        ui.label(f"{icon} {name}").classes(
            "font-semibold italic text-sm"
        )
        ui.label(subtitle).classes(
            "text-xs italic mt-2"
        )

# ================== OPEN SHEET ==================
def open_sheet():
    webbrowser.open_new_tab(SHEET_URL)

# ================== CARDS ==================
def render_cards(keyword=""):
    cards_container.clear()
    keyword = keyword.lower().strip()

    for _, row in data.iterrows():

        if not row["title"] or not row["order_no"]:
            continue

        searchable = f"{row['title']} {row['order_no']}".lower()
        if keyword and keyword not in searchable:
            continue

        stages = get_stages(row)
        current_stage = get_current_stage(stages)

        with cards_container:
            with ui.card().classes(
                "w-full p-8 rounded-3xl shadow-md hover:shadow-xl transition"
            ):
                with ui.row().classes("justify-between items-start mb-4"):
                    with ui.column():
                        ui.label(row["title"]).classes(
                            "text-2xl font-bold italic"
                        )
                        ui.label(
                            f"القسم: {row['department']}"
                        ).classes("italic text-gray-600")
                        ui.label(
                            f"رقم الطلب: {row['order_no']}"
                        ).classes("italic text-gray-600")

                    with ui.column().classes("items-end"):
                        ui.label(f"➤ {current_stage}").classes(
                            "italic text-red-700 font-semibold text-lg"
                        )
                        ui.button(
                            "✏️ تعديل الطلبية",
                            on_click=open_sheet
                        ).classes(
                            "mt-2 italic text-sm"
                        ).props("outline")

                ui.separator().classes("my-6")

                with ui.row().classes("gap-4 flex-wrap"):
                    for stage in stages:
                        stage_box(
                            stage["name"],
                            stage["date"],
                            stage["name"] == current_stage,
                        )

# ================== INIT ==================
render_cards()
ui.run(host="0.0.0.0", port=8080)


