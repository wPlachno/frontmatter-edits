import pathlib

from utilities import wcutil
from fm_file import WoodchipperObsidianFile
from fm_property import FrontMatterProperty
import constants as S
class FrontMatterActor:

    def __init__(self, directory, property_text, type):
        self.directory = directory
        self.directory_path = pathlib.Path(self.directory)
        self.property = FrontMatterProperty(property_text)
        self.type = type
        self.file_list = list(())
        self.affected = list(())
        self.summery_frame = "{0} files printed: \n"

    def run(self):
        # Get file list
        for file in self.directory_path.iterdir():
            if wcutil.tail_matches_token(file.name, S.MD):
                self.file_list.append(WoodchipperObsidianFile(file.resolve()))
        # for each file, run action
        for file in self.file_list:
            file.read()
            if self.action(file):
                self.affected.append(file)
            file.write()

    def action(self, file):
        print(S.FRAME_PLAIN_ACTION.format(self.type, self.property, file.name))
        return True

    def summarize(self):
        summary_string = self.summarize_short() + S.NL
        for affected_file in self.affected:
            summary_string += S.FRAME_SUMMARY_ITEM.format(affected_file.name)
        return summary_string
    def summarize_short(self):
        return S.FRAME_SUMMARY_HEADER.format(len(self.affected))

class FrontMatterActor_ADD(FrontMatterActor):
    def action(self, file):
        return file.add_property_if_missing(self.property)

class FrontMatterActor_SET(FrontMatterActor):
    def action(self, file):
        return file.set_property_value_or_add(self.property)

class FrontMatterActor_CHANGE(FrontMatterActor):
    def action(self, file):
        return file.change_property_value_if_exists(self.property)

class FrontMatterActor_REMOVE(FrontMatterActor):
    def action(self, file):
        return file.remove_property(self.property)

class FrontMatterActor_TOTAL(FrontMatterActor):
    def __init__(self,directory,property=S.FAKE_PROPERTY,type=S.MODE_TOTAL):
        FrontMatterActor.__init__(self,directory,property,type)
        self.total = {}
        self.summary = S.EMPTY

    def action(self, file):
        for file_property in file.properties:
            if file_property.key in self.total:
                self.total[file_property.key].append(file.name)
            else:
                self.total[file_property.key] = list((file.name,))
        return True

    def run(self):
        FrontMatterActor.run(self)
        self.summary = S.FRAME_PROPERTIES_IN.format(self.directory.resolve()) + '\n'
        for key in sorted(self.total.keys()):
            self.summary = self.summary + S.FRAME_PROPERTY.format(key, str(self.total[key])) + '\n'


actorByType = {
    S.MODE_ADD: FrontMatterActor_ADD,
    S.MODE_SET: FrontMatterActor_SET,
    S.MODE_CHANGE: FrontMatterActor_CHANGE,
    S.MODE_REMOVE: FrontMatterActor_REMOVE,
    S.MODE_TOTAL: FrontMatterActor_TOTAL
}
def create_actor(directory,property_text,type):
    return actorByType[type](directory, property_text, type)