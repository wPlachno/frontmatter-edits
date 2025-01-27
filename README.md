# frontmatter-edits
A repository of Python scripts for editing the YAML frontmatter in an Obsidian MD vault.

Created by Will Plachno
Started on 8/22/24
Version 0.0.2.004
Updated on 01/27/25

## YAML Frontmatter and Obsidian

Many people have some sort of knowledge management system, whether it's as simple as a pen and paper journal, or as complex as a personal wiki. One KMS that the developer of this script uses is Obsidian, a Markdown editor with a full plugin ecosystem and a lot of power. While at its core, Obsidian is just an editor for markdown files (this readme file is an example of a markdown file), it adds a lot of functionality on top of them. With things like the DataView plugin, you can turn your markdown library into a slow-but-still-usable database. A lot of this functionality is dependent on the YAML Frontmatter of Obsidian markdown files.

YAML Frontmatter sounds complex, but it's not as bad as you may believe. YAML is basically a way to describe key-value pairs, and "frontmatter" just means it has a special place at the beginning of a markdown file. The benefit is that users can apply attributes to their markdown files. For example, the developer uses Obsidian to generate a daily journal for them to write in. Each daily journal is represented as a markdown file, including some data-tracking frontmatter such as whether they remembered to brush their teeth that evening, or how many hours of sleep they got.

While Obsidian makes it easy to use this data through plugins, applying and maintaining frontmatter can be finicky. Obsidian has a built in templating system that is great for auto-generating different 'types' of markdown files, but if you get halfway through and realize you need to add a new attribute, it can be time-consuming and headache-inducing to do so by hand. 

This script was originally intended to make that process a little less hair-loss-inducing. Using this script, a user will be able to add, set, remove, or change frontmatter attributes, or just see which frontmatter attributes exist in the chosen directory. 

## Interface

Frontmatter-edits, or frontmat, was initially designed to use an interactive terminal-based menu system. After initially calling the script, the script would welcome the user, then ask them to select the directory that this call of the script would be interested in. Once the directory is known, the user would enter the main menu. This interface style has been deprecated (though can still be accessed in the 'menu_style' git branch). 

The modern version (starting with version 0.0.2.001) has a pure command-line interface based on the WoodchipperCore system. 

### The Modes

Frontmat allows for frontmatter attributes to be added, set, changed, or removed. While removing an attribute is pretty clear, adding, setting, and changing attributes are all similar shades of the same functionality. Generally, we create the attribute if it doesn't exist and modify the value of the attribute if it does. *Add* will create but not modify, *Set* does both, and *Change* will only edit if the attribute already exists. 

| Mode     | Creates | Modifies |
|----------|---------|----------|
| Add      | Yes     | No       |
| Set      | Yes     | Yes      |
| Change   | No      | Yes      |

Reading the markdown library can happen in two ways: Summarize and Show. Summarize will list the keys of properties found in the frontmatter of the target markdown files. Show will focus in on a specific key, noting the different values and the names of the files that have each.

#### Mode: Summarize

This is the mode that is assumed if no other mode is included in the command-line call. For example, calling `frontmat` alone will display the property information in the markdown files in the current working directory. 

Normally, it will list each Property Key followed by how many times that property is set and how many unique values that property has been set to. At the end of the property list, it will also list the number of unique properties, the number of unique values, and how many properties have been set.

If you increase the verbosity to 3, you'll see the normal WoodchipperCore debug information (Profile, Request, and Response dataa), followed by the markdown files that were checked for this call. Each property will also be followed by the unique values that property was set to and how many times that value is used.

#### Mode: Show

To get more details about a specific property, the user can operate with the mode Show. The user will supply a specific property key, and the script will print out each value assigned to that key, which files that value exists in, then summarize the key with the number of files the property exists in and how many unique values appear. 

The mode output does not change between verbosity 2 and 3. 

If the key does not appear in the target files, the script will print out the key with 0 occurrences and 0 values. 

#### Mode: Add

The first of the property editor modes, add will add the key with the given value as a property if and only if the property does not already exist in the markdown file. 

Currently, running this mode in verbosity 2 (Normal) will print out the summary: how many target files existed, how many had the property added, and how many target files were skipped because they already had the property defined. Running in verbosity 3 (debug) will also print out each target file, its previous value attached to the key, its new value attached to the key, and whether the value appeared to be added or skipped. 

#### Mode: Remove

This mode will completely remove a property from every target file. If a filter flag is included, properties will only be removed if the value of the property matches the target filter value.

### The Directory Flag

While frontmat is aware of the standard WoodchipperCore flags (config, verbose, debug), it is mainly concerned with the `-directory` flag, which should be followed by a directory path to use as the containing directory for the markdown files we want to affect. 

Without this flag, frontmat assumes the user is interested only in the files in the working directory. This flag allows you to edit frontmatter of markdown files in a different location. 

When combined with target arguments (specific files), the target files act as a filter of the files in the correct directory. 

### The Filter Flag

This flag can further filter functionality based on the previous value of a property. For example, `frontmat set genre indie -f "artist:Bright Eyes"` will set the `genre` property to the value `indie` for all files where the `artist` property is already set to `Bright Eyes`. 

The argument passed after the `-f` flag should conform to the format "[property_key]:[property_value]", including the quotation marks. the property value must match the filter value exactly for the functionality to be performed - there is currently no support for other comparisons. Only one property filter is allowed per script-use. 

## TODO:

- Test thoroughly, particularly:
  - Mode: Show
  - Mode: Add
  - Mode: Change
  - Mode: Set
  - Mode: Remove
  - Debug off for all of these.
- Expand this file to reflect all modes.


