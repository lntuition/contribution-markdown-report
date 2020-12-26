import os
from datetime import date

from src.collector import Collector
from src.date import DateRange
from src.extractor import Extractor
from src.skeleton import SkeletonFactory
from src.writer import Writer

if __name__ == "__main__":
    factory = SkeletonFactory(
        language=os.environ["INPUT_LANGUAGE"],
    )

    Writer(
        extractor=Collector.collect(
            user=os.environ["INPUT_USER"],
            date_range=DateRange(
                start=date.fromisoformat(os.environ["INPUT_START_DATE"]),
                end=date.fromisoformat(os.environ["INPUT_END_DATE"]),
            ),
        ),
        skeleton_string_map=factory.get_string_map(),
        skeleton_list_map=factory.get_list_map(),
    ).write(
        file_name=os.environ["INPUT_FILE_NAME"],
    )
