import os


class SearchTextInFileHelper:
    def __init__(self, file_path:os.PathLike[str]):
        if not os.path.isfile(file_path):
            raise FileNotFoundError("File not found")
        self.file_path = file_path

    def search_text_in_file_fuzzy(self, text_to_search):
        """
        Search text in file
        :param text_to_search: Text ready to search
        :return: True if exists else False
        """
        with open(self.file_path, "r") as file:
            lines: list[str] = file.readlines()
            for line in lines:
                if text_to_search in line:
                    return True
        return False
    
    def search_text_in_file_exact(self, text_to_search):
        """
        Search text in file
        :param text_to_search: Text ready to search
        :return: matched_text_list -> [(index,whole_matched_text),.....]
        """
        matched_text_list=[]
        with open(self.file_path, "r") as file:
            lines: list[str] = file.readlines()
            for index,line in enumerate(lines):
                if text_to_search in line:
                    start = line.find(text_to_search)
                    end = start + len(text_to_search)
                    whitespace_start = line.rfind(" ", 0, start)
                    whitespace_end = line.find(" ", end)
                    tab_start = line.rfind("\t", 0, start)
                    tab_end = line.find("\t", end)
                    start = max(whitespace_start, tab_start)
                    if whitespace_end == -1:
                        whitespace_end = len(line)
                    if tab_end == -1:
                        tab_end = len(line)
                    end = min(whitespace_end, tab_end)
                    matched_text_list.append((index,line[start+1:end]))
        return matched_text_list

