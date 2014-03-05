#set variables 
export ROOT='directory_for_file_traversal'
export FILE='file_traversal.py'

# Make sure directory starts out empty and no changes are reported
echo 'Should report no changes'
python $FILE

# Add one file
touch $ROOT/file_1.py
echo 'Should report file_1.py added'
python $FILE

# Delete only file
rm $ROOT/file_1.py
echo 'Should report file_1.py deleted'
python $FILE

# Add two files
touch $ROOT/file_1.py
touch $ROOT/file_2.py
echo 'Should report file_1.py and file_2.py added'
python $FILE

# Delete one of two files
rm $ROOT/file_1.py
echo 'Should report file_1.py deleted'
python $FILE

# Modify only file
sleep 1
touch $ROOT/file_2.py
echo 'Should report file_2.py modified'
python $FILE

# Add a second file 
touch $ROOT/file_1.py
echo 'Should report file_1.py added'
python $FILE

# Modify one of two files
sleep 1
touch $ROOT/file_1.py
echo 'Should report file_1.py modified'
python $FILE

# Modify two files
sleep 1
touch $ROOT/file_1.py
sleep 1
touch $ROOT/file_2.py
echo 'Should report file_1.py and file_2.py modified'
python $FILE

# Delete both files
rm $ROOT/file_1.py
rm $ROOT/file_2.py
echo 'Should report file_1.py and file_2.py deleted'
python $FILE

echo 'Set back to original state'
python $FILE
