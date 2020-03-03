import cv2
import platform

def open_cam_usb(dev, width, height):
    """Open a USB webcam."""
    # To make the same code work on a laptop or on a Jetson Nano, we'll detect when we are running on the Nano
    # so that we can access the camera correctly in that case.
    # On a normal Intel laptop, platform.machine() will be "x86_64" instead of "aarch64"
    # if platform.machine() == "x86_64":
    #     print('open camera')
    #     gst_str = ('v4l2src device=/dev/video{} ! '
    #                'video/x-raw, width=(int){}, height=(int){} ! '
    #                'videoconvert ! appsink').format(dev, width, height)
    #     return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
    # else:
    return cv2.VideoCapture(dev)
