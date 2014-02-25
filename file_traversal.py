import sqlite3
import os, time

new_files = []
modified_files = {}

def process_file(rootpath, path, f):
    conn = sqlite3.connect('my_database')
    c = conn.cursor()
    id = c.lastrowid
    dirpath = os.path.join(path, f)
    # Time and date that the file was last modified
    modified = (time.ctime(os.stat(dirpath).st_mtime))
    c.execute('SELECT id FROM paths WHERE rootdir = (?)',(rootpath, ))
    list_of_rootids = c.fetchall()
    # Finds first tuple out of list, then first integer out of that tuple
    rootid = list_of_rootids[0][0]
    # Seen is now true
    seen = 1
    c.execute('SELECT filename from location WHERE filename = (?)', (f,))
    old = c.fetchall()
    if old == []:
        new_files.append(f)
    c.execute('SELECT modified from location WHERE modified = (?)', (modified,))
    were_modified = c.fetchall()
    if len(were_modified) == 1:
        modified_files[f] = modified
    c.execute('INSERT INTO location VALUES (?, ?, ?, ?, ?, ?)',
                                            (id, f, dirpath, modified, seen, rootid))


def delete_file(f):
    conn = sqlite3.connect('my_database')
    cu = conn.cursor()
    cu.execute('DELETE FROM location WHERE file = f;')

def main ():
    """

    """
    conn = sqlite3.connect('my_database')
    curs = conn.cursor()
    curs.execute('''
                CREATE TABLE IF NOT EXISTS location(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    filename character varying(128),
                    dirpath character varying(511),
                    modified timestamp without time zone,
                    seen INTEGER DEFAULT 0,
                    rootid INTEGER REFERENCES paths(id))
                ''')
    curs.execute('SELECT rootdir FROM paths;')
    conn.commit()
    rootdir_rows = curs.fetchall()

    for root_path in rootdir_rows:
        for path, dirs, files in os.walk(root_path[0]):
            for f in files:
                process_file(root_path[0], path, f)


    # Makes list of deleted files and delete them from database
    curs.execute('SELECT * FROM location WHERE seen=0;')
    file_rows = curs.fetchall()
    print (file_rows)
    for file in file_rows:
        delete_file(file)
    deleted_files = [item for item in file_rows]


    # Report information
    print ("The following files have been deleted:", deleted_files )
    print ("The following files have been added:", new_files)
    print ("The following files have been modified:", modified_files)


    # Need to change seen to 0 again for next time?
    seen = 0
    curs.execute('UPDATE location SET seen = 0')


if __name__ == "__main__":
    main()
