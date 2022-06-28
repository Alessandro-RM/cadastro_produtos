from PyQt5 import  uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0

banco = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'root',
    database = 'cadastro_produtos'
)

def editar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute('SELECT id FROM produtos')
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute('SELECT * FROM produtos WHERE id='+ str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show() 

    numero_id = valor_id

    tela_editar.id_line.setText(str(produto[0][0]))
    tela_editar.codigo_line.setText(str(produto[0][1]))
    tela_editar.produto_line.setText(str(produto[0][2]))
    tela_editar.preco_line.setText(str(produto[0][3]))
    tela_editar.categoria_line.setText(str(produto[0][4]))

def salvar_dados_editados():
    #pega o numero do id
    global numero_id
    #valor digitado no lineEdit
    codigo = tela_editar.codigo_line.text()
    descricao = tela_editar.produto_line.text()
    preco = tela_editar.preco_line.text()
    categoria = tela_editar.categoria_line.text()
    #atualiza os valores no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}' WHERE id = {}"
                    .format(codigo, descricao, preco, categoria, numero_id ))
    #atualiza as janelas
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()

def excluir_dados():
   linha = segunda_tela.tableWidget.currentRow()
   segunda_tela.tableWidget.removeRow(linha)

   cursor = banco.cursor()
   cursor.execute('SELECT id FROM produtos')
   dados_lidos = cursor.fetchall()
   valor_id = dados_lidos[linha][0]
   cursor.execute('DELETE FROM produtos WHERE id='+ str(valor_id))
   

def gerar_pdf():   
    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM produtos'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadatro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10,750, 'ID')
    pdf.drawString(110,750, 'CÓDIGO')
    pdf.drawString(210,750, 'PRODUTO')
    pdf.drawString(310,750, 'PREÇO')
    pdf.drawString(410,750, 'CATEGORIA')

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print('PDF GERADO COM SUCESSO!!')

def funcao_pricipal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    
    categoria = ''

    if formulario.radioButton.isChecked():
        print('Categoria Informatica foi selecionado')
        categoria = 'Informática'
    elif formulario.radioButton_2.isChecked():
        print('Categoria Eletrônicos foi selecionado')
        categoria = 'Celulares'
    else:
        print('Categoria Celulares foi selecionado')
        categoria = 'Eletrônicos'
    print('Código: ', linha1)
    print('Descrição: ', linha2)
    print('Preço: ',linha3)

    curso = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1), str(linha2), str(linha3), categoria)
    curso.execute(comando_SQL,dados)
    banco.commit()
    
    formulario.lineEdit.setText('')
    formulario.lineEdit_2.setText('')
    formulario.lineEdit_3.setText('')

def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM produtos'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range (0, len(dados_lidos)):
        for j in range (0, 5):
            segunda_tela.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

app = QtWidgets.QApplication([])
formulario = uic.loadUi("formulario.ui")
segunda_tela = uic.loadUi('lista_dados.ui')
tela_editar = uic.loadUi('menu_editar.ui')
formulario.pushButton.clicked.connect(funcao_pricipal)
formulario.listarButton.clicked.connect(chama_segunda_tela)
segunda_tela.pdf_Button.clicked.connect(gerar_pdf)
segunda_tela.excluir_Button.clicked.connect(excluir_dados)
segunda_tela.editar_Button.clicked.connect(editar_dados)
tela_editar.salvar_Button.clicked.connect(salvar_dados_editados)

formulario.show()
app.exec()

