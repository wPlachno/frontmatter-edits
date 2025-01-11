# fm_file.py
# Created: 8/22/24 by Will Plachno
# Version: 0.0.2.001
# Last Changed: 01/11/2025

from utilities.wcutil import WoodChipperFile
from fm_property import FrontMatterProperty
import constants as S


class FrontMatterFile(WoodChipperFile):

    def __init__(self, file_path):
        WoodChipperFile.__init__(self,file_path)
        self.properties = list(())
        # properties_start = index of first attribute
        self.properties_start = -1
        # properties_end = index of second frontmatter token.
        self.properties_end = -1

    def read(self):
        WoodChipperFile.read(self)
        self._find_frontmatter_tokens()
        for line in self.text[self.properties_start:self.properties_end]:
            if len(line) > 3:
                self.properties.append(FrontMatterProperty(line))

    def _find_frontmatter_tokens(self, add_if_missing=True):
        """
        Finds and records the indices of the start and end frontmatter tokens
        in the file. These tokens are expected to consist of three quotation
        marks with nothing else in that line of text.
        :param add_if_missing: Whether we should add the tokens to the file
        if they are missing, or just raise an exception.
        :return: No return value, but will change the properties_start and
        properties_end
        """
        # Grab the indices of lines with the frontmatter token.
        front_matter_indices = [index for index, line in enumerate(self.text) if S.FM_TOKEN in line]
        if len(front_matter_indices) < 2:
            if add_if_missing:
                self.text.insert(0, S.FM_LINE)
                self.text.insert(0, S.FM_LINE)
                front_matter_indices = list((0,1))
            else:
                raise Exception(f"No frontmatter detected in {self.name}")
        self.properties_start = front_matter_indices[0]+1
        self.properties_end = front_matter_indices[1]


    def write(self):
        self.set_properties()
        WoodChipperFile.write(self)

    def set_properties(self):
        # Check if the amount of properties has changed
        text_property_length = self.properties_end - self.properties_start
        number_added = len(self.properties) - text_property_length
        target_index = 0
        # Save each attribute by either modifying the line or adding one.
        for index, prop_item in enumerate(self.properties):
            target_index = index+self.properties_start
            if index < text_property_length:
                self.text[target_index] = prop_item.as_line()
            else:
                self.text.insert(target_index, prop_item.as_line())
        # Remove any extraneous lines
        if number_added < 0:
            target_index = target_index+1
            to_be_removed = number_added
            while to_be_removed != 0:
                self.text.pop(target_index)
                to_be_removed = to_be_removed+1

        self.properties_end += number_added
        if self.text[self.properties_end+1].strip() != S.EMPTY:
            self.text.insert(self.properties_end+1, S.NL)

    def find_property(self,prop_item):
        for target_property in self.properties:
            if target_property.key == prop_item.key:
                return target_property
        return None


    def add_property_if_missing(self, prop_item):
        target_property = self.find_property(prop_item)
        if target_property:
            return False
        self.properties.append(prop_item)
        return True

    def set_property_value_or_add(self, prop_item):
        target_property = self.find_property(prop_item)
        if target_property:
            if target_property.value != prop_item.value:
                target_property.value = prop_item.value
                return True
            else:
                return False
        self.properties.append(prop_item)
        return True

    def change_property_value_if_exists(self,prop_item):
        target_property = self.find_property(prop_item)
        if target_property and target_property.value != prop_item.value:
            target_property.value = prop_item.value
            return True
        return False

    def remove_property(self, prop_item):
        target_property = self.find_property(prop_item)
        if target_property:
            self.properties.remove(target_property)
            return True
        return False

    def incorporate_properties(self, other):
        for other_prop in other.properties:
            self.add_property_if_missing(other_prop)
