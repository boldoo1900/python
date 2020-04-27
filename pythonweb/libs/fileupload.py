import os
from werkzeug.utils import secure_filename
from config.constants import Constants

class fileUpload(object):
    @staticmethod
    def upload(files, newName):
        if 'file' not in files:
            return 'No file part'

        file = files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No selected file'

        print(file.content_type)
        if file and fileUpload.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Constants.UPLOAD_DIR, newName))

        return ''

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in Constants.ALLOWED_EXTENSIONS