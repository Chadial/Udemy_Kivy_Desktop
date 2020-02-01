from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

import os


class GalleryWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        print(self.get_imgs('imgs1'))

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


class GalleryApp(App):
    def build(self):
        return GalleryWindow()


if __name__ == "__main__":
    GalleryApp().run()
