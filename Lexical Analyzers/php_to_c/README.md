# Front End of a PHP to C translater

### Dependencies:
 1. pyhton3
 2. PLY

### To install PLY on your machine for python3, follow the steps outlined below:
 - Download the source code from [link](http://www.dabeaz.com/ply/ply-3.10.tar.gz). <br>
 **Note: Do not use pip to install PLY, it will install a broken distribution on your machine.**
 - Unzip the downloaded zip file
 - Navigate into the unzipped ply-3.10 folder
 - Run the following command in your terminal: 
    ```sh 
    python setup.py install 
    ```
 
 - If you completed all the above, you should now be able to use the PLY module 
 - You can test it out by opening a python shell and import ply module using following line :
    ```sh 
    import ply.lex
    ```


### To execute the parser run the following command:
    ```
    python3 php_parser.py ./test_files/filename.php
    ```
 - **Note: The filename.php file contains the php code which you want to check. This file lies in the ./test_files folder**<br>
 - **There are several test php files in the ./test_files folder which you can use inplace of filename.php (eg.: do-whle.php, for.php, etc.)**
 - **Example: $ python3 php_parser.py ./test_files/if.php**
