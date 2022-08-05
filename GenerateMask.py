import numpy as np
import cv2

# ============================================================================

FINAL_LINE_COLOR = (255, 0, 0)
WORKING_LINE_COLOR = (255, 0, 127)

# ============================================================================

class PolygonDrawer(object):
    def __init__(self, window_name, ref_img):
        self.window_name = window_name # Name for our window
        self.ref_img = ref_img # Image to work on
        self.mask = np.zeros((self.ref_img.shape[:2]), np.uint8)

        self.id = 1 # id of active polygon (count of polys!)
        self.done = False # Flag signalling we're done
        self.current = (0, 0) # Current position to draw the line-in-progress
        self.points = [] # List of points defining our current polygon
        self.polys = {} # Dict of all polygons drawn


    def on_mouse(self, event, x, y, buttons, user_param):
        if self.done:
            return

        if event == cv2.EVENT_MOUSEMOVE:
            # update current mouse position to draw the line-in-progress
            self.current = (x, y)
        elif event == cv2.EVENT_LBUTTONDOWN:
            # Left click means adding a point at current position to the list of points
            print("Adding point with position(%d,%d)" % (x, y))
            self.points.append((x, y))
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right click means we need to remove last added point
            print("Removing point with position(%d,%d)" % (x, y))
            self.points.pop(len(self.points)-1)


    def fill_polygon(self):
        # update background image and mask with the drawn filled in polygon
        if (len(self.points) > 0):
            cv2.fillPoly(self.ref_img, np.array([self.points]), FINAL_LINE_COLOR)
            cv2.fillPoly(self.mask, np.array([self.points]), FINAL_LINE_COLOR)

        # push this polygon to dict, and clear the active polygon points list
        self.polys[self.id] = self.points.copy()
        self.points.clear()
        self.id = self.id + 1

    def run(self):
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(self.window_name, self.ref_img)
        cv2.waitKey(1)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

        while(not self.done):
            # continuously draw new images and show them in the named window
            canvas = self.ref_img.copy()
            if (len(self.points) > 0):
                # Draw all the current polygon segments
                cv2.polylines(canvas, np.array([self.points]), False, FINAL_LINE_COLOR, 3)
                # And  also show what the current segment would look like
                cv2.line(canvas, self.points[-1], self.current, WORKING_LINE_COLOR, 3)
            # Update the window
            cv2.imshow(self.window_name, canvas)
            
            k = cv2.waitKey(50)
            if k == ord('f'): # f to fill poly
                print('f pressed')
                self.fill_polygon()
                cv2.imshow(self.window_name, canvas)
            elif k == 27: # ESC to exit
                self.done = True

        cv2.destroyWindow(self.window_name)
        return self.mask

if __name__ == "__main__":
    ref_img_path = './images/cats.jpg'
    pd = PolygonDrawer("Mask Generator", cv2.imread(ref_img_path))
    mask = pd.run()
    cv2.imwrite("./images/mask.png", mask)
    print("Polygons = %s" % pd.polys)