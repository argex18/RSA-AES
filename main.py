try:
    import sys
    from traceback import print_exc

    import cipher
    import gui
except ImportError:
    print(ImportError)
    exit(-1)


class Main:
    def __init__(self):
        self.app = gui.QtWidgets.QApplication(sys.argv)
        self.__setGui()
    
    def __setGui(self):
        self.MainWindow = gui.QtWidgets.QMainWindow()
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

    def generate(self):
        keys = cipher.generateRSAkeys('pemkeys.pem')
        pbk = self.ui.pbk
        prk = self.ui.prk

        public_key = keys[0]
        private_key = keys[1]

        if len(keys) != 0:
            pbk.setText( str( public_key.exportKey(format='PEM'), encoding='ascii' ) )
            prk.setText( str( private_key.exportKey(format='PEM'), encoding='ascii' ) )

            self.ui.confirm_button.setDisabled(False)
    
    def fileDialog(self):
        file_name = gui.QtWidgets.QFileDialog.getOpenFileName(parent=self.MainWindow, directory='/', filter='*.pdf;;*.jpg;;*.*')
        print(file_name)

        if file_name[0] != '':
            format_type = file_name[0][file_name[0].rfind('.'):len(file_name[0])]

            if self.ui.mode_button.currentIndex() == 0:
                input_path = file_name[0]
                output_path = input_path.replace(format_type, '.json')

                encrypted_data = cipher.runAESencryption(input_path=input_path, output_path=output_path)

                # Saving the file extension to the output file
                file_extension = format_type
                with open(output_path, 'rb') as f:
                    file_obj = cipher.json.loads( f.read().decode('utf-8-sig') )
                    file_obj['type'] = file_extension
                file_obj = cipher.json.dumps(file_obj, indent=5)
                with open(output_path, 'wb') as f:
                    f.write( file_obj.encode('utf-8-sig') )

                if encrypted_data != None:
                    print('Successfully encrypted')
                else:
                    print('Error during encryption')
            else:
                input_path = file_name[0]

                # Reading the file extension from the input file
                file_extension = None
                with open(input_path, 'rb') as f:
                    file_extension = cipher.json.loads( f.read().decode('utf-8-sig') )['type']
                output_path = input_path.replace(format_type, file_extension)

                decrypted_data = cipher.runAESdecryption(input_path=input_path, output_path=output_path)

                if decrypted_data != None:
                    print('Successfully decrypted')
                else:
                    print('Error during decryption')
    
    def checkText(self):
        pbk = self.ui.pbk
        prk = self.ui.prk
        if pbk.toPlainText() == '' or prk.toPlainText() == '':
            self.ui.confirm_button.setDisabled(True)
        

class Slot:
    def __init__(self, callback, arg=None):
        try:
            if not callable(callback) or not isinstance(arg, tuple):
                raise TypeError('ERROR: the argument types must be the following: callback = function, arg = tuple')

            self.callback = callback
            self.arguments = arg
        except Exception:
            print_exc()
            self.callback = None
            self.arguments = None
    
    def execute(self):
        try:
            if self.callback == None:
                raise Exception('ERROR: the callback was not defined')

            if self.arguments == None:
                self.callback()
            else:
                for arg in self.arguments:
                    self.callback([arg for arg in self.arguments])
        except Exception:
            print_exc()


if __name__ == '__main__':
    try:
        main = Main()
        generate_button = main.ui.generate_button
        confirm_button = main.ui.confirm_button
        pbk = main.ui.pbk
        prk = main.ui.prk

        generate_button.setCheckable(True)
        confirm_button.setDisabled(True)

        generate_button.clicked.connect(main.generate)
        confirm_button.clicked.connect(main.fileDialog)
        pbk.textChanged.connect(main.checkText)
        
        main.MainWindow.show()
        sys.exit(main.app.exec_())
    except KeyboardInterrupt:
        pass
    except Exception:
        print_exc()
