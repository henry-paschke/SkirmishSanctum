import os
from drawable import *
from copy import deepcopy


def create_menu_from_filesystem(path: str, camera, preview_size, folder_color, margin_size=20, starting_pos = Vector2(0, 0)):
    return [
        Drawable(preview_size, folder_color, camera, [
            Text_attachment(path, font_color=(0, 0, 0)),
            Folder_attachment(create_menu_from_filesystem_recursive(path, camera, preview_size, folder_color), margin_size)
        ], position=starting_pos)
    ]


def create_menu_from_filesystem_recursive(path: str, camera, preview_size, folder_color, margin_size=20):
    entry = []
    new_preview_size = deepcopy(preview_size) - Vector2(margin_size, 0)
    if os.path.exists(path) == False:
        print("Path does not exist")
        return entry
    with os.scandir(path) as it:
        for content in it:
            if content.is_dir():
                entry.append(
                    Drawable(new_preview_size, folder_color, camera, [
                        Text_attachment(content.name, font_color=(0, 0, 0)),
                        Folder_attachment(create_menu_from_filesystem_recursive(os.path.join(path, content.name), camera, new_preview_size, folder_color, margin_size), margin_size)
                    ])
                )
            elif content.is_file():
                if content.name.endswith("top.png") and os.path.exists(os.path.join(path, content.name.replace("top", "bottom"))):
                    back_name = content.name.replace("top", "bottom")
                    entry.append(
                        Double_sided_drawable(new_preview_size, os.path.join(path, content.name), os.path.join(path, back_name), camera, [])
                    )
    return entry
        