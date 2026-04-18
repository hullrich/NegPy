from typing import Any

import numpy as np
import rawpy

from negpy.infrastructure.loaders.constants import SUPPORTED_RAW_EXTENSIONS
from negpy.kernel.system.logging import get_logger

logger = get_logger(__name__)


class NonStandardFileWrapper:
    """
    numpy -> rawpy-like interface.
    """

    def __init__(self, data: np.ndarray):
        self.data = data

    def __enter__(self) -> "NonStandardFileWrapper":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def postprocess(self, **kwargs: Any) -> np.ndarray:
        bps = kwargs.get("output_bps", 8)
        half_size = kwargs.get("half_size", False)
        data = self.data
        if half_size:
            data = data[::2, ::2]

        if bps == 16:
            return (data * 65535.0).astype(np.uint16)
        return (data * 255.0).astype(np.uint8)


def get_best_demosaic_algorithm(raw: Any) -> Any:
    """
    Selects optimal demosaicing algorithm based on sensor type and CFA pattern.
    Exclusively uses algorithms packaged in the standard permissive (LGPL) rawpy build.
    """
    selected_algo = rawpy.DemosaicAlgorithm.LINEAR

    if isinstance(raw, NonStandardFileWrapper):
        return selected_algo

    try:
        # Stacked sensors (Linear DNG, Foveon, sRAW)
        if raw.raw_type == rawpy.RawType.Stack:
            selected_algo = rawpy.DemosaicAlgorithm.LINEAR

        # Flat sensors (Bayer, X-Trans)
        elif raw.raw_type == rawpy.RawType.Flat:
            cfa_block_size = raw.raw_pattern.shape[0]

            if cfa_block_size == 6:
                # 6x6 block means it's a Fujifilm X-Trans sensor.
                selected_algo = rawpy.DemosaicAlgorithm.VNG

            elif cfa_block_size == 2:
                # 2x2 block means it's a standard Bayer sensor (Canon, Nikon, Sony, etc.)
                selected_algo = rawpy.DemosaicAlgorithm.AHD

    except Exception as e:
        logger.exception(f"Failed to determine sensor CFA pattern: {e}. Falling back to LINEAR.")
        selected_algo = rawpy.DemosaicAlgorithm.LINEAR

    return selected_algo


def get_supported_raw_wildcards() -> str:
    """
    Returns raw formats as string for file dialogs.
    """
    wildcards = []
    for ext in sorted(SUPPORTED_RAW_EXTENSIONS):
        base = ext.lstrip(".")
        wildcards.append(f"*.{base}")
        wildcards.append(f"*.{base.upper()}")

    return " ".join(wildcards)
