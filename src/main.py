import sys
import traceback

from data import DataManager

if __name__ == "__main__":
    try:
        data = DataManager()
        data.generate_report()

        sys.exit(0)
    except Exception:
        traceback.print_exc()

        sys.exit(1)
