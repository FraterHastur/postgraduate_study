from typing import Optional, Tuple

import self as self
from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtWidgets import QFileDialog

from VisualRecognition import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image, ImageEnhance
import PIL

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #---------------------Подключаем кнопки и события------------------------------#

        #Открытие пути к файлу объекта
        self.ui.btnObjectPath.clicked.connect(self.clickedObjectPath)

        #Открытие пути к файлу сцены
        self.ui.btnScenePath.clicked.connect(self.clickedScenePath)

        #Подключаем крутилку вращения к LCD
        self.ui.rotation_scale.valueChanged.connect(self.ui.rotation_progress.display)

        #Подключаем бара масштаба к прогрес бару
        self.ui.resized_scale.valueChanged.connect(self.ui.resized_progress.setValue)

        #Запуск модуля масштабирования после изменения масштаба
        self.ui.btnObjectPath.clicked.connect(self.moduleResizedTransformation)
        self.ui.btnScenePath.clicked.connect(self.moduleResizedTransformation)

        self.ui.resized_scale.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.en_resized.stateChanged.connect(self.moduleResizedTransformation)

        self.ui.rotation_scale.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.en_rotation.stateChanged.connect(self.moduleResizedTransformation)

        self.ui.kf_colorCorrection.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.en_colorCorrection.stateChanged.connect(self.moduleResizedTransformation)

        self.ui.kf_contrastCorrection.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.en_contrastCorrection.stateChanged.connect(self.moduleResizedTransformation)

        self.ui.kf_brightnessCorrection.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.en_brightCorrection.stateChanged.connect(self.moduleResizedTransformation)

        self.ui.kf_sharpnessCorrection.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.en_sharpCorrection.stateChanged.connect(self.moduleResizedTransformation)

        self.ui.en_blurCorrection.stateChanged.connect(self.moduleResizedTransformation)
        self.ui.gauss_kernell1.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.gauss_kernell2.valueChanged.connect(self.moduleResizedTransformation)

        self.ui.firstX.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.firstY.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.secondX.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.secondY.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.thirdX.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.thirdY.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.sh_firstX.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.sh_firstY.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.sh_secondX.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.sh_secondY.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.sh_thirdX.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.sh_thirdY.valueChanged.connect(self.moduleResizedTransformation)
        self.ui.en_affine.stateChanged.connect(self.moduleResizedTransformation)

        #Запуск модуля вращения после изменения угла
        self.ui.btnObjectPath.clicked.connect(self.moduleRotationTransform)
        self.ui.btnScenePath.clicked.connect(self.moduleRotationTransform)

        self.ui.rotation_scale.valueChanged.connect(self.moduleRotationTransform)
        self.ui.en_rotation.stateChanged.connect(self.moduleRotationTransform)

        self.ui.resized_scale.valueChanged.connect(self.moduleRotationTransform)
        self.ui.en_resized.stateChanged.connect(self.moduleRotationTransform)

        self.ui.kf_colorCorrection.valueChanged.connect(self.moduleRotationTransform)
        self.ui.en_colorCorrection.stateChanged.connect(self.moduleRotationTransform)

        self.ui.kf_contrastCorrection.valueChanged.connect(self.moduleRotationTransform)
        self.ui.en_contrastCorrection.stateChanged.connect(self.moduleRotationTransform)

        self.ui.kf_brightnessCorrection.valueChanged.connect(self.moduleRotationTransform)
        self.ui.en_brightCorrection.stateChanged.connect(self.moduleRotationTransform)

        self.ui.kf_sharpnessCorrection.valueChanged.connect(self.moduleRotationTransform)
        self.ui.en_sharpCorrection.stateChanged.connect(self.moduleRotationTransform)

        self.ui.en_blurCorrection.stateChanged.connect(self.moduleRotationTransform)
        self.ui.gauss_kernell1.valueChanged.connect(self.moduleRotationTransform)
        self.ui.gauss_kernell2.valueChanged.connect(self.moduleRotationTransform)

        self.ui.firstX.valueChanged.connect(self.moduleRotationTransform)
        self.ui.firstY.valueChanged.connect(self.moduleRotationTransform)
        self.ui.secondX.valueChanged.connect(self.moduleRotationTransform)
        self.ui.secondY.valueChanged.connect(self.moduleRotationTransform)
        self.ui.thirdX.valueChanged.connect(self.moduleRotationTransform)
        self.ui.thirdY.valueChanged.connect(self.moduleRotationTransform)
        self.ui.sh_firstX.valueChanged.connect(self.moduleRotationTransform)
        self.ui.sh_firstY.valueChanged.connect(self.moduleRotationTransform)
        self.ui.sh_secondX.valueChanged.connect(self.moduleRotationTransform)
        self.ui.sh_secondY.valueChanged.connect(self.moduleRotationTransform)
        self.ui.sh_thirdX.valueChanged.connect(self.moduleRotationTransform)
        self.ui.sh_thirdY.valueChanged.connect(self.moduleRotationTransform)
        self.ui.en_affine.stateChanged.connect(self.moduleRotationTransform)

        #Открываем картинку после преобразований
        self.ui.btnShowTransformImg.clicked.connect(self.clickedShowTransformImage)

        #Запуск модуля цветокоррекции по изменению коэффициента
        self.ui.btnObjectPath.clicked.connect(self.moduleColorCorrection)
        self.ui.btnScenePath.clicked.connect(self.moduleColorCorrection)

        self.ui.kf_colorCorrection.valueChanged.connect(self.moduleColorCorrection)
        self.ui.en_colorCorrection.stateChanged.connect(self.moduleColorCorrection)

        self.ui.rotation_scale.valueChanged.connect(self.moduleColorCorrection)
        self.ui.en_rotation.stateChanged.connect(self.moduleColorCorrection)

        self.ui.resized_scale.valueChanged.connect(self.moduleColorCorrection)
        self.ui.en_resized.stateChanged.connect(self.moduleColorCorrection)

        self.ui.kf_contrastCorrection.valueChanged.connect(self.moduleColorCorrection)
        self.ui.en_contrastCorrection.stateChanged.connect(self.moduleColorCorrection)

        self.ui.kf_brightnessCorrection.valueChanged.connect(self.moduleColorCorrection)
        self.ui.en_brightCorrection.stateChanged.connect(self.moduleColorCorrection)

        self.ui.kf_sharpnessCorrection.valueChanged.connect(self.moduleColorCorrection)
        self.ui.en_sharpCorrection.stateChanged.connect(self.moduleColorCorrection)

        self.ui.en_blurCorrection.stateChanged.connect(self.moduleColorCorrection)
        self.ui.gauss_kernell1.valueChanged.connect(self.moduleColorCorrection)
        self.ui.gauss_kernell2.valueChanged.connect(self.moduleColorCorrection)

        self.ui.firstX.valueChanged.connect(self.moduleColorCorrection)
        self.ui.firstY.valueChanged.connect(self.moduleColorCorrection)
        self.ui.secondX.valueChanged.connect(self.moduleColorCorrection)
        self.ui.secondY.valueChanged.connect(self.moduleColorCorrection)
        self.ui.thirdX.valueChanged.connect(self.moduleColorCorrection)
        self.ui.thirdY.valueChanged.connect(self.moduleColorCorrection)
        self.ui.sh_firstX.valueChanged.connect(self.moduleColorCorrection)
        self.ui.sh_firstY.valueChanged.connect(self.moduleColorCorrection)
        self.ui.sh_secondX.valueChanged.connect(self.moduleColorCorrection)
        self.ui.sh_secondY.valueChanged.connect(self.moduleColorCorrection)
        self.ui.sh_thirdX.valueChanged.connect(self.moduleColorCorrection)
        self.ui.sh_thirdY.valueChanged.connect(self.moduleColorCorrection)
        self.ui.en_affine.stateChanged.connect(self.moduleColorCorrection)

        #Запуск модуля контраста по изменению коэффициента
        self.ui.btnObjectPath.clicked.connect(self.moduleContrastCorrection)
        self.ui.btnScenePath.clicked.connect(self.moduleContrastCorrection)

        self.ui.kf_contrastCorrection.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.en_contrastCorrection.stateChanged.connect(self.moduleContrastCorrection)

        self.ui.rotation_scale.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.en_rotation.stateChanged.connect(self.moduleContrastCorrection)

        self.ui.resized_scale.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.en_resized.stateChanged.connect(self.moduleContrastCorrection)

        self.ui.kf_colorCorrection.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.en_colorCorrection.stateChanged.connect(self.moduleContrastCorrection)

        self.ui.kf_brightnessCorrection.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.en_brightCorrection.stateChanged.connect(self.moduleContrastCorrection)

        self.ui.kf_sharpnessCorrection.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.en_sharpCorrection.stateChanged.connect(self.moduleContrastCorrection)

        self.ui.en_blurCorrection.stateChanged.connect(self.moduleContrastCorrection)
        self.ui.gauss_kernell1.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.gauss_kernell2.valueChanged.connect(self.moduleContrastCorrection)

        self.ui.firstX.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.firstY.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.secondX.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.secondY.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.thirdX.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.thirdY.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.sh_firstX.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.sh_firstY.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.sh_secondX.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.sh_secondY.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.sh_thirdX.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.sh_thirdY.valueChanged.connect(self.moduleContrastCorrection)
        self.ui.en_affine.stateChanged.connect(self.moduleContrastCorrection)

        #Запуск модуля яркости по изменению коэффициента
        self.ui.btnObjectPath.clicked.connect(self.moduleBrightCorrection)
        self.ui.btnScenePath.clicked.connect(self.moduleBrightCorrection)

        self.ui.kf_brightnessCorrection.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.en_brightCorrection.stateChanged.connect(self.moduleBrightCorrection)

        self.ui.kf_contrastCorrection.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.en_contrastCorrection.stateChanged.connect(self.moduleBrightCorrection)

        self.ui.rotation_scale.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.en_rotation.stateChanged.connect(self.moduleBrightCorrection)

        self.ui.resized_scale.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.en_resized.stateChanged.connect(self.moduleBrightCorrection)

        self.ui.kf_colorCorrection.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.en_colorCorrection.stateChanged.connect(self.moduleBrightCorrection)

        self.ui.kf_sharpnessCorrection.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.en_sharpCorrection.stateChanged.connect(self.moduleBrightCorrection)

        self.ui.en_blurCorrection.stateChanged.connect(self.moduleBrightCorrection)
        self.ui.gauss_kernell1.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.gauss_kernell2.valueChanged.connect(self.moduleBrightCorrection)

        self.ui.firstX.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.firstY.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.secondX.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.secondY.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.thirdX.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.thirdY.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.sh_firstX.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.sh_firstY.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.sh_secondX.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.sh_secondY.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.sh_thirdX.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.sh_thirdY.valueChanged.connect(self.moduleBrightCorrection)
        self.ui.en_affine.stateChanged.connect(self.moduleBrightCorrection)

        #Запуск модуля резкости по изменению коэффициента
        self.ui.btnObjectPath.clicked.connect(self.moduleSharpCorrection)
        self.ui.btnScenePath.clicked.connect(self.moduleSharpCorrection)

        self.ui.kf_sharpnessCorrection.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.en_sharpCorrection.stateChanged.connect(self.moduleSharpCorrection)

        self.ui.kf_brightnessCorrection.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.en_brightCorrection.stateChanged.connect(self.moduleSharpCorrection)

        self.ui.kf_contrastCorrection.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.en_contrastCorrection.stateChanged.connect(self.moduleSharpCorrection)

        self.ui.rotation_scale.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.en_rotation.stateChanged.connect(self.moduleSharpCorrection)

        self.ui.resized_scale.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.en_resized.stateChanged.connect(self.moduleSharpCorrection)

        self.ui.kf_colorCorrection.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.en_colorCorrection.stateChanged.connect(self.moduleSharpCorrection)

        self.ui.en_blurCorrection.stateChanged.connect(self.moduleSharpCorrection)
        self.ui.gauss_kernell1.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.gauss_kernell2.valueChanged.connect(self.moduleSharpCorrection)

        self.ui.firstX.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.firstY.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.secondX.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.secondY.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.thirdX.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.thirdY.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.sh_firstX.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.sh_firstY.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.sh_secondX.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.sh_secondY.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.sh_thirdX.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.sh_thirdY.valueChanged.connect(self.moduleSharpCorrection)
        self.ui.en_affine.stateChanged.connect(self.moduleSharpCorrection)

        #Запуск модуля гауссового сглаживания по изменению параметров
        self.ui.btnObjectPath.clicked.connect(self.moduleGaussBlur)
        self.ui.btnScenePath.clicked.connect(self.moduleGaussBlur)

        self.ui.en_blurCorrection.stateChanged.connect(self.moduleGaussBlur)
        self.ui.gauss_kernell1.valueChanged.connect(self.moduleGaussBlur)
        self.ui.gauss_kernell2.valueChanged.connect(self.moduleGaussBlur)

        self.ui.kf_sharpnessCorrection.valueChanged.connect(self.moduleGaussBlur)
        self.ui.en_sharpCorrection.stateChanged.connect(self.moduleGaussBlur)

        self.ui.kf_brightnessCorrection.valueChanged.connect(self.moduleGaussBlur)
        self.ui.en_brightCorrection.stateChanged.connect(self.moduleGaussBlur)

        self.ui.kf_contrastCorrection.valueChanged.connect(self.moduleGaussBlur)
        self.ui.en_contrastCorrection.stateChanged.connect(self.moduleGaussBlur)

        self.ui.rotation_scale.valueChanged.connect(self.moduleGaussBlur)
        self.ui.en_rotation.stateChanged.connect(self.moduleGaussBlur)

        self.ui.resized_scale.valueChanged.connect(self.moduleGaussBlur)
        self.ui.en_resized.stateChanged.connect(self.moduleGaussBlur)

        self.ui.kf_colorCorrection.valueChanged.connect(self.moduleGaussBlur)
        self.ui.en_colorCorrection.stateChanged.connect(self.moduleGaussBlur)

        self.ui.firstX.valueChanged.connect(self.moduleGaussBlur)
        self.ui.firstY.valueChanged.connect(self.moduleGaussBlur)
        self.ui.secondX.valueChanged.connect(self.moduleGaussBlur)
        self.ui.secondY.valueChanged.connect(self.moduleGaussBlur)
        self.ui.thirdX.valueChanged.connect(self.moduleGaussBlur)
        self.ui.thirdY.valueChanged.connect(self.moduleGaussBlur)
        self.ui.sh_firstX.valueChanged.connect(self.moduleGaussBlur)
        self.ui.sh_firstY.valueChanged.connect(self.moduleGaussBlur)
        self.ui.sh_secondX.valueChanged.connect(self.moduleGaussBlur)
        self.ui.sh_secondY.valueChanged.connect(self.moduleGaussBlur)
        self.ui.sh_thirdX.valueChanged.connect(self.moduleGaussBlur)
        self.ui.sh_thirdY.valueChanged.connect(self.moduleGaussBlur)
        self.ui.en_affine.stateChanged.connect(self.moduleGaussBlur)

        # Запуск модуля афинных преобразований при изменении значений координат точек
        self.ui.btnObjectPath.clicked.connect(self.moduleAffineTransformation)
        self.ui.btnScenePath.clicked.connect(self.moduleAffineTransformation)

        self.ui.firstX.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.firstY.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.secondX.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.secondY.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.thirdX.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.thirdY.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.sh_firstX.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.sh_firstY.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.sh_secondX.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.sh_secondY.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.sh_thirdX.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.sh_thirdY.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.en_affine.stateChanged.connect(self.moduleAffineTransformation)

        self.ui.resized_scale.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.en_resized.stateChanged.connect(self.moduleAffineTransformation)

        self.ui.rotation_scale.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.en_rotation.stateChanged.connect(self.moduleAffineTransformation)

        self.ui.kf_colorCorrection.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.en_colorCorrection.stateChanged.connect(self.moduleAffineTransformation)

        self.ui.kf_contrastCorrection.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.en_contrastCorrection.stateChanged.connect(self.moduleAffineTransformation)

        self.ui.kf_brightnessCorrection.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.en_brightCorrection.stateChanged.connect(self.moduleAffineTransformation)

        self.ui.kf_sharpnessCorrection.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.en_sharpCorrection.stateChanged.connect(self.moduleAffineTransformation)

        self.ui.en_blurCorrection.stateChanged.connect(self.moduleAffineTransformation)
        self.ui.gauss_kernell1.valueChanged.connect(self.moduleAffineTransformation)
        self.ui.gauss_kernell2.valueChanged.connect(self.moduleAffineTransformation)

        #Расчет SIFT метод по нажатию кнопки
        self.ui.btnMesureImg.clicked.connect(self.clickedMessureSift)
        self.ui.mesureKeyPoint.valueChanged.connect(self.clickedMessureSift)

        #Индикация изображения SIFT
        self.ui.btnShowRecognitionSift.clicked.connect(self.clickedShowSiftImg)

        #Сохранение изображения SIFT
        self.ui.btnSaveSift.clicked.connect(self.clickedSaveSIFT)

        #Расчет SURF метод по нажатию кнопки
        self.ui.btnMesureSurfImg.clicked.connect(self.clickedMessureSurf)
        self.ui.HessianTresholdSurf.valueChanged.connect(self.clickedMessureSurf)
        self.ui.nmOctave.valueChanged.connect(self.clickedMessureSurf)
        self.ui.nmOctaveLayers.valueChanged.connect(self.clickedMessureSurf)
        self.ui.DescriptorSize.valueChanged.connect(self.clickedMessureSurf)
        self.ui.mesureKeyPointSurf.valueChanged.connect(self.clickedMessureSurf)

        #Индикация изображения SURF
        self.ui.btnShowRecognitionSurf.clicked.connect(self.clickedShowSurfImg)

        #Сохранение изображения SURF
        self.ui.btnSaveSurf.clicked.connect(self.clickedSaveSURF)

        #Расчет корреляции по нажатию кнопки
        self.ui.btnMessureCorrelation.clicked.connect(self.clickedMessureCorrelation)
        self.ui.correlationType.valueChanged.connect(self.clickedMessureCorrelation)

        #Индикация результатов корреляции
        self.ui.btnShowRecognitionCorrelation.clicked.connect(self.clickedShowCorrelationImg)


    #----------------------Здесь просто загружаем изображение в цвете и получаем его размеры---------------------------------#

    #Описание работы кнопки Обзор для загрузки Объекта
    def clickedObjectPath(self):
        self.objectPath, _filter = QFileDialog.getOpenFileName(self,
                                                 "Open Image",
                                                 "c:\\",
                                                 "Image Files (*.png *.jpg *.bmp)")
        self.ui.pathToObject.setText(self.objectPath)

        #Получение размера объекта и передача на индикацию
        self.img_obj = cv2.imread(self.objectPath, 1) #Загруженный объект публичный
        #self.img_obj_first = cv2.imread(self.objectPath, 1) #Загруженный объект без перезаписи
        self.rows, self.cols, self.ch = self.img_obj.shape #координаты публичные


    #Описание работы кнопки Обзор для загрузки Сцены
    def clickedScenePath(self):
        self.scenePath, _filter = QFileDialog.getOpenFileName(self,
                                                 "Open Image",
                                                 "c:\\",
                                                 "Image Files (*.png *.jpg *.bmp)")
        self.ui.pathToScene.setText(self.scenePath)
        self.img_scene= cv2.imread(self.scenePath, 1)  # Загруженная сцена публичная

    # ----------------------Пишем модуль геометрических преобразований---------------------------------#

    #Модуль Аффиных преобразований
    def moduleAffineTransformation(self):

        self.rowA, self.colA, self.chanA = self.img_obj_gaussBlur_out.shape

        # Передаем на индикацию количество строк, столбцов, каналов
        self.ui.absX.setText(str(self.rowA))
        self.ui.absY.setText(str(self.colA))
        self.ui.absCh.setText(str(self.chanA))

        # Первоначальные координаты точек 1 - 3
        sel_fX = self.ui.firstX.value()  # 1
        sel_fY = self.ui.firstY.value()

        sel_sX = self.ui.secondX.value()  # 2
        sel_sY = self.ui.secondY.value()

        sel_tX = self.ui.thirdX.value()  # 3
        sel_tY = self.ui.thirdY.value()

        # Координаты смещения точек 1 - 3
        mov_fX = self.ui.sh_firstX.value()  # 1
        mov_fY = self.ui.sh_firstY.value()

        mov_sX = self.ui.sh_secondX.value()  # 2
        mov_sY = self.ui.sh_secondY.value()

        mov_tX = self.ui.sh_thirdX.value()  # 3
        mov_tY = self.ui.sh_thirdY.value()

        # Строим вектор точек основного изображения
        pts1 = np.float32([[sel_fX, sel_fY], [sel_sX, sel_sY], [sel_tX, sel_tY]])
        # Строим вектор точек смещения
        pts2 = np.float32([[mov_fX, mov_fY], [mov_sX, mov_sY], [mov_tX, mov_tY]])

        if self.ui.en_affine.isChecked():
            #Строим аффинную матрицу
            matrix = cv2.getAffineTransform(pts1, pts2)

            #Немного аффиной магии
            affine_result = cv2.warpAffine(self.img_obj_gaussBlur_out, matrix, (self.colA, self.rowA))
            self.img_obj_affineTransformation_out = affine_result
        else:
            self.img_obj_affineTransformation_out = self.img_obj_gaussBlur_out

    #Модуль масштабирования
    def moduleResizedTransformation(self):
        self.resized = self.ui.resized_scale.value() #Значение масштаба

        #Выполнение масшабирования при подключении модуля масштабирования
        if self.ui.en_resized.isChecked():
            img_rows, img_cols, img_ch = self.img_obj.shape
            widht = int(img_cols * self.resized / 100)
            height = int(img_rows * self.resized / 100)
            dim = (widht, height)

            #Изображение после масштабирования
            resized_result = cv2.resize(self.img_obj, dim, interpolation=cv2.INTER_AREA)
            self.img_obj_Res_out = resized_result

        else:
            self.img_obj_Res_out = self.img_obj

    #Модуль вращения
    def moduleRotationTransform(self):
        self.rotation = self.ui.rotation_scale.value()

        if self.ui.en_rotation.isChecked():
            img_rows_, img_cols_, img_ch_ = self.img_obj_Res_out.shape
            image_center = (img_cols_ // 2, img_rows_ // 2)

            rotation_mat = cv2.getRotationMatrix2D(image_center, self.rotation, 1.)

            abs_cos = abs(rotation_mat[0, 0])
            abs_sin = abs(rotation_mat[0, 1])

            bound_w = int(img_rows_ * abs_sin + img_cols_ * abs_cos)
            bound_h = int(img_rows_ * abs_cos + img_cols_ * abs_sin)

            rotation_mat[0, 2] += bound_w / 2 - image_center[0]
            rotation_mat[1, 2] += bound_h / 2 - image_center[1]

            #Изображение после вращения
            rotated_mat = cv2.warpAffine(self.img_obj_Res_out, rotation_mat, (bound_w, bound_h))
            self.img_obj_Rot_out = rotated_mat
        else:
            self.img_obj_Rot_out = self.img_obj_Res_out

    # ----------------------Пишем модуль яркостных преобразований---------------------------------#
    #Модуль цветокоррекции
    def moduleColorCorrection(self):

        if self.ui.en_colorCorrection.isChecked():

            # Преобразуем изображение OpenCv в изображение PIL
            cv_img = cv2.cvtColor(self.img_obj_Rot_out, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(cv_img)
            color_kf = self.ui.kf_colorCorrection.value()

            #Работаем с цветокоррекцией
            enchance_color = ImageEnhance.Color(pil_img)
            color_correction = enchance_color.enhance(color_kf)

            #Преобразуем изображение PIL в изображение OpenCv
            color_result = cv2.cvtColor(np.array(color_correction), cv2.COLOR_RGB2BGR)
            self.img_obj_colorCorrection_out = color_result
        else:
            self.img_obj_colorCorrection_out = self.img_obj_Rot_out

    #Модуль контраста
    def moduleContrastCorrection(self):
        if self.ui.en_contrastCorrection.isChecked():

            # Преобразуем изображение OpenCv в изображение PIL
            cv_img = cv2.cvtColor(self.img_obj_colorCorrection_out, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(cv_img)
            contrast_kf = self.ui.kf_contrastCorrection.value()

            # Работаем с контрастом
            enchance_contrast = ImageEnhance.Contrast(pil_img)
            contrast_correction = enchance_contrast.enhance(contrast_kf)

            # Преобразуем изображение PIL в изображение OpenCv
            contrast_result = cv2.cvtColor(np.array(contrast_correction), cv2.COLOR_RGB2BGR)
            self.img_obj_contrastCorrection_out = contrast_result
        else:
            self.img_obj_contrastCorrection_out = self.img_obj_colorCorrection_out

    #Модуль Яркости
    def moduleBrightCorrection(self):
        if self.ui.en_brightCorrection.isChecked():

            # Преобразуем изображение OpenCv в изображение PIL
            cv_img = cv2.cvtColor(self.img_obj_contrastCorrection_out, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(cv_img)
            bright_kf = self.ui.kf_brightnessCorrection.value()

            # Работаем с яркостью
            enchance_bright = ImageEnhance.Brightness(pil_img)
            bright_correction = enchance_bright.enhance(bright_kf)

            # Преобразуем изображение PIL в изображение OpenCv
            bright_result = cv2.cvtColor(np.array(bright_correction), cv2.COLOR_RGB2BGR)
            self.img_obj_brightCorrection_out = bright_result
        else:
            self.img_obj_brightCorrection_out = self.img_obj_contrastCorrection_out

    #Модуль резкости
    def moduleSharpCorrection(self):
        if self.ui.en_sharpCorrection.isChecked():

            # Преобразуем изображение OpenCv в изображение PIL
            cv_img = cv2.cvtColor(self.img_obj_brightCorrection_out, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(cv_img)
            sharp_kf = self.ui.kf_sharpnessCorrection.value()

            # Работаем с яркостью
            enchance_sharp = ImageEnhance.Sharpness(pil_img)
            sharp_correction = enchance_sharp.enhance(sharp_kf)

            # Преобразуем изображение PIL в изображение OpenCv
            sharp_result = cv2.cvtColor(np.array(sharp_correction), cv2.COLOR_RGB2BGR)
            self.img_obj_sharpCorrection_out = sharp_result
        else:
            self.img_obj_sharpCorrection_out = self.img_obj_brightCorrection_out

    #Модуль сглаживания фильтром Гауса
    def moduleGaussBlur(self):
        kernel_1 = self.ui.gauss_kernell1.value()
        kernel_2 = self.ui.gauss_kernell2.value()
        k1 = kernel_1 % 2
        k2 = kernel_2 % 2
        if k1 == 1:
            kernel_1 = self.ui.gauss_kernell1.value()
        else:
            kernel_1 = self.ui.gauss_kernell1.value() + 1

        if k2 == 1:
            kernel_2 = self.ui.gauss_kernell2.value()
        else:
            kernel_2 = self.ui.gauss_kernell2.value() + 1

        if self.ui.en_blurCorrection.isChecked():
            blur_result = cv2.GaussianBlur(self.img_obj_sharpCorrection_out, (kernel_1, kernel_2), cv2.BORDER_DEFAULT)
            self.img_obj_gaussBlur_out = blur_result
        else:
            self.img_obj_gaussBlur_out = self.img_obj_sharpCorrection_out

          #Выводим картинку после преобразований
    def clickedShowTransformImage(self):
        plt.subplot(121), plt.imshow(self.img_obj)
        plt.title("Original")

        plt.subplot(122), plt.imshow(self.img_obj_affineTransformation_out)
        plt.title("Transform")

        plt.show()


    # ----------------------Пишем модуль распознавания---------------------------------#

    #Запуск SIFT (расчет)
    def clickedMessureSift(self):
        #Загрузка изображений объекта и сцены
        gray_obj_sift = cv2.cvtColor(self.img_obj_affineTransformation_out, cv2.COLOR_BGR2GRAY) #query Image in Gray
        gray_scene_sift = cv2.cvtColor(self.img_scene, cv2.COLOR_BGR2GRAY) #scene Image in Gray

        kf_kp_sift = self.ui.mesureKeyPoint.value() # Получаем коэффициент дескрипторов для сравнения

        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create(nfeatures=0, nOctaveLayers=3, contrastThreshold=0.04, edgeThreshold=10, sigma=1.6)

        # find the keypoints and descriptors with SIFT
        kp1_sift, des1_sift = sift.detectAndCompute(gray_obj_sift, None)
        kp2_sift, des2_sift = sift.detectAndCompute(gray_scene_sift, None)

        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1_sift, des2_sift, k=2)

        # Apply ratio test

        good_sift = []
        for m, n in matches:
            if m.distance < kf_kp_sift * n.distance:
                good_sift.append([m])


        # cv2.drawMatchesKnn expects list of lists as matches.
        self.sift_img = cv2.drawMatchesKnn(gray_obj_sift, kp1_sift, gray_scene_sift, kp2_sift, good_sift, None, flags=2)
        self.ui.numberKp1.setText(str(len(kp1_sift)))
        self.ui.numberKp2.setText(str(len(kp2_sift)))

        self.number_keypoints_sift = 0
        if len(kp1_sift) <= len(kp2_sift):
            self.number_keypoints_sift = len(kp1_sift)
        else:
            self.number_keypoints_sift = len(kp2_sift)
        perCent_sift = (len(good_sift) / self.number_keypoints_sift) * 100

        self.ui.numberGood.setText(str(perCent_sift)) #Вывод процента совпадений
        self.ui.goodMatchesSift.setText(str(len(good_sift))) #Вывод количества совпадений

    #Индикация изображения после SIFT
    def clickedShowSiftImg(self):
        plt.imshow(self.sift_img), plt.show()

    #Сохранение результата SIFT
    def clickedSaveSIFT(self):
       siftPath, _ = QFileDialog.getSaveFileName(self, "Save SIFT Image", "",
                                                 "JPG (*.jpg)")

       cv2.imwrite(siftPath, self.sift_img, [cv2.IMWRITE_JPEG_QUALITY, 100])


    #Запуск SURF (расчет)
    def clickedMessureSurf(self):
        # Загрузка изображений объекта и сцены
        gray_obj_surf = cv2.cvtColor(self.img_obj_affineTransformation_out, cv2.COLOR_BGR2GRAY)  # query Image in Gray
        gray_scene_surf = cv2.cvtColor(self.img_scene, cv2.COLOR_BGR2GRAY)  # scene Image in Gray

        kf_kp_surf = self.ui.mesureKeyPointSurf.value()  # Получаем коэффициент дескрипторов для сравнения

        #Получить параметры для настройки SURF

        surf_treshold = self.ui.HessianTresholdSurf.value()
        surf_octave = self.ui.nmOctave.value()
        surf_layers = self.ui.nmOctaveLayers.value()
        surf_descriptor = self.ui.DescriptorSize.value()

        # Initiate SIFT detector
        surf = cv2.xfeatures2d.SURF_create(hessianThreshold=surf_treshold, nOctaves=surf_octave, nOctaveLayers=surf_layers, extended=surf_descriptor, upright=False)

        # find the keypoints and descriptors with SURF
        kp1_surf, des1_surf = surf.detectAndCompute(gray_obj_surf, None)
        kp2_surf, des2_surf = surf.detectAndCompute(gray_scene_surf, None)

        # BFMatcher with default params
        bf = cv2.BFMatcher(cv2.NORM_L2)
        matches = bf.knnMatch(des1_surf, des2_surf, k=2)

        # Apply ratio test

        good_surf = []
        for m, n in matches:
            if m.distance < kf_kp_surf * n.distance:
                good_surf.append([m])

        # cv2.drawMatchesKnn expects list of lists as matches.
        self.surf_img = cv2.drawMatchesKnn(gray_obj_surf, kp1_surf, gray_scene_surf, kp2_surf, good_surf, None, flags=2)
        self.ui.numberKp1_Surf.setText(str(len(kp1_surf)))
        self.ui.numberKp2_Surf.setText(str(len(kp2_surf)))

        self.number_keypoints_surf = 0
        if len(kp1_surf) <= len(kp2_surf):
            self.number_keypoints_surf = len(kp1_surf)
        else:
            self.number_keypoints_surf = len(kp2_surf)
        perCent_surf = (len(good_surf) / self.number_keypoints_surf) * 100

        self.ui.numberGood_Surf.setText(str(perCent_surf))  # Вывод процента совпадений
        self.ui.goodMatchesSurf.setText(str(len(good_surf))) #Вывод количества совпадений

    #Индикация изображения после SURF
    def clickedShowSurfImg(self):
        plt.imshow(self.surf_img), plt.show()

    #Сохранение результата SURF
    def clickedSaveSURF(self):
        surfPath, _ = QFileDialog.getSaveFileName(self, "Save SURF Image", "",
                                                 "JPG (*.jpg)")
        cv2.imwrite(surfPath, self.surf_img, [cv2.IMWRITE_JPEG_QUALITY, 100])

    # Запуск корреляционных методов (расчет)
    def clickedMessureCorrelation(self):

        type_cor = self.ui.correlationType.value()

        input_object = self.img_obj_affineTransformation_out
        input_object_gray = cv2.cvtColor(input_object, cv2.COLOR_BGR2GRAY)

        self.input_scene = cv2.imread(self.scenePath, 1)
        input_scene_gray = cv2.cvtColor(self.input_scene, cv2.COLOR_BGR2GRAY)

        w_cor, h_cor = input_object_gray.shape[::-1]

        self.res = cv2.matchTemplate(input_scene_gray, input_object_gray, method=type_cor)

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(self.res)

        if type_cor == 1:
            top_left = minLoc
            self.ui.correlationKf.setText(str(100 - (minVal * 100)))
        else:
            top_left = maxLoc
            self.ui.correlationKf.setText(str(maxVal * 100))

        bottom_right = (top_left[0]+w_cor, top_left[1]+h_cor)
        cv2.rectangle(self.input_scene, top_left, bottom_right, (0, 255, 255), 2)



    #Показать изображение результатов корреляции
    def clickedShowCorrelationImg(self):

        plt.subplot(221), plt.imshow(self.res, cmap='gray')
        plt.title('Корреляция'), plt.xticks([]), plt.yticks([])
        plt.subplot(222), plt.imshow(self.input_scene, cmap='gray')
        plt.title('Результат корреляции'), plt.xticks([]), plt.yticks([])
        plt.subplot(223), plt.imshow(self.img_obj_affineTransformation_out, cmap='gray')
        plt.title('Объект'), plt.xticks([]), plt.yticks([])
        plt.subplot(224), plt.imshow(self.img_scene, cmap='gray')
        plt.title('Сцена'), plt.xticks([]), plt.yticks([])
        plt.show()














app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())