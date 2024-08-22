class FrontMatterProperty:
    def __init__(self, fullPropertyText):
        self.text = fullPropertyText
        pieces = fullPropertyText.split(':')
        if len(pieces) == 1 and ':' in self.text:
            self.key = self.text.strip()
            self.value = "false"
        elif len(pieces) == 2:
            self.key = pieces[0].strip()
            self.value = pieces[1].strip()
        else:
            raise ValueError
        self.normalise_reference()

    def as_line(self):
        return self.key + ": " + self.value + '\n'

    def normalise_reference(self):
        if "[[" in self.value and "\"[[" not in self.value:
            first_split = self.value.split("[[")
            after_open = first_split[0].strip()
            if len(first_split) >1:
                after_open = first_split[1].strip()
            inside_close = after_open.split("]]")[0].strip()
            if inside_close[0] == "\"" and inside_close[-1] == "\"":
                inside_close = inside_close[1:-1]
            self.value = "\"[["+inside_close+"]]\""
        if self.key[0] == '"' and self.value[-1] == '"':
            self.key = self.key[1:]
            self.value = self.value[:-1]


    def __str__(self):
        return self.key + ": " + self.value