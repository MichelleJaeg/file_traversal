import sqlite3
import os, time

new_files = []
modified_files = {}
conn = sqlite3.connect('my_database')
c = conn.cursor()

def process_file(rootpath, path, f):
    id = None
    dir_path = os.path.join(path, f)
    # Time and date that the file was last modified
    modified = (time.ctime(os.stat(dir_path).st_mtime))
    c.execute('SELECT id FROM paths WHERE rootdir = ?',(rootpath, ))
    list_of_rootids = c.fetchall()
    # Finds first tuple out of list, then first integer out of that tuple
    rootid = list_of_rootids[0][0]
    seen = 1
    c.execute('SELECT filename from location WHERE filename = ?', (f,))
    old = c.fetchall()
    if not old:
        new_files.append(f)
    c.execute('SELECT modified from location WHERE modified = ?', (modified,))
    were_modified = c.fetchall()
    if not were_modified and not f in new_files:
        modified_files[f] = modified
    c.execute('SELECT * FROM location WHERE filename = ?', (f,))
    found = c.fetchall()
    if found:
        c.execute('UPDATE location SET modified = ?, seen = 1 WHERE filename = (?)', (modified, f))
    else:
        c.execute('INSERT INTO location VALUES (?,?,?,?,?,?)', (id, f, dir_path, modified,
                                                               seen, rootid))
    conn.commit()

def delete_file(f):
    c.execute('DELETE FROM location WHERE filename = ?', (f,))

def main ():
    c.execute('''
                CREATE TABLE IF NOT EXISTS location(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    filename character varying(128),
                    dirpath character varying(511),
                    modified timestamp without time zone,
                    seen INTEGER DEFAULT 0,
                    rootid INTEGER REFERENCES paths(id))
                ''')
    c.execute('SELECT rootdir FROM paths')
    rootdir_rows = c.fetchall()
    for root_path in rootdir_rows:
        for path, dirs, files in os.walk(root_path[0]):
            for f in files:
                process_file(root_path[0], path, f)
    # Remove deleted files from database
    c.execute('SELECT filename FROM location WHERE seen = 0')
    file_rows = c.fetchall()
    deleted_files = [item[0] for item in file_rows]
    for file in deleted_files:
        delete_file(file)
    # Report information
    print ("The following files have been deleted:", deleted_files )
    print ("The following files have been added:", new_files)
    print ("The following files have been modified:", modified_files)
    # Set variable 'seen' back to 0 for all rows
    c.execute('UPDATE location SET seen = 0')
    conn.commit()
    c.close()


if __name__ == "__main__":
    main()
