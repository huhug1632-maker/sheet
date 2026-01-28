from nicegui import ui
import pandas as pd

# ================== Google Sheet ==================
SHEET_ID = "1WQWL2aRzD5lvqVgUzXNi_B2poEV8YCUBOd60sRnfy1Q"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
BASE_SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit#gid=0"

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
body {
  text-align: center;
}
</style>
""")

# ================== HEADER ==================
with ui.element("div").classes(
    "w-full max-w-4xl mx-auto bg-gray-900 text-white rounded-3xl p-8 mt-6 shadow-lg text-center"
):
    ui.label("نظام متابعة الطلبيات").classes(
        "text-4xl font-bold mb-2"
    )
    ui.label("متابعة • تنظيم • سيطرة").classes(
        "text-gray-300 mb-6"
    )

    search_input = ui.input(
        placeholder="بحث بالعنوان أو رقم الطلب"
    ).classes(
        "w-full mx-auto text-center bg-gray-800 text-white rounded-xl"
    )

    ui.button(
        "بحث",
        on_click=lambda: render_cards(search_input.value)
    ).classes(
        "w-full mt-3 bg-red-600 text-white rounded-xl"
    )

# ================== TITLE ==================
ui.label("الطلبيات النشطة").classes(
    "text-2xl font-bold text-center mt-10 mb-6"
)

cards_container = ui.column().classes(
    "w-full max-w-4xl mx-auto gap-6 items-center"
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
    for s in stages:
        if not s["date"]:
            return s["name"]
    return stages[-1]["name"] if stages else ""

# ================== STAGE BOX ==================
def stage_box(name, date, is_current):
    if date:
        color = "bg-emerald-100 text-emerald-800"
        subtitle = date
    elif is_current:
        color = "bg-red-100 text-red-800"
        subtitle = "قيد التنفيذ"
    else:
        color = "bg-gray-100 text-gray-500"
        subtitle = "بانتظار التنفيذ"

    with ui.card().classes(
        f"w-full text-center p-4 rounded-2xl {color}"
    ):
        ui.label(name).classes("font-bold")
        ui.label(subtitle).classes("text-sm mt-1")

# ================== CARDS ==================
def render_cards(keyword=""):
    cards_container.clear()
    keyword = keyword.lower().strip()

    for index, row in data.iterrows():

        if not row["title"] or not row["order_no"]:
            continue

        searchable = f"{row['title']} {row['order_no']}".lower()
        if keyword and keyword not in searchable:
            continue

        stages = get_stages(row)
        current_stage = get_current_stage(stages)
        sheet_row = index + 2  # الصف الحقيقي في Google Sheet

        with cards_container:
            with ui.card().classes(
                "w-full bg-white rounded-3xl p-6 shadow-md text-center"
            ):
                ui.label(row["title"]).classes(
                    "text-xl font-bold mb-1"
                )
                ui.label(f"القسم: {row['department']}").classes(
                    "text-gray-600"
                )
                ui.label(f"رقم الطلب: {row['order_no']}").classes(
                    "text-gray-600 mb-3"
                )

                ui.label(f"الحالة الحالية: {current_stage}").classes(
                    "text-red-700 font-semibold mb-4"
                )

                # 🔴 زر تعديل شغال 100%
                ui.link(
                    "✏️ تعديل الطلبية",
                    f"{BASE_SHEET_URL}&range=A{sheet_row}",
                    new_tab=True
                ).classes(
                    "block w-full text-center bg-gray-900 text-white rounded-xl py-2 mb-4"
                )

                with ui.column().classes("gap-3 items-center"):
                    for stage in stages:
                        stage_box(
                            stage["name"],
                            stage["date"],
                            stage["name"] == current_stage
                        )

# ================== INIT ==================
render_cards()
ui.run()
