from dataclasses import dataclass, field


@dataclass(frozen=True)
class BlockRule:
    match: list[str] = field(default_factory=list)
    descricao_fonte_minima: float = 0.0


@dataclass(frozen=True)
class DocumentTypeConfig:
    blocos: dict[str, BlockRule] = field(default_factory=dict)
    ignorar: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class LineData:
    text: str
    font_size: float
    is_bold: bool


@dataclass(frozen=True)
class BlockContent:
    name: str
    text: str
