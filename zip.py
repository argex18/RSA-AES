import zipfile
from traceback import print_exc
from os import path

def zipFile(file_path, output_path=None, pwd=None):
    try:
        if not path.exists(file_path):
            raise FileNotFoundError('ERROR: the input file does not exist')
        if output_path == None or not path.exists(output_path):
            file_name = path.basename(file_path)
            ext = file_name[file_name.rfind('.'):len(file_name)]
            output_path = file_path.replace(ext, '.zip')
            
            archive = zipfile.ZipFile(file=output_path, mode='x', allowZip64=True)
            archive.close()
        if pwd != None and not isinstance(pwd, str):
            raise TypeError('ERROR: the password must be of type str')
        
        file_name = path.basename(file_path)
        with zipfile.ZipFile(output_path, 'a') as zf:
            zf.write(file_path, file_name)
            if pwd != None:
                zf.setpassword( pwd.encode('ascii') )
            if zf.testzip() == None:
                return True
            else:
                return False
    except Exception:
        print_exc()

def unzipFile(zip_path, name, output_path=None, pwd=None):
    flag = False
    try:
        if not path.exists(zip_path):
            raise FileNotFoundError('ERROR: the archive does not exist')
        if output_path == None or not path.exists(output_path):
            print('WARNING: the output path passed is None or does not exist')
            print('Setting zip path directory as output path')
            output_path = zip_path.replace( path.basename(zip_path), '' )
        if pwd != None and not isinstance(pwd, str):
            raise TypeError('ERROR: the password must be of type str')
        
        with zipfile.ZipFile(zip_path, 'r') as zf:
            files = zf.namelist()

            for f in files:
                if f == name:
                    flag = True
                    if pwd != None:
                        zf.extract(f, path=output_path, pwd=pwd.encode('ascii'))
                    else:
                        zf.extract(f, path=output_path)
            if not flag:
                raise FileNotFoundError('ERROR: the file named does not exist in this archive')
    except Exception:
        print_exc()
    finally:
        return flag

def unzipAll(zip_path, output_path=None, pwd=None):
    flag = False
    try:
        if not path.exists(zip_path):
            raise FileNotFoundError('ERROR: the archive does not exist')
        if output_path == None or not path.exists(output_path):
            print('WARNING: the output path passed is None or does not exist')
            print('Setting zip path directory as output path')
            output_path = zip_path.replace( path.basename(zip_path), '' )
        if pwd != None and not isinstance(pwd, str):
            raise TypeError('ERROR: the password must be of type str')

        with zipfile.ZipFile(zip_path, 'r') as zf:
            flag = True
            if pwd != None:
                zf.extractall(path=output_path, pwd=pwd.encode('ascii'))
            else:
                zf.extractall(path=output_path)
    except Exception:
        print_exc()
    finally:
        return flag

if __name__ == '__main__':
    flag = unzipFile('tandem_1.zip', 'tandem_1.json')
    if flag:
        print('Successfully uncompressed')
    else:
        print('Some error occured')