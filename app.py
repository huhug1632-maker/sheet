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

.header-dark {
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: white;
}

.search-dark input {
  background-color: #0f172a !important;
  color: white !important;
}

.search-dark input::placeholder {
  color: #cbd5e1;
}

.order-card {
  border-radius: 20px;
}

.stage-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}
</style>
""")

# ================== HEADER ==================
with ui.element("div").classes("header-dark w-full py-10 px-4"):
    ui.label("نظام متابعة الطلبيات").classes(
        "text-4xl font-bold text-center mb-6"
    )

    with ui.row().classes("max-w-3xl mx-auto gap-2"):
        search_input = ui.input(
            placeholder="بحث بالعنوان أو رقم الطلب"
        ).classes("flex-1 search-dark")

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

# ================== SECTION TITLE ==================
ui.label("الطلبيات النشطة").classes(
    "text-2xl font-bold px-6 mt-8 mb-4"
)

cards_container = ui.column().classes("w-full gap-6 px-6 pb-10")

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
        subtitle = "المرحلة الحالية"
        icon = "➤"
    else:
        color = "bg-gray-100 text-gray-500"
        subtitle = "بانتظار التنفيذ"
        icon = "○"

    with ui.card().classes(
        f"p-3 text-center rounded-xl shadow-sm {color}"
    ):
        ui.label(f"{icon} {name}").classes("font-semibold text-sm")
        ui.label(subtitle).classes("text-xs mt-1")

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
                "order-card w-full p-6 shadow-md hover:shadow-xl transition"
            ):
                ui.label(row["title"]).classes(
                    "text-xl font-bold mb-1"
                )
                ui.label(f"القسم: {row['department']}").classes(
                    "text-sm text-gray-600"
                )
                ui.label(f"رقم الطلب: {row['order_no']}").classes(
                    "text-sm text-gray-600"
                )

                ui.label(f"➤ {current_stage}").classes(
                    "text-red-700 font-semibold mt-2"
                )

                ui.button(
                    "✏️ تعديل الطلبية",
                    on_click=open_sheet
                ).classes("mt-3").props("outline")

                ui.separator().classes("my-4")

                with ui.element("div").classes("stage-grid"):
                    for stage in stages:
                        stage_box(
                            stage["name"],
                            stage["date"],
                            stage["name"] == current_stage
                        )

# ================== INIT ==================
render_cards()
ui.run()
