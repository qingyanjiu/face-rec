# compile.py
import compileall
import shutil
import os
 
current_dir = os.path.dirname(os.path.abspath(__file__))
dist_dir = os.path.join(current_dir, 'dist')
 
 
def mk_dist(copyfile=None, copytree=None):
    try:
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir)
        os.mkdir(dist_dir)
        if copyfile:
            for filename in copyfile:
                shutil.copyfile(filename, os.path.join(dist_dir ,filename))
        if copytree:
            for dirname in copytree:
                shutil.copytree(dirname, os.path.join(dist_dir ,filename))
    except Exception as ex:
        print(ex)
 
 
def compile_pj():
    compileall.compile_dir(dist_dir, legacy=True)
 
 
def remove_file(dir, postfix):
    """删除指定目录下指定后缀的文件"""
    if os.path.isdir(dir):
        for file in os.listdir(dir):
            remove_file(dir + '/' + file, postfix)
    else:
        if os.path.splitext(dir)[1] == postfix:
            os.remove(dir)
 
def remove_dir(del_dir, filename="__pycache__"):
    """删除__pycache__目录"""
    if os.path.isdir(del_dir):
        for file in os.listdir(del_dir):
            if file == filename:
                shutil.rmtree(del_dir + '/' + file, True)
            remove_dir(del_dir + '/' + file)
 
def main():
    # 根目录要拷贝的 文件
    copyfile = [
        "api.py",
        "DataBase.py",
        "dbConfig.py",
        "faceService.py",
        "initDb.py",
        "db.yaml"
    ]
    # 根目录要拷贝的 目录
    copytree = [
    ]
    mk_dist(copyfile=copyfile, copytree=copytree)
    compile_pj()
    remove_file(dist_dir, ".py")
    remove_dir(dist_dir, filename="__pycache__")
 
if __name__ == "__main__":
    main()