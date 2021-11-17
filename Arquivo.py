# Importações:
import sys
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QPushButton, QMessageBox, QLabel, QLineEdit
from PyQt5.QtCore import Qt
import pycep_correios
from pycep_correios import exceptions
import pyperclip


# Classe da Janela:
class Janela(QWidget):
    def __init__(self):
        super(Janela, self).__init__()

        # Propriedades da Janela:
        self.topo = 0
        self.esquerda = 0
        self.largura = 360
        self.altura = 256
        self.titulo = 'Válidador de CEP'
        self.setFixedSize(self.largura, self.altura)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Variáveis:
        MouseEventColorsOpt = 'QPushButton {font: bold; font-size: 22px; color:red; background: transparent;}QPushButton::pressed{font: bold; font-size: 22px; color:#610B21; background: transparent; }QPushButton::hover{text-decoration: underline;}'
        MouseEventColorsCopy = 'QPushButton {font: bold; font-size: 14px; color:blue; background: transparent;}QPushButton::pressed{font: bold; font-size: 14px; color:#0B3361; background: transparent; }QPushButton::hover{text-decoration: underline; }'
        OnlyInt = QIntValidator()
        self.Logradouro = ""
        self.Bairro = ""
        self.Cidade = ""
        self.UF = ""

        # Label responsavel pelas opções da tela (minimizar ou fechar):
        Option = QPushButton(self)
        Option.move(322, 0)
        Option.setText('...')
        Option.setStyleSheet(MouseEventColorsOpt)
        Option.setCursor(Qt.PointingHandCursor)
        Option.resize(25, 30)
        Option.clicked.connect(self.OptionClick)

        # Label titulo do programa:
        Label1 = QLabel(self)
        Label1.move(10, 10)
        Label1.setText(self.titulo)
        Label1.setStyleSheet('QLabel {font-size: 20px; color: black}')

        # Label da caixa de texto:
        Label2 = QLabel(self)
        Label2.move(25, 52)
        Label2.setText('Insira o CEP:')
        Label2.setStyleSheet('QLabel {font-size: 16px; color: black}')

        # Caixa de texto do cep:
        self.TxtCEP = QLineEdit(self)
        self.TxtCEP.move(125, 50)
        self.TxtCEP.resize(100, 25)
        self.TxtCEP.setStyleSheet('QLineEdit {font: bold; font-size: 16px}')
        self.TxtCEP.setValidator(OnlyInt)
        self.TxtCEP.setMaxLength(8)
        self.TxtCEP.textChanged.connect(self.CEPChanged)

        # Botão para pesquisar CEP fornecido:
        self.Pesquisar = QPushButton(self)
        self.Pesquisar.move(235, 50)
        self.Pesquisar.resize(100, 25)
        self.Pesquisar.setText("Pesquisar")
        self.Pesquisar.setCursor(Qt.PointingHandCursor)
        self.Pesquisar.setStyleSheet('QPushButton {font: bold; font-size: 14px}')
        self.Pesquisar.setEnabled(False)
        self.Pesquisar.clicked.connect(self.PesquisarCEP)

        # Label status:
        self.Status = QLabel(self)
        self.Status.move(125, 80)
        self.Status.setText('Status')
        self.Status.setStyleSheet('QLabel {font-size: 16px; color: black; font: bold}')
        self.Status.resize(110, 25)

        # Botão de Copia do logradouro:
        self.CopyLogradouro = QPushButton(self)
        self.CopyLogradouro.move(45, 115)
        self.CopyLogradouro.setText('Copiar Logradouro')
        self.CopyLogradouro.setStyleSheet(MouseEventColorsCopy)
        self.CopyLogradouro.setCursor(Qt.PointingHandCursor)
        self.CopyLogradouro.resize(135, 25)
        self.CopyLogradouro.clicked.connect(self.FCopyLogradouro)

        # Botão de Copia do bairro:
        self.CopyBairro = QPushButton(self)
        self.CopyBairro.move(45, 145)
        self.CopyBairro.setText('Copiar Bairro')
        self.CopyBairro.setStyleSheet(MouseEventColorsCopy)
        self.CopyBairro.setCursor(Qt.PointingHandCursor)
        self.CopyBairro.resize(135, 25)
        self.CopyBairro.clicked.connect(self.FCopyBairro)

        # Botão de Copia do logradouro:
        self.CopyCidade = QPushButton(self)
        self.CopyCidade.move(185, 115)
        self.CopyCidade.setText('Copiar Cidade')
        self.CopyCidade.setStyleSheet(MouseEventColorsCopy)
        self.CopyCidade.setCursor(Qt.PointingHandCursor)
        self.CopyCidade.resize(135, 25)
        self.CopyCidade.clicked.connect(self.FCopyCidade)

        # Botão de Copia do bairro:
        self.CopyUF = QPushButton(self)
        self.CopyUF.move(185, 150)
        self.CopyUF.setText('Copiar UF')
        self.CopyUF.setStyleSheet(MouseEventColorsCopy)
        self.CopyUF.setCursor(Qt.PointingHandCursor)
        self.CopyUF.resize(135, 25)
        self.CopyUF.clicked.connect(self.FCopyUF)

        # Botão de Copia do bairro:
        self.CopyTudo = QPushButton(self)
        self.CopyTudo.move(115, 175)
        self.CopyTudo.setText('Copiar Tudo')
        self.CopyTudo.setStyleSheet(MouseEventColorsCopy)
        self.CopyTudo.setCursor(Qt.PointingHandCursor)
        self.CopyTudo.resize(135, 25)
        self.CopyTudo.clicked.connect(self.FCopyTudo)

        # Botão de Copia do bairro:
        self.Visualizar = QPushButton(self)
        self.Visualizar.move(115, 200)
        self.Visualizar.setText('Visualizar Tudo')
        self.Visualizar.setStyleSheet(MouseEventColorsCopy)
        self.Visualizar.setCursor(Qt.PointingHandCursor)
        self.Visualizar.resize(135, 25)
        self.Visualizar.clicked.connect(self.FVisualizarTudo)

        # Abre a Janela:
        self.LoadJanela()

    # Função que carrega a janela:
    def LoadJanela(self):
        self.setGeometry(self.esquerda, self.topo, self.largura, self.altura)
        self.setWindowTitle(self.titulo)
        self.center()
        self.ButtonsInvisible()
        self.show()

    # Função que centraliza a janela:
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Função de clique das opções:
    def OptionClick(self):
        box = QMessageBox()
        box.setWindowTitle('Opções!')
        box.setText('Clique no botão com a opcão desejada!')
        box.setIcon(QMessageBox.Question)
        pixmap = QPixmap('Logo.png').scaledToHeight(32, Qt.SmoothTransformation)
        box.setIconPixmap(pixmap)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('Fechar')
        buttonX = box.button(QMessageBox.No)
        buttonX.setText('Minimizar')
        buttonZ = box.button(QMessageBox.Cancel)
        buttonZ.setText('Cancelar')
        box.exec_()
        # Verifica no que o usuário clicou:
        if box.clickedButton() == buttonY:
            sys.exit(0)
        elif box.clickedButton() == buttonX:
            self.showMinimized()

    # Função Mudança de texto na caixa de texto cep:
    def CEPChanged(self):
        self.ButtonsInvisible()
        self.Status.setText("Status")
        CEP = "{}".format(self.TxtCEP.text())
        if len(CEP) == 8:
            self.Pesquisar.setEnabled(True)
        else:
            self.Pesquisar.setEnabled(False)

    # Função Pesquisar CEP:
    def PesquisarCEP(self):
        try:
            self.Status.setText("CEP válido!")
            CEP = self.TxtCEP.text()
            endereco = pycep_correios.get_address_from_cep(CEP)
            self.Logradouro = endereco['logradouro']
            self.Bairro = endereco['bairro']
            self.Cidade = endereco['cidade']
            self.UF = endereco['uf']
            self.ButtonsVisible()
        except exceptions.InvalidCEP:
            self.Status.setText("CEP inválido!")
            self.ButtonsInvisible()
            self.TxtCEP.setFocus()
        except exceptions.CEPNotFound:
            self.Status.setText("CEP inválido!")
            self.ButtonsInvisible()
            self.TxtCEP.setFocus()
        except exceptions.ConnectionError:
            self.Status.setText("CEP inválido!")
            self.ButtonsInvisible()
            self.TxtCEP.setFocus()
        except exceptions.Timeout:
            self.Status.setText("CEP inválido!")
            self.ButtonsInvisible()
            self.TxtCEP.setFocus()
        except exceptions.HTTPError:
            self.Status.setText("CEP inválido!")
            self.ButtonsInvisible()
            self.TxtCEP.setFocus()
        except exceptions.BaseException:
            self.Status.setText("CEP inválido!")
            self.ButtonsInvisible()
            self.TxtCEP.setFocus()

    # Funçao que define o botão como visivel:
    def ButtonsVisible(self):
        self.CopyLogradouro.setVisible(True)
        self.CopyCidade.setVisible(True)
        self.CopyBairro.setVisible(True)
        self.CopyUF.setVisible(True)
        self.CopyTudo.setVisible(True)
        self.Visualizar.setVisible(True)

    # Funçao que define o botão como visivel:
    def ButtonsInvisible(self):
        self.CopyLogradouro.setVisible(False)
        self.CopyCidade.setVisible(False)
        self.CopyBairro.setVisible(False)
        self.CopyUF.setVisible(False)
        self.CopyTudo.setVisible(False)
        self.Visualizar.setVisible(False)
        self.Logradouro = ""
        self.Bairro = ""
        self.Cidade = ""
        self.UF = ""

    # Função de Copia do Logradouro:
    def FCopyLogradouro(self):
        pyperclip.copy(self.Logradouro)
        QMessageBox.about(self, "Sucesso", "Logradouro copiado")
        self.TxtCEP.setFocus()

    # Função de Copia do Bairro:
    def FCopyBairro(self):
        pyperclip.copy(self.Bairro)
        QMessageBox.about(self, "Sucesso", "Bairro copiado")
        self.TxtCEP.setFocus()

    # Função de Copia do Cidade:
    def FCopyCidade(self):
        pyperclip.copy(self.Cidade)
        QMessageBox.about(self, "Sucesso", "Cidade copiado")
        self.TxtCEP.setFocus()

    # Função de Copia do UF:
    def FCopyUF(self):
        pyperclip.copy(self.UF)
        QMessageBox.about(self, "Sucesso", "UF copiado")
        self.TxtCEP.setFocus()

    # Função de Copia do Tudo:
    def FCopyTudo(self):
        Tudo = "{}; {}; {}; {}".format(self.Logradouro, self.Bairro, self.Cidade, self.UF)
        pyperclip.copy(Tudo)
        QMessageBox.about(self, "Sucesso", "Tudo copiado")
        self.TxtCEP.setFocus()

    # Função de Copia do Tudo:
    def FVisualizarTudo(self):
        # Tudo = "{}; {}; {}; {}".format(self.Logradouro, self.Bairro, self.Cidade, self.UF)
        Tudo = "{}; \n{}; \n{}; \n{}".format(self.Logradouro, self.Bairro, self.Cidade, self.UF)
        QMessageBox.about(self, "Sucesso", Tudo)
        self.TxtCEP.setFocus()


# Inicialização:
app = QApplication(sys.argv)
window = Janela()
sys.exit(app.exec_())
