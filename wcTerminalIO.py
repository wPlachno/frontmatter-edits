import pathlib
import readline

screenWidth = 68
screenBorder = '*'
class ScreenDisplay:
    class Form:
        def __init__(self, width):
            self.width = width
            self.frame = "{0}"
            self.divider = False

    def __init__(self, text, width=screenWidth, border=screenBorder, header=None, pause=False):
        self.text = text
        self.width = width
        self.border = border
        self.header = header
        self.pause = pause
        self.reply = ""
        self.cancel = False
        self.preDisplay = list(())
        self.postDisplay = list(())
        self.form = self.Form(self.width)
        if self.border:
            self.form.frame = self.border + " {0} " + self.border
            self.form.width -= 2*(1+len(self.border))
            self.form.divider = self.border * self.width

    def add_predisplay_method(self,method):
        self.preDisplay.append(method)
        return self
    def add_postdisplay_method(self,method):
        self.postDisplay.append(method)
        return self
    def set_format(self, width=screenWidth, border=screenBorder):
        self.width = width
        self.border = border
        return self
    def display(self):
        for preFunc in self.preDisplay:
            preFunc(self)
        self.format(self.text)
        if self.pause:
            self.reply = input("Continue? ").strip()
            self.check_for_quit()
        if self.cancel:
            return not self.cancel

        for postFunc in self.postDisplay:
            postFunc(self)
        return not self.cancel
    def format(self,text):
        print()
        if self.header:
            if self.border:
                print(self.form.divider)
            space = self.form.width - len(self.header)
            print(self.form.frame.format((" "*space) + self.header))
        if self.border:
            print(self.form.divider)
        buffer = text
        while buffer:
            end_index = 0
            space_index = 0
            if len(buffer) == 0:
                break;
            max_length = min(self.form.width+1, len(buffer))
            for index in range(0, max_length):
                current = buffer[index]
                if current == '\n':
                    end_index = index
                    break
                elif current == ' ':
                    space_index = index
            else:
                if index+1 == len(buffer):
                    end_index = index+1
                else :
                    if buffer[index] == ' ':
                        space_index = index
                    end_index = space_index
            space = (self.form.width-end_index)*' '
            print(self.form.frame.format(buffer[:end_index] + space))
            if(end_index+1 > len(buffer)):
                buffer = None
            else:
                buffer = buffer[end_index+1:]
        if self.border:
            print (self.form.divider)
    def check_for_quit(self):
        tokens = self.reply.upper().strip()
        if len(tokens) > 0 and tokens[0] == 'Q':
            if len(tokens) == 1:
                self.cancel = True
            elif tokens[1].isspace() or tokens[1] == 'U':
                self.cancel = True
        return self.cancel

class ScreenPrompt(ScreenDisplay):
    def __init__(self, text, prompt="Please enter: ", width=screenWidth, border=screenBorder, header=None, autoList=None):
        ScreenDisplay.__init__(self, text, width, border, header)
        self.auto_complete_tokens = autoList
        self.prompt = prompt
        self.validators = list(())
        self.reply = ""
        self.warning = ""
        self.add_postdisplay_method(self.collect_from_user)
    def validate_reply(self):
        if self.check_for_quit():
            return self.cancel
        if len(self.validators) > 0:
            valid = True
            for validator in self.validators:
                valid = valid and validator(self,self.reply)
            return valid
        return True

    def add_validator(self, validator):
        self.validators.append(validator)
        return self

    def collect_from_user(self, screen):
        if self.auto_complete_tokens:
            self.auto_complete_tokens = sorted(self.auto_complete_tokens)
            self.auto_complete_sessions = None
            readline.set_completer(self.complete)
            readline.parse_and_bind("tab: complete")

        self.reply = input(self.prompt).strip()
        while not self.validate_reply():
            self.format(self.warning)
            self.reply = input(self.prompt).strip()

        if self.auto_complete_tokens:
            readline.set_completer()

    def complete(self, text, sessionID):
        target_session = None
        if sessionID == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.auto_complete_sessions = list(())
                for token in self.auto_complete_tokens:
                    if token.startswith(text):
                        self.auto_complete_sessions.append(token)
            else:
                self.auto_complete_sessions = self.auto_complete_tokens.copy()

        # Return the state'th item from the match list,
        # if we have that many.
        try:
            target_session = self.auto_complete_sessions[sessionID]
        except IndexError:
            target_session = None
        return target_session



class ScreenConfirm(ScreenPrompt):
    def __init__(self, text, width=screenWidth, border=screenBorder, header=None):
        ScreenPrompt.__init__(self, text, "Please confirm (Y/N): ", width, border, header)
        self.warning = "Please confirm that you would like to proceed."
        self.confirm = False
        self.add_postdisplay_method(self.confirm_reply)
        self.add_validator(Create_String_Validator(lambda a: "Y" in a.upper() or "N" in a.upper()))
    def confirm_reply(self, screen):
        self.confirm = "Y" in self.reply.upper()

