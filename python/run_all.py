import subprocess
import sys
from pathlib import Path

folder = Path(__file__).parent

files = [
    "1.readible.py",
    "2.product-custumer.py",
    "3.customer segemtation.py",
    "4.data segmentation.py",
]

for file in files:
    file_path = folder / file

    print(f"\n===== Running {file} =====")

    if not file_path.exists():
        print(f"ERROR: File not found: {file}")
        break

    result = subprocess.run([sys.executable, str(file_path)])

    if result.returncode != 0:
        print(f"ERROR: {file} failed.")
        break

print("\n===== Finished =====")