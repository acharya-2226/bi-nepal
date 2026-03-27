"""
runner.py  -  Chains pipeline stages in order and returns the final context.
"""
import time
from logger import get_logger
from pipeline.stage_01_ingest    import ingest
from pipeline.stage_02_clean     import clean
from pipeline.stage_03_transform import transform

logger = get_logger(__name__)

STAGES = [
    ("ingest",    ingest),
    ("clean",     clean),
    ("transform", transform),
]


def run_pipeline(file_path: str) -> dict:
    context = {"file_path": file_path}
    t0 = time.perf_counter()
    for name, fn in STAGES:
        logger.info(f"--> Stage: {name}")
        ts = time.perf_counter()
        context = fn(context)
        logger.info(f"<-- Stage: {name} ({time.perf_counter() - ts:.3f}s)")
    logger.info(f"Pipeline complete in {time.perf_counter() - t0:.3f}s")
    return context
