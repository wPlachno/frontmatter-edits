# frontmatter-edits
A repository of Python scripts for editing the YAML frontmatter in an Obsidian MD vault.
Version 0.0.1.000
Written by Will Plachno. 

## YAML Frontmatter and Obsidian

Many people have some sort of knowledge management system, whether it's as simple as a pen and paper journal, or as complex as a personal wiki. One KMS that the developer of this script uses is Obsidian, a Markdown editor with a full plugin ecosystem and a lot of power. While at its core, Obsidian is just an editor for markdown files (this readme file is an example of a markdown file), it adds a lot of functionality on top of them. With things like the DataView plugin, you can turn your markdown library into a slow-but-still-usable database. A lot of this functionality is dependent on the YAML Frontmatter of Obsidian markdown files.

YAML Frontmatter sounds complex, but it's not as bad as you may believe. YAML is basically a way to describe key-value pairs, and "frontmatter" just means it has a special place at the beginning of a markdown file. The benefit is that users can apply attributes to their markdown files. For example, the developer uses Obsidian to generate a daily journal for them to write in. Each daily journal is represented as a markdown file, including some data-tracking frontmatter such as whether they remembered to brush their teeth that evening, or how many hours of sleep they got.

While Obsidian makes it easy to use this data through plugins, applying and maintaining frontmatter can be finicky. Obsidian has a built in templating system that is great for auto-generating different 'types' of markdown files, but if you get halfway through and realize you need to add a new attribute, it can be time-consuming and headache-inducing to do so by hand. 

This script was originally intended to make that process a little less hair-loss-inducing. Using this script, a user will be able to add, set, remove, or change frontmatter attributes, or just see which frontmatter attributes exist in the chosen directory. 

## Interface

Frontmatter-edits, or frontmat, was initially designed to use an interactive terminal-based menu system. After initially calling the script, the script would welcome the user, then ask them to select the directory that this call of the script would be interested in. Once the directory is known, the user would enter the main menu.

### Main Menu

The main menu allows the user to select a primary mode - Add, Set, Change, Remove,  or Total, - or to change or clear the target directory. The main menu will continually redisplay until the user chooses to quit. 

### The Modes

Frontmat allows for frontmatter attributes to be added, set, changed, or removed. While removing an attribute is pretty clear, adding, setting, and changing attributes are all similar shades of the same functionality. Generally, we create the attribute if it doesn't exist and modify the value of the attribute if it does. *Add* will create but not modify, *Set* does both, and *Change* will only edit if the attribute already exists. 

| Mode     | Creates | Modifies |
|----------|---------|----------|
| Add      | Yes     | No       |
| Set      | Yes     | Yes      |
| Change   | No      | Yes      |




