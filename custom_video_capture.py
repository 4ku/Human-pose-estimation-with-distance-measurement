import cv2
import queue
import threading
import time


class CustomVideoCapture:
    """
    Переделанный поток с cv2.VideoCapture, который возвращает всегда самый последний фрейм.
    """

    def __init__(self, name):
        """! Инициализация
        @param name идентификация потока
        """

        self.cap = cv2.VideoCapture(name)
        self.name = name
        self.q = queue.Queue()

        t = threading.Thread(target=self._reader, daemon=True)
        t.start()

    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put((ret, frame))
            if not ret:
                time.sleep(5)
                self.cap.release()
                self.cap = cv2.VideoCapture(self.name)

    def get(self, num):
        """! Возвращает число, нужно для получения размера картинки, например
        @param num число
        """
        return self.cap.get(num)

    def get_size(self):
        """! Получить размер картинки
        """
        return (int(self.get(3)), int(self.get(4)))

    def read(self):
        """! Получить последний кадр"""
        try:
            return self.q.get(timeout=0.5)
        except queue.Empty:
            return False, None

    def release(self):
        """! Освободить поток"""
        self.cap.release()