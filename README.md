<p align="center">
<a><img src="https://i.ibb.co/zGgVJdX/T-Logo-1.png" width=250 height=250></a>
  <a><img src="https://i.ibb.co/vDJJfqc/Toster-Advanced-1.png" width=250 height=250></a>
</p>

------------------------
# T* - A programming language.
T* is an interpreted, esoteric programming language created by me _(tixonochek)_. Usually people don't refer to T* by language's official name but call it **toster** (read as: toaster). This name derives from the fact that symbol `*` is an **asterisk**. If we shorten that word we get **aster**, and for the language to not have a meaningless alias **Taster** it's called **Toster**, symbolising a nice, working toaster which can be seen on the logo of the language.

⚠️ **Warning**: if you are new and would like to know more about the language, you need to read this page from this point right to the bottom of it. It isn't advised to skip parts of the text - you might miss **crucial** information about how the language works. *It's obviously fine to skip some long and detailed descriptions of functions - it's not like I can decide what are you going to read anyway.*
### Links for fast travel
1. [Main Concept](#main-concept)
2. [Installation & Usage](#installation-and-usage)
3. [Variables](#variables)
4. [Where are the floats](#where-are-the-floats)
5. [Operators](#operators)
6. [Operator descriptions](#operator-descriptions)
7. [Why strings become weird numbers](#why-strings-become-weird-numbers)
8. [Functions](#functions)
9. [Function descriptions](#function-descriptions)
10. [What `$res` is](#what-is-dollar-res)


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
You also can change the value of an already existing variable with ease. Here's how you can increase the value of a variable called `$t` by 8.
```toster
5 => $t
$t + 8 => $t
```
T* takes an interesting approach with creating variables. If there is only a single identifier on the right side of the line, it's converted to a string to create a variable. If you didn't understand, the thing is that the right side is either a single identifier or whatever you want, as long as it evaluates to a string. Check this out!
```toster
"a" => lmao
13 => "huh"
88 => lmao + huh
a13 -> Print
```
What do you think this line will print? It's right: `88`. First, we define a variable with the name `lmao` and put string `"a"` into it. Then, we create another variable called `huh` and assign the number `13` to it. Afterwards, we put the number `88` into the variable called "a13". Basically, `lmao + huh` = `"a" + 13` which evaluates to a string `"a13"`. Considering it's a string, a variable is created successefully. Afterwards we just output the new variable (called `a13`). It's just that simple ^_^

## Where are the floats
You might have noticed that we used words **number** and **string** to describe the types. But while talking about numbers, we never created a float. That's because there __are no floats, you dummy!__ Who cares about floats anyway. They are a piece of garbage that never should've been invented...

## Operators
There can only be 1 operator per side of the line. There can't be more than a single operator on the side, just remember it once and for all. For example you __can't__ do this
```toster
1 + 15 * 2 => a
a -> Print
```
This won't print anything but give an error instead. This approach works though:
```toster
15 * 2 => a
a + 1 => a
a -> Print
```
This might sound like an inconvinience, but this is actually a genius move by the developer of the language *(definitely not me)*. Don't question it - accept it.

## Operator descriptions
There are 13 operators in T*. Here's an explanation of their behaviour when working with different types. Experiment yourself to check out different behaviours ^_^
### `+` ADD Operator
Self-explanatory.
| First Argument Type | Second Argument Type | Resulting Type |
|---------------------|----------------------|----------------|
| `String`            | `String`             | `String`       |
| `Number`            | `String`             | `Number`       |
| `String`            | `Number`             | `String`       |
| `Number`            | `Number`             | `Number`       |
### `-` SUB Operator
Self-explanatory.
| First Argument Type | Second Argument Type | Resulting Type |
|---------------------|----------------------|----------------|
| `String`            | `String`             | `Number`       |
| `Number`            | `String`             | `Number`       |
| `String`            | `Number`             | `Number`       |
| `Number`            | `Number`             | `Number`       |
### `/` DIVIDE Operator
Self-explanatory.
| First Argument Type | Second Argument Type | Resulting Type |
|---------------------|----------------------|----------------|
| `String`            | `String`             | `Number`       |
| `Number`            | `String`             | `Number`       |
| `String`            | `Number`             | `Number`       |
| `Number`            | `Number`             | `Number`       |
### `*` MULTIPLY Operator
Self-explanatory. If string is multiplied by a string those strings are **crossed** together. Check it out yourself.
| First Argument Type | Second Argument Type | Resulting Type |
|---------------------|----------------------|----------------|
| `String`            | `String`             | `String`       |
| `Number`            | `String`             | `Number`       |
| `String`            | `Number`             | `String`       |
| `Number`            | `Number`             | `Number`       |
### `%` ADD Operator
Self-explanatory.
| First Argument Type | Second Argument Type | Resulting Type |
|---------------------|----------------------|----------------|
| `String`            | `String`             | `Number`       |
| `Number`            | `String`             | `Number`       |
| `String`            | `Number`             | `Number`       |
| `Number`            | `Number`             | `Number`       |
### `==` EQUALS Operator
Compares both the type and the value of the passed arguments. Is different in comparsion to the __equality__ operator.
| First Argument Type | Second Argument Type | Resulting Type |
|---------------------|----------------------|----------------|
| `String`            | `String`             | `Number`       |
| `Number`            | `String`             | `Number`       |
| `String`            | `Number`             | `Number`       |
| `Number`            | `Number`             | `Number`       |
### `>` GREATER THAN Operator
Self-explanatory. 
| First Argument Type | Second Argument Type | Resulting Type |
|---------------------|----------------------|----------------|
| `String`            | `String`             | `Number`       |
| `Number`            | `String`             | `Number`       |
| `String`            | `Number`             | `Number`       |
| `Number`            | `Number`             | `Number`       |
### `<` LESS THAN Operator
Self-explanatory. 
| First Argument Type | Second Argument Type | Resulting Type |
|---------------------|----------------------|----------------|
| `String`            | `String`             | `Number`       |
| `Number`            | `String`             | `Number`       |
| `String`            | `Number`             | `Number`       |
| `Number`            | `Number`             | `Number`       |
### `>=` GREATER THAN OR EQUALS Operator
Self-explanatory. 
| First Argument Type | Second Argument Type | Resulting Type |
|---------------------|----------------------|----------------|
| `String`            | `String`             | `Number`       |
| `Number`            | `String`             | `Number`       |
| `String`            | `Number`             | `Number`       |
| `Number`            | `Number`             | `Number`       |
### `<=` LESS THAN OR EQUALS Operator
Self-explanatory. 
| First Argument Type | Second Argument Type | Resulting Type |
|---------------------|----------------------|----------------|
| `String`            | `String`             | `Number`       |
| `Number`            | `String`             | `Number`       |
| `String`            | `Number`             | `Number`       |
| `Number`            | `Number`             | `Number`       |
### `.` DOT Operator
Selects a random operator and executes what that random operator is supposed to do. Basically _shapeshifts_ into another operator at will.
### `..` DUBLEDOT Operator
There's a 50% chance that the first value first be "picked" (and evaluated at the end) and a 50% for the second value to be "picked". Basically a 50/50. This is the operator that is being executed if there are just 2 values standing next to each other, f.e. `"Hey!" 13`. In this case, either `"Hey!"` or `13` will be picked.
### `=` EQUALITY Operator
Compares __values__ of the 2 arguments passed onto it. F.e. `"13" = 13` is true, so it evaluates to `1`.
| First Argument Type | Second Argument Type | Resulting Type |
|---------------------|----------------------|----------------|
| `String`            | `String`             | `Number`       |
| `Number`            | `String`             | `Number`       |
| `String`            | `Number`             | `Number`       |
| `Number`            | `Number`             | `Number`       |
## Why strings become weird numbers
If a string is passed onto an operator that can't generally work with strings (basically if a string __HAS__ to be converted into a number), that string takes a form of an __Ordinal Sum__. Ordinal Sum is a number, that is the sum of each character's unicode representation. For example, "Hey!" converted into it's ordinal sum is this: `72 + 101 + 121 + 33 = 327`.
## Functions
To call a function in T*, you need to use the `->` MIO. Uppercase, lowercase or _random_ case - it doesn't matter, as long as the function exists and the name is correct. Still, usually we use `PascalCase`. You can only provide a single argument to a function. Get ready, because soon everything will get more complicated.

This is an example of how you can print "Hello, World!":
```toster
"Hello, World!" -> Print
```

This example shows how you can use `Goto` and `RunIf` to make loops:
```
1 => a
a -> Print
a + 1 => a
a < 6 -> RunIf
2 -> Goto
"Program ended. Exiting..." -> Print
```
The output of this code is:
```
1
2
3
4
5
Program ended. Exiting...
```
Remember, that boolean as a type doesn't exist, and all possible bools are either 0 or 1. 

Also, make sure you understand that each function is either able to get **just** a number as an argument, **just** a string or **both** (f.e. `Print` accepts both).
## Function descriptions
Here's an explanation of what each function does and what types does it accept. Enjoy reading all of that ^_^

⚠️ **Warning**: Before starting your journey, _please_ read about what `$res` is. [Click here](#what-is-dollar-res).

### `PRINT`: Accepts both `Number` and `String`
Outputs whatever is given to it - it's that simple. Automatically puts a newline character (`"\n"`) at the end of each string.

### `GOTO`: Accepts only `Number`
A simple goto (jump) instruction. Jumps to the given __line__ of the file.

### `RUNIF`: Accepts only `Number`
If whatever is given to it is a `0` then the next line isn't executed, if it's `1` or greater than one then the next line **is** executed. Changes `$res` in this way: if that "next line" was executed, `$res` becomes `1`. Otherwise, `0`.

### `NOT`: Accepts only `Number`
If a `0` is given, sets `$res` to `1`. Otherwise, sets `$res` to `0`.

### `UPPERCASE`: Accepts only `String`
`$res` firstly becomes the string that is given and then is converted to uppercase.

### `LOWERCASE`: Accepts only `String`
`$res` firstly becomes the string that is given and then is converted to lowercase.

### `RANDOMCASE`: Accepts only `String`
`$res` firstly becomes the string that is given and then is converted to *randomcase*.

### `STRIP`: Accepts only `String`
`$res` firstly becomes the string that is given and then is being __trimmed__ or __stripped__, call it whatever you want.

### `NOSPACES`: Accepts only `String`
`$res` firstly becomes the string that is given and then all of the spaces are removed.

### `STARTSWITH`: Accepts only `String`
If whatever is in `$res` starts with the given substring, then `$res` becomes `1`. Otherwise, `0`.

### `ENDSWITH`: Accepts only `String`
If whatever is in `$res` ends with the given substring, then `$res` becomes `1`. Otherwise, `0`.

### `LENGTH`: Accepts both `Number` and `String`
`$res` becomes either the amount of digits in a number or the length of a given string.

### `COUNTUP`: Accepts only `String`
Counts up the amount of that character in a number or a string and then sets the `$res` to that amount.

### `ISSTRING`: Accepts both `Number` and `String`
Sets `$res` to `1` if a given argument is a string, otherwise `$res` becomes 0.

### `ISNUMBER`: Accepts both `Number` and `String`
Sets `$res` to `1` if a given argument is a number, otherwise `$res` becomes 0.

### `EMPOWER`: Accepts only `Number`
If `$res` is not a number, sets it to `-1`.
Otherwise, rises `$res` to the power of `N`, where `N` is the number that was provided.

### `EMROOT`: Accepts only `Number`
If `$res` is not a number, sets it to `-1`.
Otherwise, gets the `N`th root of `$res`, where `N` is the number that was provided.

### `STORE`: Accepts both `Number` and `String`
Simply sets `$res` to the given value.

### `SLEEP`: Accepts only `Number`
Sleeps (waits) for the `N` amount of time, where `N` is the number given to it. Requires __miliseconds__!

### `INPUT`: Accepts only `String`
Requests an input from the user, printing a message beforehand (the message is the string given).

### `RANDOM`: Accepts only `Number`
Generates a pseudo-random number from `1` to `N` including both endpoints, where `N` is the number given.

### `READFILE`: Accepts only `String`
Reads a file with the name `N` and puts it's contents into `$res`, where `N` is the string given. If a file can't be read, sets `$res` to `-1`.

### `WRITEFILE`: Accepts only `String`
Writes whatever is inside of `$res` into a file with the name `N` (rewriting its previous content), where `N` is the string given. If the file doesn't exist yet, creates one. If a file can't be written to / created, sets `$res` to `-1`.

### `DELETEFILE`: Accepts only `String`
Deletes the file with the name `N`, where `N` is the string given. If removal was successful, sets `$res` to `0`. If the file wasn't found, sets `$res` to `-1`. If other error emerged, sets `$res` to `-2`.

### `CREATEDIR`: Accepts only `String`
Creates a directory with the name `N`, where `N` is the string given. Sets `$res` to `0` if the creation was successful. If the directory with that name already exists, sets `$res` to `-1`. If some other error emerges during the creation process, sets `$res` to `-2`. 

### `DELETEDIR`: Accepts only `String`
Deletes the directory with the name `N`, where `N` is the string given. All of the files that were in that directory during the deleting process are also erased. If removal was successful, sets `$res` to `0`. If the directory wasn't found, sets `$res` to `-1`. If other error emerged, sets `$res` to `-2`.

## What is dollar res
`$res` makes this language magical. The concept of it is simple, but the usage may be more complicated. `$res` is being set to 0 once the application starts. You can't manually set `$res` to something you want via the `=>` MIO, however you may use the `STORE` function, but this is rarely required. `$res` is a variable that is being updated based on the previous line (either a function call or a variable assignment). 

There are functions that do __NOT__ update `$res`, f.e. `PRINT` or `GOTO`. Just remember that. Behaviour of functions that __DO__ update `$res` is written in the _Function descriptions_ above.

If the previous line was a variable assignment, f.e. `3 => a`, then `$res` becomes a "link" or a "pointer" of sorts to the value of the newly created variable. This can be used to manipulate variables with spaces and not only that. Don't question why would you want a variable like that - that's why T* is the language of _magic_ 🧙‍♂️.

Here's an example of that link behaviour:
```toster
3 => "LMFAO ..."
$res -> Print
```
This outputs `3`.
## Support
For any questions you can join this discord server (we rarely speak English in there but still can help you in any way - feel free to join): https://discord.gg/NSK7YJ2R6j
## Contribution and Inspiration
This language was heavily inspired by `Kii` and `Kii 2.0` languages - they also are _magical_. Thanks to [ICT](https://github.com/Ict00) ^_^
T* Logo in "Material" style was made by **WaterMelon**.
