# fm_property.py
# Created: 8/21/2024 by Will Plachno
# Version: 0.0.2.001
# Last Changed: 01/11/2025

class FrontMatterProperty:
    def __init__(self, property_text=None, key=None, value=None):
        self.key = key if key else ""
        self.value = value if value else ""
        self.text = property_text if property_text else ""
        self._decipher_text()
        self._normalise_values()

    def _decipher_text(self):
        """
        If we have been given a string of text to decipher, this method does
        the work of breaking it down into a key and value by splitting on a
        colon.
        If a colon exists in the text, but only one side of the colon has
        text, then we assume that text is the key, and set the value to
        "false".
        If more than one colon exists in the text, we will raise a ValueError.
        :return: None
        """
        if len(self.text) > 0:
            pieces = self.text.split(':')
            if len(pieces) == 1 and ':' in self.text:
                self.key = self.text.strip()
                self.value = "false"
            elif len(pieces) == 2:
                self.key = pieces[0].strip()
                self.value = pieces[1].strip()
            else:
                raise ValueError

    def _normalise_values(self):
        """
        Using this script gives us the opportunity to normalize different
        types of attribute values. Realistically, this is outside the scope,
        but this greatly helps when actually using Obsidian.
        :return:
        """
        self._remove_full_attribute_quotes()
        self._clean_link_values()

    def _clean_link_values(self):
        """
        While the value of a YAML attribute can be pretty much anything, it
        may include a link to another markdown file, though, only ever one.
        These links often get messed up, so we have introduced an auto-cleaner
        that makes sure they are formatted correctly.
        :return:
        """
        if '[[' in self.value and '"[[' not in self.value:
            first_split = self.value.split("[[")
            after_open = first_split[0].strip()
            if len(first_split) >1:
                after_open = first_split[1].strip()
            inside_close = after_open.split("]]")[0].strip()
            if inside_close[0] == '"' and inside_close[-1] == '"':
                inside_close = inside_close[1:-1]
            self.value = '"[['+inside_close+']]"'

    def _remove_full_attribute_quotes(self):
        """
        If the key starts with a " and the value ends with a ", remove both.
        :return:
        """
        if self.key[0] == '"' and self.value[-1] == '"':
            self.key = self.key[1:]
            self.value = self.value[:-1]

    def as_line(self):
        return str(self) + '\n'

    def __str__(self):
        return self.key + ": " + self.value