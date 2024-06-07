from pathlib import Path
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Path:
    root_path: str = field(default=Path(__file__).parent, metadata={"help": "기본 root 경로"})
    data_path: str = field(default=Path(__file__).parent / "data", metadata={"help": "csv 데이터파일들의 경로"})

    def __repr__(self):
        all_paths = "\n".join(str(k) + ":" + str(v) for k, v in self.__dict__.items())
        return f"Paths:\n{all_paths}"