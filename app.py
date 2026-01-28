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

# ================== GLOBAL STYLE ==================
ui.add_head_html("""
<style>
* {
    font-family: "Times New Roman", serif;
    font-style: italic;
}
</style>
""")

# ================== HEADER ==================
with ui.element("div").classes(
    "w-full bg-gradient-to-b from-slate-800 to-slate-900 text-white "
    "py-10 mb-10 rounded-b-3xl shadow flex flex-col items-center text-center"
):
    ui.label("نظام متابعة الطلبيات").classes(
        "text-4xl font-bold mb-2"
    )
    ui.label("متابعة • تنظيم • سيطرة").classes(
        "text-sm text-gray-300"
    )

# ================== SEARCH ==================
with ui.column().classes("w-full max-w-xl mx-auto px-4 mb-10 items-center"):
    search_input = ui.input(
        placeholder="🔍 بحث بعنوان الطلب أو رقم الطلب"
    ).classes("w-full text-center text-lg")

    with ui.row().classes("gap-4 mt-4 justify-center"):
        ui.button(
            "بحث",
            on_click=lambda: render_cards(search_input.value)
        ).props("color=primary")

        ui.button(
            "مسح",
            on_click=lambda: (
                search_input.set_value(""),
                render_cards("")
            )
        ).props("outline")

cards_container = ui.column().classes(
    "w-full max-w-xl mx-auto px-4 gap-10 items-center"
)

# ================== STAGES ==================
def get_stages(row):
    stages = []
    for i in range(1, 8):
        name = row.get(f"stage_{i}_name", "")
        date = row.get(f"stage_{i}_date", "")
        if name:
            stages.append({"name": name, "date": date})
    return stages

def get_current_stage(stages):
    for stage in stages:
        if stage["date"] == "":
            return stage["name"]
    return stages[-1]["name"] if stages else ""

# ================== STAGE BOX ==================
def stage_box(name, date, is_current):
    if date:
        color = "bg-emerald-100 text-emerald-800"
        subtitle = date
        icon = "✔"
    elif is_current:
        color = "bg-red-100 text-red-800"
        subtitle = "قيد التنفيذ"
        icon = "➤"
    else:
        color = "bg-gray-100 text-gray-500"
        subtitle = "بانتظار التنفيذ"
        icon = "○"

    with ui.card().classes(
        f"""
        w-full
        rounded-2xl
        shadow
        p-6
        flex flex-col
        items-center
        justify-center
        text-center
        {color}
        """
    ):
        ui.label(f"{icon} {name}").classes(
            "font-bold text-lg"
        )
        ui.label(subtitle).classes(
            "text-sm mt-2"
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
                "w-full bg-white rounded-3xl shadow-xl p-6 "
                "flex flex-col items-center text-center"
            ):
                # ===== INFO =====
                ui.label(row["title"]).classes(
                    "text-2xl font-bold mb-2"
                )
                ui.label(f"القسم: {row['department']}").classes(
                    "text-gray-600"
                )
                ui.label(f"رقم الطلب: {row['order_no']}").classes(
                    "text-gray-600 mb-4"
                )

                ui.label(f"الحالة الحالية: {current_stage}").classes(
                    "text-red-700 font-semibold mb-6"
                )

                ui.button(
                    "✏️ تعديل الطلبية",
                    on_click=open_sheet
                ).classes(
                    "w-full max-w-sm mb-8"
                ).props("outline")

                # ===== STAGES =====
                with ui.column().classes(
                    "w-full gap-4 items-center"
                ):
                    for stage in stages:
                        stage_box(
                            stage["name"],
                            stage["date"],
                            stage["name"] == current_stage,
                        )

# ================== INIT ==================
render_cards()
ui.run()
