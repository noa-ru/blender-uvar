import bpy
from bpy.props import BoolProperty

import os
import sys
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import atexit

bl_info = {
    "name": "UV Auto reload",
    "description": "UV auto reload",
    "author": "Oleg Nazarov",
    "version": (1, 0, 0),
    "blender": (2, 7, 9),
    "location": "UV/Image Editor > Tool Shelf > UV Autoreload",
    "category": "UV",
    "tracker_url": "https://github.com/noa-ru/blender-uvar/issues"
}


def debug(msg="", self=None):
    # enabled = True
    enabled = False

    if enabled:
        import inspect
        obj = ""
        if self is not None:
            obj = type(self).__name__ + " "
        method = inspect.stack()[1][3] + " "

        beforemsg = obj + method

        if msg == "/":
            print("- " + beforemsg)
        else:
            print("+ " + beforemsg + msg)


class UVARModel:
    areas = None
    fileWatcherThread = None

    def __init__(self):
        debug("", self)
        atexit.register(self.exit_callback, self)
        debug("/", self)

    def __del__(self):
        debug("destruct")
        self.disable()
        debug("destruct")

    @staticmethod
    def exit_callback(self):
        """
        @type self: UVARModel
        """
        debug("", self)
        self.disable()
        debug("/", self)

    @staticmethod
    def checkbox_update_handler(property_group, context):
        self = context.scene.UVARModel  # type: UVARModel
        property_group = context.window_manager.UVARPropertyGroup  # type: UVARPropertyGroup
        areas = context.screen.areas
        debug("", self)

        if property_group.checkbox_state:
            image_filepath = self.get_watch_filepath(context)
            if image_filepath:
                self.enable(areas, image_filepath)
            else:
                property_group.checkbox_state = False
        else:
            self.disable()

        debug("/", self)
        return None

    @staticmethod
    def dynamic_select_options():
        debug("", UVARModel)

        def get_select_state_list(self, context) -> tuple:
            # debug("")
            result = [("0", "", "")]
            if context is not None:
                # debug("context is not None")
                images_list = bpy.data.images.items()
                for img in images_list:
                    strid = str(img[0])
                    result.append(
                        (strid, strid, "")
                    )
            # debug("/")
            return tuple(result)

        debug("/", UVARModel)
        return get_select_state_list

    @staticmethod
    def get_watch_filepath(context):
        debug("", UVARModel)
        property_group = context.window_manager.UVARPropertyGroup
        image_name = property_group.select_state
        if image_name != 0:
            if bpy.data.images.get(image_name):
                debug("file path found", UVARModel)
                return bpy.data.images[image_name].filepath_from_user()
        debug("file not path found", UVARModel)
        debug("/", UVARModel)
        return False

    def redraw_handler(self):
        debug("", self)
        if self.areas is not None:
            debug("areas is not None", self)
            for area in self.areas:
                if area.type == "IMAGE_EDITOR":
                    area.spaces.active.image.reload()
                    area.tag_redraw()
                elif area.type == "VIEW_3D":
                    area.tag_redraw()
        debug("/", self)

    def enable(self, areas, image_filepath):
        debug("", self)
        if self.fileWatcherThread is None:
            debug("fileWatcherThread is None", self)
            self.areas = areas
            self.fileWatcherThread = FileWatcherThread(
                os.path.dirname(image_filepath),
                os.path.basename(image_filepath),
                self.redraw_handler
            )
            self.fileWatcherThread.daemon = True
            self.fileWatcherThread.start()
        debug("/", self)

    def disable(self):
        debug("", self)
        if self.areas is not None:
            debug("areas is not None", self)
            self.areas = None
            self.fileWatcherThread.stop()
            self.fileWatcherThread = None
        debug("/", self)


class UVARPropertyGroup(bpy.types.PropertyGroup):
    checkbox_state = bpy.props.BoolProperty(
        name="Enable",
        description="Start a reloading current uv image",
        default=False,
        update=UVARModel.checkbox_update_handler
    )
    select_state = bpy.props.EnumProperty(items=UVARModel.dynamic_select_options())


class UVARPanel(bpy.types.Panel):
    bl_idname = "UVARPanel"
    bl_label = "UV Autoreload"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "UV Autoreload"

    def draw(self, context):
        layout = self.layout
        property_group = context.window_manager.UVARPropertyGroup  # type: UVARPropertyGroup
        layout.prop(property_group, "checkbox_state")
        layout.prop(property_group, 'select_state', text="")


class FileWatcher(FileSystemEventHandler):

    def __init__(self, path, file_name, callback):
        debug("", self)
        self.file_name = file_name
        self.callback = callback

        self.observer = Observer()
        self.observer.schedule(self, path, recursive=False)
        debug("/", self)

    def __del__(self):
        debug("/", self)

    def start(self):
        debug("", self)
        self.observer.start()
        self.observer.join()
        debug("/", self)

    def stop(self):
        debug("", self)
        self.observer.stop()
        self.observer.join()
        debug("/", self)

    def on_modified(self, event):
        debug("", self)
        if not event.is_directory and event.src_path.endswith(self.file_name):
            debug("callback", self)
            self.callback()
        debug("/", self)


class FileWatcherThread(threading.Thread):

    def __init__(self, dirpath, filename, callback):
        debug("", self)
        self.fileWatcher = FileWatcher(dirpath, filename, callback)
        threading.Thread.__init__(self)
        debug("/", self)

    def __del__(self):
        debug("/", self)

    def run(self):
        debug("", self)
        try:
            self.fileWatcher.start()
        except BaseException as e:
            debug("Exception:" + str(e), self)
            self.fileWatcher.stop()
            self.fileWatcher.join()
        debug("/", self)

    def stop(self):
        debug("", self)
        self.fileWatcher.stop()
        self.join()
        debug("/", self)


def register():
    debug()
    bpy.utils.register_module(__name__)
    bpy.types.Scene.UVARModel = UVARModel()
    bpy.types.WindowManager.UVARPropertyGroup = bpy.props.PointerProperty(
        type=UVARPropertyGroup
    )
    debug("/")


def unregister():
    debug()
    bpy.utils.unregister_module(__name__)
    del bpy.types.WindowManager.UVARPropertyGroup
    del bpy.types.Scene.UVARModel
    debug("/")
    debug("\n\n-----------------------------------------------------------\n\n")


if __name__ == '__main__':
    register()
