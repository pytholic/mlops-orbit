def upload_directory_with_transfer_manager(bucket_name, source_directory, workers=8):
    """Upload every file in a directory, including all files in subdirectories.

    Each blob name is derived from the filename, not including the `directory` parameter itself.
    For complete control of the blob name for each file (and other aspects of individual blob
    metadata), use transfer_manager.upload_many() instead.
    """

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The directory on your computer to upload. Files in the directory and its
    # subdirectories will be uploaded. An empty string means "the current
    # working directory".
    # source_directory=""

    # The maximum number of processes to use for the operation. The performance
    # impact of this value depends on the use case, but smaller files usually
    # benefit from a higher number of processes. Each additional process occupies
    # some CPU and memory resources until finished. Threads can be used instead
    # of processes by passing `worker_type=transfer_manager.THREAD`.
    # workers=8

    import os
    from pathlib import Path

    from dotenv import find_dotenv, load_dotenv
    from google.cloud.storage import Client, transfer_manager

    load_dotenv(find_dotenv())
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GCS_ACCESS_TOKEN")
    storage_client = Client()
    bucket = storage_client.bucket(bucket_name)

    # Generate a list of paths (in string form) relative to the `directory`.
    # This can be done in a single list comprehension, but is expanded into
    # multiple lines here for clarity.

    # First, recursively get all files in `directory` as Path objects.
    directory_as_path_obj = Path(source_directory)
    paths = directory_as_path_obj.rglob("*")

    # Filter so the list only includes files, not directories themselves.
    file_paths = [path for path in paths if path.is_file()]

    # These paths are relative to the current working directory. Next, make them
    # relative to `directory`
    relative_paths = [path.relative_to(source_directory) for path in file_paths]

    # Finally, convert them all to strings.
    string_paths = [str(path) for path in relative_paths]

    print(f"Found {len(string_paths)} files.")

    # Start the upload.
    results = transfer_manager.upload_many_from_filenames(
        bucket,
        string_paths,
        source_directory=source_directory,
        max_workers=workers,
        blob_name_prefix="data/",
    )

    for name, result in zip(string_paths, results):
        # The results list is either `None` or an exception for each filename in
        # the input list, in order.

        if isinstance(result, Exception):
            print(f"Failed to upload {name} due to exception: {result}")
        else:
            print(f"Uploaded {name} to {bucket.name}.")


if __name__ == "__main__":
    upload_directory_with_transfer_manager(
        bucket_name="taxi-ride-prediction", source_directory="../../data"
    )
