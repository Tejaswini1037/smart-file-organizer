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

    if not os.path.exists(destination):
       shutil.copy2(source, destination)

    write_log(
        f"Moved '{source}' -> '{destination}'"
    )


def organize_files(folder_path):

    create_folder(os.path.join(folder_path, "Images"))
    create_folder(os.path.join(folder_path, "Documents"))
    create_folder(os.path.join(folder_path, "Videos"))
    create_folder(os.path.join(folder_path, "Others"))

    total_files = 0
    image_count = 0
    document_count = 0
    video_count = 0
    other_count = 0

    for file in os.listdir(folder_path):
        if file in ["Images", "Documents", "Videos", "Others", "logs.txt"]:
            continue
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

        if category == "Images":
            image_count += 1
        elif category == "Documents":
            document_count += 1
        elif category == "Videos":
            video_count += 1
        else:
            other_count += 1

    return (
        total_files,
        image_count,
        document_count,
        video_count,
        other_count
    )


def main():

    print("=" * 50)
    print("SMART FILE ORGANIZER")
    print("=" * 50)

    folder_path = input("Enter folder path to organize: ")

    try:

        if not os.path.exists(folder_path):
            raise FileNotFoundError(
                "Folder does not exist."
            )

        total, images, documents, videos, others = organize_files(folder_path)

        print("\nOrganization Completed!")

        print("\n===== SUMMARY =====")
        print(f"Total Files Processed : {total}")
        print(f"Images               : {images}")
        print(f"Documents            : {documents}")
        print(f"Videos               : {videos}")
        print(f"Others               : {others}")

        print("\nLogs saved in logs.txt")

        write_log(
            f"Organization completed. Total={total}, Images={images}, Documents={documents}, Videos={videos}, Others={others}"
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