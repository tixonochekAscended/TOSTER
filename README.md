<p align="center">
<a href="https://ibb.co/V2GYm6g"><img src="https://i.ibb.co/zGgVJdX/T-Logo-1.png" width=250 height=250></a>
</p>

------------------------
# T* - A programming language.
T* is an interpreted, esoteric programming language created by me _(tixonochek)_. Usually people don't refer to T* by language's official name but call it **toster** (read as: toaster). This name derives from the fact that symbol `*` is an **asterisk**. If we shorten that word we get **aster**, and for the language to not have a meaningless alias **Taster** it's called **Toster**, symbolising a nice, working toaster which can be seen on the logo of the language.

### Links for fast travel
1. [Main Concept](#main-concept)
2. [Installation & Usage](#installation-and-usage)
3. [Variables](#variables)

## Main Concept
Every single line contains a **MIO**, which stands for **Mega Important Operator**. Right now you shouldn't question the naming decisions made by the developer but how the language works itself. **MIO** is either `->` or `=>`, where `->` makes line a function call and `=>` makes line assign a certain value to a certain variable. You can indeed think of those as putting bread 🍞 into the toaster. 

Every single line also contains a **left side** and a **right side**. This is pretty straightforward: whatever is on the left side of the MIO is, well, on the left side and whatever is on the right is considered to be the right side of the line. You can see that in practice by looking at this example:
```toster
3 + 10 => a
```
Here `3 + 10` is the left side and `a` is the right side. And yes, I forgot to mention the fact that everything here is a bit reversed, but it all makes sense if you think about this language as a toaster: you put a value into a variable or put a value (argument) into a function. This is how you would output `Hello, World!` in T*:
```toster
"Hello, World!" -> Print
```

Every single line can also be **commented**. Remember that a line can't exist having a comment only. Let's see it on the real example: this wouldn't work.
```toster
// This is a comment ^_^
"..." -> Print
```
However this would be executed flawlessly:
```toster
"..." -> Print // This is a comment ^_^
```

## Installation and Usage
As you might've noticed, T* is written fully in Python. There are 2 ways on how you can install and enjoy coding in the toaster language.

**Method number 1️⃣**: You can install an executable from the **Releases** page of this github repository for your OS. After that, just run the executable with the application arguments you want whilst providing a file name of a file with `.tost` extension. As an example, if you are on **Windows**, you would use a command similar to that: `toster.exe FILENAME.tost` where `FILENAME` is the name of your file.

**Method number 2️⃣**: You can download the file `toster.py` from this repository and execute it manually, that is if you have `Python` already installed on your machine. To execute `.tost` files just follow the steps described in the __first method__.

## Variables
To create a variable, you need to create a line using `=>` MIO. Here's an example on how you can create a variable with the name `tix` containing the number `13` as it's value. 
```toster
13 => tix
```
You also can change the value of an already existing variable with ease. Here's how you can increase the value of a variable called `t` by 8.
```toster
5 => t
t + 8 => t
```
