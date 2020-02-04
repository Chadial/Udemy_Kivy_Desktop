from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.anchorlayout import AnchorLayout

from kivy.garden.iconfonts import *

import os
from os.path import join, dirname


class ViewImage(ModalView):
    pass


class GalleryWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # print(self.get_imgs('imgs'))
        # im = Image(source='imgs/G-Psi.png')
        # self.add_widget(im)

        images = self.get_imgs("imgs")
        self.show_imgs(images)

    def get_imgs(self, img_path):
        if not os.path.exists(img_path):
            print("Invalid Path...")
            return -1
        else:
            all_files = os.listdir(img_path)
            imgs = []
            for f in all_files:
                if f.endswith('.png') or f.endswith('.PNG') \
                        or f.endswith('.jpg') or f.endswith('.JPG') \
                        or f.endswith('.jpeg') or f.endswith('.JPEG'):
                    imgs.append('/'.join([img_path, f]))
            return imgs

    def show_imgs(self, imgs):
        base = self.ids.img_base
        base_data = []
        for img in imgs:
            im_name = img[img.rfind('/')+1:]
            if len(im_name) > 20:
                im_name = im_name[:18] + '...'
            base_data.append({"im_source": img, 'im_caption': im_name})
        base.data = base_data

    def viewimg(self, instance):
        # print(instance.im_source)
        btn_prev = Button(text='%s'%(icon('zmdi-caret-left', 24)), markup=True)
        btn_rename = Button(text='%s' % (icon('zmdi-file', 24)), markup=True)
        btn_effects = Button(text='%s' % (icon('zmdi-blur', 24)), markup=True)
        btn_next = Button(text='%s' % (icon('zmdi-caret-right', 24)), markup=True)

        image_ops = BoxLayout(size_hint=(None, None),
                              size=(200, 30),
                              spacing=4)
        image_ops.add_widget(btn_prev)
        image_ops.add_widget(btn_rename)
        image_ops.add_widget(btn_effects)
        image_ops.add_widget(btn_next)

        anchor = AnchorLayout(anchor_x='center', anchor_y='bottom')
        anchor.add_widget(image_ops)

        image_container = BoxLayout()

        view = ViewImage(size_hint=(None, None),
                         size=(400, 400))
        image_container.add_widget(Image(source=instance.im_source))
        view.add_widget(image_container)
        view.add_widget(anchor)
        view.open()


class GalleryApp(App):
    def build(self):
        return GalleryWindow()


if __name__ == "__main__":
    register('default_font', './assets/fonts/Material-Design-Iconic-font.ttf',
             join(dirname(__file__), 'assets/fonts/zmd.fontd'))
    GalleryApp().run()
