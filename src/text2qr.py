from generator import generate
import argparse
from PIL import Image


def show_image(qrcode):
  img = Image.new( 'RGB', (512, 512), "black") # Create a new black image
  pixels = img.load() # Create the pixel map
  for i in range(img.size[0]):    # For every pixel:
    for j in range(img.size[1]):
      x = int((i / img.size[0]) * qrcode.size)
      y = int((j / img.size[1]) * qrcode.size)
      state = 255 if qrcode.board[y][x].state else 0
      color = (state, state, state)
      if qrcode.board[y][x].reserved:
        if qrcode.board[y][x].state:
          color = (255, 200, 200)
        else:
          color = (55, 0, 0)
      pixels[i,j] = color
  img.show()


if __name__ == "__main__":
  message = "www.wikipedia.org"
  code = generate(message)

  show_image(code)