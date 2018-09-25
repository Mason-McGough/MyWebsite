from os import listdir
from os.path import join, dirname, splitext
from django.shortcuts import render

def photos(request):
    def _is_img(img_name):
        valid_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')
        _, ext = splitext(img_name)
        return True if ext in valid_exts else False

    static_dir = 'photoviewer/zoom'
    mydir = join(dirname(__file__), 'static', static_dir)
    imgs_list = [join('/static', static_dir, i) for i in listdir(mydir) if _is_img(i)]

    return render(
        request, 
        'photoviewer/photos.html', 
        {'imgs_list': imgs_list}
    )
