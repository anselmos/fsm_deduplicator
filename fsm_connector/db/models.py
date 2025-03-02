from typing import Optional

from sqlalchemy import String, Text, Boolean, BIGINT
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from fsm_connector.db.JsonDecorator import JsonDecorator


Base = declarative_base()


class File(Base):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    extension: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(Text)
    md5sum: Mapped[str] = mapped_column(String(255))
    clean: Mapped[bool] = mapped_column(Boolean)
    duplicated_md5: Mapped[bool] = mapped_column(Boolean, default=False)
    size: Mapped[int] = mapped_column(BIGINT)
    created: Mapped[int] = mapped_column(BIGINT)
    modified: Mapped[int] = mapped_column(BIGINT)
    date_created: Mapped[Optional[int]] = mapped_column(BIGINT)
    exiftool_data: Mapped[str] = mapped_column(JsonDecorator)
    File_FileModifyDate: Mapped[str] = mapped_column(Text)
    EXIF_ModifyDate: Mapped[str] = mapped_column(Text)
    EXIF_DateTimeOriginal: Mapped[str] = mapped_column(Text)
    to_be_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    new_path_after_deleted: Mapped[str] = mapped_column(Text, default="", nullable=True)

    def __repr__(self) -> str:
        return f"path={self.path!r} md5: {self.md5sum}"


class Image(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    extension: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(Text)
    md5sum: Mapped[str] = mapped_column(String(255))
    clean: Mapped[bool] = mapped_column(Boolean)
    duplicated_md5: Mapped[bool] = mapped_column(Boolean, default=False)
    size: Mapped[int] = mapped_column(BIGINT)
    created: Mapped[int]
    modified: Mapped[int]


