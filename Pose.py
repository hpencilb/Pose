import keyboard
import pyautogui
import pydirectinput
import tensorflow as tf
from PIL import ImageGrab

pyautogui.FAILSAFE = False

if __name__ == '__main__':
    window = 200
    aim_offset_x = 0
    aim_offset_y = 0

    interpreter = tf.lite.Interpreter(model_path="lite-model_movenet_singlepose_lightning_tflite_float16_4.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_size = 192
    half_w = window / 2
    width, height = pyautogui.size()
    print('Start monitoring...')
    while True:
        keyboard.wait('left alt')
        x, y = pyautogui.position()
        x, y = x + aim_offset_x, y + aim_offset_y
        g = ImageGrab.grab((max(0, x - half_w), max(0, y - half_w), min(width, x + half_w), min(height, y + half_w)))
        # g.save('window.jpg')
        image = tf.keras.preprocessing.image.array_to_img(g)
        image = tf.expand_dims(image, axis=0)
        image = tf.image.resize_with_pad(image, input_size, input_size)
        image = tf.cast(image, dtype=tf.uint8)
        interpreter.set_tensor(input_details[0]['index'], image.numpy())
        interpreter.invoke()
        keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
        dest_y, dest_x, c = keypoints_with_scores[0, 0, 0]
        if c >= 0.3:
            # pydirectinput.moveRel(int((dest_x - 0.5) * window), int((dest_y - 0.5) * window), relative=True)
            pyautogui.moveRel((dest_x - 0.5) * window, (dest_y - 0.5) * window)