class ScreenMenu(ScreenPrompt):
    def __init__(self, options, width=screenWidth, border=screenBorder, header=None):
        self.options = options
        text = ''
        for index, option in enumerate(self.options):
            text += str(index+1) + ". " + option
            if (index+1 < len(self.options)):
                text+='\n'
        ScreenPrompt.__init__(self, text, "Your choice (1,2,etc): ", width, border, header)
        self.warning = "Please select a valid option by typing the number associated with your choice.\n"+self.text
        self.choice = -1
        self.add_validator(Create_Range_Validator(range(0, len(self.options)), -1))

class ScreenDirectory():
    def __init__(self, startingDirectoryPath=None, directoryDescription="This directory path will be used in the rest of the program."):

        self.directory_path = startingDirectoryPath
        if not self.directory_path:
            self.directory_path = pathlib.Path().resolve()
        self.previous_path = self.directory_path
        self.description = directoryDescription

        self.success = False
        self.canceled = False
        self.status = "Starting at {0}".format(self.directory_path)
        self.move_tokens = {".": self.move_to_parent_folder, "-": self.move_to_previous, "/": self.move_to_drive_root_or_relative_path, "\\": self.move_to_drive_root_or_relative_path, "~": self.move_to_home, "Y": self.confirm_current_path, "Q": self.cancel_current_path}
        self.entry_text = "Please enter a directory. {0} If you simply hit enter, the chosen path will be '{1}'.".format(self.description, self.directory_path)
        self.prompt = "Please enter a Directory Path: "
        self.core_completions = { str(self.previous_path) }

    def display(self):
        reply = self.entry_display()
        while self.execute_reply(reply):
            reply = self.confirmation_display()
        return self.success

    def entry_display(self):
        screen = ScreenPrompt(self.entry_text, self.prompt)
        screen.display()
        return screen.reply.strip()

    def describe_directory(self):
        # - Current Directory
        # - Subdirectories of current directory
        # - Number of files
        # - Allow hook for custom
        prompt_frame = "Current Directory: {0}\nNumber of Files: {1}\nSubdirectories:\n{2}Once you have found the directory you wish to choose, please input 'Y'."
        number_of_files = 0
        self.current_completions = self.core_completions.copy()
        subdirectory_frame = "- /{0}\n"
        subdirectory_total = ""
        for item in pathlib.Path(self.directory_path).iterdir():
            if item.is_dir():
                subdirectory_total += subdirectory_frame.format(item.name)
                self.current_completions.add("/{0}".format(item.name))
            elif item.is_file():
                number_of_files += 1
        return prompt_frame.format(self.directory_path, number_of_files, subdirectory_total)


    def confirmation_display(self):
        text = self.describe_directory()
        prompt = "{0}: ".format(self.directory_path)
        screen = ScreenPrompt(text, prompt, header=self.status, autoList=list(self.current_completions))
        screen.display()
        return screen.reply.strip()

    def execute_reply(self, reply):
        if len(reply) < 1:
            return True
        first_char = reply[0].upper()
        if first_char in self.move_tokens:
            return self.move_tokens[first_char](reply)
        else:
            return self.move_to_path(reply)

    def move_to_path(self, reply):
        if pathlib.Path(reply).exists():
            self.set_path(reply)
        else:
            self.set_status("Path does not exist: {0}".format(reply))
        return True
    def move_to_parent_folder(self, reply):
        if len(reply) == 2:
            # Set directory path to parent
            parent_path = pathlib.Path(self.directory_path).parent.resolve()
            self.set_path(parent_path)
        else:
            self.set_status("Invalid Entry, Still at", True)
        return True
    def move_to_drive_root_or_relative_path(self, reply):
        if len(reply) == 1:
            # Move to drive root
            drive_root = pathlib.Path(pathlib.Path(self.directory_path).anchor).resolve()
            self.set_path(drive_root)
        else:
            self.move_to_path(self.directory_path / pathlib.Path(reply[1:]))
        return True
    def move_to_previous(self, reply):
        self.set_path(self.previous_path)
        return True
    def move_to_home(self, reply):
        self.set_path(pathlib.Path.home())
        return True
    def confirm_current_path(self, reply):
        self.success = True
        self.canceled = False
        self.set_status("Confirmed", True)
        return False
    def cancel_current_path(self, reply):
        self.success = False
        self.canceled = True
        self.set_status("Directory choice cancelled.")
        return False

    def set_path(self, newPath):
        new_auto_token = str(self.previous_path)
        if new_auto_token not in self.core_completions:
            self.core_completions.add(new_auto_token)
        self.previous_path = self.directory_path
        self.directory_path = newPath
        self.set_status("Moved", True)

    def set_status(self, action, includeDirectory=False):
        if includeDirectory:
            self.status = "{0}: {1}".format(action, self.directory_path)
        else:
            self.status = action



def Create_String_Validator(string_validator):
    def validate_to_string(screen, reply):
        return string_validator(reply)
    return validate_to_string

def Create_Number_Validator(tap_number=0):
    def validate_to_number(screen, reply):
        try:
            screen.choice = int(reply)+tap_number
            return True
        except ValueError:
            return False
    return validate_to_number

def Create_Range_Validator(valid_range, tap_number=0):
    def validate_to_range(screen, reply):
        try:
            screen.choice = int(reply)+tap_number
            return screen.choice in valid_range
        except ValueError:
            return False
    return validate_to_range
