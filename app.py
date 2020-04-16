import base64
from flask_cors import CORS, cross_origin
from io import BytesIO
from flask import Flask, jsonify, request
from urllib.request import urlopen, Request
import os
import sys
import io
from PIL import Image, ImageDraw, ImageFont
#pip install Pillow


app = Flask(__name__)
cors = CORS(app,resource={r"/*":{"origens":"*"}})


@app.route("/<id>", methods=['GET'])
def index(id):
  barra = codigodebarra()
  if len(sys.argv) > 1:
    codigo = sys.argv[1]
  else:
    # codigo de barra completo em dígitos
    codigo = id
  # formato que deseja salvar a imagem (PNG,GIF)
  tipo='PNG'

  # retornando uma imagem a partir do código de barra
  image = barra.getcodbarra(codigo)

  # transformando a imagem da variavel 'tipo' em bytes pra gerar imagem em sstring  
  
  buffered = BytesIO()
  image.save(buffered, format="PNG")
  img_str = base64.b64encode(buffered.getvalue()).decode("ascii")
 
  html_img = '<img style="width: 750px;" src="data:image/png;base64,{}">'.format(img_str)
  return html_img
# ------------------------------ M O N T A N D O    I M A G E M ------------------------------

class codigodebarra:
  def __init__(self):
    pass

  
  def getcodbarra(self, valor, posX=150, posY=10, height = 60):
    # padrão 2 por 5 intercalado ( utilizado em boletos bancários )
    padrao = ('00110', '10001', '01001', '11000', '00101',
          '10100', '01100', '00011', '10010', '01010')

    # criando imagem
    imagem = Image.new('RGB', (750,80), 'white')
    draw = ImageDraw.Draw(imagem)

    # verificando se o conteudo para gerar barra é impar, se for,
    # adiciona 0 no inicial para fazer intercalação em seguida dos pares 

    if (len(valor) % 2) != 0:
      valor= '0' + valor

    # faz intercalação dos pares
    l=''
    for i in range(0,len(valor),2):
      p1=padrao[int(valor[i])]
      p2=padrao[int(valor[i+1])]
      for p in range(0,5):
        l+=p1[:1] + p2[:1]
        p1=p1[1:]
        p2=p2[1:]

    # gerando espaços e barras
    barra=True
    b=''

    # P = preto
    # B = banco

    for i in range(0,len(l)):
      if l[i] == '0':
        if barra:
          b+='P'
          barra=False
        else:
          b+='B'
          barra=True
      else:
        if barra:
          b+='PPP'
          barra=False
        else:
          b+='BBB'
          barra=True

    # concatena inicio e fim
    b='PBPB' + b + 'PPPBP'

    # P = preto
    # B = banco 

    # percorre toda a string b e onde for P pinta de preto, onde for B pinta de banco 

    for i in range(0,len(b)):
      if b[i] == 'P':
        draw.line((posX,posY,posX,posY + height),'black')
      else:
        draw.line((posX,posY,posX,posY + height),'white')
      posX+=1
    return imagem
  


def main():
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)

if __name__ == "__main__":
    main()
