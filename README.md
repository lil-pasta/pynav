
# Table of Contents

1.  [Introduction and Purpose](#org6dd0ff4)
2.  [Roadmap](#orgf9d82e0)
    1.  [<code>[3/3]</code> Crawling](#org21f7ae2)
    2.  [<code>[2/4]</code> Walking](#orgb0e81e3)



<a id="org6dd0ff4"></a>

# Introduction and Purpose

The purpose of this application is create a console based file manager application which allows for the in-terminal navigation of a nix based machine. 
The program features python code leveraging builtin packages like ncurses and os. The initial idea for this was inspired by applications like lfm so a huge thank you to the people who created them!


<a id="orgf9d82e0"></a>

# Roadmap

This is where ill keep track of work that i've done on features that I'd like to have in the application


<a id="org21f7ae2"></a>

## <code>[3/3]</code> Crawling

-   [X] Get all files and folders in working dir
-   [X] Add them to a dict or list or class with relevant meta-data attached
-   [X] Print them to terminal and make them high-light-abable through navigation gestures like key up and down


<a id="orgb0e81e3"></a>

## <code>[2/4]</code> Walking

-   [X] Make list of files scrollable
-   [ ] Handle filenames larger than your window
-   [X] differentiate between directories and files
-   [ ] if an item is a file display some facts about it in the third screen

