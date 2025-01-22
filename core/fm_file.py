# fm_file.py
# Created: 8/22/24 by Will Plachno
# Version: 0.0.2.002
# Last Changed: 01/22/2025

from utilities.wcutil import WoodChipperFile
from core.fm_property import FrontMatterProperty
import constants as S


class WoodchipperObsidianFile:

    def __init__(self, file_path):
        self.file = WoodChipperFile(file_path)
        self.properties = list(())
        self.content = list(())

    def read(self):
        self.file.read()
        property_text = self._grab_content_and_frontmatter()
        for line in property_text:
            if len(line) > 3:
                self.properties.append(FrontMatterProperty(line))
    
    def _grab_content_and_frontmatter(self):
        property_text = list(())
        front_matter_indices = [index for index, line in enumerate(self.file.text) if S.FM_TOKEN in line]
        if len(front_matter_indices) == 0:
            self.content = self.file.text[:]
        else:
            property_text = self.file.text[front_matter_indices[0]+1:front_matter_indices[1]]
            self.content = self.file.text[(front_matter_indices[1]+1):]
        del self.file.text
        self.file.text = list(())
        return property_text


    def write(self):
        if not self.content:
            self.content = list(())
        self.file.text = [S.FM_LINE] + self._compile_properties() + [S.FM_LINE] + self.content
        self.file.write()
        del self.content
    
    def _compile_properties(self):
        property_list = list(())
        for property_item in self.properties:
            property_list.append(property_item.as_line())
        return property_list

    def __getitem__(self, item):
        if type(item) == str:
            for target_property in self.properties:
                if target_property.key == item:
                    return target_property.value
            return None
        elif type(item) == int:
            if -1 < item < len(self.content):
                return self.content[item]
            return None
        else:
            raise Exception(f"Cannot interpret the type '{type(item)}' as an index for a frontmatter file.")

    def __setitem__(self, key, value):
        if type(key) == str:
            for target_property in self.properties:
                if target_property.key == key:
                    target_property.value = value
        elif type(key) == int:
            if -1 < key < len(self.content):
                self.content[key] = value
        else:
            raise Exception(f"Cannot interpret the type '{type(key)}' as an index for a frontmatter file.")

    def __delitem__(self, key):
        if type(key) == str:
            for target_property in self.properties:
                if target_property.key == key:
                    self.properties.remove(target_property)
                    del target_property
        elif type(key) == int:
            if -1 < key < len(self.content):
                del self.content[key]
        else:
            raise Exception(f"Cannot interpret the type '{type(key)}' as an index for a frontmatter file.")

    def __contains__(self, item):
        if type(item) == str:
            for target_property in self.properties:
                if target_property.key == item:
                    return True
        elif type(item) == int:
            if -1 < item < len(self.content):
                return True
        else:
            raise Exception(f"Cannot interpret the type '{type(item)}' as an index for a frontmatter file.")
        return False

    def set_property(self, key, value, add_if_necessary=False, change_if_existing=False):
        if add_if_necessary or change_if_existing:
            target_property = self[key]
            found = bool(target_property)
            if found and change_if_existing:
                self[key] = value
            elif not found and add_if_necessary:
                self.properties.append(FrontMatterProperty(key=key, value=value))
        return self[key]

    def remove_property(self, key):
            for target_property in self.properties:
                if target_property.key == key:
                    self.properties.remove(target_property)
                    return True
            return False
