import pathlib as p
from natsort import natsorted
from gui.message_popup import MessagePopup

class ImageRenamer:
    def __init__(self):
        self.image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        self.MAX_LEADING_ZEROS = 10

    def validate_directory(self, base_directory):
        if not base_directory:
            self._show_error("Please select a valid directory.")
            return False
            
        if not p.Path(base_directory).is_dir():
            self._show_error(f"The path {base_directory} is not a valid directory.")
            return False
        
        return True

    def validate_start_number(self, start_number):
        try:
            return int(start_number) if start_number.strip() else 1
        except ValueError:
            self._show_error("Starting number must be a valid integer")
            return None

    def rename_files(self, base_directory, use_leading_zeros, use_custom_name, custom_name, start_number, 
                     continue_numbering, number_of_leading_zeros, sort_by, sort_direction):
        if not self.validate_directory(base_directory):
            return
            
        initial_counter = self.validate_start_number(start_number)
        if initial_counter is None:
            return

        counter = initial_counter

        for root, _, files in p.Path(base_directory).walk():
            dir_name = p.Path(root).name

            if not files:
                continue

            image_files = self._sort_files(files, root, sort_by, sort_direction)
            
            if not image_files:
                continue

            try:
                if not continue_numbering:
                    counter = initial_counter
                counter = self._process_directory(root, image_files, dir_name, counter,
                                               use_leading_zeros, use_custom_name, custom_name, number_of_leading_zeros)
            except Exception as e:
                self._show_error(f"Error renaming files: {str(e)}")
                return

        self._show_success()

    def _sort_files(self, files, root, sort_by, sort_direction):
        image_files = [f for f in files if p.Path(f).suffix.lower() in self.image_extensions]
        
        if not image_files:
            return []

        reverse = sort_direction == "desc"
        
        if sort_by == "name":
            return natsorted(image_files, reverse=reverse)
        
        if sort_by == "creation_date":
            return sorted(image_files, 
                        key=lambda x: p.Path.joinpath(root, x).stat().st_birthtime,
                        reverse=reverse)
        
        if sort_by == "modified_date":
            return sorted(image_files,
                        key=lambda x: p.Path.joinpath(root, x).stat().st_mtime,
                        reverse=reverse)
        
        return []

    def _process_directory(self, root, image_files, dir_name, counter, use_leading_zeros, use_custom_name, custom_name, number_of_leading_zeros):
        # First pass: Create temporary files
        temp_files = self._create_temp_files(root, image_files)
        
        # Second pass: Rename to final names
        return self._rename_to_final(root, temp_files, dir_name, counter,
                                   use_leading_zeros, use_custom_name, custom_name, number_of_leading_zeros)

    def _create_temp_files(self, root, image_files):
        temp_files = []
        for idx, file_name in enumerate(image_files):
            original_path = p.Path.joinpath(root, file_name)
            temp_name = f"__temp_{idx}{p.Path(file_name).suffix}"
            temp_path = p.Path.joinpath(root, temp_name)
            
            try:
                p.Path.rename(original_path, temp_path)
                temp_files.append((temp_path, file_name))
            except Exception as e:
                self._revert_temp_files(temp_files, root)
                raise e
                
        return temp_files

    def _rename_to_final(self, root, temp_files, dir_name, counter, use_leading_zeros, use_custom_name, custom_name, number_of_leading_zeros):
        for temp_path, _ in temp_files:
            file_extension = p.Path(temp_path).suffix
            prefix = self._get_prefix(use_custom_name, custom_name, dir_name)
            new_name = self._format_new_name(prefix, counter, file_extension, use_leading_zeros, number_of_leading_zeros)
            new_path = p.Path.joinpath(root, new_name)

            try:
                p.Path.rename(temp_path, new_path)
                counter += 1
            except Exception as e:
                self._revert_temp_files([f for f in temp_files if p.Path(f[0]).exists()], root)
                raise e
                
        return counter

    def _get_prefix(self, use_custom_name, custom_name, dir_name):
        if use_custom_name:
            return f"{custom_name.strip()}-" if custom_name.strip() else ""
        return f"{dir_name}-"

    def _format_new_name(self, prefix, counter, file_extension, use_leading_zeros, number_of_leading_zeros):
        if use_leading_zeros:
            zeros = max(1, int(number_of_leading_zeros))
            zeros = min(zeros, self.MAX_LEADING_ZEROS)
            return f"{prefix}{counter:0{zeros}d}{file_extension}"
        return f"{prefix}{counter}{file_extension}"

    def _revert_temp_files(self, temp_files, root):
        for temp_path, original_name in temp_files:
            try:
                p.Path.rename(temp_path, p.Path.joinpath(root, original_name))
            except:
                pass

    def _show_error(self, message):
        MessagePopup.show_error(message)

    def _show_success(self):
        MessagePopup.show_success("Files renamed successfully")
