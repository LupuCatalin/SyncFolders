import os
import shutil
import logging
import sys
import time

# create a logger object
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)


def sync_folders(source_folder, replica_folder):

    source_items=os.listdir(source_folder)
    for item in source_items:
        source_path=os.path.join(source_folder,item)
        replica_path = os.path.join(replica_folder, item)

        # if item is a file will copy to the replica folder
        if os.path.isfile(source_path):
            shutil.copy2(source_path,replica_path)
            logger.info(f'File {item} copied to {replica_folder}')
            print()

        # if item is a directory will sync recursively
        elif os.path.isdir(source_path):
            if not os.path.exists(replica_path):
                os.makedirs(replica_path)
                logger.info(f'Directory {item} created to {replica_folder}')
            sync_folders(source_path,replica_path)

    # remove any items in the replica folder that don't exist in the source folder
    replica_items=os.listdir(replica_folder)
    for item in replica_items:
        replica_path = os.path.join(replica_folder, item)
        if item not in source_items:
            if os.path.isfile(replica_path):
                os.remove(replica_path)
                logger.info(f'File {item} removed from {replica_folder}')
            elif os.path.isdir(replica_path):
                shutil.rmtree(replica_path)
                logger.info(f'Directory {item} removed to {replica_folder}')

if "__main__":
    
    source_folder=sys.argv[1] #argv[1] is source folder
    replica_folder=sys.argv[2] #argv[2] is replica folder
    log_file=sys.argv[3] #argv[3] is file log
    sync_time=int(sys.argv[4]) #argv[4] is syncronization time

    # configure logging 
    # for fio=le logging
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # for console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # create a formatter that formats log messages
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # set the formatter for the file handler and console handler
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add the file handler and console handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # scheduler
    try:
      while True:
        sync_folders(source_folder,replica_folder)
        time.sleep(sync_time)
       
    except Exception as e:
        logger.error(e)
        print(e)


