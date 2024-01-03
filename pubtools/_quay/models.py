import dataclasses
from typing import Dict, Any, List


@dataclasses.dataclass
class BuildIndexImageParam:
    """Parameter data for building index image and part of data required by iib_results."""

    bundles: list[str]
    index_image: str
    deprecation_list: List[str] | None
    build_tags: List[str]
    target_settings: Dict[str, Any]
    tag: str
    signing_keys: List[str]
    destination_tags: List[str]
    origin: str
