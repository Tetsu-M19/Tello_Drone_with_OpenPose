from email.mime import image
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import cv2

# 使うフォント，サイズ，描くテキストの設定
ttfontname = '/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf'
fontsize = 36
text = "flip"

# 画像サイズ，背景色，フォントの色を設定
canvasSize    = (300, 150)
backgroundRGB = (255, 255, 255)
textRGB       = (0, 0, 0)

# 文字を描く画像の作成
img  = PIL.Image.new('RGB', canvasSize, backgroundRGB)
draw = PIL.ImageDraw.Draw(img)

# 用意した画像に文字列を描く
font = PIL.ImageFont.truetype(ttfontname, fontsize)
textWidth, textHeight = draw.textsize(text,font=font)
textTopLeft = (canvasSize[0]//2-textWidth//2, canvasSize[1]//2-textHeight//2) # 前から1/6，上下中央に配置
draw.text(textTopLeft, text, fill=textRGB, font=font)

img.save(f"{text}.png")
