import subprocess


# def list_files(hdfs_url='', recurse=False, use_full_path=False):
#     result = ls(hdfs_url=hdfs_url, recurse=recurse, use_full_path=use_full_path, obj_type=TYPE_FILE)
#     return result
#
#
# def list_dirs(hdfs_url='', recurse=False, use_full_path=False):
#     result = ls(hdfs_url=hdfs_url, recurse=recurse, use_full_path=use_full_path, obj_type=TYPE_DIR)
#     return result
#
#
# def mv(hdfs_src, hdfs_dst):
#     """
#     Move/rename file(s) on HDFS
#     :param hdfs_src: source URL
#     :param hdfs_dst: destination URL
#     :return: stdout
#     """
#     command = "hadoop fs -mv {} {}".format(hdfs_src, hdfs_dst)
#     stdout, stderr = exec_command(command)
#     return stdout, stderr
#
#
# def mkdir(dir_name):
#     """
#     Create directory on HDFS
#     :param dir_name: directory URL
#     :return: stdout, stderr
#     """
#     command = "hadoop fs -mkdir {}".format(dir_name)
#     stdout, stderr = exec_command(command)
#     return stdout, stderr


def exec_command(command):
    """
    Execute the command and return the exit status.
    """
    pobj = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    stdout, stderr = pobj.communicate()

    exit_code = pobj.returncode
    if exit_code != 0:
        raise IOError("Command '{}' failed: {} \n {}".format(command, stdout, stderr))

    return stdout, stderr
