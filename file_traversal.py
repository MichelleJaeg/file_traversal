import sqlite3
import os

def process_file(rootpath, path, f):
    conn = sqlite3.connect('my_database')
    c = conn.cursor()
    id = c.lastrowid
    dirpath = os.path.join(path, f)
    modified = os.stat(dirpath)[9]
    rootid = c.execute('SELECT id From rootdir WHERE rootdir = (?)',(rootpath, ))
    print (type(rootid))
    seen = 1
    c.execute('REPLACE INTO location VALUES (?, ?, ?, ?, ?, ?)',
                                            (id, f, dirpath, modified, seen, rootid))

def delete_file(f):
    conn = sqlite3.connect('my_database')
    cu = conn.cursor()
    cu.execute('DELETE FROM location WHERE file = f;')

def main ():
    conn = sqlite3.connect('my_database')
    curs = conn.cursor()
    #curs.execute('DROP TABLE IF EXISTS location;')
    curs.execute('''
                CREATE TABLE IF NOT EXISTS location(
                    id serial NOT NULL PRIMARY KEY,
                    filename character varying(128),
                    dirpath character varying(511),
                    modified timestamp without time zone,
                    seen boolean NOT NULL DEFAULT 0,
                    rootid INTEGER REFERENCES rootdir(id))
                ''')
    curs.execute('SELECT rootdir FROM rootdir;')
    conn.commit()
    rootdir_rows = curs.fetchall()


    for rootpath in rootdir_rows:
        rootpath = str(rootpath)
        rootpath = rootpath.replace(",", "")
        rootpath = rootpath.strip("(, )")
        rootpath = rootpath.strip("', '")
        for path, dirs, files in os.walk(rootpath):
            for f in files:
                process_file(rootpath, path, f)

    # Make lists of new and modified files

    # Make list of deleted files and delete them from database
    curs.execute('SELECT * FROM location WHERE seen=0;')
    file_rows = curs.fetchall()
    for file in file_rows:
        delete_file(file)
    deleted_files = [item for item in file_rows]


    # Report information
    print ("The following files have been deleted: ", deleted_files )





if __name__ == "__main__":
    main()
