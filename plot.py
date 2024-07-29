import pyglet as pg
import numpy as np


def img(arr=np.array([])):
    if len(arr.shape)<3:
        arr = np.array([arr]*3).transpose([1, 2, 0])
    if arr.dtype not in [np.int64, np.int32, np.int16, np.int8]:
        arr = np.floor(arr*255).astype(np.int8)
    shp = arr.shape
    pixels = arr.flatten()
    rawData = (pg.gl.GLubyte * len(pixels))(*pixels)
    return pg.image.ImageData(shp[0], shp[1], 'RGB', rawData)


def image_plot(arr=np.array([]), caption='Image_Plot', save=False):
    shp = arr.shape
    pic = img(arr)
    if save:
        pic.save(caption+'.png')

    class W(pg.window.Window):
        def on_draw(self):
            pic.blit(5, 5)

    w = W(shp[0]+10, shp[1]+10)
    w.set_caption(caption)
    pg.app.run()


def bin_plot(arr=np.array([]), caption='Image_Plot'):
    shp = arr.shape
    if arr.dtype is not np.int32:
        arr = np.floor(arr * 255).astype(int)

    class W(pg.window.Window):
        def on_draw(self):
            for i in range(8):
                pic = arr % 2
                arr[:] -= pic
                arr[:] += (arr/2).astype(int)-arr
                pic = pic*.5+.25
                pic = img(pic)
                pic.blit(5*(i+1)+shp[0]*i, 5)

    w = W(shp[0]*8 + 50, shp[1] + 10)
    w.set_caption(caption)
    pg.app.run()


def clip_plot(arr=np.array([]), caption='Image_Plot', fps=10):
    shp = arr[0].shape
    pic = []
    for i in arr:
        pic += [img(i)]

    class W(pg.window.Window):

        t = 0.0

        def on_draw(self):
            pass

        def upd(self, dt):
            self.t += dt
            p = int(self.t*fps%len(pic))
            pic[p].blit(5, 5)


    w = W(shp[0]+10, shp[1]+10)
    w.set_caption(caption)
    pg.clock.schedule(w.upd)
    pg.app.run()


