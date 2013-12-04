import sqlite3
import os


def process_file(rootpath, path, f):
    conn = sqlite3.connect('my_database')
    c = conn.cursor()
    dirpath = os.path.join(path, f)
    modified = os.stat(f)
    rootid = rootpath.id
    seen = 1
    c.execute('''IF EXISTS(SELECT * FROM location WHERE file = f)
                     UPDATE location SET (?, ?, ?, ?, ?, ?) WHERE file = f;
                 ELSE
                     INSERT INTO location VALUES (?, ?, ?, ?, ?, ?);''',
                     (id, f, dirpath, modified, seen, rootid),(id, f, dirpath, modified, seen, rootid))

def delete_file(f):
    conn = sqlite3.connect('my_database')
    cu = conn.cursor()
    cu.execute('DELETE FROM location WHERE file = f;')

def main ():
    # existed = os.path.exists("/Users/mswank/Documents/Dev/")
    conn = sqlite3.connect('my_database')
    curs = conn.cursor()
    #if not existed:
    curs.execute('DROP TABLE IF EXISTS rootdir;')
    curs.execute('''
                CREATE TABLE rootdir(
                    id SERIAL PRIMARY KEY,
                    rootdir CHARACTER VARYING(255))
                ''')
    curs.execute('DROP TABLE IF EXISTS location;')
    curs.execute('''
                CREATE TABLE location(
                    id serial NOT NULL PRIMARY KEY,
                    filename character varying(128),
                    dirpath character varying(511),
                    modified timestamp without time zone,
                    digest character(64),
                    seen boolean NOT NULL DEFAULT 0,
                    rootid INTEGER REFERENCES rootdir(id))
                ''')
    curs.execute('SELECT * FROM rootdir;')
    conn.commit()
    rootdir_rows = curs.fetchall()
    #else:
        #curs.execute('SELECT * FROM rootdir;')
        #.rootdir_rows = curs.fetchall()

    for rootpath in rootdir_rows:
        for path, dirs, files in os.walk("/Users/mswank/Documents/Dev"):
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
