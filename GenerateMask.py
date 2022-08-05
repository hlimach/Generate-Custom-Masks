import numpy as np
import cv2

# ============================================================================

FINAL_LINE_COLOR = (255, 0, 0)
WORKING_LINE_COLOR = (255, 0, 127)

# ============================================================================

class PolygonDrawer(object):
    def __init__(self, window_name, ref_img):
        self.window_name = window_name # Name for our window
        self.ref_img = ref_img

        self.fill = False
        self.done = False # Flag signalling we're done
        self.current = (0, 0) # Current position, so we can draw the line-in-progress
        self.points = [] # List of points defining our polygon


    def on_mouse(self, event, x, y, buttons, user_param):

        if self.done: # Nothing more to do
            return

        if event == cv2.EVENT_MOUSEMOVE:
            # We want to be able to draw the line-in-progress, so update current mouse position
            self.current = (x, y)
        elif event == cv2.EVENT_LBUTTONDOWN:
            # Left click means adding a point at current position to the list of points
            print("Adding point #%d with position(%d,%d)" % (len(self.points), x, y))
            self.points.append((x, y))
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right click means we need to remove last added point
            print("Removing point #%d with position(%d,%d)" % (len(self.points), x, y))
            self.points.pop(len(self.points)-1)


    def run(self):
        cv2.namedWindow(self.window_name)
        cv2.imshow(self.window_name, self.ref_img)
        cv2.waitKey(1)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

        while(not self.done):
            # This is our drawing loop, we just continuously draw new images
            # and show them in the named window
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
                self.fill = True
            elif k == 27: # ESC to exit
                self.done = True
            elif k == -1:
                continue
            else:
                print(k)

        # User finised entering the polygon points, so let's make the final drawing
        canvas = self.ref_img.copy()
        mask = np.zeros((self.ref_img.shape[:2]), np.uint8)
        if (len(self.points) > 0):
            cv2.fillPoly(canvas, np.array([self.points]), FINAL_LINE_COLOR)
            cv2.fillPoly(mask, np.array([self.points]), FINAL_LINE_COLOR)

        cv2.imshow(self.window_name, canvas)

        cv2.waitKey()
        cv2.destroyWindow(self.window_name)
        return mask

# ============================================================================

if __name__ == "__main__":
    ref_img_path = './images/cat.jpg'
    pd = PolygonDrawer("Mask Generator", cv2.imread(ref_img_path))
    mask = pd.run()
    cv2.imwrite("mask.png", mask)
    print("Polygon = %s" % pd.points)
    # events = [i for i in dir(cv2) if 'EVENT' in i]
    # print( events )