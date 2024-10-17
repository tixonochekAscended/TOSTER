<p align="center">
<a href="https://ibb.co/V2GYm6g"><img src="https://i.ibb.co/zGgVJdX/T-Logo-1.png" width=250 height=250></a>
</p>

------------------------
# T* - A programming language.
T* is an interpreted, esoteric programming language created by me _(tixonochek)_. Usually people don't refer to T* by language's official name but call it **toster** (read as: toaster). This name derives from the fact that symbol `*` is an **asterisk**. If we shorten that word we get **aster**, and for the language to not have a meaningless alias **Taster** it's called **Toster**, symbolising a nice, working toaster which can be seen on the logo of the language.

### Links for fast travel in this file & documentation
1. [Main Concept](#main-concept)

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
```
// This is a comment ^_^
"..." -> Print
```
However this would be executed flawlessly:
```
"..." -> Print // This is a comment ^_^
```

------------------------
# Documentation
