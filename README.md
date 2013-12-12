How to setup
------------

1. Create a MySQL database called 'imagematchdb' as user 'root'. In Linux, you can do
    ```
    $ mysql -uroot -p
    mysql> create database imagematchdb;
    ```

2. Create a file named 'password' in the same folder with settings.py . Then
    Write you password for root user of the database into it.

3. Put the image files in folder CBIRdataset/images/ .

4. In project root folder, run:
    ```    
    ./manage.py syncdb
    ```    

5. To test if it works, run:
    ```    
    ./manage.py runserver
    ```    
  Then open your browser and visit `127.0.0.1:8000`. 

Other usage
-----------
### Access database
```
$ ./manage.py dbshell
```

### Import images to database
For example, if you have a bunch of images in folder `~/secret/images`.
```
$ ./manage.py images --add ~/secret/images
```

### View image database status
```
$ ./manage.py images --status
```

### Clear image database
```
$ ./manage.py images --clear
```

### Clear query images
```
$ ./manage.py query --clear
```
