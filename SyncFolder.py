import os
import shutil

def sync_folders(source_folder, replica_folder):

    source_items=os.listdir(source_folder)

    for item in source_items:
        source_path=os.path.join(source_folder,item)
        replica_path = os.path.join(replica_folder, item)

        # if item is a file will copy to the replica folder
        if os.path.isfile(source_path):
            shutil.copy2(source_path,replica_path)

        # if item is a directory will sync recursively
        elif os.path.isdir(source_path):
            if not os.path.exists(replica_path):
                os.makedirs(replica_path)
            sync_folders(source_path,replica_path)

    # remove any items in the replica folder that don't exist in the source folder
    replica_items=os.listdir(replica_folder)
    for item in replica_items:
        replica_path = os.path.join(replica_folder, item)
        if item not in source_items:
            if os.path.isfile(replica_path):
                os.remove(replica_path)
            elif os.path.isdir(replica_path):
                shutil.rmtree(replica_path)

if "__main__":
    source_folder="C:\\Users\\cata_\\Desktop\\source"
    replica_folder="C:\\Users\\cata_\\Desktop\\replica"

    try:
        sync_folders(source_folder,replica_folder)
    except Exception as e:
        print(e)


