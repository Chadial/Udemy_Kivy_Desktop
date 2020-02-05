from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window

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
        """ Check existance of given path "img_path" and return list "imgs" of all absolute paths of found images """
        if not os.path.exists(img_path):                    # Check existance
            print("Invalid Path...")
            return -1
        else:
            all_files = os.listdir(img_path)
            imgs = []
            for f in all_files:                             # Add only images to list
                if f.endswith('.png') or f.endswith('.PNG') \
                        or f.endswith('.jpg') or f.endswith('.JPG') \
                        or f.endswith('.jpeg') or f.endswith('.JPEG'):
                    imgs.append('/'.join([img_path, f]))    # Concate path and image name as path
            return imgs

    def show_imgs(self, imgs):
        """ Connected to RecycleView in gallery.kv with id: img_base
            Fills the img_base.data with a Dictionary of images found by "get_imgs"
        """
        base = self.ids.img_base
        base_data = []
        for img in imgs:
            im_name = img[img.rfind('/')+1:]
            if len(im_name) > 20:               # Cut image name if longer than 20 chars
                im_name = im_name[:18] + '...'
            base_data.append({"im_source": img, 'im_caption': im_name})
        base.data = base_data

    def viewimg(self, instance):
        """ Generate a ModalView of an clicked image with functional Buttons """
        # print(instance.im_source)
        im = Image(source=instance.im_source)
        view_size = self.img_resize(im)

        # Define BoxLayout for ModalView Buttons
        image_ops = BoxLayout(size_hint=(None, None),
                              size=(200, 30),
                              spacing=4)
        # Define icons of functional Buttons using zmd.fontd file and garden.iconfonts
        btn_prev = Button(text='%s'%(icon('zmdi-caret-left', 24)), markup=True)
        btn_rename = Button(text='%s' % (icon('zmdi-file', 24)), markup=True)
        btn_effects = Button(text='%s' % (icon('zmdi-blur', 24)), markup=True)
        btn_next = Button(text='%s' % (icon('zmdi-caret-right', 24)), markup=True)
        # Add Buttons to BoxLayout image_ops
        image_ops.add_widget(btn_prev)
        image_ops.add_widget(btn_rename)
        image_ops.add_widget(btn_effects)
        image_ops.add_widget(btn_next)
        # Define AnchorLayout "anchor" position and add BoxLayout "image_ops"
        anchor = AnchorLayout(anchor_x='center', anchor_y='bottom')
        anchor.add_widget(image_ops)

        # Fill ViewImage(ModalView) "view" with BoxLayout, Image and AnchorLayout
        image_container = BoxLayout()
        view = ViewImage(size_hint=(None, None),
                         size=view_size)
        image_container.add_widget(im)
        view.add_widget(image_container)
        view.add_widget(anchor)
        # PopUp "view"
        view.open()

    def img_resize(self, img):
        """ Trims the image size to the underlying box"""
        im_size_x, im_size_y = img.texture_size
        ratio = im_size_x/im_size_y
        aspect = self.aspect_ratio(ratio, 50)

        while im_size_x >= Window.width or im_size_y >= Window.height:
            if im_size_x > im_size_y:
                im_size_x -= aspect[0]
                im_size_y -= aspect[1]
            else:
                im_size_y -= aspect[1]
        return [im_size_x, im_size_y]

    def aspect_ratio(self, val, lim):
        """ Calculates the aspect ratio of given ratio value """
        lower = [0, 1]
        upper = [1, 0]

        while True:
            mediant = [lower[0] + upper[0], lower[1] + upper[1]]

            if val * mediant[1] > mediant[0]:
                if lim < mediant[1]:
                    return upper
                lower = mediant
            elif val * mediant[1] == mediant[0]:
                if lim >= mediant[1]:
                    return mediant
                if lower[1] < upper[1]:
                    return lower
                return upper
            else:
                if lim < mediant[1]:
                    return lower
                upper = mediant


class GalleryApp(App):
    def build(self):
        return GalleryWindow()


if __name__ == "__main__":
    register('default_font', './assets/fonts/Material-Design-Iconic-font.ttf',
             join(dirname(__file__), 'assets/fonts/zmd.fontd'))
    GalleryApp().run()
