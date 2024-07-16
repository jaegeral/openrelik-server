from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import BaseModel
from ..database import file_workflow_association_table

if TYPE_CHECKING:
    from .file import File
    from .folder import Folder
    from .user import User


class Workflow(BaseModel):
    display_name: Mapped[str] = mapped_column(UnicodeText, index=True)
    description: Mapped[Optional[str]] = mapped_column(UnicodeText, index=False)
    uuid: Mapped[Optional[str]] = mapped_column(Unicode(45), index=True)
    spec_json: Mapped[Optional[str]] = mapped_column(UnicodeText, index=False)
    # Relationships
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="workflows")
    folder_id: Mapped[Optional[int]] = mapped_column(ForeignKey("folder.id"))
    folder: Mapped[Optional["Folder"]] = relationship(back_populates="workflows")
    files: Mapped[List["File"]] = relationship(
        secondary=file_workflow_association_table, back_populates="workflows"
    )
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="workflow",
        cascade="all, delete-orphan",
        order_by="Task.id.asc()",
    )


class WorkflowTemplate(BaseModel):
    display_name: Mapped[str] = mapped_column(UnicodeText, index=True)
    description: Mapped[Optional[str]] = mapped_column(UnicodeText, index=False)
    spec_json: Mapped[str] = mapped_column(UnicodeText, index=False)
    # Relationships
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="workflow_templates")


class Task(BaseModel):
    display_name: Mapped[str] = mapped_column(UnicodeText, index=True)
    description: Mapped[Optional[str]] = mapped_column(UnicodeText, index=False)
    uuid: Mapped[str] = mapped_column(Unicode(45), index=True)
    config: Mapped[Optional[str]] = mapped_column(UnicodeText, index=False)
    status_short: Mapped[Optional[str]] = mapped_column(UnicodeText, index=True)
    status_detail: Mapped[Optional[str]] = mapped_column(UnicodeText, index=False)
    status_progress: Mapped[Optional[str]] = mapped_column(UnicodeText, index=False)
    result: Mapped[Optional[str]] = mapped_column(UnicodeText, index=False)
    runtime: Mapped[Optional[float]] = mapped_column(index=False)
    error_exception: Mapped[Optional[str]] = mapped_column(UnicodeText, index=False)
    error_traceback: Mapped[Optional[str]] = mapped_column(UnicodeText, index=False)
    # Relationships
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")
    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflow.id"))
    workflow: Mapped["Workflow"] = relationship(back_populates="tasks")

    # Input Files Relationship (One-to-Many)
    input_files: Mapped[List["File"]] = relationship(
        back_populates="task_input", foreign_keys="[File.task_input_id]"
    )

    # Output Files Relationship (One-to-Many)
    output_files: Mapped[List["File"]] = relationship(
        back_populates="task_output", foreign_keys="[File.task_output_id]"
    )