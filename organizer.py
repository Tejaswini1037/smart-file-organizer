import os
import shutil
from datetime import datetime

LOG_FILE = "logs.txt"

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
DOCUMENT_EXTENSIONS = [".pdf", ".docx", ".txt", ".pptx", ".xlsx"]
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi"]


def write_log(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"[{datetime.now()}] {message}\n")


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        write_log(f"Created folder: {folder_path}")


def get_category(file_name):
    ext = os.path.splitext(file_name)[1].lower()

    if ext in IMAGE_EXTENSIONS:
        return "Images"
    elif ext in DOCUMENT_EXTENSIONS:
        return "Documents"
    elif ext in VIDEO_EXTENSIONS:
        return "Videos"
    else:
        return "Others"


def move_file(source, destination_folder):

    file_name = os.path.basename(source)
    destination = os.path.join(destination_folder, file_name)

    count = 1

    while os.path.exists(destination):
        name, ext = os.path.splitext(file_name)
        destination = os.path.join(
            destination_folder,
            f"{name}_{count}{ext}"
        )
        count += 1

    shutil.move(source, destination)

    write_log(
        f"Moved '{source}' -> '{destination}'"
    )


def organize_files(folder_path):

    create_folder(os.path.join(folder_path, "Images"))
    create_folder(os.path.join(folder_path, "Documents"))
    create_folder(os.path.join(folder_path, "Videos"))
    create_folder(os.path.join(folder_path, "Others"))

    total_files = 0

    for file in os.listdir(folder_path):

        source_path = os.path.join(folder_path, file)

        if os.path.isdir(source_path):
            continue

        category = get_category(file)

        destination_folder = os.path.join(
            folder_path,
            category
        )

        move_file(source_path, destination_folder)

        total_files += 1

    return total_files


def main():

    print("=" * 50)
    print("SMART FILE ORGANIZER")
    print("=" * 50)

    folder_path = input(
        "Enter folder path to organize: "
    )

    try:

        if not os.path.exists(folder_path):
            raise FileNotFoundError(
                "Folder does not exist."
            )

        total = organize_files(folder_path)

        print("\nOrganization Completed!")
        print(f"Total Files Processed: {total}")
        print("Logs saved in logs.txt")

        write_log(
            f"Organization completed. Files processed: {total}"
        )

    except FileNotFoundError as e:
        print(e)
        write_log(str(e))

    except PermissionError:
        print("Permission denied.")
        write_log("Permission denied.")

    except Exception as e:
        print(f"Unexpected Error: {e}")
        write_log(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()