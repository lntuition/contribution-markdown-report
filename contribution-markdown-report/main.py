import os

from src.collector import Collector
from src.date import DateBuilder, DateRange
from src.extractor import Extractor
from src.skeleton import SkeletonFactory

if __name__ == "__main__":
    print(os.environ["INPUT_END_DATE"])
