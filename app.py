from nicegui import ui
import pandas as pd

# ================== Google Sheet ==================
SHEET_ID = "1WQWL2aRzD5lvqVgUzXNi_B2poEV8YCUBOd60sRnfy1Q"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

def load_data():
    return pd.read_csv(CSV_URL).fillna("")

data = load_data()

# ================== CARD COLORS ==================
CARD_COLORS = [
    "bg-sky-50",
    "bg-emerald-50",
    "bg-amber-50",
    "bg-rose-50",
    "bg-violet-50",
    "bg-cyan-50",
]

# ================== GLOBAL STYLE ==================
ui.add_head_html("""
<style>
* {
    font-family: "Times New Roman", serif;
    font-style: italic;
    text-align: center;
}
</style>
""")

# ================== HEADER ==================
with ui.column().classes(
    "w-full bg-gradient-to-b from-slate-800 to-slate-900 text-white "
    "py-10 mb-10 rounded-b-3xl shadow items-center justify-center text-center"
):
    ui.label("نظام متابعة الطلبيات").classes("text-4xl font-bold mb-2")
    ui.label("متابعة • تنظيم • سيطرة").classes("text-sm text-gray-300")

cards_container = ui.column().classes(
    "w-full max-w-xl mx-auto px-4 gap-10 items-center justify-center"
)

# ================== OPEN ROW (RAILWAY SAFE) ==================
def open_row(row_number: int):
    url = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
        f"#gid=0&range=A{row_number}"
    )
    ui.open(url, new_tab=True)

# ================== STAGES ==================
def get_stages(row):
    stages = []
    for i in range(1, 10):
        name = row.get(f"stage_{i}_name", "")
        date = row.get(f"stage_{i}_date", "")
        if name:
            stages.append({"name": name, "date": date})

    if row.get("receive"):
        stages.append({
            "name": row.get("receive"),
            "date": row.get("receive_date", "")
        })

    return stages

def get_current_stage(stages):
    for stage in stages:
        if stage["date"] == "":
            return stage["name"]
    return stages[-1]["name"] if stages else ""

# ================== STAGE BOX ==================
def stage_box(name, date, is_current):
    if date:
        color = "bg-emerald-100 text-emerald-900"
        subtitle = date
    elif is_current:
        color = "bg-amber-100 text-amber-900"
        subtitle = "قيد التنفيذ"
    else:
        color = "bg-gray-100 text-gray-700"
        subtitle = "بانتظار التنفيذ"

    with ui.card().classes(
        f"""
        w-full rounded-2xl shadow p-5
        flex flex-col items-center justify-center text-center
        {color}
        """
    ):
        ui.label(name).classes("font-bold text-lg")
        ui.label(subtitle).classes("text-sm mt-2 font-semibold")

# ================== CARDS ==================
def render_cards():
    cards_container.clear()
    index = 0

    for idx, row in data.iterrows():

        if not row["title"] or not row["order_no"]:
            continue

        card_color = CARD_COLORS[index % len(CARD_COLORS)]
        index += 1

        stages = get_stages(row)
        current_stage = get_current_stage(stages)

        sheet_row_number = idx + 2  # مهم جداً

        with cards_container:
            with ui.card().classes(
                f"""
                w-full rounded-3xl shadow-xl p-8
                flex flex-col items-center justify-center text-center
                {card_color}
                """
            ):
                ui.label(row["title"]).classes("text-2xl font-bold mb-2")
                ui.label(f"القسم: {row['department']}").classes("text-gray-700")
                ui.label(f"رقم الطلب: {row['order_no']}").classes("text-gray-700 mb-4")

                ui.label(
                    f"الحالة الحالية: {current_stage}"
                ).classes("text-red-700 font-bold mb-6")

                # ===== EDIT BUTTON =====
                ui.button(
                    "تعديل الطلبية",
                    on_click=lambda r=sheet_row_number: open_row(r),
                    color="black"
                ).props("unelevated").classes(
                    "w-full max-w-sm mb-4 text-white text-lg font-bold rounded-full"
                )

                # ===== DETAILS =====
                details_container = ui.column().classes(
                    "w-full gap-4 items-center justify-center"
                )
                details_container.visible = False

                ui.button(
                    "تفاصيل مراحل الطلبية",
                    on_click=lambda dc=details_container: setattr(dc, "visible", not dc.visible),
                    color="teal"
                ).props("unelevated").classes(
                    "w-full max-w-sm mb-6 text-white text-lg font-bold rounded-full"
                )

                with details_container:
                    for stage in stages:
                        stage_box(
                            stage["name"],
                            stage["date"],
                            stage["name"] == current_stage
                        )

# ================== INIT ==================
render_cards()
ui.run()
