from sqlalchemy.orm import Session

from datastores.sql.models.file import File, FileSummary

from .folder import get_folder_from_db

import magic
import os


def get_files_from_db(db: Session, folder_id: str):
    """Retrieves a list of files from the database for a specific folder.

    Args:
        db (Session): A SQLAlchemy database session object.
        folder_id (str): The ID of the folder to retrieve files from.

    Returns:
        List[File]: A list of File objects representing the files in the folder.
    """
    return db.query(File).filter_by(folder_id=folder_id).order_by(File.id.desc()).all()


def get_file_from_db(db: Session, file_id: int):
    """Retrieves a file from the database by its ID.

    Args:
        db (Session): A SQLAlchemy database session object.
        file_id (int): The ID of the file to retrieve.

    Returns:
        File: A File object representing the file with the specified ID.
    """
    return db.get(File, file_id)


def create_file_in_db(db: Session, file: dict):
    """Creates a new file in the database.

    Args:
        db (Session): A SQLAlchemy database session object.
        file (dict): A dictionary representing the file to be created.

    Returns:
        File: The newly created File object.
    """
    folder = get_folder_from_db(db, file.get("folder_id"))
    filename = f"{file.get("uuid")}"
    if file.get("extension"):
        filename = f"{file.get("uuid")}.{file.get("extension")}"
    output_file = os.path.join(folder.path, filename)

    # File metadata
    file["magic_text"] = magic.from_file(output_file)
    file["magic_mime"] = magic.from_file(output_file, mime=True)
    file["filesize"] = os.stat(output_file).st_size
    # TODO: Get data type from KB
    if not file.get("data_type"):
        file["data_type"] = "file:generic"

    db_file = File(**file)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def delete_file_from_db(db: Session, file_id: int):
    """Delete a file from the database by its ID.

    Args:
        db (Session): A SQLAlchemy database session object.
        file_id (int): The ID of the file representing the file to be deleted.
    """

    file = db.get(File, file_id)
    db.delete(file)
    db.commit()


def get_file_summary_from_db(db: Session, file_summary_id: int):
    """Retrieves a file summary from the database by its ID."""
    return db.get(FileSummary, file_summary_id)


def create_file_summary_in_db(db: Session, file_summary: dict):
    """Creates a new file summary in the database using generative AI.

    Args:
        db (Session): A SQLAlchemy database session object.
        file_summary (dict): A dictionary representing a FileSummary.

    Returns:
        FileSummary: The newly created FileSummary object.
    """
    db_file_summary = FileSummary(**file_summary)
    db.add(db_file_summary)
    db.commit()
    db.refresh(db_file_summary)
    return db_file_summary


def update_file_summary_in_db(db: Session, file_summary: FileSummary):
    """Update a FileSummary object in the database.

    Args:
        db (Session): SQLAlchemy session object
        file_summary (FileSummary): FileSummary object to be updated

    Returns:
        FileSummary: Updated FileSummary object
    """
    db.add(file_summary)
    db.commit()
    db.refresh(file_summary)
    return file_summary