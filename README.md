# Python Tutorial

I'm using this repository to improve my Python skills. After using Anaconda for many years, I'm now looking to create isolated environments for each project to better manage them.

# Python as calculator 
[ref.](https://docs.python.org/3.13/tutorial/introduction.html)

We can continue a calculation using _ to reference to the last calculated value.

# String 

We can write any string inside doble ou single quotes ("..." or '....'), but to write a quote inside a quote we need to add a backslash \. 

## There are to forms to print a string
print('C:\some\name')  # here \n means newline!
print(r'C:\some\name')  # note the r before the quote

The first will ommit some caracters a print a new line, the second form will show the raw text by just add **r** before the string. 

## Launcher Windows
This manual provides examples illustrating the usage of the Windows Python Launcher (py.exe).

A shebang directive (**#!**), located on the first line of a script, specifies the interpreter version that the launcher should invoke for execution.

#! python - invokes the last version of python installed 
#! python3.7 - invokes python 3.7 version 

https://docs.python.org/3.13/using/windows.html#launcher 


# Fuctions 

## \*arguments, \*\*keywords

The special syntax \*\*kwargs is added to a function when we want to add **additional arguments** and **keywords**. The keywords would act as a dictionary, the arguments must be positional.

## __main__

The main function can be placed in modules to execute them as a script or as a function. See fibo module. 

## The dir() Function

The built-in function dir() is used to find out which names a module defines. It returns a sorted list of strings

# I/O representation

This [link](https://docs.python.org/3.13/tutorial/inputoutput.html) shows how represent numers ou print statement ou send it to a file. 