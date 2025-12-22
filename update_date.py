import re
from datetime import datetime
import os


def update_cover_date():
    file_path = "src/covermenu.py"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    today_str = datetime.now().strftime("%m/%d/%Y")

    with open(file_path, "r") as f:
        content = f.read()

    # Regex to find the RPG Box version string and replace the date
    # It looks for: setText("RPG Box v[anything] [date-pattern]")
    pattern = r'(self\.cover_label\.setText\("RPG Box v\d+ )(\d{1,2}/\d{1,2}/\d{4})("\))'
    new_content = re.sub(pattern, rf'\1{today_str}\3', content)

    if content != new_content:
        with open(file_path, "w") as f:
            f.write(new_content)
        print(f"Updated {file_path} with date: {today_str}")
        # Stage the file so the change is included in the current commit
        os.system(f"git add {file_path}")
    else:
        print("No date update needed or pattern not found.")


if __name__ == "__main__":
    update_cover_date()