import csv
from itertools import islice
from pathlib import Path
from typing import Generator, Iterable, Iterator

from loguru import logger


def validate_csv_file(csv_file: Path):
    if csv_file.suffix != ".csv":
        raise Exception("文件类型错误")


def generate_csv_row(stream: Iterable, skip: int) -> Generator[dict, None, None]:
    """生成 csv 内容

    Args:
        stream (Iterable): 文件流或字符串列表
        skip (int): 跳过的行数

    Yields:
        dict: 生成字典内容
    """
    _iter = islice(stream, skip, None)
    _dict = csv.DictReader(_iter)
    for _line_dict in _dict:
        yield _line_dict


def get_csv_no(csv_file: Path, no: int, default_val: str = None):
    validate_csv_file(csv_file)
    result = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > no:
                result.append(row[no])
            else:
                # 列不足时填空值
                result.append(default_val)
    return result


def split_csv_with_cnt(csv_file: Path, dst_dir: Path, max_cnt: int):
    """
    将一个大 CSV 文件按行数拆分为多个小文件，每个文件最多 max_cnt 条数据行。
    每个拆分文件都保留原始表头。
    """
    dst_dir.mkdir(parents=True, exist_ok=True)
    stem = csv_file.stem
    suffix = csv_file.suffix
    logger.info("拆分开始 START")
    with open(csv_file, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        for index, batch in enumerate(_batched(reader, max_cnt), start=1):
            part_path = dst_dir / f"{stem}_part{index}{suffix}"
            _write_csv(part_path, header, batch)
    logger.info("拆分结束 END")


def _write_csv(path: Path, header: list[str], rows: list[list[str]]):
    """将表头 + 数据行写入一个 CSV 文件。"""
    logger.info("写入文件 START path: ", path)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    logger.info("写入文件 END path: ", path)


def _batched(iterator: Iterator, size: int) -> Iterator[list]:
    """将迭代器按 size 分批产出，每批是一个 list。"""
    batch = []
    for item in iterator:
        batch.append(item)
        if len(batch) == size:
            logger.info("分批导出:", size)
            yield batch
            batch = []
    if batch:
        yield batch
